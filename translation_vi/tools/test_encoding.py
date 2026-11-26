import sys, os, json, struct
sys.path.insert(0, 'translation_vi/tools')
from insert import Encoder, NORMALIZE
from gen3text import CHR2BYTE
from expanded_battle_dict import EXPANDED_BATTLE_TRANSLATIONS
from bst_full_dict import BST_FULL_TRANSLATIONS

with open('translation_vi/build/Hyper Emerald v5.7 VIE.gba', 'rb') as f:
    rom = bytearray(f.read())

report = json.load(open('translation_vi/build/build_report.json', encoding='utf-8'))
cmap = {c: int(b, 16) for c, b in report['font']['slots'].items()}

def enc_battle(text):
    text = text.replace('\\\\n', '\\n').replace('\\\\l', '\\l').replace('\\\\p', '\\p')
    for k, v in NORMALIZE.items(): text = text.replace(k, v)
    out = bytearray()
    i = 0
    L = len(text)
    while i < L:
        if text[i] == '\\' and i + 1 < L and text[i + 1] in 'nlp':
            out.append({'n': 0xFE, 'l': 0xFA, 'p': 0xFB}[text[i + 1]])
            i += 2
            continue
        if text[i] == '[':
            end = text.find(']', i)
            if end != -1:
                token = text[i:end+1]
                if token.startswith('[BUF'):
                    code = int(token[4:6], 16)
                    out.extend([0xFD, code])
                elif token.startswith('[FC'):
                    raw_hex = bytes.fromhex(token[3:-1])
                    out.extend([0xFC] + list(raw_hex))
                elif token == '[F7]':
                    out.append(0xF7)
                elif token == '[Lv]':
                    out.append(0x34)
                elif len(token) == 6 and token[1:3] in ('F8', 'F9'):
                    out.extend(bytes.fromhex(token[1:5]))
                i = end + 1
                continue
        c = text[i]
        if c in cmap: out.append(cmap[c])
        elif c in CHR2BYTE: out.append(CHR2BYTE[c])
        elif c.lower() in cmap: out.append(cmap[c.lower()])
        else: raise ValueError(f'Cannot encode {repr(c)} in {repr(text)}')
        i += 1
    out.append(0xFF)
    return bytes(out)

print('Testing encoding for all 310 expanded battle strings...')
for k, v in EXPANDED_BATTLE_TRANSLATIONS.items():
    b = enc_battle(v)

print('Testing encoding for all 250 BST strings...')
for k, v in BST_FULL_TRANSLATIONS.items():
    b = enc_battle(v)

print('SUCCESS! All 560 battle strings encoded with zero errors!')
