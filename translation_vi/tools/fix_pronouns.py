"""Batch adjust pronouns in Vietnamese dialogues:
Replace 2nd-person pronoun 'bạn / Bạn' (referring to the player) with 'cậu / Cậu'
while strictly preserving:
- Friendship terms: 'người bạn', 'những người bạn', 'các bạn ấy', 'các bạn', 'bạn bè', 'bạn thân', 'tình bạn', 'kết bạn', 'làm bạn', 'bạn tốt', 'bạn của', 'bạn nhỏ', 'bạn hiền', etc.
"""
import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
VI = os.path.dirname(HERE)

PROTECTED = [
    'người bạn', 'Người bạn', 'những người bạn', 'Những người bạn',
    'các bạn ấy', 'Các bạn ấy', 'các bạn nhỏ', 'Các bạn nhỏ',
    'các bạn Pokémon', 'Các bạn Pokémon', 'các bạn', 'Các bạn',
    'bạn đồng hành', 'Bạn đồng hành', 'bạn bè', 'Bạn bè',
    'bạn thân', 'Bạn thân', 'tình bạn', 'Tình bạn',
    'kết bạn', 'Kết bạn', 'làm bạn', 'Làm bạn',
    'bạn tốt', 'Bạn tốt', 'bạn gái', 'Bạn gái', 'bạn trai', 'Bạn trai',
    'bạn hiền', 'Bạn hiền', 'bạn nhỏ', 'Bạn nhỏ',
    'bạn của', 'Bạn của'
]

DELIM = r'(\\[pnl]|^|[\s\.,!?:;\(\)\[\]\"\'”`—–\-])'
LOOKAHEAD = r'(?=(\\[pnl]|$|[\s\.,!?:;\(\)\[\]\"\'”`—–\-]))'
RE_BAN = re.compile(DELIM + r'(Bạn|bạn)' + LOOKAHEAD)

def fix_pronouns_in_text(text):
    if 'bạn' not in text and 'Bạn' not in text:
        return text
    
    masked = text
    masks = {}
    for i, p in enumerate(PROTECTED):
        m_str = f'__PROT_{i:02d}__'
        if p in masked:
            masks[m_str] = p
            masked = masked.replace(p, m_str)
    
    def repl(m):
        prefix = m.group(1)
        word = m.group(2)
        new_word = 'Cậu' if word == 'Bạn' else 'cậu'
        return prefix + new_word
    
    masked = RE_BAN.sub(repl, masked)
    
    for m_str, orig in masks.items():
        masked = masked.replace(m_str, orig)
    
    return masked

def main(dry_run=False):
    total_changed = 0
    total_files = 0
    dialogue_files = sorted(glob.glob(os.path.join(VI, 'dialogues', 'dialogues_*.json')))
    
    for f in dialogue_files:
        with open(f, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        
        file_changed = 0
        for e in data:
            vi = e.get('translation_vi', '')
            if not vi: continue
            new_vi = fix_pronouns_in_text(vi)
            if new_vi != vi:
                if total_changed < 25:
                    print(f"[{e['id']}] {e['offset_hex']}")
                    print(f"  OLD: {vi[:90]}")
                    print(f"  NEW: {new_vi[:90]}")
                e['translation_vi'] = new_vi
                file_changed += 1
                total_changed += 1
        
        if file_changed > 0:
            total_files += 1
            if not dry_run:
                with open(f, 'w', encoding='utf-8') as fh:
                    json.dump(data, fh, ensure_ascii=False, indent=2)
    
    print(f"\nCompleted! Total entries updated: {total_changed} across {total_files} files (dry_run={dry_run}).")

if __name__ == '__main__':
    import sys
    dry = '--dry' in sys.argv
    main(dry_run=dry)
