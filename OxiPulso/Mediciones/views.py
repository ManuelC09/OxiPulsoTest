from flask import (
    render_template,
    Blueprint,
    request,
    jsonify,
    session,
    redirect,
    url_for 
)
from OxiPulso.Mediciones.models import Mediciones

from OxiPulso.funciones import init_mqtt, wait_for_message
from OxiPulso import app, db
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Iniciar MQTT
topic = os.environ.get('MQTT_TOPIC')
mqtt_client = init_mqtt(app, topic)


mediciones = Blueprint('mediciones', __name__)


@mediciones.route('/mediciones', methods=['GET', 'POST'])
def medicion():
    return render_template("mediciones/mediciones.html")

@mediciones.route('/tutorial')
def tutorial():
    return render_template("mediciones/tutorial.html")

@app.route('/mediciones/medir', methods=['POST'])
def publish_message():
    request_data = request.form['message']
    publish_result = mqtt_client.publish(topic, request_data)
    print(publish_result)
    
    # Espera a que se publique el valor medido
    measured_value = wait_for_message()
    # measured_value = {"HR":51,"SPO2":90}
    # measured_value = None
    
    if measured_value is not None:
        print(measured_value)
        
        usuario_id = session.get('usuario_id')
        if usuario_id:
            try:
                nueva_medicion = Mediciones(
                    usuario_id=usuario_id,
                    bpm=measured_value["HR"],
                    spo2=measured_value["SPO2"],
                    fecha=datetime.today().date(),
                    hora=datetime.now().time()
                )
                
                db.session.add(nueva_medicion)
                db.session.commit()
           
            except Exception as e:
               
                db.session.rollback()
                return jsonify(success=False, error="Error inesperado al guardar la medición")
        
        return jsonify(success=True, hr=measured_value["HR"], spo2=measured_value["SPO2"])
    else:
        return jsonify(success=False, error="No se recibió el valor del sensor a tiempo")
    
@mediciones.route('/mediciones/historial')
def historial():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        mediciones = Mediciones.obtener_datos(id=usuario_id)
        #return render_template("mediciones/historial.html", mediciones=mediciones)
        return mediciones
    else:
        return redirect(url_for('usuarios.login'))
    
@mediciones.route('/mediciones/descargar')
def descargar():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        Mediciones.descargar_csv(usuario_id)
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="No se ha iniciado sesión")