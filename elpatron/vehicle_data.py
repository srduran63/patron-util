import os
import re
from datetime import datetime
from typing import List, Dict, Any

# Mapeos para normalizar nombres
BRAND_DIRS = {
    'toyota': 'Toyota',
    'honda': 'Honda',
}

MODEL_DISPLAY = {
    'accord': 'Accord',
    'civic': 'Civic',
    'hrv': 'HR-V',
    'camry': 'Camry',
    'corolla': 'Corolla',
    'rav4': 'RAV4',
}

COLOR_DISPLAY = {
    'blanco': 'Blanco',
    'rojo': 'Rojo',
    'negro': 'Negro',
    'gris': 'Gris',
}

# Precios base aproximados por modelo (solo demostrativo)
MODEL_BASE_PRICE = {
    'accord': 28500,
    'civic': 23500,
    'hrv': 27500,
    'camry': 30000,
    'corolla': 21000,
    'rav4': 32000,
}

FILENAME_REGEX = re.compile(r'^(?P<model>[a-z0-9]+)_(?P<year>\d{4})_(?P<color>[a-z]+)_(?P<index>\d+)\.jpg$')

CURRENT_YEAR = datetime.now().year


def _compute_mileage(year: int) -> int:
    # Simple formula: 8,000 base + 11,000 por año de diferencia (mínimo 5,000)
    diff = max(0, CURRENT_YEAR - year)
    miles = 8000 + diff * 11000
    return max(5000, miles)


def _compute_price(model_key: str, year: int) -> float:
    base = MODEL_BASE_PRICE.get(model_key, 20000)
    age = max(0, CURRENT_YEAR - year)
    depreciation = 0.07 * age  # 7% anual simplificado
    price = base * (1 - depreciation)
    return round(max(price, base * 0.35), 2)


def load_static_vehicles(static_images_dir: str) -> List[Dict[str, Any]]:
    """Carga vehículos a partir de los archivos en static/images/<brand>/*.jpg

    Agrupa por (brand, model, year, color) y crea una entrada por conjunto de imágenes.
    """
    vehicles = []
    for brand_dir, brand_display in BRAND_DIRS.items():
        brand_path = os.path.join(static_images_dir, brand_dir)
        if not os.path.isdir(brand_path):
            continue
        grouped: Dict[tuple, List[str]] = {}
        for filename in os.listdir(brand_path):
            if not filename.lower().endswith('.jpg'):
                continue
            m = FILENAME_REGEX.match(filename.lower())
            if not m:
                continue
            model_key = m.group('model')
            year = int(m.group('year'))
            color_key = m.group('color')
            color_display = COLOR_DISPLAY.get(color_key, color_key.title())
            model_display = MODEL_DISPLAY.get(model_key, model_key.title())
            key = (brand_display, brand_dir, model_display, model_key, year, color_display, color_key)
            grouped.setdefault(key, []).append(filename)
        # Crear vehículos
        for key, files in grouped.items():
            brand_display, brand_dir_norm, model_display, model_key, year, color_display, color_key = key
            files_sorted = sorted(files)
            main_image = f"{brand_dir_norm}/{files_sorted[0]}"
            additional = [f"{brand_dir_norm}/{f}" for f in files_sorted[1:]]
            vehicle_dict = {
                'marca': brand_display,
                'modelo': model_display,  # Mantener modelo limpio (año y color en otros campos)
                'año': year,
                'color': color_display,
                'precio': _compute_price(model_key, year),
                'kilometraje': _compute_mileage(year),
                'imagen': main_image,  # relativo a images/
                'imagenes': [f"images/{img}" for img in additional],  # para compatibilidad con get_vehicle_images
                'descripcion': f"{model_display} {year} color {color_display}. Excelente condición. Disponible en El Patrón 217 Corp.",
                'detalles': {
                    'motor': '2.0L',
                    'combustible': 'Gasolina',
                    'color': color_display,
                }
            }
            vehicles.append(vehicle_dict)
    return vehicles

if __name__ == '__main__':
    base_dir = os.path.dirname(__file__)
    static_images = os.path.join(base_dir, 'static', 'images')
    data = load_static_vehicles(static_images)
    from pprint import pprint
    pprint(data)
