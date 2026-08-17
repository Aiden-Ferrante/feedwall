import json
tpl=open('tpl.html',encoding='utf-8').read()
ENT={'·':'&middot;','—':'&mdash;','›':'&rsaquo;','×':'&times;','≥':'&ge;','“':'&ldquo;','”':'&rdquo;'}
ESC={k:'\\u%04x'%ord(k) for k in ENT}
head,sep,body=tpl.partition('<script>')
for a,b in ENT.items(): head=head.replace(a,b)
for a,b in ESC.items(): body=body.replace(a,b)
tpl=head+sep+body
left=sorted({c for c in tpl if ord(c)>127})
assert not left, left
out=tpl.replace('__DATA__', json.dumps(json.load(open('sources.json')),separators=(',',':')))
assert '__DATA__' not in out and all(ord(c)<128 for c in out)
open('index.html','w',encoding='ascii').write(out)
print('built', len(out), 'bytes')
