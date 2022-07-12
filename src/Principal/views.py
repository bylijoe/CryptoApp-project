from flask import render_template,request
from datetime import datetime
from . import app, metrics
from .models import CryptoCambio, DBManager 
from .forms import PurchaseForm


MYSQL_HOST=app.config['MYSQL_HOST']
MYSQL_USER=app.config['MYSQL_USER']
MYSQL_PORT=app.config['MYSQL_PORT']
MYSQL_PASSWORD=app.config['MYSQL_PASSWORD']
MYSQL_DATABASE=app.config['MYSQL_DATABASE']

# staic information as metric
metrics.info('app_info', 'Application info' , version='1.0.3')

@app.route("/")
def inicio():
    
    db = DBManager( MYSQL_HOST, MYSQL_USER, MYSQL_DATABASE, MYSQL_PASSWORD, int(MYSQL_PORT) )
    movimientos = db.querySQL(
        "SELECT id, date , time, from_currency, from_quantity, to_currency, to_quantity FROM movimientos")

    return render_template("inicio.html", movs=movimientos)

@app.route("/purchase/", methods=['GET', 'POST'])
def purchase():
    
    if request.method=="GET":

        return render_template("purchase.html", form=PurchaseForm())

    elif request.method=="POST":
        
        form=PurchaseForm(request.form)

        cantidadCambiada=0
        P_U = 0

        aCambiar=CryptoCambio(form.from_currency.data,form.to_currency.data)
        rate= aCambiar.exchange()

        cantidadAcambiar=int(form.from_quantity.data)
        cantidadCambiada= cantidadAcambiar * rate

        P_U=cantidadAcambiar/cantidadCambiada

        date = datetime.now().strftime('%d-%m-%y')
        time = datetime.now().strftime('%H:%M:%S')

        if form.data["submit_aceptar"]:
            
            db=DBManager( MYSQL_HOST, MYSQL_USER, MYSQL_DATABASE, MYSQL_PASSWORD, int(MYSQL_PORT) )
            val=(date,time,form.from_currency.data,form.from_quantity.data,form.to_currency.data,cantidadCambiada)
            sql="INSERT INTO movimientos (date,time,from_currency,from_quantity,to_currency,to_quantity) VALUES (%s,%s,%s,%s,%s,%s);"
            resultado=db.ejecutarConParametros(sql, val)

            return  render_template("compra_ok.html",resultado=resultado)

        elif form.data["submit_calcular"]:

            return render_template('purchase.html',form=form, P_U=P_U, cantidadCambiada=cantidadCambiada)
        
     
    
@app.route('/borrar/<int:id>')
def borrar(id):
    
    db=DBManager( MYSQL_HOST, MYSQL_USER, MYSQL_DATABASE, MYSQL_PASSWORD, int(MYSQL_PORT) )
    sql="DELETE FROM movimientos WHERE id=%s"
    val=(id,)        
    resultado= db.ejecutarConParametros(sql,val)
    
    return render_template("borrado.html", resultado=resultado)   


@app.route("/purchase/status")
def status_inversion():
    
    return render_template("status.html")


@app.route('/health/liveness')
@metrics.do_not_track()   
def healthx():
    return {"healthx": "ok"}   

@app.route('/health/readiness')
@metrics.do_not_track()
def healthz():
    return {"healthz": "ok"}    

