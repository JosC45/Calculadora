from app import db

# class Usuario(db.model):
#     __tablename__="Users"
#     id=db.Column(db.Integer,primary_key=True)
#     def __repr__(self):
#         return f"<Usuario numero {self.id}>"
    
class Seleccion(db.Model):
    __tablename__="seleccion"
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50),nullable=False)
    victorias=db.Column(db.Integer,nullable=False)
    empates=db.Column(db.Integer,nullable=False)
    derrotas=db.Column(db.Integer,nullable=False)
    goles_f=db.Column(db.Integer,nullable=False)
    goles_c=db.Column(db.Integer,nullable=False)
    def puntajes(self):
        puntos=self.victorias*3+self.empates
        return puntos
    def goles(self):
        diferencia=self.goles_f-self.goles_c
        return diferencia

class Partido(db.Model):
    __tablename__="partidos"
    id=db.Column(db.Integer,primary_key=True)
    local=db.Column(db.Integer,db.ForeignKey("seleccion.id"),nullable=False)
    visitante=db.Column(db.Integer,db.ForeignKey("seleccion.id"),nullable=False)