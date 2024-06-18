from OxiPulso import db
import pandas as pd
import os
from OxiPulso.Autenticacion.models import Usuario

class Mediciones(db.Model):
    _tablename_ = "mediciones"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    bpm = db.Column(db.Integer, nullable=False)
    spo2 = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

    def __init__(self, usuario_id, bpm, spo2, fecha, hora):
        self.usuario_id = usuario_id
        self.bpm = bpm
        self.spo2 = spo2
        self.fecha = fecha
        self.hora = hora
    
    def __repr__(self):
        return f"BPM: {self.bpm}\nSPO2: {self.spo2}\nFecha: {self.fecha}\nHora: {self.hora}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'bpm': self.bpm,
            'spo2': self.spo2,
            'fecha': self.fecha.isoformat(),
            'hora': str(self.hora)
        }
    
    
    @classmethod
    def obtener_datos(cls, id):
        datos = cls.query.filter_by(usuario_id=id).all()
        datos_dict = [dato.to_dict() for dato in datos]
        return datos_dict
        

    
    @classmethod
    def descargar_csv(cls, usuario_id):
        usuario = Usuario.query.filter_by(id=usuario_id).first()
    
        datos = db.session.query(Usuario, Mediciones).join(Mediciones,
            Usuario.id == Mediciones.usuario_id).with_entities(Usuario.nombre, Mediciones.bpm, Mediciones.spo2, Mediciones.hora, Mediciones.fecha).filter(Usuario.id == usuario_id).all()

    
        df = pd.DataFrame(datos, columns=['Nombre', 'BPM', 'SPO2', 'Hora', 'Fecha'])

        carpeta = 'OxiPulso/archivos'
        
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        ruta = os.path.join(carpeta, f"{usuario.nombre}.csv")

        print("Se descargó")
        # Convertimos el dataframe en un archivo excel y lo guardamos
        df.to_csv(ruta, index=False)
        return ruta
        
    