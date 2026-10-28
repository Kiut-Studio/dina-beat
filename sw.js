// Copia sin conexión. Comparte sitio con otros juegos: solo toca sus propias cachés.
const CACHE='dina-beat-v12';
const FILES=['./','index.html','manifest.json','favicon-32.png','icon-192.png','icon-512.png',
  'assets/sofi.webp','assets/sofi_hoodie.webp','assets/deisy.webp','assets/leandro.webp','assets/nora.webp','assets/cinthia.webp','assets/dina.webp','assets/dina_corre.webp','assets/frutilla.webp','assets/pancito.webp','assets/torta.webp','assets/nubes.webp'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.startsWith('dina-beat-')&&n!==CACHE).map(n=>caches.delete(n)))));self.clients.claim()});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)))});
