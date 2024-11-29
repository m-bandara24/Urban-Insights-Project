const backendURL = 'http://127.0.0.1:5000'
window.onload = function () {
    checkCredentials();
};


async function signUp(event) {
    console.log('Inside js');
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmpassword').value;
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const phoneNumber = document.getElementById('phoneNumber').value;
    const address = document.getElementById('address').value;
    const city = document.getElementById('city').value;
    const policeDivision = document.getElementById('policeDivision').value;
    const userid = document.getElementById('userid').value;
    console.log("Sending data:", { email, password, firstName, lastName, phoneNumber, address, city, policeDivision, userid });


    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    try {
        const response = await fetch(`${backendURL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
    body: JSON.stringify({ email, password, firstName,lastName,phoneNumber,address, city,policeDivision,userid})
        });

        const result = await response.json();

        if (response.ok) {
            alert('Sign Up successful! Please log in.');
            window.location.href = '/login_m';
        } else {
            alert(`Sign Up failed: ${result.message}`);
        }
    } catch (error) {
        console.error('Error during sign up:', error);
        alert('An error occurred. Please try again.');
    }
}

async function login(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${backendURL}/login_m`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: username, password }),
        });
        const result = await response.json();
        if (response.ok) {
            localStorage.setItem('token', result.token)
            window.location.href = '/dashboard';
        } else {
            alert(`Login failed: ${result.message}`);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again.');
    }
}


function logout() {
    localStorage.clear()
}

function checkCredentials() {
    const iframe = document.getElementById('isVisible');
    if (window.location.pathname.includes('/dashboard') || window.location.pathname.includes('/Dashboard')) {
        if (localStorage.getItem('token')) {
            validatingToken()
        } else {
            iframe.style.display = 'none';
            alert("Please login to continue...");
            window.location.href = '/login_m';
        }
    }


    if (window.location.pathname.includes('/login_m') || window.location.pathname.includes('/Login_m')) {
        logout()
    }

}

async function validatingToken() {
    const token = localStorage.getItem('token');
    const iframe = document.getElementById('isVisible');

    try {
        const response = await fetch(`${backendURL}/api/validate-token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token })
        });
        const result = await response.json();

        if (result.success === 'false') {
            iframe.style.display = 'none';
            logout();
            window.location.href = '/login_m';
            alert(`${result.message}`);
        } else {
            const tableauUrl = "https://public.tableau.com/app/profile/bimsari.lekamge/viz/CrimesAnalysisDashboards_17321614926280/TorontoCrimesAnalysisDashboard2";
            iframe.style.display = 'block';
            var divElement = document.getElementById('viz1732592139974');
            var vizElement = divElement.getElementsByTagName('object')[0];
            if (divElement.offsetWidth > 800) {
                vizElement.style.width = '1320px';
                vizElement.style.height = '1227px';
            } else if (divElement.offsetWidth > 500) {
                vizElement.style.width = '1320px';
                vizElement.style.height = '1227px';
            } else {
                vizElement.style.width = '100%';
                vizElement.style.height = '2327px';
            }
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        }
    } catch (error) {
        logout();
        iframe.style.display = 'none';
        window.location.href = '/login_m';
        alert('An error occurred. Please try again.');
    }
}
