// Helper function to get a cookie by name
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

// Logout function
function logout() {
    // Clear access token cookie
    document.cookie = "access_token=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    // Redirect to login page
    window.location.href = '/auth/login-page';
}

// Add generic fetch helper that inserts the Authorization header automatically
async function authenticatedFetch(url, options = {}) {
    const token = getCookie('access_token');
    if (token) {
        options.headers = {
            ...options.headers,
            'Authorization': `Bearer ${token}`
        };
    }
    return fetch(url, options);
}

// Authentication Forms Handlers
document.addEventListener('DOMContentLoaded', () => {
    // Login Form Handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const form = event.target;
            
            // Disable button and show spinner
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalHTML = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="btn-spinner"></span>Signing In...';

            const formData = new FormData(form);
            const payload = new URLSearchParams();
            for (const [key, value] of formData.entries()) {
                payload.append(key, value);
            }

            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: payload.toString()
                });

                if (response.ok) {
                    const data = await response.json();
                    // Clear old token and set new cookie
                    document.cookie = "access_token=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
                    document.cookie = `access_token=${data.access_token}; path=/; SameSite=Lax`;
                    
                    window.location.href = '/wishes/dashboard';
                } else {
                    const errorData = await response.json();
                    alert(`Login Failed: ${errorData.detail || 'Invalid username or password'}`);
                    // Restore button state
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalHTML;
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred. Please try again.');
                // Restore button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalHTML;
            }
        });
    }

    // Register Form Handler
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            if (data.password !== data.password2) {
                alert("Passwords do not match!");
                return;
            }

            // Disable button and show spinner
            const submitBtn = registerForm.querySelector('button[type="submit"]');
            const originalHTML = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="btn-spinner"></span>Creating Account...';

            const payload = {
                email: data.email,
                username: data.username,
                first_name: data.firstname,
                last_name: data.lastname,
                role: data.role,
                phone_number: data.phone_number,
                password: data.password
            };

            try {
                const response = await fetch('/auth', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    alert("Registration successful! Redirecting to login page...");
                    window.location.href = '/auth/login-page';
                } else {
                    const errorData = await response.json();
                    alert(`Registration Failed: ${errorData.detail || 'Could not register user'}`);
                    // Restore button state
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalHTML;
                }
            } catch (error) {
                console.error('Error during registration:', error);
                alert('An error occurred. Please try again.');
                // Restore button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalHTML;
            }
        });
    }
});
