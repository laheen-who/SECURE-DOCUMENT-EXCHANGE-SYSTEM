import ssl
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive():
    print("Successful mTLS connection established.")
    print("Received XML:", request.data.decode('utf-8'))
    return "Received", 200

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    context.load_verify_locations(cafile="rootCA.pem")
    context.verify_mode = ssl.CERT_REQUIRED
    app.run(host='0.0.0.0', port=8000, ssl_context=context)