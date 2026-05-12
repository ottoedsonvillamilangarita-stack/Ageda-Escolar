import requests

SUPABASE_URL = "https://tu-proyecto.supabase.co"  # CAMBIA A TU URL
SUPABASE_KEY = "tu-anon-key"  # CAMBIA A TU ANON KEY

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

# Probar conexión
url = f"{SUPABASE_URL}/rest/v1/usuarios_login?username=eq.estudiante.laura"
response = requests.get(url, headers=headers)

print(f"Código: {response.status_code}")
print(f"Respuesta: {response.text}")
