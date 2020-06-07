from flask import Flask, render_template, redirect, request, url_for, session,flash, jsonify
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

@app.route("/login")
def login():
    return render_template('login.html')

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
    cur.execute("SELECT Start_Date,Finish_Date FROM calendar WHERE Topic_ID = '"+topic+"' AND Term = '"+term+"'")
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
        # Topicid = request.form.get('Topic')
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
# @app.route("/showform")
# def showform():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM topic")
#     rows=cur.fetchall()
#     return render_template('addcalendar.html',datas = rows)
# @app.route("/update", methods=['POST','GET'])
# def update():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM topic")
#     rows=cur.fetchall()
#     if request.method == 'POST': #เช็คว่าส่งmethod POST มาหรือไม่ ถ้าใช่ให้ทำในเงื่อนไข
#         id = request.form['id'] #รับค่าไอดีมา จากหน้าupdateจะได้รู้ว่าจะแก้ไขแถวไหน
#         Topic_ID = request.form['Topic_ID']
#         # Topicid = request.form.get('Topic')
#         Start_Date = request.form['Start_Date']
#         Finish_Date = request.form['Finish_Date']
#         Term = request.form['Term']
#         Year = request.form['Year']
#         print("id"+id,'Topic_ID'+Topic_ID,'Start_Date'+ Start_Date,Finish_Date,Term,Year)
#         cur.execute("UPDATE calendar SET Topic_ID=%s, Term=%s, Start_Date=%s, Finish_Date=%s, Year=%s WHERE id='"+id+"' " ,(Topic_ID,Term,Start_Date,Finish_Date,Year,id) )
        
#         mysql.connection.commit()
#     return redirect(url_for('calendar'))
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
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM gpa')
    rows=cur.fetchall()
    # for row in rows :
    #     print(row)
 
    Subject = request.form.getlist("Subject[]") #รับค่าเป็น list จากform index.html
    Unit = request.form.getlist("Unit[]")
    Grade = request.form.getlist("Grade[]")

    # ---------------------- start  ส่งค่าแล้วprintออกมาเป็นjson -------------------------
    # headers = ('Subject', 'Unit', 'Grade')
    # values = (
    #     request.form.getlist('Subject[]'),  
    #     request.form.getlist('Unit[]'),  
    #     request.form.getlist('Grade[]'),         
    # )
    # items = [{} for i in range(len(values[0]))]
    # for x,i in enumerate(values):  #enumerate เป็นคำสั่งสำหรับแจกแจงค่า index และข้อมูลใน index ในรูปแบบทูเพิล (Tuple) ดังนี้ (Index,Value) โดยต้องใช้กับข้อมูลชนิด list
    #     for _x,_i in enumerate(i): 
    #         items[_x][headers[x]] = _i
    # return jsonify(items)
    # -------------------- stop  ส่งค่าแล้วprintออกมาเป็นjson-----------------------

    print("***********************************************************************")
    print('วิชา:',Subject)
    print('หน่วยกิต:',Unit)
    print('เกรด:',Grade)
    print("***********************************************************************")
    
    #------------------------- start เช็ค W ---------------------------
    for i in range(len(Grade)): #วนลูปเช็คว่ามี W ไหม
        # print(Grade[i])
        if Grade[i] == 'W':
            Grade[i] = 0
            for x in range(len(Unit)): #วนหาหน่วยกิตที่ติด W
                if x == i:
                    Unit[x] = 0 #เปลี่ยนหน่วตกิตวิชาที่ติด W ให้มีค่าเป็น 0
                    
        else :
             print(Grade[i]) #เกรดที่นำมาคิด

    print("***********************************************************************")
    print('วิชา:',Subject)
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
    
    return render_template("index.html",datas=rows,item=GPA,sum=sum)
    # return render_template("index.html",datas=rows)
    
    
if __name__== "__main__" :
    app.run(debug=True)