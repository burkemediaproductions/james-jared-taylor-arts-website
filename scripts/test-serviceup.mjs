import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {createServer} from 'node:http';
const manifest=JSON.parse(fs.readFileSync('serviceup/james-jared-taylor-import.json','utf8'));
const server=createServer((req,res)=>{
 if(req.headers['x-serviceup-tenant']!=='james-jared-taylor'){res.writeHead(400);res.end('Tenant header required');return;}
 const route=new URL(req.url,'http://local').pathname;
 let body;
 if(route.startsWith('/api/content/')){
  const slug=route.split('/').at(-1);
  body=manifest.entries.filter(x=>x.content_type_slug===slug);
  if(process.env.TEST_SERVICEUP_EDIT==='1'&&slug==='page')body=body.map(e=>{if(e.slug!=='home')return e;const c=structuredClone(e);const hero=c.data.panels.panels.find(x=>x.type==='jjt-home-hero');hero.data.bottom_text='A test change made in ServiceUp.';return c;});
 }else if(route==='/api/public/menu/main')body={items:manifest.menus[0].items};
 else {res.writeHead(404);res.end('Not found');return;}
 res.setHeader('Content-Type','application/json');res.end(JSON.stringify(body));
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const port=server.address().port;
// Synchronous spawn would block the mock HTTP server; use asynchronous child.
const {spawn}=await import('node:child_process');
const p=spawn(process.execPath,['scripts/build-serviceup.mjs'],{stdio:'inherit',env:{...process.env,SERVICEUP_API_BASE:`http://127.0.0.1:${port}`,SERVICEUP_TEST_LOCAL:'1'}});
const exit=await new Promise(resolve=>p.on('close',resolve));server.close();
if(exit!==0)process.exit(exit||1);
const actual=fs.readFileSync('dist/serviceup/index.html','utf8');
for(const expected of ['/serviceup/assets/css/styles.css','/serviceup/about/','noindex,nofollow','hero-art-left','hero-art-right','Between the image'])if(!actual.includes(expected))throw Error(`ServiceUp homepage missing ${expected}`);
const about=fs.readFileSync('dist/serviceup/about/index.html','utf8');
if(!about.includes('/serviceup/assets/images/james-jared-taylor-portrait.jpeg'))throw Error('Missing portrait');
if(process.env.TEST_SERVICEUP_EDIT==='1'){if(!actual.includes('A test change made in ServiceUp.'))throw Error('Panel edit was not rendered in static HTML');console.log('Edited panel rendered from ServiceUp.');}else console.log('ServiceUp mocked API integration passed.');
