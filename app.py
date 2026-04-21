from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
# CORS configurado para permitir peticiones desde cualquier origen (importante para Byethost)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración del cliente Groq
# Recuerda que GROQ_API_KEY debe estar en las "Environment Variables" de Render
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

SISTEMA = """
Eres el asistente virtual de ROADED (antes Soluciones Tecnológicas Bocatoreñas), 
ubicada en Changuinola, Bocas del Toro, Panamá.

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
- Curso de Arduino y Robótica (STEAM)
- Programación de Robots y mantenimiento preventivo
- Servicio de Diseño Web y Software Personalizado
- Soporte y Reparación de equipos físicos (PC, Laptops)

Instrucciones de comportamiento:
- Responde siempre en español, de forma amable, breve y profesional.
- Usa emojis de forma moderada.
- Si el usuario pregunta por algo fuera de estos servicios, invítalo a escribir al WhatsApp o al email.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Verificar que la API KEY existe
        if not api_key:
            return jsonify({'respuesta': 'Error: API Key no configurada en el servidor.'}), 500

        data = request.get_json()
        if not data:
            return jsonify({'respuesta': 'Error: No se enviaron datos válidos.'}), 400
            
        mensaje = data.get('mensaje', '')

        if not mensaje:
            return jsonify({'respuesta': 'Por favor, escribe un mensaje para poder ayudarte.'}), 400

        # Llamada a Groq con manejo de errores específico
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SISTEMA},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.7,
            max_tokens=500
        )

        # Extraer respuesta de forma segura
        respuesta_texto = completion.choices[0].message.content

        return jsonify({
            'respuesta': respuesta_texto
        })
    
    except Exception as e:
        print(f"Error detectado: {str(e)}")
        return jsonify({'respuesta': 'Lo siento, tuve un problema interno. Inténtalo de nuevo en un momento.'}), 500

# Ruta de prueba para verificar que el servidor está vivo
@app.route('/')
def health_check():
    return "Servidor ROADED en funcionamiento", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)