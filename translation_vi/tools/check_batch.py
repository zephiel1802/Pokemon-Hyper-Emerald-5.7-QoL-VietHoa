"""Validate a translation batch WITHOUT touching the dump files (safe to run in parallel).

    python3 translation_vi/tools/check_batch.py translation_vi/batches/d_005_a.json

Prints one line per problem: unknown key, lost/changed control token, \\p count, unencodable char,
table text that does not fit its box, plus a length summary. Exit code 1 if anything must be fixed.
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import insert, make_font  # noqa: E402

ROM = '/Users/zephiel/Downloads/Pokemons/Hyper Emerald Lost Artifacts 5.7.gba'


def index():
    idx = {}
    for f in glob.glob(os.path.join(VI, 'dialogues', '*.json')):
        for e in json.load(open(f, encoding='utf-8')):
            idx[e['id']] = ('dialogue', e)
    for kind in insert.FMT:
        p = os.path.join(VI, 'tables', kind + '.json')
        if kind == 'dialogue' or not os.path.exists(p): continue
        for e in json.load(open(p, encoding='utf-8')):
            idx['%s@%s' % (kind, e['offset_hex'])] = (kind, e)
            for lk in ('items', 'moves', 'abilities', 'dex'):
                us = e.get(lk, [])
                for u in (us if isinstance(us, list) else [us]):
                    idx['%s#%s' % (kind, u)] = (kind, e)
    return idx


def main(paths):
    data = bytearray(open(ROM, 'rb').read())
    cmap, _ = make_font.build_font(data)
    enc = insert.Encoder(data, cmap)
    idx = index()
    bad = 0
    for path in paths:
        batch = json.load(open(path, encoding='utf-8'))
        en_len = vi_len = 0
        longer = 0
        for k, vi in batch.items():
            if k not in idx: print('%s: unknown key' % k); bad += 1; continue
            kind, e = idx[k]
            vi = vi.strip()
            if vi == '@@SKIP@@': continue
            if '\n' in vi or '\\n' in vi or '\\l' in vi:
                print('%s: contains a line break - use spaces (only \\p is allowed)' % k); bad += 1; continue
            err = insert.check(e['original_en'], vi)
            if err: print('%s: %s' % (k, err)); bad += 1; continue
            text = vi
            for a, b in insert.NORMALIZE.items(): text = text.replace(a, b)
            try:
                b = enc.encode(text, kind)
            except ValueError as ex:
                print('%s: %s' % (k, ex)); bad += 1; continue
            if b is None:
                print('%s: too long for its box (%s) - shorten' % (k, kind)); bad += 1; continue
            en_len += e['byte_len']; vi_len += len(b)
            if len(b) > e['byte_len']: longer += 1
        print('%s: %d entries, vi/en bytes = %d/%d (%.0f%%), %d longer than English' % (
            os.path.basename(path), len(batch), vi_len, en_len, 100.0 * vi_len / max(en_len, 1), longer))
    print('OK' if not bad else '%d PROBLEMS' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
