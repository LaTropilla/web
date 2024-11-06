document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/autenticacion/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById('message').innerText = 'Login exitoso';
            // Almacenar el token en el local storage
            localStorage.setItem('token', result.token);
            // Redirigir a admin.html
            window.location.href = '/pagsadmin/admin.html';
        } else {
            const result = await response.json();
            document.getElementById('message').innerText = result.message;
        }
    } catch (error) {
        document.getElementById('message').innerText = 'Error al iniciar sesión';
    }
});
