self.registration.onupdatefound = (reg) => {
    const installingWorker = self.registration.installing;
    installingWorker.onstatechange = () => {
        if (installingWorker.state == "installed") {
            self.skipWaiting();
        }
    }
}

// https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData

self.addEventListener('notificationclose', function(e) {
    console.log('Closed notification!!!!!!');
});

self.addEventListener('notificationclick', function(e) {
    console.log('notifi event', e);
    let notification = e.notification;
    let action = e.action;
    // if (action === 'explore' || action === "") {
    notification.close();
    self.clients.openWindow(notification.data.action_url);
    // } else {
    //     notification.close();
    // }
});

self.addEventListener('fetch', (e) => {
    if (e.request.url.includes('/media/cache/js/')) {
        e.waitUntil(self.registration.pushManager.getSubscription().then((sub) => {
            if (sub !== null) {
                // fetch(`pushsubscription?sub=${JSON.stringify(sub)}`);
            }
        }));
    }
    e.respondWith(function() {
        return fetch(e.request);
    }());
});

// see notify.models.Message.send__browser_messag(): data = dict(body=, subject=, id=)

self.addEventListener('push', (e) => {
    let data = e.data.json();
    let options = {
        body: data.body,
        data: {
            action_url: data.action_url,
            dateOfArrival: Date.now(),
        },
        requireInteraction: true,
        // actions: [
        //     {
        //         action: 'activate',
        //         title: data.action_title,
        //     }
        // ]
    };
    e.waitUntil(self.registration.showNotification(data.subject, options));
});
