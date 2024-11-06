document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    document.getElementById('logout').addEventListener('click', function () {
        localStorage.removeItem('token');
        window.location.href = '/login';
    });
});
