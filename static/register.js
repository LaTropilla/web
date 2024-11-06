document.getElementById('registerForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/autenticacion/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const result = await response.text();
        document.getElementById('message').innerText = result;
    } catch (error) {
        document.getElementById('message').innerText = 'Error al registrar el usuario';
    }
});

