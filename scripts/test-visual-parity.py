"""Offline headless responsive layout regression test.
Browser network navigation is disabled in this runner; inject generated HTML,
original CSS, and original JS directly. This validates layout/interaction but not Netlify networking.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re
root=Path(__file__).resolve().parents[1]/'dist'
css=(root/'assets/css/styles.css').read_text()
js=(root/'assets/js/site.js').read_text()
blank='data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="800" height="900"/%3E'
def html_at(path):
 s=path.read_text()
 s=re.sub(r'<link[^>]+(?:rel="stylesheet"|rel="preload")[^>]*>', '', s)
 s=re.sub(r'<script defer src="[^"]+"></script>', '',s)
 s=re.sub(r'(<img\b[^>]*?\bsrc=")[^"]+',lambda m:m.group(1)+blank,s)
 s=s.replace('</head>','<style>'+css+'</style></head>')
 return s
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--no-proxy-server'])
 for width,height in [(1440,900),(820,1024),(390,844)]:
  context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce')
  a=context.new_page();b=context.new_page()
  for slug in ['','about/','current-work/paintings/','blog/']:
   for page,prefix in [(a,''),(b,'serviceup/')]:
    page.set_content(html_at(root/prefix/slug/'index.html'),wait_until='load')
    page.add_script_tag(content=js)
    page.evaluate('document.fonts.ready')
   def metrics(page):
    return page.evaluate('''() => ({title:document.title, headings:[...document.querySelectorAll('h1,h2')].map(x=>x.textContent.trim()), sections:[...document.querySelectorAll('main>section')].map(x=>({name:x.className.replace(' visible','').trim(),height:Math.round(x.getBoundingClientRect().height)})),links:document.querySelectorAll('a').length,images:document.querySelectorAll('img').length,overflow:document.documentElement.scrollWidth>innerWidth,menuVisible:getComputedStyle(document.querySelector('.menu-button')).display})''')
   left,right=metrics(a),metrics(b)
   assert left==right,(width,slug,left,right)
   results.append({'width':width,'route':slug or '/','result':'matching DOM and section-size metrics','horizontal_overflow':left['overflow']})
  if width==390:
   b.set_content(html_at(root/'serviceup/index.html'),wait_until='load');b.add_script_tag(content=js)
   button=b.locator('.menu-button');button.click();assert button.get_attribute('aria-expanded')=='true'
   b.keyboard.press('Escape');assert button.get_attribute('aria-expanded')=='false'
  if width==1440:
   artwork=next((root/'serviceup/current-work/paintings').glob('*/index.html'))
   b.set_content(html_at(artwork),wait_until='load');b.add_script_tag(content=js)
   b.locator('[data-open-lightbox]').first.click();assert b.locator('#lightbox').is_visible()
   b.keyboard.press('Escape');assert not b.locator('#lightbox').is_visible()
  context.close()
 browser.close()
Path(__file__).resolve().parents[1].joinpath('serviceup/visual-audit.json').write_text(json.dumps(results,indent=2))
print('Offline 1440/820/390px DOM, layout, menu & lightbox checks passed.')
