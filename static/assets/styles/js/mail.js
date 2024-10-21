// Select all input fields for adding focus effect
const inputs = document.querySelectorAll(".input");

// Add focus effect to input fields
function focusFunc() {
  let parent = this.parentNode;
  parent.classList.add("focus");
}

// Remove focus effect when input is empty
function blurFunc() {
  let parent = this.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

// Attach focus and blur events to all input fields
inputs.forEach((input) => {
  input.addEventListener("focus", focusFunc);
  input.addEventListener("blur", blurFunc);
});

// Get form field elements
const firstName = document.getElementById('edit-first-name');
const lastName = document.getElementById('edit-last-name');
const emailAddress = document.getElementById('edit-email-address');
const message = document.getElementById('edit-message');
const phoneNumber = document.getElementById('edit-phone-number');
const submitForm = document.getElementById('webform-submission-get-in-touch-paragraph-3727-add-form');

// Add submit event listener to the form
submitForm.addEventListener('submit', (e) => {
  e.preventDefault(); // Prevent default form submission
  console.log("Form submitted!");

  // Send email using EmailJS
  Email.send({
    SecureToken: "83d1d6ed-39bd-474e-8cc4-e69d44d59009",
    To: 'vandhana.jayakumar1106@gmail.com',
    From: "vandhana.jayakumar1106@gmail.com",
    Subject: "Contact Form Submission",
    Body: `
      <b>First Name:</b> ${firstName.value}<br>
      <b>Last Name:</b> ${lastName.value}<br>
      <b>Email:</b> ${emailAddress.value}<br>
      <b>Phone Number:</b> ${phoneNumber.value}<br>
      <b>Message:</b> ${message.value}
    `
  }).then(() => {
    document.getElementById("alert").showModal(); // Show success modal
  });
});

// Function to close the alert modal
function notify() {
  document.getElementById("alert").close();
}
