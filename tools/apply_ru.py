#!/usr/bin/env python3
"""Generate res/values-ru/strings.xml in an apktool-decoded 长安启源 APK
from translation/ru/*.json, checking that format placeholders survive."""
import glob, json, os, re, sys

dec = sys.argv[1]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(dec, 'res/values/strings.xml'), encoding='utf-8').read()
orig = dict(re.findall(r'<string name="([^"]+)"[^>]*>(.*?)</string>', src, re.S))

tr = {}
for f in sorted(glob.glob(os.path.join(root, 'translation/ru/*.json'))):
    tr.update(json.load(open(f, encoding='utf-8')))

ph = re.compile(r'%(?:\d+\$)?[sdf]|\$s')
bad = 0
out = ['<?xml version="1.0" encoding="utf-8" standalone="no"?>', '<resources>']
for k, v in sorted(tr.items()):
    if k not in orig:
        print('unknown key:', k); bad += 1; continue
    if sorted(ph.findall(orig[k])) != sorted(ph.findall(v)):
        print('placeholder mismatch:', k, orig[k], '->', v); bad += 1
    v = v.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    v = re.sub(r"(?<!\\)'", r"\\'", v)
    out.append(f'    <string name="{k}">{v}</string>')
out.append('</resources>')
if bad:
    sys.exit(f'{bad} problem(s), not writing')
os.makedirs(os.path.join(dec, 'res/values-ru'), exist_ok=True)
open(os.path.join(dec, 'res/values-ru/strings.xml'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f'wrote {len(tr)} strings')
