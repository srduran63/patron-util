# El Patrón 217 Corp - Dealer de Autos

[![Netlify Status](https://api.netlify.com/api/v1/badges/35a143d7-0052-4932-acb3-2ca12b396927/deploy-status)](https://app.netlify.com/projects/keen-cranachan-81648f/deploys)

## Descripción

Sitio web moderno para dealer de autos con efectos 3D, diseño luxury y catálogo dinámico de vehículos.

## Características

- ✨ **Efectos 3D**: Cards con tilt interactivo y parallax
- 🎨 **Diseño Luxury**: Paleta sophisticada con toques dorados
- 🚗 **Catálogo Dinámico**: Carga automática desde imágenes
- 📱 **Responsive**: Adaptativo a móviles y tablets
- ⚡ **Performance**: Optimizado con lazy loading y animaciones suaves
- 🎯 **Canvas Effects**: Partículas animadas de fondo
- 💬 **WhatsApp Integration**: Contacto directo por cada vehículo

## Tecnologías

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Estilos**: CSS Grid, Flexbox, 3D Transforms
- **Efectos**: Canvas 2D, CSS animations, parallax
- **Fonts**: Orbitron, Montserrat (Google Fonts)

## Instalación

```bash
# Clonar repositorio
git clone [tu-repo-url]
cd elpatron

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app_new.py
```

## Estructura del Proyecto

```
elpatron/
├── app_new.py          # Aplicación Flask principal
├── vehicle_data.py     # Generador dinámico de vehículos
├── static/
│   ├── css/
│   │   └── main.css    # Estilos principales con efectos 3D
│   ├── js/
│   │   └── main.js     # Interacciones y canvas effects
│   └── images/         # Imágenes organizadas por marca
├── templates/
│   ├── base.html       # Template base con canvas
│   ├── index.html      # Página principal
│   └── vehicle_detail.html # Detalle de vehículo
└── requirements.txt
```

## Configuración de Efectos 3D

### Ajustar Intensidad del Tilt
En `static/js/main.js`:
```javascript
const maxTilt = 10;      // Reducir para menos rotación
const maxTranslate = 14; // Reducir para menos parallax
```

### Desactivar Efectos Temporalmente
Agregar clase CSS:
```css
html.no-fx .vehicle-card { transform: none !important; }
.no-fx .fx-canvas { display: none; }
```

### Configurar Canvas Shapes
En `static/js/main.js`:
```javascript
const density = 28;     // Menos partículas
opacity: .25;          // Más sutil en CSS
```

## Despliegue en Netlify

1. Conecta tu repositorio GitHub
2. Build command: `pip install -r requirements.txt && python -c "print('Static site ready')"`
3. Publish directory: `./`
4. El badge muestra el estado actual del deploy

## Personalización

### Colores
En `static/css/main.css` modificar variables CSS:
```css
:root {
    --accent: #b61f3a;     /* Color principal */
    --gold: #c9a24b;       /* Acentos dorados */
    --accent-glow: #ff88a1; /* Brillos suaves */
}
```

### Agregar Nuevos Vehículos
1. Subir imágenes a `static/images/[marca]/`
2. Formato: `modelo_año_color_numero.jpg`
3. La app carga automáticamente desde `vehicle_data.py`

## Performance

- Canvas optimizado con `requestAnimationFrame`
- Respeta `prefers-reduced-motion`
- Z-index controlado para no bloquear interacciones
- Lazy loading de imágenes con fallback

## Soporte

Para ajustes o consultas sobre efectos 3D y personalización del sitio.