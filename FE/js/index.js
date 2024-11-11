const backendURL = 'http://127.0.0.1:5000'
window.onload = function () {
    checkCredentials();
};


async function signUp(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return;
    }

    try {
        const response = await fetch(`${backendURL}/api/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok) {
            alert('Sign Up successful! Please log in.');
            window.location.href = 'login.html';
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
        const response = await fetch(`${backendURL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: username, password })
        });

        const result = await response.json();
        if (response.ok) {
            localStorage.setItem('token', result.token)
            window.location.href = './dashboard.html';
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
    if (window.location.pathname.includes('dashboard.html') || window.location.pathname.includes('Dashboard.html')) {
        if (localStorage.getItem('token')) {
            validatingToken()
        } else {
            iframe.style.display = 'none';
            alert("Please login to continue...");
            window.location.href = './index.html';
        }
    }


    if (window.location.pathname.includes('login.html') || window.location.pathname.includes('Login.html')) {
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
            window.location.href = './login.html';
            alert(`${result.message}`);
        } else {
            const tableauUrl = "https://public.tableau.com/views/TorontoCrimesAnalysis/TorontoCrimesAnalysisDashboard";
            iframe.style.display = 'block';
            var divElement = document.getElementById('viz1731023434304');
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
        window.location.href = './login.html';
        alert('An error occurred. Please try again.');
    }
}
