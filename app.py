from flask import Flask, render_template, request,  redirect, url_for
import pyodbc  as odbccon

app = Flask(__name__)
conn = odbccon.connect("Driver={ODBC Driver 17 for SQL Server};" 
                       "Server=DESKTOP-QQGKONI\SQLEXPRESS;" 
                       "Database=Zoro_E_magasin;" 
                       "Trusted_Connection=yes")

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

@app.route("/Ajouter/")
def Ajouter():
    return render_template("Magasin/Ajouter_magasin.html")

@app.route("/Succes/")
def Succes():
    return render_template("Magasin/Succes_ajout_mag.html")

@app.route("/Modifier/")
def Modifier():
    return render_template("Magasin/Modifier_magasin.html")

@app.route("/Succes_modif/")
def Succes_modif():
    return render_template("Magasin/Succes_modif_mag.html")

@app.route("/Supprimer/")
def Supprimer():
    return render_template("Magasin/Supprimer_magasin.html")

@app.route("/Succes_supp/")
def Succes_supp():
    return render_template("Magasin/Succes_supp_mag.html")


##Produits

@app.route("/List_produit/")
def Produit():
    # Exécution de la requête de sélection
    cursor = conn.cursor()
    cursor.execute( "SELECT IdProduit, NomProduit, CatProduit, PrixUnitaire, Descriptions FROM Produit ")
    list = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()
    return render_template("Produit/Produit.html", list=list)

@app.route("/Ajout_produit/", methods=['GET'])
def Ajout_produit():
    return render_template("Produit/Ajout_produit.html")

@app.route("/Succes_ajout_produit/", methods=['POST'])
def Succes_ajout_produit():
    # cursor = conn.cursor()
    # Récupération des données du formulaire
    NomProduit = request.form["NomProduit"]
    CatProduit = request.form["CatProduit"]
    PrixUnitaire = request.form["PrixUnitaire"]
    Descriptions = request.form["Descriptions"]
    # Traitement des données
    list = {
        "NomProduit": NomProduit,
        "CatProduit": CatProduit,
        "PrixUnitaire": PrixUnitaire,
        "Descriptions": Descriptions
    }
    
    # Exécution de la requête d'insertion
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO Produit (NomProduit, CatProduit, PrixUnitaire,) VALUES (list['NomProduit'], list['CatProduit'], list['PrixUnitaire'])")
    
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO Produit (NomProduit, CatProduit, PrixUnitaire, Descriptions) VALUES ('{list['NomProduit']}', '{list['CatProduit']}', '{list['PrixUnitaire']}', '{list['Descriptions']}')"
    )

    # Commit des modifications
    conn.commit()

    cursor = conn.cursor()
    cursor.execute( "SELECT IdProduit, NomProduit, CatProduit, PrixUnitaire, Descriptions FROM Produit ")
    list = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()
    # return render_template("Produit/Succes_ajout_produit.html", list=list)
    return redirect(url_for('Produit', list=list))

@app.route("/Modifier_produit/<int:IdProduit>", methods=['GET', 'POST'])
def Modifier_produit(IdProduit):
    _id = int(IdProduit)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Produit WHERE IdProduit = ?", _id)
    list = cursor.fetchall() 
   
    conn.commit()  
    return render_template("Produit/Modifier_produit.html", list=list, _id=_id)

@app.route("/Succes_modif_prod/<int:IdProduit>", methods=['GET', 'POST'])
def Succes_modif_prod(IdProduit):
    _id = int(IdProduit)
    NomProduit = request.form["NomProduit"]
    CatProduit = request.form["CatProduit"]
    PrixUnitaire = request.form["PrixUnitaire"]
    Descriptions = request.form["Descriptions"]
    cursor = conn.cursor()
    cursor.execute( 
        "UPDATE Produit SET NomProduit =?, CatProduit =?, PrixUnitaire =?, Descriptions =? WHERE IdProduit=?",
        (NomProduit,CatProduit,PrixUnitaire, Descriptions, _id))
    conn.commit()
    # cursor.close()
    return redirect(url_for('Produit', _id=_id))

@app.route("/Supprimer_produit/<int:IdProduit>", methods=['GET', 'POST'])
def Supprimer_produit(IdProduit):
    _id = int(IdProduit)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Produit WHERE IdProduit = ?", _id)
    list = cursor.fetchall()
    conn.commit()
    return render_template("Produit/Supprimer_produit.html", list=list,  _id=_id)

@app.route("/Succes_supp_prod/<int:IdProduit>", methods=['GET', 'POST'])
def Succes_supp_prod(IdProduit):
    _id = int(IdProduit)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Produit WHERE IdProduit = ?", (_id,))
    conn.commit()
    return redirect(url_for('Produit', _id=_id))

    


if __name__ == "__main__":
    app.run(debug=True)