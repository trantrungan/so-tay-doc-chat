const PHIEN_BAN = "25069cad4f";
const KHO = "so-tay-doc-chat-" + PHIEN_BAN;
const TEP = [
  "./",
  "index.html",
  "style.css",
  "app.js",
  "manifest.webmanifest",
  "icon.svg",
  "icon-192.png",
  "icon-512.png",
  "data/doc-chat.json",
  "hinh/lidocaine.png",
  "hinh/tetrahydrocannabinol.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(KHO).then((k) => k.addAll(TEP)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((ten) => Promise.all(ten.filter((t) => t !== KHO).map((t) => caches.delete(t))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then((sanCo) => {
      const mang = fetch(e.request)
        .then((kq) => {
          if (kq && kq.status === 200 && kq.type === "basic") {
            const ban = kq.clone();
            caches.open(KHO).then((k) => k.put(e.request, ban));
          }
          return kq;
        })
        .catch(() => sanCo);
      return sanCo || mang;
    })
  );
});
