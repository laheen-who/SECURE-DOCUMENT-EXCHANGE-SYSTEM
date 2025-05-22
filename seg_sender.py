import requests

with open('document.xml', 'r') as f:
    xml_data = f.read()

try:
    response = requests.post('https://localhost:8000', data=xml_data, cert=('client.crt', 'client.key'), verify='rootCA.pem')
    print("Server response:", response.text)
except Exception as e:
    print(f"Error sending request: {str(e)}")