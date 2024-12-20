from flask import Flask, jsonify, request
import requests
from swagger.config import init_swagger
from flasgger import swag_from

app = Flask(__name__)
swagger = init_swagger(app)

# Microservices URL'er
MICROSERVICES = {
    "kunde_api": "https://kunde-api-dnecdehugrhmbghu.northeurope-01.azurewebsites.net/",  # Kunde API
    "login_api": "https://loginmicroservice-cxake5d4d6chg7d0.northeurope-01.azurewebsites.net/",  # Login API
    "bildatabase_api": "https://bildatabasedemo-hzfbegh6eqfraqdd.northeurope-01.azurewebsites.net/", # Bildatabase API
    "abonnement_api":"https://abonnement-beczhgfth9axdzd9.northeurope-01.azurewebsites.net/", # Abonnement API
    "damage_api":"https://skade-demo-b2awcyb4gedxdnhj.northeurope-01.azurewebsites.net/", # Skadeservice API 
    "calculate_api": "https://skadeberegner-d9fferbzcgddfycm.northeurope-01.azurewebsites.net/", # Beregning service API 
}

# Home directory så man kan se hvad der er i API gateway når man besøger
@app.route('/', methods=['GET'])
@swag_from('swagger/home.yaml')
def home():
    """
    Gateway overview
    """
    return jsonify({
        "service": "API Gateway",
        "version": "1.0.0",
        "routes": {
            "Kunde API POST":"/kundeapi/adduser",
            "Kunde API GET":"/kundeapi/customers",
            "Kunde API GET kunde by ID":"/kundeapi/<int:kunde_id>",
            "Kunde API DELETE":"/kundeapi/delete/<int:kunde_id>",
            "Login API POST to register":"/loginapi/register",
            "Login API POST to login":"/loginapi/login",
            "Cars API GET Cars":"/carsapi/cars",
            "Cars API GET cars by ID ":"/carsapi/cars/<int:car_id>",
            "Cars API POST":"/carsapi/cars/add", 
            "Cars API DELETE":"/carsapi/cars/delete/<int:car_id>", 
            "Abonnement API GET":"/abonnementapi/abonnement",
            "Abonnement API POST":"/abonnementapi/abonnement/add",
            "Abonnement API GET Abonnement by ID":"/abonnementapi/abonnement/<int:subscription_id>",
            "Damage API GET":"/damageapi/damage",
            "Damage API POST":"/damageapi/damage/add",
            "Damage API PUT":"/damageapi/damage/change/<int:damage_id>",
            "Damage API DELETE":"/damageapi/damage/delete/<int:damage_id>",
            "Calculate API GET total price":"/calculateapi/calculate-total-price",
            "Calculate API GET get all calculations":"/calculateapi/get-all-calculations",
            "Calculate API GET get total revenue":"/calculateapi/get-all-calculations"
        }
    })

# Kunde API proxy
@app.route('/kundeapi/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/kunde.yaml')
def proxy_kunde(path):
    """
    Proxy requests to Kunde API
    """
     # Kun inkluder json for POST og PUT anmodninger
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = None
        
    service_url = f"{MICROSERVICES['kunde_api']}/{path}"
    response = requests.request(
        method=request.method,  # Use the same HTTP method
        url=service_url,        # Forward to the target microservice
        headers={key: value for key, value in request.headers if key != 'Host'},  # Forward headers
        json=data
    )
    return jsonify(response.json()), response.status_code

# Login API - Register
@app.route('/loginapi/register', methods=['POST'])
@swag_from('swagger/register.yaml')
def proxy_register():
    """
    Proxy requests to Login API - Register
    """
    service_url = f"{MICROSERVICES['login_api']}/register"
    response = requests.post(
        url=service_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=request.get_json()
    )
    return jsonify(response.json()), response.status_code

# Login API - Login
@app.route('/loginapi/login', methods=['POST'])
@swag_from('swagger/login.yaml')
def proxy_login():
    """
    Proxy requests to Login API - Login
    """
    service_url = f"{MICROSERVICES['login_api']}/login"
    response = requests.post(
        url=service_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=request.get_json()
    )
    return jsonify(response.json()), response.status_code

# Bil API
@app.route('/carsapi/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/cars.yaml')
def proxy_cars(path):
    """
    Proxy requests to CARS API
    """
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = None

    service_url = f"{MICROSERVICES['bildatabase_api']}/{path}"
    response = requests.request(
        method=request.method,
        url=service_url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=data
    )
    return jsonify(response.json()), response.status_code

 # Abonnement API
@app.route('/abonnementapi/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/abonnement.yaml')
def proxy_abonnement(path):
    """
    Proxy requests to Abonnement API
    """
    # For POST and PUT, include JSON body
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = None
    
    service_url = f"{MICROSERVICES['abonnement_api']}/{path}"
    response = requests.request(
        method=request.method,  
        url=service_url,        
        headers={key: value for key, value in request.headers if key != 'Host'},  
        json=data  
    )
    return jsonify(response.json()), response.status_code

# Damage API
@app.route('/damageapi/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/damage.yaml')   
def proxy_damage(path):
    """
    Proxy requests to Damage API
    """
    service_url = f"{MICROSERVICES['damage_api']}/{path}"

    # For POST and PUT, include JSON body
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = None

    # Send the proxied request
    response = requests.request(
        method=request.method,  
        url=service_url,        
        headers={key: value for key, value in request.headers if key != 'Host'},  
        json=data  # Only send JSON for POST and PUT
    )
    
    return jsonify(response.json()), response.status_code

# Calculate API
@app.route('/calculateapi/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@swag_from('swagger/calculate.yaml')
def proxy_calculate(path):
    """
    Proxy requests to Calculate API
    """
    if request.method in ['POST', 'PUT']:
        data = request.get_json()
    else:
        data = None
    service_url = f"{MICROSERVICES['calculate_api']}/{path}"
    response = requests.request(
        method=request.method,  
        url=service_url,        
        headers={key: value for key, value in request.headers if key != 'Host'},  
        json=data
    )
    return jsonify(response.json()), response.status_code


if __name__ == '__main__':
    app.run()