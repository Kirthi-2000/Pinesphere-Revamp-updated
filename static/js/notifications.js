document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('notificationForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const title = document.getElementById('title').value;
        const body = document.getElementById('body').value;
        const url = document.getElementById('url').value;
        const imageFile = document.getElementById('image').files[0];

        const formData = new FormData();
        formData.append('title', title);
        formData.append('body', body);
        formData.append('url', url);
        formData.append('image', imageFile);

        fetch('/send-notification/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => {
            console.log('Response status:', response.status); // Check the response status
            return response.json();
        })
        .then(result => {
            console.log('Result:', result); // Log the result for debugging
            // Check the result and show appropriate SweetAlert
            if (result.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Notification Sent',
                    text: result.message, // Use the message from the result
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: result.error || 'Failed to send notification. Please try again.',
                });
            }
        })
        .catch(error => {
            console.error('Error sending notification:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'An error occurred while sending the notification.',
            });
        });
    });

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
});
