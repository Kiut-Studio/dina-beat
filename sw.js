// Copia sin conexión. Comparte sitio con otros juegos: solo toca sus propias cachés.
const CACHE='dina-beat-v26';
const FILES=['./','index.html','manifest.json','favicon-32.png','icon-192.png','icon-512.png',
  'assets/sofi.webp','assets/sofi_hoodie.webp','assets/deisy.webp','assets/leandro.webp','assets/nora.webp','assets/cinthia.webp','assets/dina.webp','assets/dina_corre.webp','assets/frutilla.webp','assets/pancito.webp','assets/torta.webp','assets/nubes.webp',
  'assets/sofi_alicia.webp','assets/calabaza.webp','assets/dina_calabaza.webp','assets/dina_bruja.webp','assets/dina_brujito.webp','assets/dina_vampiro.webp',
  'assets/hw_caramelo_verde.webp','assets/hw_chupetin.webp','assets/hw_candy_corn.webp','assets/hw_gomita.webp','assets/hw_bombon.webp','assets/hw_caramelo_violeta.webp'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.startsWith('dina-beat-')&&n!==CACHE).map(n=>caches.delete(n)))));self.clients.claim()});
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request)))});
