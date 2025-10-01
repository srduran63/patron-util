# app.py

from flask import Flask

app = Flask(__name__)

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

@app.route('/')
def home():
    """Ruta principal que muestra las marcas de carros disponibles."""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Catálogo de Carros</title>
        <style>
            body { font-family: sans-serif; margin: 40px; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
            a { text-decoration: none; color: #007bff; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>El Catálogo de Carros</h1>
        <p>Selecciona una marca para ver sus modelos.</p>
        <ul>
            <li><a href="/catalog/toyota">Toyota</a></li>
            <li><a href="/catalog/nissan">Nissan</a></li>
        </ul>
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
                body {{ font-family: sans-serif; margin: 40px; }}
                ul {{ list-style: none; padding: 0; }}
                li {{ margin: 20px 0; border: 1px solid #ccc; padding: 15px; border-radius: 8px; }}
                strong {{ color: #333; }}
                a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
            </style>
        </head>
        <body>
            <a href="/">Volver a las marcas</a>
            <h1>Modelos de {brand.capitalize()}</h1>
            <ul>
        """
        for car in car_list:
            html += f"""
                <li>
                    <strong>Modelo:</strong> {car['model']}<br>
                    <strong>Año:</strong> {car['year']}<br>
                    <strong>Millas:</strong> {car['miles']}
                </li>
            """
        html += """
            </ul>
        </body>
        </html>
        """
        return html
    else:
        return "Marca no encontrada.", 404

if __name__ == '__main__':
    app.run(debug=True)