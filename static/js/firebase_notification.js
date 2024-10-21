import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
import { getMessaging, getToken } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-messaging.js";

// Your Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDBD03TAn29Lwl1O-e95TianP3TLdSeaXA",
    authDomain: "pinesphere-c7119.firebaseapp.com",
    databaseURL: "https://pinesphere-c7119-default-rtdb.firebaseio.com",
    projectId: "pinesphere-c7119",
    storageBucket: "pinesphere-c7119.appspot.com",
    messagingSenderId: "149871110322",
    appId: "1:149871110322:web:d8b7d13e413724b70a41ab",
    measurementId: "G-ZTPLRHW31Y"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

// Request notification permission and get FCM token
Notification.requestPermission().then((permission) => {
    if (permission === 'granted') {
        console.log('Notification permission granted.');
        // You can now request the FCM token
        getToken(messaging, { vapidKey: 'BBcFpUHgU9bP_xQTNEM4Va_saj4kn3eAkIwC39cou3yD5WcwK1nNwvXyJGd1dWN7wmSzdKP5IHyrzMEOLN-WL1E' })
            .then((currentToken) => {
                if (currentToken) {
                    console.log('FCM Token:', currentToken);
                    // Save the FCM token to the Django backend
                    saveFcmToken(currentToken);
                } else {
                    console.log('No registration token available.');
                }
            })
            .catch((err) => {
                console.error('An error occurred while retrieving token.', err);
            });
    } else if (permission === 'denied') {
        console.log('Notification permission was blocked.');
        // Inform the user to enable notifications
    }
});

// Register the service worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/firebase-messaging-sw.js/')
        .then((registration) => {
            console.log('Service Worker registered with scope:', registration.scope);
        })
        .catch((err) => {
            console.error('Service Worker registration failed:', err);
        });
} else {
    console.error('Service workers are not supported in this browser.');
}

// Function to send FCM token to the Django backend
function saveFcmToken(token) {
    fetch('/save_fcm_token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // Django CSRF token for security
        },
        body: new URLSearchParams({
            'token': token
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('FCM Token saved successfully.');
        } else {
            console.log('Failed to save FCM Token.');
        }
    })
    .catch((err) => {
        console.error('Error saving FCM Token:', err);
    });
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
