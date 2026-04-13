# Memoria de la Actividad 3: Uso de una API en aplicación de componentes

**Nombre del Alumno:** [Tu Nombre / Apellidos]

---

## 1. Descripción de la Aplicación

La aplicación **GeoGasolineras España** es un sistema web diseñado para facilitar al usuario la consulta de información en tiempo real sobre gasolineras, precios de combustibles y ubicaciones a lo largo del territorio español. Cumple el propósito principal de obtener la ubicación actual del usuario a través de geolocalización (o ingreso manual de coordenadas) y cruza dicha posición con los datos gubernamentales expuestos por el **Ministerio para la Transformación Digital y Función Pública** para mostrar qué gasolineras están cerca, filtrarlas por marca, distancia y tipo de carburante, y comprobar de forma heurística cuáles podrían estar abiertas en base a la información horaria otorgada.

El sistema se divide en un esquema monolítico híbrido:
1.  **Backend (Python + Flask)**: Escrito puramente en Python para consumir los endpoints XML/JSON del gobierno, realizar cálculos de geocodificación mediante la fórmula de Haversine y dar un punto de acceso API seguro para los componentes del Frontend.
2.  **Frontend (Vue.js + Tailwind CSS)**: Creado bajo el paradigma de sitios web por componentes orientados a *Single Page Applications* (SPA). Se ha usado tecnología asíncrona (AJAX) para su comunicación con el Backend.

---

## 2. Elementos que la Componen y su Funcionamiento

### 2.1 Backend (`app.py`)
- **Gestión de Peticiones API**: El Backend de Python realiza una petición segura usando la librería `requests` a la URL del Servicio REST de Precios de Carburantes del Gobierno.
- **Fórmula de Haversine**: Dado que el Ministerio expone todas las estaciones de forma general y las clasifica por comunidades y municipios pero no por proximidad directa GPS en un Endpoint específico, el Backend toma la lista completa, parsea sus campos y calcula la distancia asimilando el radio de la tierra.
- **Microservicio AJAX**: Devuelve información curada y filtrada, calculando además estadísticas extra (como la gasolinera "Más Barata" y "Más Cercana").

### 2.2 Frontend (`templates/index.html`)
Se apoya en *Vue.js* (por CDN) para dividir funcionalmente la pantalla en dos flujos dinámicos sin necesidad de recargar la página.
- **Componente de Entrada de Datos**: Interfaz interactiva donde el usuario puede activar un *Web API* de Geolocalización (`navigator.geolocation`) que extrae su latitud y longitud. También tiene los campos de filtro: Radio de búsqueda, carburante, distribuidora o marca.
- **Componente de Salida de Resultados**: Utiliza el motor reactivo de Vue 3 (`v-for`, `v-if`) para generar un listado dinámico extraído mediante Axios, destacando de forma gráfica prioridades.

---

## 3. Descripción de la Llamada a API REST

El flujo es canalizado mediante nuestro Backend de Flask quien actúa como un puente, o middleware, para evitar problemas de _CORS_ y de procesado intensivo en el cliente.

### Consumo Gubernamental:
```python
URL_MINETUR = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
response = requests.get(URL_MINETUR, verify=False, timeout=10)
data = response.json()
```
El objeto devuelto en JSON encapsula un arrary principal dentro de la clave `"ListaEESSPrecio"`.

### Parseo de datos:
Con la data recibida, nuestro código descodifica parámetros críticos. Dado que la API rest del gobierno envía representaciones de coma flotante europeo (comas en vez de puntos), se aplica un procesamiento:
```python
def parse_float_es(val):
    return float(val.replace(',', '.'))
```

### La Llamada AJAX en Cliente:
La parte gráfica en JS en el navegador gatilla todo el proceso mediante *Axios* de esta manera:
```javascript
const response = await axios.get('/api/gasolineras', {
    params: { lat, lon, radius, fuel_type, brand }
});
this.results_data = response.data;
```

---

## 4. Procesamiento de la Información Recibida

Con la respuesta de nuestro Backend alimentada por la del Ministerio, la información se muestra al usuario del siguiente modo:

1. **Top Insights (Highlights)**: La aplicación determina programáticamente cuáles son las estaciones de mayor interés para el usuario. Asigna una tarjeta prioritaria indicando "La Más Cercana" y "La Más Barata" en relación precio y kilómetros.
2. **Tabulación Espacial**: Usando Tailwind CSS se procesa la metadata para que se despliegue en un layout flexible de _Cards_, mostrando: Direccion, Localidad, Precio (en divisa Euro), Distancia real y un Status de Abierto/Cerrado.
3. El **Estado de Abierto/Cerrado** se calcula inspeccionando el texto de la clave `Horario`, combinándolo con el datetime de Python para dar un feedback al instante de la apertura 24H o en días diarios.

---

## 5. Conclusiones

La realización de esta práctica comprueba los grandes desafíos que supone el consumo de Open Data de entidades públicas (formatos inconsistentes de números, errores de cadena de certificación SSL de la plataforma ministerial y esquemas no siempre optimizados espacialmente). 

Mediante un enfoque de Backend en **Python/Flask** aunado a un empaquetador moderno como **Vue.js**, se logró reducir dicha complejidad; la integración lógica se mantuvo ágil mediante AJAX, proveyendo al usuario final de una experiencia altamente usable, directa y visualmente atractiva con Tailwind CSS. Este paradigma es altamente escalable y de valor fundamental en proyectos mayores relacionados a la red de hidrocarburos. 

---
**Enlace a la solución en GitHub**: _[Incluye tu enlace aquí]_
