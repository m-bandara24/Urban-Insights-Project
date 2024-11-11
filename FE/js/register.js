    document.getElementById('register-form').addEventListener('submit', function(event) {
        // Prevent form submission if validation fails
        event.preventDefault();

    // Get form fields
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const phoneNumber = document.getElementById('phoneNumber').value.trim();
    const email = document.getElementById('email').value.trim();
    const address = document.getElementById('address').value.trim();
    const city = document.getElementById('city').value.trim();
    const province = document.getElementById('province').value.trim();
    const postalCode = document.getElementById('postalCode').value.trim();
    const password1 = document.getElementById('password1').value;
    const confirmPassword = document.getElementById('confirmpassword').value;
    const termsCheckbox = document.getElementById('gridCheck').checked;

    // Validation checks
    let isValid = true;
    let errorMessage = '';

    // Validate names
    if (!firstName || !lastName) {
        errorMessage += 'First and Last names are required.\n';
    isValid = false;
        }

    // Validate phone number (example pattern for North America, adjust if needed)
    const phonePattern = /^[0-9]{10}$/;
    if (!phonePattern.test(phoneNumber)) {
        errorMessage += 'Please enter a valid 10-digit phone number.\n';
    isValid = false;
        }

    // Validate email format
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        errorMessage += 'Please enter a valid email address.\n';
    isValid = false;
        }

    // Validate address fields
    // if (!address || !city || !province || !postalCode) {
    //     errorMessage += 'Address, City, Province, and Postal Code are required.\n';
    // isValid = false;
    //     }

    // Validate password length and match
    if (password1.length < 8) {
        errorMessage += 'Password must be at least 8 characters long.\n';
    isValid = false;
        }
    if (password1 !== confirmPassword) {
        errorMessage += 'Passwords do not match.\n';
    isValid = false;
        }

    // Validate terms and conditions checkbox
    if (!termsCheckbox) {
        errorMessage += 'You must agree to the Terms and Conditions.\n';
    isValid = false;
        }

    // Show validation errors or submit form
    if (isValid) {
        // If form is valid, allow submission
        this.submit();
        } else {
        // Otherwise, display error message
        alert(errorMessage);
        }
    });
