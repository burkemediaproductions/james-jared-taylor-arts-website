from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,hashlib
root=Path(__file__).resolve().parents[1]/'dist'
all_original=sorted(root.glob('**/index.html'))
all_original=[x for x in all_original if 'serviceup' not in x.relative_to(root).parts]
errors=[];identical=0
class Scan(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.sources=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('a','link') and a.get('href'):self.links.append(a['href'])
  if tag in ('img','script') and a.get('src'):self.sources.append(a['src'])
for file in all_original:
 relative=file.relative_to(root);other=root/'serviceup'/relative
 if not other.exists():errors.append(f'Missing ServiceUp page: {relative}');continue
 original=file.read_text();ported=other.read_text()
 if original!=ported.replace('/serviceup/','/'):
  errors.append(f'HTML parity mismatch on {relative}')
 else:identical+=1
 check=Scan();check.feed(ported)
 for link in check.links+check.sources:
  if link.startswith('/serviceup/'):
   target=(root/link.lstrip('/'))
   if not target.exists() and not (target/'index.html').exists():errors.append(f'{relative}: missing {link}')
  if link.startswith('/assets/'):
   errors.append(f'{relative}: unprefixed asset/link {link}')
 if '<meta name="robots" content="noindex,nofollow,noarchive">' not in ported:errors.append(f'{relative}: not noindex')
 if 'application/ld+json' not in ported:errors.append(f'{relative}: no structured data')
 if '<link rel="canonical" href="https://jamesjaredtaylorarts.com/serviceup/' not in ported:errors.append(f'{relative}: wrong canonical')
print(f'Exact normalized HTML parity {identical}/{len(all_original)} routes; {len(errors)} issues')
if errors:
 print('\n'.join(errors[:50]));raise SystemExit(1)
