document.getElementById('send-email').addEventListener('click', function () {
    const formData = new FormData();
    
    // Main fields
    formData.append('main_title', document.getElementById('main-title').value);
    formData.append('main_content', document.getElementById('main-content').value);
    formData.append('main_url', document.getElementById('main_url').value);  // Main URL

    const mainImageInput = document.getElementById('main_image');
    if (mainImageInput.files.length > 0) {
        formData.append('main_image', mainImageInput.files[0]);  // Main Image
    }

    // Topic One fields
    formData.append('topic_one_heading', document.getElementById('topic-one-heading').value);
    formData.append('topic_one_content', document.getElementById('topic-one-content').value);
    formData.append('topic_one_link', document.getElementById('topic-one-link').value);

    const topicOneImageInput = document.getElementById('topic_one_image');
    if (topicOneImageInput.files.length > 0) {
        formData.append('topic_one_image', topicOneImageInput.files[0]);  // Topic One Image
    }

    // Topic Two fields
    formData.append('topic_two_heading', document.getElementById('topic-two-heading').value);
    formData.append('topic_two_content', document.getElementById('topic-two-content').value);
    formData.append('topic_two_link', document.getElementById('topic-two-link').value);

    const topicTwoImageInput = document.getElementById('topic_two_image');
    if (topicTwoImageInput.files.length > 0) {
        formData.append('topic_two_image', topicTwoImageInput.files[0]);  // Topic Two Image
    }

    // Sending the FormData with the fetch request
    fetch('/send-welcome-email/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken,  // Use the correct CSRF token
        }
    })
    .then(response => {
        if (response.ok) {
            Swal.fire({
                title: 'Success!',
                text: 'Emails sent successfully!',
                icon: 'success',
                confirmButtonText: 'OK'
            });
        } else {
            Swal.fire({
                title: 'Error!',
                text: 'Something went wrong while sending emails!',
                icon: 'error',
                confirmButtonText: 'Try Again'
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            title: 'Error!',
            text: 'An error occurred while sending the emails.',
            icon: 'error',
            confirmButtonText: 'Try Again'
        });
    });
});
