from flask import Flask,redirect,url_for,render_template,session,request,flash,jsonify
import time,os,bcrypt
import mysql.connector

#create database
conn=mysql.connector.connect(host="127.0.0.1",user="root",password="")
database="groupchat"
#create database
try:
    cursor=conn.cursor()
    sql="CREATE DATABASE IF NOT EXISTS groupchat"
    cursor.execute(sql)
    conn.commit()
except Exception as e:
    pass
conn=mysql.connector.connect(host="127.0.0.1",user="root",password="",database=database)
def db_functions():
    #create table users
    sql1="""CREATE TABLE IF NOT EXISTS users(
        userid int NOT NULL AUTO_INCREMENT,
        name varchar(100) NOT NULL,
        phoneno varchar(20) NOT NULL,
        email varchar(60) NOT NULL,
        country varchar(30) NOT NULL,
        education varchar(100) NOT NULL,
        profession varchar(100) NOT NULL,
        username varchar(40) NOT NULL,
        password varchar(100) NOT NULL,
        profilepic varchar(50) NOT NULL,
        joindate date NOT NULL,
        PRIMARY KEY(userid),
        UNIQUE KEY(phoneno),
        UNIQUE KEY(email)
    )"""
    #create table add group
    sql2="""CREATE TABLE IF NOT EXISTS groups(
        groupid int NOT NULL AUTO_INCREMENT,
        groupname varchar(50) NOT NULL,
        groupdescription varchar(150) NOT NULL,
        groupicon varchar(100) NOT NULL,
        groupadminid int NOT NULL,
        datecreated date NOT NULL,
        PRIMARY KEY(groupid)
    )"""
    #create table membership
    sql3="""CREATE TABLE IF NOT EXISTS groupmembers(
        memberid int NOT NULL AUTO_INCREMENT,
        groupid int NOT NULL,
        userid int NOT NULL,
        joindate date NOT NULL,
        PRIMARY KEY(memberid),
        FOREIGN KEY(groupid) references groups(groupid),
        FOREIGN KEY(userid) references users(userid)
    )"""
    #table chats
    sql4="""CREATE TABLE IF NOT EXISTS chats(
        chatid int NOT NULL AUTO_INCREMENT,
        groupid int NOT NULL,
        userid int NOT NULL,
        chat varchar(600) NOT NULL,
        media varchar(60) NOT NULL,
        chattime time NOT NULL,
        chatdate date NOT NULL,
        PRIMARY KEY(chatid),
        FOREIGN KEY(groupid) references groups(groupid),
        FOREIGN KEY(userid) references users(userid)
    )"""
    try:
        cursor=conn.cursor()
        cursor.execute(sql1)
        conn.commit()
        cursor=conn.cursor()
        cursor.execute(sql2)
        conn.commit()
        cursor=conn.cursor()
        cursor.execute(sql3)
        conn.commit()
        cursor=conn.cursor()
        cursor.execute(sql4)
        conn.commit()
    except Exception as e:
        pass

db_functions()

app=Flask(__name__)
app.config['SECRET_KEY']="ericsoftwares"

app.config['UPLOAD_FOLDER']="/"
ALLOWED_EXTENSIONS={'png','jpg','gif','jpeg'}
def check_file(file):
    return "." in file and file.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
#today
today=time.strftime("%Y-%m-%d")
#defined
selectedid=""
groupchats=""
searchallgroups=""

@app.route("/",methods=['GET','POST'])
def func_index():
    global profile,username,phoneno
    try:
        if 'userid' in session:
            userid=session['userid']
            phoneno=session['phoneno']
            username=session['username']
            profile=session['profile']
            return render_template('index.html',userid=userid,phoneno=phoneno,username=username,profile=profile)
            #return render_template('index.html')
        else:
            return redirect(url_for('func_login'))
    except IOError:
        pass

@app.route("/home",methods=['GET','POST'])
def func_home():
    return redirect(url_for('func_index'))
@app.route("/login",methods=['GET','POST'])
def func_login():
    global username,phoneno,profile
    msg=""
    if request.method=="POST":
        u_email=request.form['email']
        u_password=request.form['password']
        if u_email=="" or u_password=="":
            msg="fill in every field !!"
        else:
            #check is the u_email exist in database
            try:
                cursor=conn.cursor()
                sql="SELECT userid,email,username,password,phoneno,profilepic FROM users WHERE email='%s'"%(u_email)
                cursor.execute(sql)
                results=cursor.fetchall()
                if results:
                    dbpass=results[0][3].encode('utf-8')
                    inppass=u_password.encode('utf-8')
                    if bcrypt.checkpw(inppass,dbpass)==True:
                        msg="Login Successful"
                        session['userid']=results[0][0]
                        session['phoneno']=results[0][4]
                        session['username']=results[0][2]
                        session['profile']=results[0][5]
                        msg=1
                        #return redirect(url_for('func_index'))
                    else:
                        msg="Password does not match !"
                else:
                    msg="Email does not exist. Please Register !"
            except Exception as e:
                msg=str(e)
        return jsonify({"message":msg})
    return render_template('login.html')

@app.route("/register",methods=['GET','POST'])
def func_register():
    msg=""
    if request.method=="POST":
        if request.form['name']=="":
            msg="Name is empty"
        elif request.form['phoneno']=="":
            msg="Phone No is empty"
        elif request.form['email']=="":
            msg="Email is empty"
        elif request.form['country']=="":
            msg="Country is empty"
        elif request.form['education']=="":
            msg="Education is empty"
        elif request.form['profession']=="":
            msg="Profession/Work is empty"
        elif request.form['username']=="":
            msg="Username is empty"
        elif request.form['password']=="":
            msg="Password is empty"
        elif request.form['confirmpassword']!=request.form['password']:
            msg="Password does not match !"
        else:
            password=request.form.get('password').encode('utf-8')
            hashed=bcrypt.hashpw(password,bcrypt.gensalt())
            #msg=hashed.decode('utf-8')
            #check for profile
            profilepic=request.files['profile']
            filename=profilepic.filename
            if filename=="":
                msg="Select Profile"
            elif check_file(filename)==False:
                msg="File Not allowed"
            else:
                try:
                    profilerename=f"{request.form['phoneno']}{time.strftime('%H%M%S')}.png"
                    profilepic.save("static/images/profiles/"+profilerename)
                    cursor=conn.cursor()
                    sql="INSERT INTO users(name,phoneno,email,country,education,profession,username,password,profilepic,joindate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    values=(request.form['name'],request.form['phoneno'],request.form['email'],request.form['country'],request.form['education'],request.form['profession'],request.form['username'],hashed.decode('utf-8'),profilerename,today)
                    cursor.execute(sql,values)
                    conn.commit()
                    msg=1
                except Exception as e:
                    msg=str(e)
            
        return jsonify({"message":msg})
    return render_template('register.html')

@app.route("/logout",methods=['GET','POST'])
def func_logout():
    if 'userid' in session:
        session.pop('userid',None)
        session.pop('username',None)
        session.pop('password',None)
    return redirect(url_for('func_login'))

@app.route("/addgroup",methods=['GET','POST'])
def func_addgroup():
    if request.method=="POST":
        if request.form['groupname']=="":
            msg="Group Name is empty"
        elif request.form['groupinfo']=="":
            msg="Group Info is empty"
        else:
            #check group icons
            groupicon=request.files['groupicon']
            file=groupicon.filename
            if file=="":
                msg="Group Icon Not selected"
            elif check_file(file)==False:
                msg="File not allowed"
            else:
                #check is the user has another group
                try:
                    cursor=conn.cursor()
                    sql="SELECT * FROM groups WHERE groupadminid=%s"%(session['userid'])
                    cursor.execute(sql)
                    results=cursor.fetchall()
                    if results:
                        msg="You can create only one group"
                    else:
                        try:
                            groupprofilerename=f'Icon{session["userid"]}{time.strftime("%Y%m%d%H%M%S")}.png'
                            groupicon.save("static/images/groupicons/"+groupprofilerename)
                            cursor=conn.cursor()
                            sql="INSERT groups(groupname,groupdescription,groupicon,groupadminid,datecreated) VALUES('%s','%s','%s',%s,'%s')"
                            values=(request.form['groupname'],request.form['groupinfo'],groupprofilerename,session['userid'],today)
                            cursor.execute(sql%values)
                            conn.commit()
                            
                            msg=1
                        except Exception as e:
                            msg=str(e)
                except Exception as e:
                    msg=str(e)
        return jsonify({"message":msg})
    return render_template("addgroup.html")

@app.route("/viewallgroups")
def func_viewallgroups():
    #check my groups
    mygroups=""
    othergroups=""
    joinedgroups=""
    memberships=""
    groupchats=""
    try:
        cursor=conn.cursor()
        sql="SELECT * FROM groups WHERE groupadminid=%s"
        values=(session['userid'])
        cursor.execute(sql%values)
        results=cursor.fetchall()
        if results:
            mygroups=results
        else:
            pass
    except Exception as e:
        pass
    #check joined groups
    try:
        cursor=conn.cursor()
        sql="SELECT groups.groupid,groups.groupname,groups.groupdescription,groups.groupicon FROM groups INNER JOIN groupmembers ON groups.groupid=groupmembers.groupid WHERE groupmembers.userid=%s"%(session['userid'])
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            joinedgroups=results
    except Exception as e:
        pass
    #check other groups
    try:
        cursor=conn.cursor()
        sql="SELECT DISTINCT * FROM groups"#WHERE NOT groupadminid=%s"%(session['userid'])
        #sql="SELECT DISTINCT groups.groupid,groups.groupname,groups.groupdescription,groups.groupicon,groupmembers.groupid,groupmembers.userid,groups.groupadminid FROM groups INNER JOIN groupmembers ON groups.groupid=groupmembers.groupid WHERE groupmembers.userid!=%s"%(session['userid'])
        #sql="SELECT groups.groupid,groups.groupname,groups.groupdescription,groups.groupicon FROM groups LEFT JOIN groupmembers ON groups.groupid = groupmembers.groupid WHERE NOT groups.groupadminid=%s"%(session['userid'])
        #values=(session['userid'])
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            othergroups=results
        else:
            pass
    except IOError as e:
        pass
   
    return render_template('allgroups.html',mygroups=mygroups,joinedgroups=joinedgroups,othergroups=othergroups)

@app.route("/joingroup",methods=['GET','POST'])
def func_joingroup():
    global selectedid
    if request.method=="POST":
        groupid=request.form['groupid']
        selectedid=groupid
        try:
            cursor=conn.cursor()
            sql="INSERT INTO groupmembers(groupid,userid,joindate) VALUES('%s','%s','%s')"
            values=(groupid,session['userid'],today)
            cursor.execute(sql%values)
            conn.commit()
            msg=1
        except Exception as e:
            conn.rollback()
            msg=str(e)
        return jsonify({"message":msg})

@app.route("/viewgroupmembers",methods=['GET','POST'])
def func_viewgroupmembers():
    global selectedid,groupchats
    msg=""
    groupmembers=""
    groupadmin=""
    totalmembers=1
    
    
    try:
        if request.method=="POST":
            groupid=request.form['groupid']
            selectedid=groupid
            
        
        #get groupmembers
        cursor=conn.cursor()
        sql="SELECT groupmembers.groupid,groupmembers.userid,users.name,users.phoneno,users.profilepic FROM groupmembers INNER JOIN users ON groupmembers.userid=users.userid WHERE groupmembers.groupid=%s"%(selectedid)
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            groupmembers=results
        
        #get groupadmin
        cursor=conn.cursor()
        sql1="SELECT groups.groupid,groups.groupadminid,users.name,users.phoneno,users.profilepic FROM groups INNER JOIN users ON groups.groupadminid=users.userid WHERE groups.groupid=%s"%(selectedid)
        cursor.execute(sql1)
        results1=cursor.fetchall()
        if results1:
            groupadmin=results1
        
        try:
            cursor=conn.cursor()
            sql1="SELECT COUNT(groupid) FROM groupmembers WHERE groupid=%s"%(selectedid)
            cursor.execute(sql1)
            results1=cursor.fetchall()
            if results1:
                totalmembers=results1[0][0]+1
        except:
            pass
        
        #get groupchats
        try:
            cursor=conn.cursor()
            sql="SELECT chats.chatid,chats.groupid,chats.userid,chats.chat,chats.media,chats.chattime,chats.chatdate,users.userid,users.name,users.phoneno FROM chats INNER JOIN users ON chats.userid=users.userid WHERE chats.groupid=%s"%(selectedid)
            #sql="SELECT * FROM chats"
            cursor.execute(sql)
            results=cursor.fetchall()
            if results:
                groupchats=results
            else:
                groupchats=""
                
        except Exception as e:
            pass

        return render_template('viewgroupmembers.html',groupadmin=groupadmin,groupmembers=groupmembers,totalmembers=totalmembers,groupchats=groupchats)
    except IOError:
        pass
#get group chats area cahts total members
@app.route("/chatarea",methods=['GET','POST'])
def func_chatarea():
    global groupchats,selectedid
    return render_template('chatarea.html',groupchats=groupchats,groupchid=selectedid)
#submit messages
@app.route("/sendmessage",methods=['GET','POST'])
def func_sendmessage():
    global groupchats,selectedid
    if request.method=="POST":
        chatgrpid=request.form['chatgroupid']
        selectedid=chatgrpid
        chatmsg=request.form['groupchatmessage']
        if chatgrpid=="" or chatmsg=="":
            msg="message is empty"
        else:
             #check group media
            chatfile=request.files['groupchatfile']
            file=chatfile.filename
            if file=="":
                groupmediafile=""
            else:
                groupmediafile=f'{chatgrpid}{session["userid"]}{time.strftime("%Y%m%d%H%M%S")}{file}'
            try:
                cursor=conn.cursor()
                sql="INSERT chats(groupid,userid,chat,media,chattime,chatdate) VALUES(%s,%s,'%s','%s','%s','%s')"
                values=(chatgrpid,session['userid'],chatmsg,groupmediafile,str(time.strftime("%H:%M:%S")),today)
                cursor.execute(sql%values)
                conn.commit()
                if file=="":
                    pass
                else:
                    chatfile.save("static/media/"+groupmediafile)
                msg=1
            except Exception as e:
                    msg=str(e)
    return jsonify({"message":msg})
    #get groupchats
    '''try:
        cursor=conn.cursor()
        sql="SELECT chats.chatid,chats.groupid,chats.userid,chats.chat,chats.media,chats.chattime,chats.chatdate,users.userid,users.name,users.phoneno FROM chats INNER JOIN users ON chats.userid=users.userid WHERE chats.groupid=%s"%(selectedid)
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            groupchats=results
    except Exception as e:
        pass
    return render_template('chatarea.html',groupchats=groupchats,groupchid=selectedid)'''

@app.route("/viewmember",methods=['GET','POST'])
def func_viewmember():
    if request.method=="POST":
        memberid=request.form['userid']
        try:
            cursor=conn.cursor()
            sql="SELECT name,phoneno,email,profilepic FROM users WHERE userid=%s"%(memberid)
            cursor.execute(sql)
            results=cursor.fetchone()
            if results:
                memberdetails=results
            else:
                memberdetails=""
        except:
            pass
    return jsonify({"memberdetails":memberdetails})

@app.route("/searchgroup",methods=['GET','POST'])
def func_searchgroup():
    global searchallgroups
    if request.method=="POST":
        searchname=request.form['searchname']
        try:
            cursor=conn.cursor()
            sql="SELECT * FROM groups WHERE groupname LIKE'%"+searchname+"%'"
            cursor.execute(sql)
            results=cursor.fetchall()
            if results:
                searchallgroups=results
            else:
                searchallgroups=""
        except IOError:
            searchallgroups=""
        return jsonify({"got":"got"})
    
    
@app.route("/displaysearchedgroups",methods=['GET','POST'])
def func_displaysearchedgroups():
    global searchallgroups
    return render_template('searchedgroup.html',searchallgroups=searchallgroups)

@app.route("/displayallgroups",methods=['GET','POST'])
def func_displayall():
    global searchallgroups
    try:
        cursor=conn.cursor()
        sql="SELECT * FROM groups"
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            searchallgroups=results
        else:
            searchallgroups=""
    except IOError:
        pass
    return jsonify({"got":"got"})

@app.route("/checkgroup",methods=['GET','POST'])
def func_checkgroup():
    if request.method=="POST":
        groupid=request.form['groupid']
        userid=session['userid']
        #check if im the group admin
        try:
            cursor=conn.cursor()
            sql="SELECT * FROM groups WHERE groupadminid=%s AND groupid=%s"%(groupid,userid)
            cursor.execute(sql)
            results=cursor.fetchall()
            if results:
                msg=1
            else:
                #check if you are a member
                try:
                    cursor=conn.cursor()
                    sql1="SELECT * FROM groupmembers WHERE groupid=%s AND userid=%s"%(groupid,session['userid'])
                    cursor.execute(sql1)
                    results1=cursor.fetchall()
                    if results1:
                        msg=2
                    else:
                        msg=3
                except Exception as e:
                    msg=str(e)
        except IOError as e:
            msg=str(e)
    return jsonify({"msg":msg})
@app.route("/displaychats",methods=['GET','POST'])
def func_displaychats():
    global selectedid
    #get groupchats
    try:
        cursor=conn.cursor()
        sql="SELECT chats.chatid,chats.groupid,chats.userid,chats.chat,chats.media,chats.chattime,chats.chatdate,users.userid,users.name,users.phoneno FROM chats INNER JOIN users ON chats.userid=users.userid WHERE chats.groupid=%s ORDER BY chats.chatid ASC"%(selectedid)
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            groupchats=results
    except Exception as e:
        pass
    return render_template('chatarea.html',groupchats=groupchats,groupchid=selectedid)

#check my bio
@app.route("/displaymybio",methods=['GET','POST'])
def func_displaymybio():
    try:
        cursor=conn.cursor()
        sql="SELECT * FROM users WHERE userid=%s"%(session['userid'])
        cursor.execute(sql)
        results=cursor.fetchall()
        if results:
            ret=results
            msg=1
        else:
            ret=""
            msg=2
    except Exception as e:
        ret=str(e)
        msg=2
    
    return jsonify({"ret":ret,"msg":msg})
if __name__=="__maim__":
    app.run(debug=True)