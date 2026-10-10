#!/usr/bin/env python3
"""Regenera el bloque de vocabulario de los capítulos 1-3 en index.html desde vocab_ch123.txt.
Uso: python3 tools/build_vocab.py   (desde la carpeta site/)"""
import re, json
MARK = '// ===== Capítulos 1-3'
html = open('index.html').read()
if MARK in html:  # quitar bloque anterior
    a = html.index(MARK); a = html.rindex('\n', 0, a)
    b = html.index('\n        ];', a)
    html = html[:a].rstrip().rstrip(',') + ',' + html[b:] if False else html[:a] + html[b:]
ch4 = set(x.lower() for x in re.findall(r'german: "([^"]*)"', html))
seen, ch, out = set(ch4), None, []
art = re.compile(r'^(el|la|los|las|un|una) ')
for l in open('tools/vocab_ch123.txt').read().split('\n'):
    l = l.strip()
    if not l or (l.startswith('#') and not l.startswith('##')): continue
    if l.startswith('##'): ch = int(l[2:]); continue
    g, a = [x.strip() for x in l.split(' = ', 1)]
    if g.lower() in seen: continue
    seen.add(g.lower())
    ans = []
    for x in (y.strip() for y in a.split('|')):
        for v in (x, art.sub('', x)):
            if v and v not in ans: ans.append(v)
    out.append((ch, g, ans))
block = ['\n            ' + MARK + ' (generado desde tools/vocab_ch123.txt) =====']
block += ['            { german: %s, spanish: %s, ch: %d },' % (json.dumps(g, ensure_ascii=False), json.dumps(a, ensure_ascii=False), c) for c, g, a in out]
i = html.index('const fullVocab = ['); j = html.index('\n        ];', i)
body = html[i:j].rstrip()
if not body.endswith(','): body += ','
open('index.html', 'w').write(html[:i] + body + '\n'.join(block) + '\n' + html[j:].lstrip('\n') if False else html[:i] + body + '\n'.join(block) + html[j:])
print(len(out), 'palabras nuevas')
