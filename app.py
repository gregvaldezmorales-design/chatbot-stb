from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key="gsk_TU_API_KEY_AQUI")

SISTEMA = """
Eres el asistente virtual de Soluciones Tecnológicas Bocatoreñas, 
una empresa de tecnología ubicada en Bocas del Toro, Panamá.

Ayudas a los usuarios con información sobre:
- Curso de Arduino y Robótica
- Curso de Programación (HTML, CSS, Python, Node.js, SQL)
- Servicio de Diseño Web
- Soporte y Reparación de equipos informáticos
- Programación de Robots en Arduino

Responde siempre en español, de forma amable, breve y profesional.
Si no sabes algo, invita al usuario a contactar directamente.
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje = data.get('mensaje', '')

    respuesta = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": SISTEMA},
            {"role": "user", "content": mensaje}
        ]
    )

    return jsonify({
        'respuesta': respuesta.choices[0].message.content
    })

if __name__ == '__main__':
    app.run(debug=True)