from flask import Flask, render_template, request,redirect,url_for,flash
from flask_mysqldb import MySQL

#Inicializacion del APP
app= Flask (__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="DB_Fruteria"
app.secret_key= 'mysecrety'
mysql= MySQL(app)

app.secret_key='mysecretkey'
mysql= MySQL(app)

#Declaramos una ruta
@app.route('/')
def index():
  CC= mysql.connection.cursor();
  CC.execute('select * from tbFrutas')
  conFrutas= CC.fetchall()
  print(conFrutas)
  return render_template('index.html',listFrutas= conFrutas)

@app.route('/guardari', methods=['POST'])
def guardari():
    if request.method == 'POST':
        Vfruta = request.form['txtFruta']
        Vatemp = request.form['txtTemporada']
        Vpr = request.form['txtPrecio']
        Vst = request.form['txtStock']
        
        #print(Fruta, Temporada, Precio, Stock)
        
        #Conectamos y ejecutamos el Insert
        CS = mysql.connection.cursor()
        CS.execute('insert into tbFrutas (fruta,temporada,precio,stock) values (%s,%s,%s,%s)',(Vfruta,Vatemp,Vpr,Vst))
        mysql.connection.commit()
    flash('Fruta agregada correctamente ')
    return redirect(url_for('index'))

@app.route('/editari/<string:id>')
def editari(id):
   cursoID=mysql.connection.cursor()
   cursoID.execute('select*from tbFrutas where id=%s', (id,))
   consultID=cursoID.fetchone()

   return render_template('editar.html', consultID=consultID)

@app.route('/actualizari/<id>', methods=['POST'])
def actualizari(id):
    if request.method == 'POST':
        Vfruta = request.form['txtFruta']
        Vatemp = request.form['txtTemporada']
        Vpr = request.form['txtPrecio']
        Vst = request.form['txtStock']
        
        CS = mysql.connection.cursor()
        CS.execute('update tbFrutas set fruta =%s ,temporada = %s ,precio = %s ,stock = %s where id = %s',(Vfruta,Vatemp,Vpr,Vst,id))
        mysql.connection.commit()
        
    flash('Fruta actuializadfa correctamente en la Base de datos DB_Fruteria:')
    return redirect(url_for('index'))

# Seleccionar el producto que se eliminara despúes
@app.route('/eliminari/<id>')
def eliminari(id):
    CEID = mysql.connection.cursor()
    CEID.execute('select * from tbFrutas where id = %s',(id,))
    consultID = CEID.fetchone()
    
    return render_template('eliminar.html', consultID=consultID)

# Eliminar de la lista 
@app.route('/eliminarfruta/<id>', methods=['POST'])
def eliminarafruta(id):
    if request.method == 'POST':
        
        CE = mysql.connection.cursor()
        CE.execute('delete from tbFrutas where id = %s',(id,))
        mysql.connection.commit()
        
    flash('Se elimino la Fruta en la BD :')
    return redirect(url_for('index'))
    
@app.route('/buscari', methods=['GET', 'POST'])
def buscari():
    if request.method == 'POST':
        Vfruta = request.form['txtFruta']
        
        curslect = mysql.connection.cursor()
        curslect.execute('SELECT * FROM tbFrutas WHERE fruta = %s', (Vfruta,))
        CNT = curslect.fetchone()
    
    CS = mysql.connection.cursor()
    CS.execute('SELECT fruta FROM tbFrutas')
    frutas = CS.fetchall()
    return render_template('buscar.html', list=frutas)

#Ejecucion de servidor
if __name__ =='__main__':
    app.run(port=2000,debug=True)
