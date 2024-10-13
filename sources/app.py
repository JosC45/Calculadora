from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
import pymysql,os
from flask_migrate import Migrate


app=Flask(__name__)




# # Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita advertencias innecesarias
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
    seleccion=Seleccion.query.all()
    at=[]
    pais= sorted(seleccion, key=lambda x: x.puntajes(), reverse=True)
    return render_template('calculadora.html',primera=partidos,fecha_id=fecha_id,pais=pais)

@app.route('/ordenar')
def listar():
    seleccion=Seleccion.query.all()
    at=[]
    pais= sorted(seleccion, key=lambda x: x.puntajes(), reverse=True)
    return render_template('listado.html',pais=pais)


@app.route('/calculadora')
def calculadora():
    return render_template("calculadora.html")

@app.route('/listado')
def prueba():
    seleccion=Seleccion.query.all()
    for i in range(0,9):
        print(seleccion[i].nombre)
    return None

@app.route('/salir')
def salir():
    seleccion=Seleccion.query.all()
    seleccion[0].victorias=6
    seleccion[0].empates=0
    seleccion[0].derrotas=2
    seleccion[0].goles_f=12
    seleccion[0].goles_c=4
    seleccion[1].victorias=3
    seleccion[1].empates=0
    seleccion[1].derrotas=5
    seleccion[1].goles_f=10
    seleccion[1].goles_c=15
    seleccion[2].victorias=3
    seleccion[2].empates=1
    seleccion[2].derrotas=4
    seleccion[2].goles_f=9
    seleccion[2].goles_c=8
    seleccion[3].victorias=1
    seleccion[3].empates=2
    seleccion[3].derrotas=5
    seleccion[3].goles_f=4
    seleccion[3].goles_c=12
    seleccion[4].victorias=4
    seleccion[4].empates=4
    seleccion[4].derrotas=0
    seleccion[4].goles_f=9
    seleccion[4].goles_c=5
    seleccion[5].victorias=4
    seleccion[5].empates=2
    seleccion[5].derrotas=2
    seleccion[5].goles_f=6
    seleccion[5].goles_c=4
    seleccion[6].victorias=2
    seleccion[6].empates=3
    seleccion[6].derrotas=3
    seleccion[6].goles_f=2
    seleccion[6].goles_c=3
    seleccion[7].victorias=0
    seleccion[7].empates=3
    seleccion[7].derrotas=5
    seleccion[7].goles_f=2
    seleccion[7].goles_c=10
    seleccion[8].victorias=4
    seleccion[8].empates=3
    seleccion[8].derrotas=1
    seleccion[8].goles_f=13
    seleccion[8].goles_c=5
    seleccion[9].victorias=2
    seleccion[9].empates=4
    seleccion[9].derrotas=2
    seleccion[9].goles_f=6
    seleccion[9].goles_c=7
    db.session.commit()
    return redirect(url_for('index'))   

if __name__=="__main__":
    app.run(debug=True)