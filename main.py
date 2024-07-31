import requests

# Configuración
CLIENT_ID = 'tu-client-id'
CLIENT_SECRET = 'tu-client-secret'
TOKEN_URL = 'https://api.sistemaA.com/oauth/token'
API_A_URL = 'https://api.sistemaA.com/facturas'
API_B_URL = 'https://api.sistemaB.com/bills'
API_B_KEY = 'tu-api-key'

# Obtener token OAuth 2.0 de API A
def obtener_token_oauth2(client_id, client_secret, token_url):
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, data=data)
    token = response.json().get('access_token')
    return token

# Consultar facturas en API A
def obtener_facturas(fecha_inicio, fecha_fin, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    }
    response = requests.get(API_A_URL, headers=headers, params=params)
    return response.json()

# Transformar datos de API A al formato de API B
def transformar_facturas(facturas_api_a):
    facturas_transformadas = []
    for factura in facturas_api_a['facturas']:
        factura_transformada = {
            'invoice_id': factura['id'],
            'customer': factura['cliente'],
            'amount_due': factura['monto'],
            'date_issued': factura['fecha_emision'],
            'status': factura['estado']
        }
        facturas_transformadas.append(factura_transformada)
    return {'invoices': facturas_transformadas}

# Enviar facturas a API B
def enviar_facturas_api_b(facturas_transformadas, api_key):
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(API_B_URL, headers=headers, json=facturas_transformadas)
    return response.status_code

# Flujo principal
if __name__ == '__main__':
    token = obtener_token_oauth2(CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
    facturas_api_a = obtener_facturas('2024-07-01', '2024-07-31', token)
    facturas_transformadas = transformar_facturas(facturas_api_a)
    status_code = enviar_facturas_api_b(facturas_transformadas, API_B_KEY)
    print(f'Status Code API B: {status_code}')
