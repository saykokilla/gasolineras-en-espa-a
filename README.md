# GeoGasolineras España

Esta aplicación web permite consultar y localizar las gasolineras terrestres en España de acuerdo a las coordenadas de posición proporcionadas (mediante geolocalización o de forma manual), consultando en tiempo real la **API Rest del Ministerio para la Transformación Digital y Función Pública**.

El objetivo de este proyecto es cumplir con la **Actividad 3: Uso de una API en aplicación de componentes**. 

## Características

- **Realizado completamente en Python (Backend)** usando el micro-framework Flask.
- **Frontend basado en componentes** utilizando **Vue 3** y llamadas **AJAX** con Axios.
- Diseño visual atractivo, Premium y responsive gracias a **Tailwind CSS**.
- Filtros por: Radio de distancia, Tipo de Carburante, y Marca o empresa suministradora.
- Información sobre si la estación se encuentra "Abierta" en base a heurística sobre el `<Horario>`.

## Requisitos Previos

Necesitas tener **Python 3.x** instalado en tu sistema.
Es recomendable utilizar un entorno virtual.

## Instalación y Ejecución Local

1. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el servidor Flask:
   ```bash
   python app.py
   ```

3. Abre en tu navegador la ruta:
   **http://127.0.0.1:5000**

## Archivos del Proyecto
- `app.py`: Backend centralizado en Python. Funciona como puente procesador entre el Ministerio y el Frontend. 
- `templates/index.html`: Una Single Page Application (SPA) en Vue.js + Tailwind CSS.
- `Memoria_Actividad.md`: Documento de texto con la información descriptiva y de funcionamiento para la entrega.
- `requirements.txt`: Archivo de dependencias.

## Subir a Github

Para presentar este proyecto en GitHub, puedes crear un repositorio nuevo, añadir estos archivos y hacer el commit principal. Las instrucciones provistas arriba servirán de base para tu tutor/profesor al calificar el código.
