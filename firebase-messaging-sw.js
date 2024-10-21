importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.0.0/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyDBD03TAn29Lwl1O-e95TianP3TLdSeaXA",
  authDomain: "pinesphere-c7119.firebaseapp.com",
  projectId: "pinesphere-c7119",
  storageBucket: "pinesphere-c7119.appspot.com",
  messagingSenderId: "149871110322",
  appId: "1:149871110322:web:d8b7d13e413724b70a41ab",
};

// Initialize Firebase in the service worker
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage((payload) => {
  console.log('Received background message:', payload);

  // Extract dynamic data from the payload
  const notificationTitle = payload.data.title || 'Default Title';
  const notificationOptions = {
    body: payload.data.body || 'Default Body',
    icon: payload.data.image || '/path/to/default/icon.png',
    data: {
      url: payload.data.click_action || 'https://default-url.com'  // Default URL if not provided
    }
  };

  // Show the notification
  self.registration.showNotification(notificationTitle, notificationOptions);
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
  event.notification.close();  // Close the notification

  event.waitUntil(
    clients.matchAll({ type: 'window' }).then((clientList) => {
      const matchingClient = clientList.find(client => client.url === event.notification.data.url && 'focus' in client);
      if (matchingClient) {
        return matchingClient.focus();  // Focus on the existing tab if already open
      } else {
        return clients.openWindow(event.notification.data.url);  // Otherwise, open a new tab
      }
    })
  );
});
