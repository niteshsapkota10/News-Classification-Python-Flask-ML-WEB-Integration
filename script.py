from flask import *
import sqlite3
import numpy as np
import pickle
import os
import fakeorreal
import itertools
from env import secret_key

file1 = open("multinomial.pickle", "rb")
mnb = pickle.load(file1)
file1.close()
file2 = open("count_vect.pickle", "rb")
count_vect = pickle.load(file2)
file2.close()
file3 = open("tranformer.pickle", "rb")
trans = pickle.load(file3)
file3.close()
file4 = open("transformercategories.pickle", "rb")
transformer = pickle.load(file4)
file4.close()
file5 = open("logclassify.pickle", "rb")
logreg = pickle.load(file5)
file5.close()

filerepkn = open("knreport.pickle", "rb")
repknn = pickle.load(filerepkn)
filerepkn.close()


app = Flask(__name__)
app.secret_key = secret_key

app.config["IMAGE_UPLOADS"] = "static/profilepics"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["image_posts"] = "static/image_POST"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/newsclassify')
def form():
    return render_template('form.html')


@app.route('/signup.html')
def signup():
    return render_template("signup.html")


@app.route('/data', methods=['POST'])
def data():
    error = None
    fullname = request.form['full_name']
    email = request.form['email']
    phno = request.form['ph_no']
    password = request.form['password']
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users2")
    row = cur.fetchall()
    for i in row:
        if i['email'] == email:
            error = "Email Already Exists"
            return render_template("signup.html", error=error)
    cur = con.cursor()
    cur.execute("INSERT into users2(fullname,email,phonenumber,password,profilepic) values (?,?,?,?,?)",
                (fullname, email, phno, password, "default.jpg"))
    con.commit()
    cur = con.cursor()
    cur.execute("select * from posts3 ORDER BY post_id DESC")
    rows = cur.fetchall()
    con.close()
    return render_template("user.html", name=fullname, rows=rows)


@app.route('/user.html')
def user():
    nm = session['name']
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from posts3 ORDER BY post_id DESC")
    con.commit()
    rows = cur.fetchall()
    con.close()
    return render_template("user.html", name=nm, rows=rows)


@app.route('/loin', methods=['POST'])
def loin():
    email = request.form['email']
    password = request.form['password']
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from users2")
    row = cur.fetchall()
    for i in row:
        if i['email'] == email and i['password'] == password:
            nm = i['fullname']
            ids = i['id']
            pic = i['profilepic']
            session['pic'] = pic
            session['id'] = ids
            session['name'] = nm
            rw = cur.fetchall()
            con = sqlite3.connect("users.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from posts3 ORDER BY post_id DESC")
            rows = cur.fetchall()
            con.close()
            con = sqlite3.connect("users.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM users2 WHERE id = (SELECT id FROM posts3 ORDER BY post_id DESC);")
            row2 = cur.fetchall()
            con.close()
            return render_template("user.html", name=nm, rows=rows, row2=row2)
        else:
            error = "Invalid Email or Password"
            return render_template("login.html", error=error)

    return render_template("user.html", name=email)


@app.route('/login.html')
def login():
    return render_template("login.html")


@app.route('/form.html')
def check():
    return render_template("form.html")


@app.route('/process', methods=['POST'])
def process():
    id = session['id']
    nm = session['name']
    cat = (['alt.atheism',
            'comp.graphics',
            'comp.os.ms-windows.misc',
            'comp.sys.ibm.pc.hardware',
            'comp.sys.mac.hardware',
            'comp.windows.x',
            'misc.forsale',
            'rec.autos',
            'rec.motorcycles',
            'rec.sport.baseball',
            'rec.sport.hockey',
            'sci.crypt',
            'sci.electronics',
            'sci.med',
            'sci.space',
            'soc.religion.christian',
            'talk.politics.guns',
            'talk.politics.mideast',
            'talk.politics.misc',
            'talk.religion.misc'])

    title = request.form['title']
    # pic=request.files['pic']
    # author=request.form['author']
    news = request.form['news']
    total = title+' '+nm+' '+news
    total_count = count_vect.transform([total])
    total_data = trans.fit_transform(total_count)
    u_pred = mnb.predict(total_data)
    transformed_news = transformer.transform([total])
    if u_pred[0] == 0:
        clpr = logreg.predict(transformed_news)
        cat = cat[clpr[0]]
        mypred = "real "+cat
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        cur.execute("INSERT into posts3(id,title,author,news,category) values (?,?,?,?,?)",
                    (id, title, nm, news, cat))
        con.commit()
        con.close()
    else:
        mypred = "fake"
    if title and news:
        return jsonify({'name': mypred})
    return jsonify({'error': 'Missing Data !'})


@app.route('/logout')
def logout():
    session.pop('id')
    return render_template('index.html')


@app.route('/profile.html')
def profile():
    pic = session['pic']
    id = session['id']
    nm = session['name']
    con = sqlite3.connect("users.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(
        "SELECT title,author,category,news,post_id FROM posts3 WHERE author=? ORDER BY post_id DESC", (nm,))
    con.commit()
    row = cur.fetchall()
    # for i in row:
    #   if i['id']==id:
    #      row2=i
    return render_template('profile.html', name=nm, rows=row, pic=pic)


@app.route('/advs.html')
def advancesettings():
    return render_template('advs.html', mnbscore=fakeorreal.mnbscore(), clfmnb=fakeorreal.clfrepmnb(), cnfmatmnb=fakeorreal.cnfmatmnb(), svmscore=fakeorreal.svmscore(), clfsvm=fakeorreal.clfrepsvm(), cnfmatsvm=fakeorreal.cnfmatsvm())


@app.route('/algoprocess', methods=['POST'])
def algoprocess():
    mnb2 = fakeorreal.model()
    svm2 = fakeorreal.model2()
    algo = request.form['algo']
    email = request.form['email']
    name = request.form['name']
    if name and email:
        if algo == 'mnb':
            total = email+' '+name
            total_count = count_vect.transform([total])
            total_data = trans.fit_transform(total_count)
            u_pred = mnb2.predict(total_data)
            if u_pred[0] == 0:
                rep = "Real"
            else:
                rep = "Fake"
            return jsonify({'name': rep})
        elif algo == 'svm':
            total = email+' '+name
            total_count = count_vect.transform([total])
            total_data = trans.fit_transform(total_count)
            u_pred = svm2.predict(total_data)
            if u_pred[0] == 0:
                rep = "Real"
            else:
                rep = "Fake"
            return jsonify({'name': rep})
    return jsonify({'error': 'Missing Data!'})


@app.route('/deletepost', methods=['POST'])
def deletepost():
    if request.method == 'POST':
        pid = request.form['pid']
        con = sqlite3.connect("users.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("delete from posts3 where post_id=?", (pid,))
        con.commit()
        id = session['id']
        nm = session['name']
        con = sqlite3.connect("users.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(
            "SELECT title,author,category,news,post_id FROM posts3 WHERE author=? ORDER BY post_id DESC", (nm,))
        con.commit()
        row = cur.fetchall()
        # for i in row:
        #   if i['id']==id:
        #      row2=i
        return render_template('profile.html', name=nm, rows=row)


@app.route('/settings.html')
def settings():
    return render_template('settings.html')


@app.route('/pswchange', methods=['POST'])
def pswchange():
    id = session['id']
    nm = session['name']
    if request.method == 'POST':
        crtpswd = request.form['curpswd']
        newpswd = request.form['password']
        con = sqlite3.connect("users.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT password FROM users2 WHERE id=?", (id,))
        con.commit()
        row = cur.fetchall()
        con.close()
        for i in row:
            if i['password'] == crtpswd:
                con = sqlite3.connect("users.db")
                cur = con.cursor()
                cur.execute(
                    "UPDATE users2 SET password=? WHERE id=?", (newpswd, id,))
                con.commit()
                con.close()
                msg = "Updated Successfully"
            else:
                msg = "Your Passwords doesnt match"
    return render_template('settings.html', error=msg)


@app.route('/uploadprofile', methods=['POST'])
def uploadprofile():
    id = session['id']
    nm = session['name']
    if request.method == 'POST':
        f = request.files['file']
        if allowed_image(f.filename):
            f.save(os.path.join(app.config["IMAGE_UPLOADS"], f.filename))
            con = sqlite3.connect("users.db")
            cur = con.cursor()
            cur.execute("UPDATE users2 SET profilepic=? WHERE id=?",
                        (f.filename, id,))
            con.commit()
            con.close()
            con = sqlite3.connect("users.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT title,author,category,news,post_id FROM posts3 WHERE author=? ORDER BY post_id DESC", (nm,))
            con.commit()
            row = cur.fetchall()
            return render_template('profile.html', name=nm, rows=row, pic=f.filename)
        else:
            name = "EXTENSION NOT ALLOWED."


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)
