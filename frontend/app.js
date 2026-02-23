const API = '/api';
let mode = 'login';

// --- CONFIGURACIÓN DE BOTONES (LISTENERS) ---
document.getElementById('tab-login').addEventListener('click', () => cambiarTab('login'));
document.getElementById('tab-reg').addEventListener('click', () => cambiarTab('reg'));
document.getElementById('btn-auth').addEventListener('click', ejecutarAuth);
document.getElementById('btn-save').addEventListener('click', crearJugador);
document.getElementById('btn-logout').addEventListener('click', logout);

function cambiarTab(a) {
    mode = a;
    document.getElementById('btn-auth').innerText = a === 'login' ? 'Entrar al Sistema' : 'Crear mi Cuenta';
    document.getElementById('tab-login').classList.toggle('active', a === 'login');
    document.getElementById('tab-reg').classList.toggle('active', a === 'reg');
    document.getElementById('pin-area').style.display = a === 'login' ? 'block' : 'none';
    document.getElementById('pin-result').style.display = 'none';
    document.getElementById('msg').innerText = '';
}

async function ejecutarAuth() {
    const u = document.getElementById('username').value;
    const p = document.getElementById('password').value;
    const st = document.getElementById('security_token').value;
    const msg = document.getElementById('msg');
    const pinResult = document.getElementById('pin-result');

    if (mode === 'reg') {
        try {
            const res = await fetch(`${API}/register?username=${u}&password=${p}`, { method: 'POST' });
            const data = await res.json();
            if (res.ok) {
                msg.className = 'text-success';
                msg.innerText = '¡Usuario creado!';
                document.getElementById('pin-number').innerText = data.tu_pin_de_seguridad;
                pinResult.style.display = 'block';
            } else {
                msg.className = 'text-danger';
                msg.innerText = data.detail || 'Error al registrar';
            }
        } catch (e) { console.error(e); }
    } else {
        const form = new FormData();
        form.append('username', u);
        form.append('password', p);
        try {
            const res = await fetch(`${API}/token?security_token=${st}`, { method: 'POST', body: form });
            if (res.ok) {
                const data = await res.json();
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('user', u);
                iniciarApp();
            } else {
                const errorData = await res.json();
                msg.className = 'text-danger';
                msg.innerText = errorData.detail || 'PIN o Clave incorrectos';
            }
        } catch (e) { console.error(e); }
    }
}

async function cargarTabla() {
    const token = localStorage.getItem('token');
    try {
        const res = await fetch(`${API}/jugadores/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.status === 401) { logout(); return; }
        const data = await res.json();
        document.getElementById('tabla').innerHTML = data.map(j => `
            <tr>
                <td>#${j.id}</td>
                <td><strong>${j.nombre}</strong></td>
                <td><span class="badge bg-success">${j.posicion}</span></td>
                <td>${j.equipo}</td>
            </tr>
        `).join('');
    } catch (e) { console.error(e); }
}

async function crearJugador() {
    const token = localStorage.getItem('token');
    const nuevo = {
        nombre: document.getElementById('j-nombre').value,
        posicion: document.getElementById('j-pos').value,
        equipo: document.getElementById('j-eq').value
    };
    try {
        const res = await fetch(`${API}/jugadores/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify(nuevo)
        });
        if (res.ok) {
            document.getElementById('j-nombre').value = "";
            document.getElementById('j-pos').value = "";
            document.getElementById('j-eq').value = "";
            cargarTabla();
        }
    } catch (e) { console.error(e); }
}

function iniciarApp() {
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('app-section').style.display = 'block';
    document.getElementById('user-display').innerText = localStorage.getItem('user');
    cargarTabla();
}

function logout() {
    localStorage.clear();
    location.reload();
}

if (localStorage.getItem('token')) iniciarApp();
