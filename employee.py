from flask import Flask,render_template,request,redirect,url_for
import pymysql

app=Flask(__name__)

db=None
cur=None

def connectDB():
    global db
    global cur
    db = pymysql.connect(host="localhost",
                        user="root",
                        password="",
                        database="Assign")
    cur = db.cursor()

def disconnectDB():
    cur.close()
    db.close()

def readallrecords():
    connectDB()
    selectquery="select * from employee"
    cur.execute(selectquery)
    result=cur.fetchall()
    disconnectDB()
    return result

@app.route('/')
def index():
    data = readallrecords()
    return render_template('eindex.html',data=data)

@app.route('/insert')
def insert():
    return render_template('einsert.html')

@app.route('/insertrecord')
def insertrecord():
    connectDB()
    ID = request.args.get('id')
    Name = request.args.get('name')
    Department_No = request.args.get('Department_no')
    salary = request.args.get('salary')
    insertquery = 'insert into employee(id,name,department,salary) values("{}","{}","{}","{}")'.format(ID,Name,Department_No,salary)
    cur.execute(insertquery)
    db.commit()
    disconnectDB()
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    connectDB()
    deletequery = 'delete from employee where id={}'.format(id)
    cur.execute(deletequery)
    db.commit()
    disconnectDB()
    return redirect(url_for('index'))

def readonerecord(id):
    connectDB()
    selectquery="select * from employee where id={}".format(id)
    cur.execute(selectquery)
    result=cur.fetchone()
    disconnectDB()
    return result

@app.route('/update/<id>')
def update(id):
    data=readonerecord(id)
    return render_template('eupdate.html',data=data)

@app.route('/updaterecord/<id>',methods=['GET','POST'])
def updaterecord(id):
    connectDB()
    Id = request.form['id']
    Name = request.form['name']
    Department = request.form["Department_no"]
    Salary =  request.form['salary']
    updatequery='update employee set id="{}", name="{}",department="{}",salary="{}" where id={}'.format(Id,Name,Department,Salary,id)
    cur.execute(updatequery)
    db.commit()
    disconnectDB()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)