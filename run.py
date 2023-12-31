from app import app
import ssl

# app = app
if __name__ == "__main__":
    # context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    # context.load_cert_chain("/ssl/cert.pem", "/ssl/key.pem")
    app.run(debug=True, host="0.0.0.0")
