"""Merge a translation batch into the dump JSONs.

    python3 translation_vi/tools/merge_batch.py translation_vi/batches/poc_01_opening.json

Batch = {key: vietnamese}. Keys:
  D00304                         a dialogue id
  <table>@0x57fea6               a table entry by offset (table = items_descriptions, moves_descriptions ...)
  <table>#<label>                a table entry whose users list contains <label> ("13 Potion", "33 Tackle")
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)


def main(batch_path):
    batch = json.load(open(batch_path, encoding='utf-8'))
    left = dict(batch)
    for f in sorted(glob.glob(os.path.join(VI, 'dialogues', '*.json'))) + sorted(glob.glob(os.path.join(VI, 'tables', '*.json'))):
        table = os.path.basename(f)[:-5]
        recs = json.load(open(f, encoding='utf-8'))
        hit = False
        for e in recs:
            keys = [e.get('id'), '%s@%s' % (table, e.get('offset_hex'))]
            for lk in ('items', 'moves', 'abilities', 'dex'):
                us = e.get(lk, [])
                for u in (us if isinstance(us, list) else [us]):
                    keys.append('%s#%s' % (table, u))
            for k in keys:
                if k in left:
                    e['translation_vi'] = left.pop(k); e.pop('auto_skip', None); hit = True
        if hit:
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump(recs, fh, ensure_ascii=False, indent=2)
    print('merged %d / %d' % (len(batch) - len(left), len(batch)))
    for k in left: print('  NOT FOUND:', k)
    return 1 if left else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
