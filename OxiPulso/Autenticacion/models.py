from OxiPulso import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fechaNacimiento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(250), nullable=False)
    fechaRegistro = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, nombre, fechaNacimiento, sexo, usuario, correo, contraseña, fechaRegistro):
        self.nombre = nombre
        self.fechaNacimiento = fechaNacimiento
        self.sexo = sexo
        self.usuario = usuario
        self.correo = correo
        self.contraseña = contraseña
        self.fechaRegistro = fechaRegistro
    
    def __repr__(self):
        return f"Nombre: {self.nombre}\nUsuario: {self.usuario}\nCorreo: {self.correo}"