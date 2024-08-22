from flask import Flask
from flask_mysqldb import MySQL


from flask_mysqldb import MySQL
from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect, session, flash,Response,jsonify
from datetime import date
from werkzeug.utils import secure_filename
import random
import os

from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)

app.config['SECRET_KEY'] = "dadafafasferfwa" 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_user'

mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def index():
   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM products ")
   pr = cursor.fetchall()  

   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM products where p_cat=%s ",("electronics",))
   el = cursor.fetchall()  

   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM products where p_cat=%s ",("cosmetics",))
   co = cursor.fetchall()   
             
   cursor = mysql.connection.cursor()
   cursor.execute("SELECT * FROM products where p_cat=%s ",("beautyproducts",))
   be = cursor.fetchall() 

   return render_template('index.html',pr=pr,el=el,co=co,be=be)
  



@app.route("/logindash", methods=['GET', 'POST'])
def logindash():
   if 'username' in session:
        return render_template('sign.html')
   else:
        return render_template('sign.html')
   

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("select * from usertabel where username =%s and password=%s", (username,pwd))
        user = cur.fetchone()
        cur.close()
        if user:
            session['name']=user[1]
            session['id']=user[0]

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM products ")
            pr = cursor.fetchall()  

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM products where p_cat=%s ",("electronics",))
            el = cursor.fetchall()  

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM products where p_cat=%s ",("cosmetics",))
            co = cursor.fetchall()   
             
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM products where p_cat=%s ",("beautyproducts",))
            be = cursor.fetchall()   

            return render_template('index.html',pr=pr,el=el,co=co,be=be)
        
        else:
            return render_template('login.html')


        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        pwd = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("insert into usertabel (username,email,phonenumber,password) values (%s,%s,%s,%s) ",(username,email, phonenumber, pwd))
        mysql.connection.commit()
        cur.close()

        return render_template('login.html')
    
    return render_template('register.html')


@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():

    pid=request.args.get('p_id')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products where p_id=%s ",(pid,))
    be = cursor.fetchone()
    # Logic to add the product to the cart
    return render_template('shop-detail.html',be=be)



@app.route('/cart', methods=['GET', 'POST'])
def cart():

    if 'name' in session:
        username = session['name']
        uid=session['id']
        pid=request.args.get('p_id')
        qty=int(request.args.get('qty'))

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products where p_id=%s ",(pid,))
        be = cursor.fetchone()
        prz=int(be[4])
        dis=int(be[5])

        total=qty*prz

        discount_amount = total * (dis / 100)
    
        # Calculate the final price after discount
        final_price = total - discount_amount


        dat=date.today()
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO `cart`( `cid`, `p_name`, `p_cat`, `p_img`, `p_price`, `p_dis`, `p_qty`, `p_date`, `status`,`total`,`final`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                                    (uid,be[1],be[2], be[3],be[4],be[5],qty,dat,'0',total,final_price))
                        
        cursor.connection.commit()
        cursor.close()

        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM cart where cid=%s",(uid,))
        cr = cursor.fetchall() 
    
        return render_template('chackout.html',cr=cr)
    
    return render_template('login.html')
    


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    uid =int(request.args.get('cid'))
    conn =  mysql.connection.cursor()
    conn.execute('DELETE FROM cart WHERE id=%s', (uid,))
    conn.connection.commit()
    conn.close()
    conn =  mysql.connection.cursor()
    conn.execute('select * from cart ')
    de = conn.fetchall() 
    return render_template('chackout.html',cr=de)



if __name__=='__main__':
    app.run(debug=True)