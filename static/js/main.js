// Initialize AOS (Animate On Scroll)
AOS.init({
    once: true,
    offset: 50,
});

// Particles.js configuration
if (document.getElementById('particles-js')) {
    particlesJS('particles-js', {
        "particles": {
            "number": { "value": 80, "density": { "enable": true, "value_area": 800 } },
            "color": { "value": "#00f3ff" },
            "shape": { "type": "circle" },
            "opacity": { "value": 0.3, "random": true },
            "size": { "value": 3, "random": true },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#00f3ff",
                "opacity": 0.2,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 2,
                "direction": "none",
                "random": true,
                "out_mode": "out"
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": { "enable": true, "mode": "grab" },
                "onclick": { "enable": true, "mode": "push" },
                "resize": true
            },
            "modes": {
                "grab": { "distance": 140, "line_linked": { "opacity": 0.8 } },
                "push": { "particles_nb": 4 }
            }
        },
        "retina_detect": true
    });
}

// TODO: Replace with your actual Firebase config
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}
const auth = firebase.auth();

// Auth State Observer
auth.onAuthStateChanged(user => {
    const loginNav = document.getElementById('nav-login');
    const dashNav = document.getElementById('nav-dashboard');
    const logoutNav = document.getElementById('nav-logout');
    
    // Check for mock user if Firebase API Key is not set
    const isMockUser = sessionStorage.getItem('mock_user') === 'true';
    const activeUser = user || isMockUser;

    if (activeUser) {
        if (loginNav) loginNav.style.display = 'none';
        if (dashNav) dashNav.style.display = 'block';
        if (logoutNav) logoutNav.style.display = 'block';
        
        // If on login/signup page, redirect to dashboard
        const path = window.location.pathname;
        if (path === '/login' || path === '/signup') {
            window.location.href = '/dashboard';
        }
    } else {
        if (loginNav) loginNav.style.display = 'block';
        if (dashNav) dashNav.style.display = 'none';
        if (logoutNav) logoutNav.style.display = 'none';
        
        // Protect dashboard
        const path = window.location.pathname;
        if (path.startsWith('/dashboard') || path.startsWith('/upload')) {
            window.location.href = '/login';
        }
    }
});

// Logout function
function logout() {
    if (sessionStorage.getItem('mock_user') === 'true') {
        sessionStorage.removeItem('mock_user');
        sessionStorage.removeItem('mock_name');
        window.location.href = '/';
        return;
    }

    auth.signOut().then(() => {
        window.location.href = '/';
    }).catch(error => {
        console.error("Logout Error", error);
    });
}

// Handle Login Form
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('login-error');
        const btn = document.getElementById('login-btn');
        
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Authenticating...';
        btn.disabled = true;

        // --- MOCK LOGIN BYPASS ---
        if (firebaseConfig.apiKey === "YOUR_API_KEY") {
            console.log("Mock Login: Bypassing Firebase Auth because API Key is not set.");
            setTimeout(() => {
                sessionStorage.setItem('mock_user', 'true');
                window.location.href = '/dashboard';
            }, 1000);
            return;
        }
        // -------------------------
        
        auth.signInWithEmailAndPassword(email, password)
            .then((userCredential) => {
                // Redirect will happen in onAuthStateChanged
            })
            .catch((error) => {
                errorDiv.textContent = error.message;
                errorDiv.classList.remove('hidden');
                btn.innerHTML = 'Login to System';
                btn.disabled = false;
            });
    });
}

// Handle Signup Form
const signupForm = document.getElementById('signup-form');
if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const name = document.getElementById('name').value;
        const errorDiv = document.getElementById('signup-error');
        const btn = document.getElementById('signup-btn');
        
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
        btn.disabled = true;

        // --- MOCK SIGNUP BYPASS ---
        if (firebaseConfig.apiKey === "YOUR_API_KEY") {
            console.log("Mock Signup: Bypassing Firebase Auth because API Key is not set.");
            setTimeout(() => {
                sessionStorage.setItem('mock_user', 'true');
                sessionStorage.setItem('mock_name', name);
                window.location.href = '/dashboard';
            }, 1000);
            return;
        }
        // -------------------------
        
        auth.createUserWithEmailAndPassword(email, password)
            .then((userCredential) => {
                return userCredential.user.updateProfile({
                    displayName: name
                });
            })
            .then(() => {
                // Redirect will happen in onAuthStateChanged
            })
            .catch((error) => {
                errorDiv.textContent = error.message;
                errorDiv.classList.remove('hidden');
                btn.innerHTML = 'Register';
                btn.disabled = false;
            });
    });
}
