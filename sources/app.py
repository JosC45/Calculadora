from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import pymysql,os
from flask_migrate import Migrate


app=Flask(__name__)
app.secret_key=os.urandom(24)

db_user='root'
db_password='12345'
db_host='127.0.0.1'
db_port=3306
db_database='base_de_datos'

# # Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/base_de_datos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita advertencias innecesarias
# def coneccion():
#     try:
#         conexion=pymysql.connect(
#             host=db_host,
#             user=db_user,
#             password=db_password,
#             database=db_database,  
#             port=db_port, 
#             charset='utf8',
#         )
#         print("Conexion con exito")
#         return conexion
#     except pymysql.MySQLError as e:
#         print(f"Error al conectar {e}")
#         return None
# coneccion()
db=SQLAlchemy(app)
from models import Seleccion,Partido
migrate=Migrate(app,db)

@app.route('/conexion')
def conexion():
    return "Conexion con exito"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/suma')
def suma100():
    suma=0
    for i in range(1,100):
        suma=+i
    return str(suma)



@app.route('/ver_fecha/<int:fecha_id>',methods=['GET','POST'])
def resultados(fecha_id):
    partidos=Partido.query.filter_by(fecha=fecha_id).all()
    if request.method=='POST':
        for partido in partidos:
            goles_local=request.form.get(f'goles_local_{partido.equipo_local.nombre}')
            goles_visita=request.form.get(f'goles_visita_{partido.equipo_visitante.nombre}')

            if goles_local is not None and goles_visita is not None:
                goles_local=int(goles_local)
                goles_visita=int(goles_visita)
                if goles_local>goles_visita:
                    partido.equipo_local.victorias+=1
                    partido.equipo_visitante.derrotas+=1
                elif goles_local==goles_visita:
                    partido.equipo_local.empates+=1
                    partido.equipo_visitante.empates+=1
                else:
                    partido.equipo_visitante.victorias+=1
                    partido.equipo_local.derrotas+=1

                partido.equipo_local.goles_f+=goles_local
                partido.equipo_local.goles_c+=goles_visita

                partido.equipo_visitante.goles_f+=goles_visita
                partido.equipo_visitante.goles_c+=goles_local
        db.session.commit()
        siguiente_fecha=Partido.query.filter(Partido.fecha>fecha_id).order_by(Partido.fecha).first()
        if siguiente_fecha:
            return redirect(url_for('resultados',fecha_id=siguiente_fecha.fecha))
        else:
            return redirect(url_for('listar'))
    return render_template('calculadora.html',primera=partidos,fecha_id=fecha_id)

@app.route('/ordenar')
def listar():
    seleccion=Seleccion.query.all()
    at=[]
    pais= sorted(seleccion, key=lambda x: x.puntajes(), reverse=True)
    return render_template('listado.html',pais=pais)


@app.route('/calculadora')
def index():
    return render_template("calculadora.html")

@app.route('/salir')
def salir():
    for 
        Partido.query.filter(fecha=i).delete()
    
    db.session.commit()
    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)