
// This is the AlekSIS service worker

const CACHE = 'aleksis-cache';

const offlineFallbackPage = 'offline/';

const channel = new BroadcastChannel('cache-or-not');

var comesFromCache = false;

self.addEventListener("install", function (event) {
    console.log("[AlekSIS PWA] Install Event processing.");

    console.log("[AlekSIS PWA] Skipping waiting on install.");
    self.skipWaiting();

    event.waitUntil(
        caches.open(CACHE).then(function (cache) {
            console.log("[AlekSIS PWA] Caching pages during install.");
            return cache.add(offlineFallbackPage);
        })
    );
});

// Allow sw to control of current page
self.addEventListener("activate", function (event) {
    console.log("[AlekSIS PWA] Claiming clients for current page.");
    event.waitUntil(self.clients.claim());
});

// If any fetch fails, it will look for the request in the cache and serve it from there first
self.addEventListener("fetch", function (event) {
    if (event.request.method !== "GET") return;
    networkFirstFetch(event);
    if (comesFromCache) channel.postMessage(true);
});

function networkFirstFetch(event) {
    event.respondWith(
        fetch(event.request)
            .then(function (response) {
                // If request was successful, add or update it in the cache
                console.log("[AlekSIS PWA] Network request successful.");
                event.waitUntil(updateCache(event.request, response.clone()));
                comesFromCache = false;
                return response;
            })
            .catch(function (error) {
                console.log("[AlekSIS PWA] Network request failed. Serving content from cache: " + error);
                return fromCache(event);
            })
    );
}

function fromCache(event) {
    // Check to see if you have it in the cache
    // Return response
    // If not in the cache, then return offline fallback page
    return caches.open(CACHE).then(function (cache) {
        return cache.match(event.request)
            .then(function (matching) {
                if (!matching || matching.status === 404) {
                    console.log("[AlekSIS PWA] Cache request failed. Serving offline fallback page.");
                    comesFromCache = false;
                    // Use the precached offline page as fallback
                    return caches.match(offlineFallbackPage);
                }
                comesFromCache = true;
                return matching;
            });
    });
}

function updateCache(request, response) {
    if (response.headers.get('cache-control') && response.headers.get('cache-control').includes('no-cache')) {
        return Promise.resolve();
    } else {
        return caches.open(CACHE).then(function (cache) {
            return cache.put(request, response);
        });
    }
}
