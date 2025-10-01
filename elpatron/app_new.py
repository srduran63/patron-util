from flask import Flask, render_template, request, jsonify, abort, url_for, redirect
import os

app = Flask(__name__)

# Inserción: importar generador dinámico
try:
    from vehicle_data import load_static_vehicles
except ImportError:
    load_static_vehicles = None

# Reemplazo: lista base mínima (solo vehículos con fotos reales .jpg en static/images)
vehicles = [
    {
        "id": 1,
        "marca": "Toyota",
        "modelo": "Corolla",
        "año": 2020,
        "precio": 15000.00,
        "kilometraje": 45000,
        "imagen": "toyota/corolla_2020_rojo_1.jpg",
        "detalles": {"motor": "1.8L"},
        "descripcion": "Toyota Corolla 2020 excelente condición, listo para carretera."
    }
]

# --- Nuevo: cargar dinámicamente vehículos desde las imágenes ---
STATIC_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
if load_static_vehicles is not None and os.path.isdir(STATIC_IMAGES_DIR):
    generated = load_static_vehicles(STATIC_IMAGES_DIR)
    # Asignar IDs continuando después de los existentes
    max_id = max((int(v.get('id', 0)) for v in vehicles), default=0)
    next_id = max_id + 1
    for gv in generated:
        if gv.get('imagen', '').startswith('data:'):
            continue
        gv['id'] = next_id
        next_id += 1
        vehicles.append(gv)

# Filtro defensivo adicional (por si quedaron modelos no deseados)
ALLOWED_BRANDS = {"toyota", "honda"}
vehicles = [v for v in vehicles if v.get('marca', '').lower() in ALLOWED_BRANDS and not str(v.get('imagen', '')).startswith('data:')]

def get_vehicle_by_id(vehicle_id):
    # Busca un vehículo por su ID (asegura que ambos sean int)
    return next((v for v in vehicles if int(v['id']) == int(vehicle_id)), None)

def get_vehicle_images(vehicle):
    # Devuelve la lista de imágenes adicionales si existen
    if 'imagenes' in vehicle:
        return vehicle['imagenes']
    if 'imagenes_adicionales' in vehicle:
        return vehicle['imagenes_adicionales']
    return []

def get_vehicle_details(vehicle):
    # Devuelve los detalles adicionales si existen
    if 'detalles' in vehicle:
        return vehicle['detalles']
    if 'detalles_adicionales' in vehicle:
        return vehicle['detalles_adicionales']
    return {}

@app.route('/')
def index():
    # Asegura que todos los vehículos tengan la clave 'detalles' y que no sea None
    vehs = []
    for v in vehicles:
        v_copy = v.copy()
        if 'detalles' not in v_copy or v_copy['detalles'] is None:
            v_copy['detalles'] = {}
        # Mejora: agrega un resumen si no existe
        if 'descripcion' not in v_copy:
            v_copy['descripcion'] = f"{v_copy['marca']} {v_copy['modelo']} año {v_copy['año']}."
        vehs.append(v_copy)
    return render_template('index.html', vehicles=vehs)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_detail(vehicle_id):
    vehicle = get_vehicle_by_id(vehicle_id)
    if vehicle is None:
        abort(404)
    vehicle = vehicle.copy()
    vehicle['imagenes_adicionales'] = get_vehicle_images(vehicle)
    vehicle['detalles_adicionales'] = get_vehicle_details(vehicle)
    # Mejora: agrega un resumen si no existe
    if 'descripcion' not in vehicle:
        vehicle['descripcion'] = f"{vehicle['marca']} {vehicle['modelo']} año {vehicle['año']}."
    if request.headers.get('Accept') == 'application/json' or request.args.get('json') == '1':
        return jsonify(vehicle)
    return render_template('vehicle_detail.html', vehicle=vehicle)

# Catálogo simple de marcas/modelos (de app.py)
cars = {
    'toyota': [
        {'model': 'Corolla', 'year': 2022, 'miles': 15000},
        {'model': 'RAV4', 'year': 2021, 'miles': 25000},
        {'model': 'Camry', 'year': 2023, 'miles': 10000}
    ],
    'nissan': [
        {'model': 'Sentra', 'year': 2020, 'miles': 40000},
        {'model': 'Rogue', 'year': 2022, 'miles': 18000},
        {'model': 'Titan', 'year': 2021, 'miles': 30000}
    ]
}

@app.route('/brands')
def brands_home():
    """Ruta principal que muestra las marcas de carros disponibles."""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Catálogo de Carros</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f7f7fa; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
            a { text-decoration: none; color: #007bff; font-weight: bold; }
            .brand-card { display: inline-block; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 24px 32px; margin: 16px; transition: box-shadow .2s; }
            .brand-card:hover { box-shadow: 0 4px 16px #0002; }
        </style>
    </head>
    <body>
        <h1 style="color:#222;">El Catálogo de Carros</h1>
        <p>Selecciona una marca para ver sus modelos.</p>
        <div>
            <a class="brand-card" href="/catalog/toyota">Toyota</a>
            <a class="brand-card" href="/catalog/nissan">Nissan</a>
        </div>
        <p style="margin-top:40px;"><a href="/">Ir al catálogo avanzado</a></p>
    </body>
    </html>
    """
    return html

@app.route('/catalog/<brand>')
def catalog(brand):
    """Muestra el catálogo de carros por marca."""
    if brand in cars:
        car_list = cars[brand]
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>{brand.capitalize()} Catálogo</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f7f7fa; }}
                ul {{ list-style: none; padding: 0; }}
                li {{ margin: 20px 0; border: 1px solid #e0e0e0; background: #fff; padding: 18px 24px; border-radius: 8px; box-shadow: 0 2px 8px #0001; }}
                strong {{ color: #333; }}
                a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
                .back-link {{ margin-bottom: 24px; display: inline-block; }}
            </style>
        </head>
        <body>
            <a class="back-link" href="/brands">&larr; Volver a las marcas</a>
            <h1 style="color:#222;">Modelos de {brand.capitalize()}</h1>
            <ul>
        """
        for car in car_list:
            html += f"""
                <li>
                    <strong>Modelo:</strong> {car['model']}<br>
                    <strong>Año:</strong> {car['year']}<br>
                    <strong>Millas:</strong> {car['miles']:,}
                </li>
            """
        html += """
            </ul>
            <p style="margin-top:40px;"><a href="/">Ir al catálogo avanzado</a></p>
        </body>
        </html>
        """
        return html
    else:
        return "Marca no encontrada.", 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

if __name__ == '__main__':
    base_dir = r'c:\Users\Lenovo\Desktop\elpatron'
    if os.getcwd().lower() != base_dir.lower():
        os.chdir(base_dir)
    import threading
    import webbrowser

    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)