from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# Configuración del cliente Groq 
# Asegúrate de configurar GROQ_API_KEY en las variables de entorno de tu servidor o local
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SISTEMA = """
Eres el asistente virtual de Soluciones Tecnológicas Bocatoreñas, 
ubicada en Bocas del Toro, Panamá.

Información importante para el cliente:
- Precios de Cursos y Servicios:
    * Curso de Programación (HTML y CSS): 150.00
    * Soporte técnico en línea: 45.00
    * Instalación de Office: 25.00
- Horarios de atención: Lunes a Viernes de 8:00 a.m. a 4:00 p.m.
- Contacto directo:
    * WhatsApp: 68629178
    * Email: gregvaldezmorales@gmail.com

Servicios adicionales que ofreces:
- Curso de Arduino y Robótica
- Programación de Robots
- Servicio de Diseño Web
- Soporte y Reparación de equipos físicos

Instrucciones de comportamiento:
- Responde siempre en español, de forma amable, breve y profesional.
- Usa emojis de forma moderada para ser cercano.
- Si el usuario pregunta por algo fuera de estos servicios, invítalo a escribir al WhatsApp o al email mencionados.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        mensaje = data.get('mensaje', '')

        if not mensaje:
            return jsonify({'error': 'No se proporcionó un mensaje'}), 400

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
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Usar el puerto que asigne el servidor o el 5000 por defecto
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)