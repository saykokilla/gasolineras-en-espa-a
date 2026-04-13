import math
from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

URL_MINETUR = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return float(R * c)

def parse_float_es(val):
    try:
        if not val:
            return None
        return float(val.replace(',', '.'))
    except:
        return None

def is_open(horario: str, current_time=None) -> bool:
    if not horario:
        return False
        
    if not current_time:
        current_time = datetime.now()
    
    horario_upper = horario.upper()
    if "24H" in horario_upper:
        return True
        
    day_idx = current_time.weekday() # 0 = Monday, 6 = Sunday
    days = ["L", "M", "X", "J", "V", "S", "D"]
    current_day = days[day_idx]
    
    # Improve heuristic matching for days
    if "L-D" in horario_upper:
        return True
        
    if "L-S" in horario_upper and day_idx <= 5:
        return True
        
    if "L-V" in horario_upper and day_idx <= 4:
        return True
        
    if current_day in horario_upper:
        return True
        
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/gasolineras', methods=['GET'])
def get_gasolineras():
    lat_str = request.args.get('lat')
    lon_str = request.args.get('lon')
    radius_km = float(request.args.get('radius', 5.0))
    fuel_type = request.args.get('fuel_type', 'Precio Gasolina 95 E5')
    brand_filter = request.args.get('brand', '').upper()
    
    if not lat_str or not lon_str:
        return jsonify({"error": "Latitude and longitude are required"}), 400
        
    try:
        user_lat = float(lat_str)
        user_lon = float(lon_str)
    except ValueError:
        return jsonify({"error": "Invalid coordinates"}), 400

    # Fetch data from MINETUR (Note: We use verify=False due to frequent SSL issues with MINETUR)
    # Using verify=False because the Spanish government API sometimes has certificate chain issues
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        response = requests.get(URL_MINETUR, verify=False, timeout=10)
        response.raise_for_status()
        data = response.json()
        estaciones_crudo = data.get('ListaEESSPrecio', [])
    except Exception as e:
        return jsonify({"error": f"Error fetching data from API: {str(e)}"}), 502

    results = []
    
    for est in estaciones_crudo:
        lat = parse_float_es(est.get('Latitud'))
        lon = parse_float_es(est.get('Longitud (WGS84)'))
        price = parse_float_es(est.get(fuel_type))
        
        if lat is None or lon is None or price is None:
            continue
            
        dist = haversine_distance(user_lat, user_lon, lat, lon)
        
        if dist <= radius_km:
            rotulo = est.get('Rótulo', '')
            if brand_filter and brand_filter not in rotulo.upper():
                continue
                
            horario = est.get('Horario', '')
            abierta = is_open(horario)
            
            results.append({
                "id": est.get('IDEESS'),
                "name": rotulo,
                "address": est.get('Dirección'),
                "municipality": est.get('Municipio'),
                "distance": round(dist, 2),
                "price": price,
                "lat": lat,
                "lon": lon,
                "schedule": horario,
                "is_open": abierta
            })

    # Sort results by distance and price
    closest = min(results, key=lambda x: x['distance']) if results else None
    cheapest = min(results, key=lambda x: x['price']) if results else None

    # Sort returning list by distance
    results.sort(key=lambda x: x['distance'])

    return jsonify({
        "total": len(results),
        "closest": closest,
        "cheapest": cheapest,
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
