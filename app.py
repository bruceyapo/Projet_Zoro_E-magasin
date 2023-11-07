from flask import Flask, render_template, request,  redirect, url_for
#import pyodbc  as odbccon

app = Flask(__name__)

# conn = odbccon.connect("Driver={ODBC Driver 17 for SQL Server};"
#                       "Server=DESKTOP-QQGKONI\SQLEXPRESS;"
#                       "Database=e_magasin;"
#                       "Trusted_Connection=yes;")

# cursor = conn.cursor()

@app.route("/")
def Connexion():
    return render_template("Authentification/connexion.html")

@app.route("/Accueil/")
def index():
    return render_template("Partials/Base.html")
# Magasin
@app.route("/Magasin/")
def Magasin():
    return render_template("Magasin/Magasin.html")



if __name__ == "__main__":
    app.run(debug=True)