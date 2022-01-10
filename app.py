from flask import Flask, redirect, url_for, render_template, request,session, flash
from bs4 import BeautifulSoup
import requests
from flask_mysqldb import MySQL
from datetime import timedelta


app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "datafilm"

mysql= MySQL(app)



app.secret_key="enggar"
@app.route("/")
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_film")
    data = cur.fetchall()
    cur.close()
    return render_template("home.html", datafilm = data)

@app.route("/scraping", methods = ["POST", "GET"])
def scrap():
    if request.method == "POST":
        proses = request.form["pcr"]
        proses_scraping(proses)
        flash("data berhasil")
        return render_template("scraping.html")
    else :
        flash("data tidak berhasil")
        return render_template("scraping.html")
        
@app.route("/datafilm")
def data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_film")
    data = cur.fetchall()
    cur.close()
    return render_template("datafilm.html",datafilm = data)







def proses_scraping(url):
    res = requests.get(url)
    doc = BeautifulSoup(res.text, "html.parser")
#titile_film
    title_tag = doc.select('h1[itemprop="name"] span')
    title = title_tag[0].getText()
#cover_img film
    cover_tag = doc.find('img', 'T75of Nywl9c')
    cover = cover_tag['srcset'].replace(' 2x', '')

#sinopsis film
    sinopsis_tag = doc.select('div[class="JHTxhe IQ1z0d"]')
    sinopsis = sinopsis_tag[0].getText()

#genre film
    genre_tag = doc.select(' a[itemprop="genre"]')
    genre = genre_tag[0].getText()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO data_film (title,sinopsis,genre,img) VALUES (%s,%s,%s,%s)" , (title,sinopsis,genre,cover))
    mysql.connection.commit()
    cur.close()
    return "suscces"

       



if __name__ == "__main__":
    app.run(debug=True)
