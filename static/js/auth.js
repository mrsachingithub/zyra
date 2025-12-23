document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('auth-form');
    const toggleBtn = document.getElementById('toggle-auth');
    const formTitle = document.getElementById('form-title');
    const emailField = document.getElementById('email-field');
    const btnText = document.getElementById('btn-text');
    const toggleText = document.getElementById('toggle-text');
    const errorMsg = document.getElementById('error-msg');
    const successMsg = document.getElementById('success-msg');

    let isLogin = true;

    if (toggleBtn) {
        toggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            isLogin = !isLogin;
            
            if (isLogin) {
                formTitle.textContent = 'Log in to Zyra';
                emailField.classList.add('hidden');
                btnText.textContent = 'Log In';
                toggleText.textContent = "Don't have an account?";
                toggleBtn.textContent = 'Sign up for Zyra';
            } else {
                formTitle.textContent = 'Sign up for free';
                emailField.classList.remove('hidden');
                btnText.textContent = 'Sign Up';
                toggleText.textContent = "Already have an account?";
                toggleBtn.textContent = 'Log in';
            }
            errorMsg.classList.add('hidden');
            successMsg.classList.add('hidden');
        });
    }

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            errorMsg.classList.add('hidden');
            successMsg.classList.add('hidden');
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
            
            try {
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await res.json();
                
                if (!res.ok) {
                    throw new Error(result.error || 'Something went wrong');
                }
                
                if (isLogin) {
                    localStorage.setItem('access_token', result.access_token);
                    localStorage.setItem('refresh_token', result.refresh_token);
                    localStorage.setItem('user', JSON.stringify(result.user));
                    window.location.href = '/dashboard';
                } else {
                    successMsg.textContent = 'Registration successful! Please log in.';
                    successMsg.classList.remove('hidden');
                    // Switch to login view automatically
                    toggleBtn.click();
                }
            } catch (err) {
                errorMsg.textContent = err.message;
                errorMsg.classList.remove('hidden');
            }
        });
    }
});
