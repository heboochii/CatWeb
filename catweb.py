from flask import Flask, render_template, request, session, redirect
import sqlite3 as s
from bs4 import BeautifulSoup
import requests


DATABASE = 'main1'
app = Flask(__name__, static_url_path="", static_folder="static")
db = s.connect(DATABASE, check_same_thread=False)


@app.route('/guestbook')
def guest():
    connection = s.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM guestbook")
    rv = cursor.fetchall()
    cursor.close()
    return render_template("guestbook.html", rv=rv)


@app.route('/guestinsert', methods={'POST','GET'})
def guestinsert():
    if request.method == "POST":
        _insert1(request.form['name'], request.form['email'], request.form['comment'])
        return render_template('guestinsert.html', msg="Thank you for your feedback")

    else:
        return render_template('guestinsert.html')

def _insert1(name, email, comment):
    params = {'name': name, 'email': email, 'comment': comment}
    cursor = db.cursor()
    cursor.execute("INSERT INTO guestbook(name,email,comment) values (:name,:email,:comment)", params)
    db.commit()
    cursor.close()


@app.route("/", methods={'POST', 'GET'})
def home():
    connection = s.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM catbreeds")
    rv = cursor.fetchall()
    cursor.close()
    return render_template("main.html", breeds=rv)


@app.route("/breeds", methods={'POST', 'GET'})
def breeds():
    connection = s.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM catbreeds")
    rv = cursor.fetchall()
    cursor.close()
    return render_template("breeds.html", breeds=rv)


@app.route("/breedinfo", methods={'POST', 'GET'})
def breedinfo():
    connection = s.connect(DATABASE)
    cursor = connection.cursor()
    breed_id = request.args.get("id")
    cursor.execute("select * from catbreeds where breed_id='" + str(breed_id) + "'")
    rv = cursor.fetchall()
    cursor.close()
    return render_template("breedinfo.html", breed=rv)


# @app.route("/beautiful", methods={'POST', 'GET'})
# def beautiful():
#     page = requests.get("https://dubai.dubizzle.com/classified/pets/pets-for-free-adoption/cats/")
#     soup = BeautifulSoup(page.content, "html.parser")
#     pic = soup.find('div', attrs={"class": "thumb"})
#     img1 = pic.find('a')
#     img = img1.find('div')
#     img2 = img.get('style')
#     print(img2)
#     return render_template("beautiful.html", img2=img2)


@app.route("/articles", methods={'POST', 'GET'})
def articles():
    page1 = requests.get("https://www.catster.com/cat-behavior/cat-behavior-problems-and-how-to-handle-them")
    soup1 = BeautifulSoup(page1.content, "html.parser")
    title1 = soup1.find(class_="dmg-words")
    h1 = soup1.find("h1").text
    print(h1)
    image1 = soup1.find(id="attachment_371264")
    i = image1.find("img")
    i = i["src"]
    print(i)
    heads1 = title1.find_all("h3")
    for head in heads1:
        s = head.text
        p = head.find_next_sibling().text
        print(s)
        print(p)
        print("\n")



        cursor = db.cursor()
        cursor.execute("SELECT * FROM ARTICLES WHERE article_image='" + str(i) + "';")
        rv = cursor.fetchall()
        if len(rv)==0:
            paramsD = {'article_title': h1, 'article_h3': s, 'article_p': p, 'article_image': i}
            cursor.execute("INSERT INTO ARTICLES (article_title, article_h3, article_p, article_image) VALUES (:article_title, :article_h3, :article_p, :article_image)", paramsD)
            db.commit()

    cursor.execute("SELECT * FROM articles;")
    rv = cursor.fetchall()
    cursor.close()
    print(rv)
    return render_template("articles.html", rv=rv)


@app.route("/adoption", methods={'POST', 'GET'})
def adoption():
    try:
        page1 = requests.get("https://www.petsmartcharities.ca/find-a-pet-results?city_or_zip=toronto%2C%20on&species=cat&geo_range=250&breed_id=&hair&age=&sex&color_id")
        soup1 = BeautifulSoup(page1.content, "html.parser")
        pic = soup1.find('div', class_="pet-result")
        pic2 = pic.find('img')
        img = pic2.get('src')
        print(img)
        name1 = soup1.find('div', attrs={"class": "pet-name"})
        name1 = name1.text
        breed1 = soup1.find('div', attrs={"class": "pet-breed"})
        breed1 = breed1.text
        location1 = soup1.find('span', attrs={"class": "pet-addr-city-state clearfix"})
        location1 = location1.text
        # brd1 is brief_description1
        brd1 = soup1.find('div', attrs={"class": "age-sex-size"})
        brd1 = brd1.text


        paramsA = {'adoption_img': img, 'adoption_name' : name1, 'adoption_breed' : breed1, 'adoption_location' : location1, 'adoption_brd' : brd1}
        print(paramsA.items())
        cursor = db.cursor()
        cursor.execute("INSERT INTO ADOPTION (adoption_img, adoption_name, adoption_breed, adoption_location, adoption_brd) VALUES (:adoption_img, :adoption_name, :adoption_breed, :adoption_location, :adoption_brd)",paramsA)
        db.commit()
        cursor.close()
        return render_template("adoption.html", img=img, name1=name1, breed1=breed1, location1=location1, brd1=brd1)
    except:
        return render_template("adoption.html")


@app.route("/pictures", methods={'POST', 'GET'})
def pictures():
    connection = s.connect(DATABASE)
    cursor = connection.cursor()
    query = "SELECT * FROM pictures"
    cursor.execute(query)
    rv = cursor.fetchall()
    cursor.close()
    return render_template("pictures.html", pictures=rv)


@app.route('/facts', methods={'POST', 'GET'})
def facts():
    connection = s.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM facts")
    rv = cursor.fetchall()
    cursor.close()
    return render_template("facts.html", facts=rv)


@app.route('/signup', methods={'POST', 'GET'})
def signup():
    if request.method == "POST":
        _insert(request.form['sign_username'], request.form['sign_password'], request.form['sign_email'])
        return render_template('signup.html', msg="Thank you for signing up with us")
    else:
        return render_template('signup.html')


def _insert(username, password, email):
    print ("hello")
    params = {'username': username, 'password': password, 'email': email}
    print(params.items())
    cursor = db.cursor()
    cursor.execute("INSERT INTO USER (username,password,email) VALUES (:username,:password,:email)", params)
    db.commit()
    cursor.close()


@app.route('/login', methods={'POST', 'GET'})
def login():
    if (request.method == 'POST'):
        query = "SELECT * FROM USER WHERE username='" + request.form['username']
        query = query + "' and password='" + request.form['password']+"';"
        print(query)
        cur = db.execute(query)
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 1:
            session['username'] = request.form['username']
            session['password'] = rv[0][0]
            session['logged_in'] = True;
            return render_template('login.html')
        else:
            render_template('login.html', msg="username/password not found")
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in')
    session.pop('username')
    session.pop('password')
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = "meow"
    app.run(debug=True)
