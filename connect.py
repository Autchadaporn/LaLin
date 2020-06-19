from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify,json
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
import bcrypt

# Start connect DB
app = Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='lalin'
app.config['MYSQL_CURSORCLASS']='DictCursor'
# Stop connect
mysql = MySQL(app)

# ----------------start login -------------#
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/checklogin",methods=['GET', 'POST'])
def checklogin():
    if request.method == 'POST':
        Student_ID = request.form['Student_ID']
        # print (Student_ID)
        cur = mysql.connection.cursor()
        cur.execute("SELECT Student_Name,Student_Lastname FROM student WHERE Student_ID = '"+Student_ID+"'")
        NameStudent =cur.fetchall()
    return render_template('hello.html',Name=NameStudent,Student_ID=Student_ID)


# ----------------stop login -------------#

# ---------------- ดูข้อมูลการศึกษา -------------#
@app.route("/inforstudy",methods=['GET', 'POST'])
def inforstudy():
    if request.method == 'POST':
        Student_ID = request.form['Student_ID']
        # print (Student_ID)
        cur = mysql.connection.cursor()
        cur.execute("SELECT  Subject_ID,Subject_TH, Unit, Grade FROM informationstudy WHERE Student_ID = '"+Student_ID+"'")
        Subject =cur.fetchall()
    return render_template('inforstudy.html',Subject=Subject)
# ---------------- ดูข้อมูลการศึกษา -------------#
@app.route("/test")
def test():
    return render_template('test.html') 


# ---------------------------ปฏิทินการศึกษา----------------------------------------------------

# แสดงปฏิทิน
@app.route("/calendar")
def calendar(): 
        cur = mysql.connection.cursor()
        cur.execute("SELECT calendar.id, topic.Topic_ID, topic.Topic, calendar.Term, calendar.Start_Date, calendar.Finish_Date, calendar.Year FROM topic INNER JOIN calendar ON topic.Topic_ID = calendar.Topic_ID  ")
        rows = cur.fetchall()
        return render_template('calendar.html',datas=rows)

@app.route("/formsearch")
def formsearch():
    return render_template('formsearch.html')

# ค้นหา
@app.route("/search" ,methods=['GET', 'POST'])
def search():
    Topic =  request.form['Topic']
    Term =  request.form['Term']
    # print(Topic,Term)
    cur = mysql.connection.cursor() #เชื่อมdatabase
    cur.execute("SELECT Start_Date,Finish_Date FROM calendar WHERE Topic_ID = '"+Topic+"' AND Term = '"+Term+"'")
    rows=cur.fetchall() #แสดงข้อมูลทั้งหมด
    return render_template('search.html',datas = rows)

# เพิ่มวันเดือนปี ปฏิทินการศึกษา
@app.route("/showform")
def showform():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM topic")
    rows=cur.fetchall()
    return render_template('addcalendar.html',datas = rows)
@app.route("/addcalendar", methods=['POST','GET'])
def addcalendar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM topic")
    rows=cur.fetchall()
    if request.method == 'POST': #เช็คว่าส่งmethod POST มาหรือไม่ ถ้าใช่ให้ทำในเงื่อนไข
        
        Topic_ID = request.form['Topic_ID']
        # Topicid = request.form.get('Topic') # เขียนแบบ method GET
        Start_Date = request.form['Start_Date']
        Finish_Date = request.form['Finish_Date']
        Term = request.form['Term']
        Year = request.form['Year']
        # print(Topic_ID,Start_Date,Finish_Date,Term,Year)
        cur.execute("INSERT INTO calendar (Topic_ID,Term,Start_Date,Finish_Date,Year) VALUES (%s,%s,%s,%s,%s)",(Topic_ID,Term,Start_Date,Finish_Date,Year))
        
        mysql.connection.commit()
    return redirect(url_for('calendar'))

# เพิ่มหัวข้อกิจกรรม
@app.route("/addtopic")
def addtopic():
    return render_template('addtopic.html')
@app.route("/inserttopic",methods=["POST"])
def inserttopic():
    Topic_ID = request.form['Topic_ID']
    Topic = request.form['Topic']
    # print(Topic_ID,Topic)
    cur = mysql.connection.cursor()
    cur.execute (" INSERT INTO topic (Topic_ID,Topic) VALUES (%s,%s)",(Topic_ID,Topic)) #เพิ่มห้อข้อกิจกรรมลงในตารางTopic
    # print(cur)
    # cur.execute(cur)
    mysql.connection.commit()
    return render_template('addtopic.html')

#ลบแถว
@app.route("/delete/<string:id>",methods=["POST","GET"])
def delete(id):
    # print(id)
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM calendar WHERE id=%s",(id)) #เลือกลบข้อมูลที่มีค่าเท่ากับ id รับค่ามาจาก หน้า calendar
    mysql.connection.commit()
    return redirect(url_for('calendar'))

#อัพเดทข้อมูล
@app.route("/update", methods=['POST','GET'])
def update():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM topic")
    rows=cur.fetchall()
    if request.method == 'POST': #เช็คว่าส่งmethod POST มาหรือไม่ ถ้าใช่ให้ทำในเงื่อนไข
        # Finish_Date = 'null'
        id = request.form['id'] #รับค่าไอดีมา จากหน้าupdateจะได้รู้ว่าจะแก้ไขแถวไหน

        Start_Date = request.form['Start_Date']
        Finish_Date = "null"
        
        if request.form['Finish_Date'] is not "" :
            Finish_Date = request.form['Finish_Date']
        
        Term = request.form['Term']
        Year = request.form['Year']
        print("id:",id,'Start_Date: ',Start_Date,'Finish_Date: ',Finish_Date,'Term: ',Term,'Year',Year)
        cur.execute("UPDATE calendar SET  Term="+Term+",Start_Date= '"+Start_Date+"', Finish_Date= '"+Finish_Date+"', Year= '"+Year+"' WHERE id= "+id+" " )
        print("UPDATE calendar SET  Term="+Term+",Start_Date="+Start_Date+", Finish_Date="+Finish_Date+", Year= '"+Year+"' WHERE id= "+id+" " )
        # print(cur)
        mysql.connection.commit()
    return redirect(url_for('calendar'))
# ---------------------------ปฏิทินการศึกษา----------------------------------------------------



# -------------------คำนวณเกรด---------------------------------------------------------------
@app.route("/")
def index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM gpa')
    rows=cur.fetchall()
    

    return render_template("index.html",datas=rows) #นำ datas ไปแสดงผลที่หน้า html

@app.route("/calculate",methods=['POST','GET']) #รับค่ามาจาก form index.html
def calculate():

    if request.method == 'POST':
        Rows_id = request.form.getlist("Rows_id[]")
        Subject_ID = request.form.getlist("Subject_ID[]")
        Name_TH = request.form.getlist("Name_TH[]") #รับค่าเป็น list จากform index.html
        Unit = request.form.getlist("Unit[]")
        Grade = request.form.getlist("Grade[]")
     # ---------------------- start  ส่งค่าแล้วprintออกมาเป็นjson -------------------------
    headers = ('Rows_id','Subject_ID','Name_TH', 'Unit', 'Grade')
    values = (
        request.form.getlist("Rows_id[]"),
        request.form.getlist('Subject_ID[]'), 
        request.form.getlist("Name_TH[]") ,
        request.form.getlist('Unit[]'),  
        request.form.getlist('Grade[]'),         
    )
    items = [{} for i in range(len(values[0]))]
    for x,i in enumerate(values):  #enumerate เป็นคำสั่งสำหรับแจกแจงค่า index และข้อมูลใน index ในรูปแบบทูเพิล (Tuple) ดังนี้ (Index,Value) โดยต้องใช้กับข้อมูลชนิด list
        for _x,_i in enumerate(i): 
            items[_x][headers[x]] = _i
    result = jsonify(items)
    print("---------------------------------------------------")
    print(result)
    print(items)
    
    # rows = json.dumps(items)
    rows=items
    print(rows)
    print("---------------------------------------------------")
    # -------------------- stop  ส่งค่าแล้วprintออกมาเป็นjson-----------------------

#     rows = [
#   {
#     "Grade": "3.0", 
#     "Name_TH": "\u0e01\u0e32\u0e23\u0e40\u0e02\u0e35\u0e22\u0e19\u0e42\u0e1b\u0e23\u0e41\u0e01\u0e23\u0e21\u0e40\u0e0a\u0e34\u0e07\u0e42\u0e04\u0e23\u0e07\u0e2a\u0e23\u0e49\u0e32\u0e07", 
#     "Rows_id": "1", 
#     "Subject": "0", 
#     "Unit": "3"
#   }, 
#   {
#     "Grade": "2.0", 
#     "Name_TH": "\u0e2a\u0e16\u0e32\u0e1b\u0e31\u0e15\u0e22\u0e01\u0e23\u0e23\u0e21\u0e04\u0e2d\u0e21\u0e1e\u0e34\u0e27\u0e40\u0e15\u0e2d\u0e23\u0e4c", 
#     "Rows_id": "2", 
#     "Subject": "225434", 
#     "Unit": "4"
#   }, 
#   {
#     "Grade": "1.0", 
#     "Name_TH": "\u0e15\u0e23\u0e23\u0e01\u0e30\u0e1e\u0e37\u0e49\u0e19\u0e10\u0e32\u0e19\u0e41\u0e25\u0e30\u0e01\u0e32\u0e23\u0e41\u0e01\u0e49\u0e1b\u0e31\u0e0d\u0e2b\u0e32", 
#     "Rows_id": "3", 
#     "Subject": "225101", 
#     "Unit": "5"
#   }, 
#   {
#     "Grade": "0.0", 
#     "Name_TH": "\u0e04\u0e13\u0e34\u0e15\u0e28\u0e32\u0e2a\u0e15\u0e23\u0e4c\u0e40\u0e15\u0e47\u0e21\u0e2b\u0e19\u0e48\u0e27\u0e22", 
#     "Rows_id": "4", 
#     "Subject": "241334", 
#     "Unit": "2"
#   }
# ]


    

   

    print("***********************************************************************")
    print('วิชา:',Subject_ID)
    print('หน่วยกิต:',Unit)
    print('เกรด:',Grade)
    print("***********************************************************************")
    
    #------------------------- start เช็ค W ---------------------------
    for i in range(len(Grade)): #วนลูปเช็คว่ามี W ไหม
        # print(Grade[i])
        if Grade[i] == '-1.0':
            Grade[i] = 0
            for x in range(len(Unit)): #วนหาหน่วยกิตที่ติด W
                if x == i:
                    Unit[x] = 0 #เปลี่ยนหน่วตกิตวิชาที่ติด W ให้มีค่าเป็น 0
                    
        else :
             print(Grade[i]) #เกรดที่นำมาคิด
    print("***********************************************************************")
    print('วิชา:',Subject_ID)
    print('หน่วยกิต:',Unit)
    print('เกรด:',Grade)
    print("***********************************************************************")
    #------------------------- stop เช็ค W ----------------------------
   
    #------------------------- start หาค่าผลรวมของหน่วยกิต ---------------------------
    sum =0
    for x in range(len(Unit)):
        #print(float(Unit[x])) #หน่วยกิตแต่ละตัว อ้างจาก x คือ index
        sum = sum + (float(Unit[x]))
    print('ผลรวมหน่วยกิต =',sum)
    #--------------------------- Stop หาค่าผลรวมของหน่วยกิต -------------------------
    
    # print("***********************************************************************")
    total =0 
    for x in range(len(Unit)):
        for i in range(len(Grade)):
            if i == x: #ถ้า index ของ Unit และ Grade เท่ากัน ให้นำมาคำนวณ
                sum1 = (float(Unit[x])* float(Grade[i])) # หน่วยกิต คูณ เกรด
                # print(sum1)
                total = total+sum1 # เช่น (3*4.0)+(3*3.5)
    print('ผลรวม หน่วยกิต*เกรด =',total)
    # print("***********************************************************************")
    GPA = total / sum
    GPA = '%.2f'%(GPA) # ตัดทศนิยมให้เหลือ 2 ตำแหน่ง เช่น 2.9642857142857144 เป็น 2.96
    print(GPA)
    print(Grade)
    for i in Grade:
        print(i)
        # if i == '4.0':
        #     print ('A')
        # if i == '3.5':
        #     print ('B+')
        # if i == '3.0':
        #     print ('B')
        # if i == '2.5':
        #     print ('C+')
        # if i == '2.0':
        #     print ('C')
        # if i == '1.5':
        #     print('D+')
        # if i == '1.0':
        #     print('D')
        # if i == '0.0':
        #     print('F')

    return render_template("calculate.html",datas=rows,item=GPA,Grade=Grade)
    # return redirect(url_for('index',item=GPA,Grade=Grade))
    # return render_template("index.html",datas=rows)
    
    
if __name__== "__main__" :
    app.run(debug=True)