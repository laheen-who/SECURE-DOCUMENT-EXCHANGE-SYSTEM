from flask import Flask, request
import ssl

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive():
    try:
        print("Successful mTLS connection established.")
        xml_data = request.data.decode('utf-8')
        print("Received XML:", xml_data)
        return "Received", 200
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="server.crt", keyfile="server.key")
        context.load_verify_locations(cafile="rootCA.pem")
        context.verify_mode = ssl.CERT_REQUIRED
        app.run(host='0.0.0.0', port=8000, ssl_context=context)
    except Exception as e:
        print(f"Failed to start server: {str(e)}")