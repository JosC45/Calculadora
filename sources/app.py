from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_migrate import Migrate


app=Flask(__name__)

db_user='root'
db_password='12345'
db_host='127.0.0.1'
db_port=3306
db_database='base_de_datos'

# # Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@127.0.0.1:3306/base_de_datos'
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

@app.route('/pelis_favoritas')
def pelis():

    return render_template()
@app.route('/calculadora')
def calculadora():
    return render_template("calculadora.html")


if __name__=="__main__":
    app.run(debug=True)