from flask import Flask, render_template,url_for,flash,request,session,redirect
# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
from flask_mysqldb import MySQL
import yaml
import MySQLdb.cursors
import re



app = Flask(__name__)

db = yaml.full_load(open('db.yaml'))
app.config['SECRET_KEY']="secretkey"
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/home1')
def home1():
    return render_template("home1.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:            
            if user['role'] == 'admin':
                session['loggedin'] = True
                session['userid'] = user['userid']
                session['name'] = user['name']
                session['email'] = user['email']
                mesage = 'Logged in successfully !'
                return redirect(url_for('homech'))
                
            else:
               mesage = 'Only admin can login' 
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    return render_template('login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        country = request.form['country']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s, % s)', (userName, email, password, role, country))
            mysql.connection.commit()
            mesage = 'New user created!'
            return render_template('login.html')
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)


@app.route("/users", methods =['GET', 'POST'])
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user')
        users = cursor.fetchall()    
        return render_template("users.html", users = users)
    return redirect(url_for('login'))



@app.route("/edit", methods =['GET', 'POST'])
def edit():
    msg = ''    
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE userid = % s', (editUserId, ))
        editUser = cursor.fetchone()
        if request.method == 'POST' and 'name' in request.form and 'userid' in request.form and 'role' in request.form and 'country' in request.form :
            userName = request.form['name']   
            role = request.form['role']
            country = request.form['country']            
            userId = request.form['userid']
            if not re.match(r'[A-Za-z0-9]+', userName):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE user SET  name =% s, role =% s, country =% s WHERE userid =% s', (userName, role, country, (userId, ), ))
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('users'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'        
        return render_template("edit.html", msg = msg, editUser = editUser)
    return redirect(url_for('login'))

@app.route("/password_change", methods =['GET', 'POST'])
def password_change():
    mesage = ''
    if 'loggedin' in session:
        changePassUserId = request.args.get('userid')        
        if request.method == 'POST' and 'password' in request.form and 'confirm_pass' in request.form and 'userid' in request.form  :
            password = request.form['password']   
            confirm_pass = request.form['confirm_pass'] 
            userId = request.form['userid']
            if not password or not confirm_pass:
                mesage = 'Please fill out the form !'
            elif password != confirm_pass:
                mesage = 'Confirm password is not equal!'
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE user SET  password =% s WHERE userid =% s', (password, (userId, ), ))
                mysql.connection.commit()
                mesage = 'Password updated !'            
        elif request.method == 'POST':
            mesage = 'Please fill out the form !'        
        return render_template("password_change.html", mesage = mesage, changePassUserId = changePassUserId)
    return redirect(url_for('login'))


@app.route("/view", methods =['GET', 'POST'])
def view():
    if 'loggedin' in session:
        viewUserId = request.args.get('userid')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE userid = % s', (viewUserId, ))
        user = cursor.fetchone()   
        return render_template("view.html", user = user)
    return redirect(url_for('login'))


@app.route('/homech', methods=['GET', 'POST'])
def homech():
    if 'loggedin' in session:
        return render_template('homech.html')
    return redirect(url_for('login'))

@app.route('/gamebegin', methods=['GET', 'POST'])
def gamebegin():
    return render_template('gamebegin.html')

@app.route('/instruction1', methods=['GET', 'POST'])
def instruction1():
    return render_template('instruction1.html')

@app.route('/instruction2', methods=['GET', 'POST'])
def instruction2():
    return render_template('instruction2.html')

@app.route('/instruction3', methods=['GET', 'POST'])
def instruction3():
    return render_template('instruction3.html')


@app.route('/gamebegin2', methods=['GET', 'POST'])
def gamebegin2():
    return render_template('gamebegin2.html')




@app.route('/gamebegin3', methods=['GET', 'POST'])
def game3n():
    if request.method == 'POST':
        rf = request.form
        gans = rf['gans']
        cans = 1607
        if gans == str(cans):                                  
            cur= mysql.connection.cursor()
            cur.execute("INSERT INTO unlck(cans, gans) values(%s,%s)",(cans, gans))
            mysql.connection.commit()
            cur.close()  
            return render_template('gamebegin4.html')
        else:
            return "try again"  
        
    return render_template('gamebegin3.html')
            
@app.route('/gamebegin3', methods=['GET', 'POST'])
def gamebegin3():
    return render_template('gamebegin3.html')
    

@app.route('/gamebegin4', methods=['GET', 'POST'])
def gamebegin4():
    return render_template('gamebegin4.html')

@app.route('/gamebegin5', methods=['GET', 'POST'])
def gamebegin5():
    if request.method =='POST':
        ss = request.form
        flag= ss['flag']
        if flag=="Bing0_Flag_F0unD":
            return redirect('success')
        else :
            flash("retry!!")
            return render_template('gamebegin5.html')
        
    return render_template('gamebegin5.html')

@app.route('/gamebegin5', methods=['GET', 'POST'])
def gamebegin5s():
    return render_template('gamebegin5.html')

@app.route('/success/<email>',methods=['GET','POST'])
def succeed(email):
    if request.method == 'POST':
        return redirect('quizz/<email>')
    return render_template('success.html')
        
    

@app.route('/success',methods=['GET','POST'])
def success():
    if request.method == 'POST':
        return redirect('quizz/cherry')
    return render_template('success.html')


@app.route('/quizz/<email>', methods=['GET', 'POST'])
def quizz(email):
    if request.method == 'POST':
        answerDetails=request.form
        correct="Bad"
        qid=1
        score=0
        submitted=answerDetails['option']
        if submitted == correct:
            score=score+1
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO answer(qid,correct,submitted,score, email) values(%s,%s,%s,%s,%s)",(qid,correct,submitted,score,email))
        mysql.connection.commit()
        cur.close()
        return redirect(f'/quizz2/{email}')
    
    return render_template('quizz.html')



@app.route('/quizz2/<email>', methods=['GET', 'POST'])
def quizz2(email):
    if request.method == 'POST':
        answer2Details=request.form
        correct1="Carding"
        score=0
        qid=2
        submitted=answer2Details['option']
        if submitted == correct1:
            score=score+1
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO answer(qid,correct,submitted,score, email) values(%s,%s,%s,%s,%s)",(qid,correct1,submitted,score,email))
        mysql.connection.commit()
        cur.close()
        return redirect(f'/quizz3/{email}')
    
    return render_template('quizz2.html')



@app.route('/quizz3/<email>', methods=['GET', 'POST'])
def quizz3(email):
    if request.method == 'POST':
        answer3Details=request.form
        correct3="True"
        score=0
        qid=3
        submitted=answer3Details['option']
        if submitted == correct3:
            score=score+1
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO answer(qid,correct,submitted,score,email) values(%s,%s,%s,%s,%s)",(qid,correct3,submitted,score,email))
        mysql.connection.commit()
        cur.close()
        return redirect(f'/quizz4/{email}')
    
    return render_template('quizz3.html')



@app.route('/quizz4/<email>', methods=['GET', 'POST'])
def quizz4(email):
    if request.method == 'POST':
        answer4Details=request.form
        correct4="all of the above"
        score=0
        qid=4
        submitted=answer4Details['option']
        if submitted == correct4:
            score=score+1
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO answer(qid,correct,submitted,score,email) values(%s,%s,%s,%s,%s)",(qid,correct4,submitted,score,email))
        mysql.connection.commit()
        cur.close()
        return redirect(f'/quizz5/{email}')
        
    
    return render_template('quizz4.html')


@app.route('/quizz5/<email>', methods=['GET', 'POST'])
def quizz5(email):
    if request.method == 'POST':
        answer5Details=request.form
        correct5="To gain vital personal information"
        score=0
        qid=5
        submitted=answer5Details['option']
        if submitted == correct5:
            score=score+1
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO answer(qid,correct,submitted,score,email) values(%s,%s,%s,%s,%s)",(qid,correct5,submitted,score,email))
        select_stmt = "SELECT count(score) FROM answer WHERE score=1 and email = %(email)s"
        cur.execute(select_stmt, { 'email': email })
        cnt=cur.fetchone()
        cur.execute("INSERT INTO scores(score,email) values(%s,%s)",(cnt,email))         
        # viewscr = request.args.get('cnt')
        # print(viewscr)
        
        cur.execute('SELECT score FROM scores WHERE email = % s', (email, ))
        score = cur.fetchone()
        print(score)
        mysql.connection.commit()
        cur.close() 
                 
        return render_template('score.html', score = score)
        
    
    return render_template('quizz5.html')


# @app.route('/view', methods=['GET', 'POST'])
# def view():
#     return render_template('view.html')


# @app.route('/users', methods=['GET', 'POST'])
# def users():
#     return render_template('users.html')


# @app.route('/password_change', methods=['GET', 'POST'])
# def password_change():
#     return render_template('password_change.html')


# @app.route('/edit', methods=['GET', 'POST'])
# def edit():
#     return render_template('edit.html')
@app.route('/contact')
def contact():
    return render_template('contact.html') 

@app.route('/contact', methods=['GET', 'POST'])
def contactnav():
    if request.method == 'POST':
        ctus=request.form
        username = ctus['username']
        email_id = ctus['email_id']
        query = ctus['query']
        cur= mysql.connection.cursor()
        cur.execute("INSERT INTO contact_us(username,email_id,query) values(%s,%s,%s)",(username,email_id,query))
        mysql.connection.commit()
        cur.close()
        return render_template('contactsuccess.html')
    else:
        return render_template('contact.html')    


@app.route('/contactsuccess')
def contactsuccess():
    return render_template('contactsuccess.html')

@app.route('/quizz')
def question1():
    return render_template('quizz.html')

@app.route('/quizz2')
def question2():
    return render_template('quizz2.html')

@app.route('/quizz3')
def question3():
    return render_template('quizz3.html')

@app.route('/quizz4')
def question4():
    return render_template('question4.html')

@app.route('/quizz5')
def question5():
    return render_template('quizz5.html')

if __name__ == "__main__":
    app.run(debug=True)
    