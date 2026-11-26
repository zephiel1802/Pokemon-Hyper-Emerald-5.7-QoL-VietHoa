"""Fast merge of ALL batches into the dump JSON files in one single pass."""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)


def main():
    batch_files = sorted(glob.glob(os.path.join(VI, 'batches', '*.json')))
    print(f'Loading {len(batch_files)} batch files...')
    all_batches = {}
    for bf in batch_files:
        if bf.endswith('poc_01_opening.json'):
            continue
        try:
            d = json.load(open(bf, encoding='utf-8'))
            all_batches.update(d)
        except Exception as ex:
            print(f'Error reading {bf}: {ex}')
            return 1

    print(f'Total translation entries in all batches: {len(all_batches)}')
    left = dict(all_batches)

    target_files = sorted(glob.glob(os.path.join(VI, 'dialogues', '*.json'))) + sorted(glob.glob(os.path.join(VI, 'tables', '*.json')))
    total_updated = 0

    for f in target_files:
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
                    val = left.pop(k)
                    e['translation_vi'] = val
                    if val != '@@SKIP@@':
                        e.pop('auto_skip', None)
                    hit = True
                    total_updated += 1
        if hit:
            with open(f, 'w', encoding='utf-8') as fh:
                json.dump(recs, fh, ensure_ascii=False, indent=2)

    print(f'Successfully merged {total_updated} entries into dump files.')
    print(f'Remaining unmatched keys: {len(left)}')
    if left:
        for k in list(left.keys())[:20]:
            print('  Unmatched:', k)
    return 0


if __name__ == '__main__':
    sys.exit(main())
