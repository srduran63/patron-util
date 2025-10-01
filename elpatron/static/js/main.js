document.addEventListener('DOMContentLoaded', () => {

    // --- FILTROS DE VEHÍCULOS ---
    function applyFilters() {
        const marca = (document.querySelector('.filter-btn.active') && document.querySelector('.filter-btn.active').dataset.filter) || 'all';
        const year = (document.getElementById('filterYear') && document.getElementById('filterYear').value) || '';
        const price = parseFloat(document.getElementById('filterPrice') && document.getElementById('filterPrice').value) || null;
        const fuel = (document.getElementById('filterFuel') && document.getElementById('filterFuel').value) || '';
        const trans = (document.getElementById('filterTrans') && document.getElementById('filterTrans').value) || '';
        document.querySelectorAll('.vehicle-card').forEach(vehicle => {
            let show = true;
            if (marca !== 'all' && vehicle.dataset.marca !== marca) show = false;
            if (year && vehicle.querySelector('.badge.year').textContent != year) show = false;
            if (price && parseFloat(vehicle.querySelector('.amount').textContent.replace(/[^\d.]/g, '')) > price) show = false;
            if (fuel && !vehicle.querySelector('.vehicle-specs').textContent.includes(fuel)) show = false;
            if (trans && !vehicle.querySelector('.vehicle-specs').textContent.includes(trans)) show = false;
            vehicle.style.display = show ? 'block' : 'none';
        });
    }
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            button.classList.add('active');
            applyFilters();
        });
    });
    ['filterYear', 'filterPrice', 'filterFuel', 'filterTrans'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', applyFilters);
    });

    // --- BÚSQUEDA EN TIEMPO REAL ---
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.vehicle-card').forEach(vehicle => {
                const title = vehicle.querySelector('.vehicle-title').textContent.toLowerCase();
                vehicle.style.display = title.includes(searchTerm) ? 'block' : 'none';
            });
        });
    }

    // --- BOTÓN WHATSAPP (contacto directo) ---
    document.querySelectorAll('.btn-whatsapp').forEach(button => {
        button.addEventListener('click', function(e) {
            const vehicleCard = button.closest('.vehicle-card');
            const vehicleTitle = vehicleCard ? vehicleCard.querySelector('.vehicle-title') : null;
            const vehicleInfo = vehicleTitle ? vehicleTitle.textContent : '';
            const message = encodeURIComponent(`Me interesa: ${vehicleInfo}`);
            button.href = `https://wa.me/?text=${message}`;
        });
    });

    // --- FALLBACK DE IMÁGENES ---
    document.querySelectorAll('.vehicle-image').forEach(img => {
        img.onerror = () => {
            img.src = '/static/images/placeholder.jpg';
        };
    });


    // --- MODAL DETALLES ---
    const modal = document.getElementById('vehicleModal');

    function closeModal() {
        modal.style.display = "none";
        document.body.classList.remove('modal-open');
    }
    // Delegación para todos los botones de cerrar modales
    document.querySelectorAll('.modal .close').forEach(btn => {
        btn.onclick = closeModal;
    });
    // Cerrar modal al hacer click fuera del contenido
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) closeModal();
    });
    // Cerrar modal con Escape
    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') closeModal();
    });

    // --- BOTÓN DE CONTACTO GENERAL (si existe) ---
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Aquí puedes agregar lógica para enviar el formulario por AJAX o mostrar un mensaje de éxito
            alert('¡Mensaje enviado! Nos pondremos en contacto contigo pronto.');
            contactForm.reset();
        });
    }

    // JS base para interacción futura
    // Ejemplo: resalta el logo al hacer click
    const logo = document.querySelector('.logo');
    if (logo) {
        logo.addEventListener('click', () => {
            logo.style.color = '#4f8cff';
            setTimeout(() => logo.style.color = '', 500);
        });
    }

    /* --- 3D Tilt / Parallax Cards --- */
    const supportsMotion = window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
    const grid = document.querySelector('.vehicles-grid');
    if (grid && supportsMotion) {
        const cards = Array.from(grid.querySelectorAll('.vehicle-card'));
        const maxTilt = 10; // grados
        const maxTranslate = 14; // px parallax interno
        let rafId = null;

        function handlePointer(e) {
            if (!cards.length) return;
            const rect = grid.getBoundingClientRect();
            const gx = (e.clientX - rect.left) / rect.width; // 0..1
            const gy = (e.clientY - rect.top) / rect.height; // 0..1
            if (rafId) cancelAnimationFrame(rafId);
            rafId = requestAnimationFrame(() => {
                cards.forEach(card => {
                    const cRect = card.getBoundingClientRect();
                    const cx = (e.clientX - cRect.left) / cRect.width; // 0..1
                    const cy = (e.clientY - cRect.top) / cRect.height; // 0..1
                    const tiltX = (cy - .5) * maxTilt * -1; // invert vertical tilt
                    const tiltY = (cx - .5) * maxTilt;
                    card.style.transform = `rotateX(${tiltX.toFixed(2)}deg) rotateY(${tiltY.toFixed(2)}deg) translateZ(0)`;
                    card.dataset.tiltActive = '1';
                    // Parallax imagen ligera
                    const img = card.querySelector('.vehicle-image');
                    if (img) {
                        const tx = (cx - .5) * maxTranslate;
                        const ty = (cy - .5) * maxTranslate;
                        img.style.transform = `translate3d(${tx.toFixed(1)}px, ${ty.toFixed(1)}px, 0) scale(1.05)`;
                    }
                });
            });
        }

        function resetTilt() {
            if (rafId) cancelAnimationFrame(rafId);
            cards.forEach(card => {
                card.style.transform = '';
                card.dataset.tiltActive = '0';
                const img = card.querySelector('.vehicle-image');
                if (img) img.style.transform = '';
            });
        }
        grid.addEventListener('pointermove', handlePointer);
        grid.addEventListener('pointerleave', resetTilt);
        window.addEventListener('scroll', () => { // sutil parallax global
            const sc = window.scrollY * 0.04;
            document.documentElement.style.setProperty('--parallax-shift', `${sc.toFixed(2)}px`);
        });
    } else {
        document.documentElement.classList.add('no-tilt');
    }

});

// Mueve showDetails fuera del DOMContentLoaded para que sea global
function showDetails(vehicleId) {
    const modal = document.getElementById('vehicleModal');
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = '<p>Cargando...</p>';
    modal.style.display = "block";
    document.body.classList.add('modal-open');
    fetch(`/vehicle/${vehicleId}?json=1`)
        .then(response => response.json())
        .then(data => {
            // Manejar posibles datos faltantes
            const detalles = data.detalles || {};
            modalContent.innerHTML = `
                <h2>${data.marca} ${data.modelo}</h2>
                <div class="vehicle-details">
                    <img src="/static/images/vehicles/${data.imagen}" alt="${data.marca} ${data.modelo}" onerror="this.src='/static/images/placeholder.jpg'">
                    <div class="specs">
                        <p>Año: ${data.año}</p>
                        <p>Kilometraje: ${data.kilometraje ? data.kilometraje.toLocaleString() : ''} km</p>
                        <p>Motor: ${detalles.motor || ''}</p>
                        <p>Transmisión: ${detalles.transmision || ''}</p>
                        <p>Combustible: ${detalles.combustible || ''}</p>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            modalContent.innerHTML = '<p>Error al cargar detalles.</p>';
        });
}

// --- SCRIPT PARA CANVAS CON FORMAS DINÁMICAS ---
(function() {
    const canvas = document.getElementById('fxCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;
    const density = Math.min(42, Math.max(24, Math.floor(w * h / 48000))); // adaptativo
    const shapes = [];
    const palette = [
        '#b61f3a', '#d94a63', '#ff88a1', '#c9a24b', '#ffffff10', '#ffffff08'
    ];

    function rand(a, b) { return Math.random() * (b - a) + a; }

    function init() {
        shapes.length = 0;
        for (let i = 0; i < density; i++) {
            shapes.push({
                x: rand(0, w),
                y: rand(0, h),
                z: rand(.2, 1.2),
                r: rand(14, 110),
                a: rand(0, Math.PI * 2),
                av: rand(-0.002, 0.002),
                spx: rand(-.12, .12),
                spy: rand(-.08, .08),
                color: palette[Math.floor(Math.random() * palette.length)],
                form: Math.random() < .5 ? 'circle' : 'poly'
            });
        }
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);
        ctx.globalCompositeOperation = 'lighter';
        shapes.forEach(s => {
            s.a += s.av;
            s.x += s.spx * s.z;
            s.y += s.spy * s.z;
            if (s.x < -120) s.x = w + 60;
            if (s.x > w + 120) s.x = -60;
            if (s.y < -120) s.y = h + 60;
            if (s.y > h + 120) s.y = -60;
            const grd = ctx.createRadialGradient(s.x, s.y, s.r * 0.05, s.x, s.y, s.r);
            grd.addColorStop(0, s.color);
            grd.addColorStop(1, 'rgba(0,0,0,0)');
            ctx.fillStyle = grd;
            ctx.save();
            ctx.translate(s.x, s.y);
            ctx.rotate(s.a);
            if (s.form === 'circle') {
                ctx.beginPath();
                ctx.arc(0, 0, s.r, 0, Math.PI * 2);
                ctx.fill();
            } else {
                const sides = 5;
                ctx.beginPath();
                for (let i = 0; i <= sides; i++) {
                    const ang = i / sides * Math.PI * 2;
                    const rx = Math.cos(ang) * s.r;
                    const ry = Math.sin(ang) * s.r;
                    if (i === 0) ctx.moveTo(rx, ry);
                    else ctx.lineTo(rx, ry);
                }
                ctx.fill();
            }
            ctx.restore();
        });
        requestAnimationFrame(draw);
    }
    window.addEventListener('resize', () => { w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
        init(); });
    init();
    draw();
})();