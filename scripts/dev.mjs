import {spawn} from 'node:child_process';
import {createServer} from 'node:http';
import {readFile,stat} from 'node:fs/promises';
import path from 'node:path';
const tasks=process.argv.includes('--serviceup')?['scripts/build.mjs','scripts/build-serviceup.mjs']:['scripts/build.mjs'];
for(const script of tasks)await new Promise((resolve,reject)=>{const p=spawn(process.execPath,[script],{stdio:'inherit'});p.on('close',c=>c===0?resolve():reject(Error('Build failed: '+script)))});
const root=path.resolve('dist'); const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.xml':'application/xml','.txt':'text/plain','.json':'application/json','.webp':'image/webp','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.gif':'image/gif'};
createServer(async(req,res)=>{try{let url=decodeURI(new URL(req.url,'http://localhost').pathname);let f=path.resolve(root,'.'+url);if(!f.startsWith(root))throw Error();const s=await stat(f).catch(()=>null);if(s?.isDirectory())f=path.join(f,'index.html');let data=await readFile(f);res.setHeader('Content-Type',types[path.extname(f)]||'application/octet-stream');res.end(data)}catch{res.statusCode=404;res.end('Not found')}}).listen(4173,()=>console.log('http://localhost:4173'));
