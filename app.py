from flask import Flask, render_template, request,  redirect, url_for, flash,jsonify
from flask_bcrypt import Bcrypt
import pyodbc  as odbccon
app = Flask(__name__)

bcrypt = Bcrypt(app)

conn = odbccon.connect("Driver={ODBC Driver 17 for SQL Server};" 
                       "Server=DESKTOP-QQGKONI\SQLEXPRESS;" 
                       "Database=Zoro_E_magasin;" 
                       "Trusted_Connection=yes")
# Authentification
@app.route("/")
def Connexion():
    return render_template("Authentification/connexion.html")

@app.route("/Succes_Connexion/", methods=['POST'])
def Succes_Connexion():
    
    E_mail = request.form["E_mail"]
    Mot_de_passe = request.form["Mot_de_passe"]
    cursor = conn.cursor()
    cursor.execute(f"SELECT Id, E_mail, Mot_de_passe  FROM Utilisateurs WHERE E_mail = '{E_mail}'")
    utilisateur = cursor.fetchone()
    
    if utilisateur:
        # Vérification du mot de passe haché
        if bcrypt.check_password_hash(utilisateur[2], Mot_de_passe):
            # Authentification réussie
            flash(f"Succès! Bienvenue sur le site E-magazin ", 'success')
            print("succès admin")
            return redirect(url_for('DashbordAdmin'))
        elif utilisateur and bcrypt.check_password_hash(utilisateur[2], Mot_de_passe):
            
            flash(f"Succès! Bienvenue sur le site E-magazin ", 'success')
            print("succes user")
            return redirect(url_for('index'))
        else:


            # Mot de passe incorrect
            print(Mot_de_passe)
            print("Connexion echouée")
            flash('connexion échoué! Vous avez certainement entré un e-mail ou mot de passe incorrect', 'danger')
            return redirect(url_for('Connexion'))
    else:
        # Utilisateur non trouvé
        flash('Utilisateur non trouvé!', 'danger')
        return redirect(url_for('Connexion'))

@app.route("/inscription/", methods=['GET'])
def inscription():
    return render_template("Authentification/inscription.html")

@app.route("/InscriptionStandatUser/", methods=['GET'])
def InscriptionStandatUser():
    return render_template("Authentification/InscriptionStandatUser.html")

@app.route("/Succes_inscription/", methods=['POST', 'GET'])
def Succes_inscription():
    # Récupération des données du formulaire
    if request.method == 'POST':
        Nom = request.form["Nom"]
        Prenoms = request.form["Prenoms"]
        Ville = request.form["Ville"]
        E_mail = request.form["E_mail"]
        Mot_de_passe = 'request.form["Mot_de_passe"]'
        Roles = request.form["Roles"]
    # Hachage du mot de passe
    mot_de_passe_hache = bcrypt.generate_password_hash(Mot_de_passe).decode('utf-8')
    list = {
        "Nom": Nom,
        "Prenoms": Prenoms,
        "Ville": Ville,
        "E_mail": E_mail,
        "Mot_de_passe" : mot_de_passe_hache,
        "Roles" : Roles
    }
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO Utilisateurs (Nom, Prenoms, Ville, E_mail, Mot_de_passe, Roles) VALUES ('{Nom}', '{Prenoms}', '{Ville}', '{E_mail}', '{mot_de_passe_hache}', '{Roles}')"
    )

    # Commit des modifications
    conn.commit()
    flash('Inscription réussie! Connectez-vous maintenant.', 'success')
    return redirect(url_for('Connexion',list=list))

# Authentification
@app.route("/DashbordAdmin/")
def DashbordAdmin():
    # Exécution de la requête de sélection
    cursor = conn.cursor()
    cursor.execute( "SELECT Id, Nom, Prenoms, Ville, E_mail, Roles FROM Utilisateurs ")
    list = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()
    return render_template("Partials/DashbordAdmin.html", list=list)

@app.route("/Modif_user/<int:Id>", methods=['GET', 'POST'])
def Modif_user(Id):
    _id = int(Id)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Utilisateurs WHERE Id = ?", _id)
    list = cursor.fetchall() 
    conn.commit()  
    return render_template("Partials/Modif_user.html", list=list, _id=_id)

@app.route("/Succes_modif_user/<int:Id>", methods=['GET', 'POST'])
def Succes_modif_user(Id):
    _id = int(Id)
     # cursor = conn.cursor()
    # Récupération des données du formulaire
    Nom = request.form["Nom"]
    Prenoms = request.form["Prenoms"]
    Ville = request.form["Ville"]
    E_mail = request.form["E_mail"]
    Roles = request.form["Roles"]
    # Traitement des données
    cursor = conn.cursor()
    cursor.execute( 
        "UPDATE Utilisateurs SET Nom =?, Prenoms =?, Ville =?, E_mail =?, Roles =? WHERE Id=?",
        (Nom,Prenoms,Ville, E_mail, Roles, _id))
    conn.commit()
    # cursor.close()
    flash(f"Utilisateurs modifier avec succès!", 'warning')
    return redirect(url_for('DashbordAdmin', _id=_id))

@app.route("/Supp_user/<int:Id>", methods=['GET', 'POST'])
def Supp_user(Id):
    _id = int(Id)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Utilisateurs WHERE Id = ?", _id)
    list = cursor.fetchall() 
    conn.commit()  
    return render_template("Partials/Supp_user.html", list=list, _id=_id)

@app.route("/Succes_supp_user/<int:Id>", methods=['GET', 'POST'])
def Succes_supp_user(Id):
    _id = int(Id)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Utilisateurs WHERE Id = ?", (_id,))
    conn.commit()
    flash("Utilisateurs Supprimer avec succès!", 'danger')
    return redirect(url_for('DashbordAdmin', _id=_id))

@app.route("/Accueil/")
def index():
    return render_template("Partials/Base.html")
# Magasin
@app.route("/Magasin/")
def Magasin():
    # Exécution de la requête de sélection
    cursor = conn.cursor()
    cursor.execute( "SELECT IdMagasin, NomMagasin, AdresseMagasin, Telephone, Mail FROM Magasin ")
    list = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()
    return render_template("Magasin/Magasin.html", list=list)

@app.route("/Ajouter_magasin/", methods=['GET'])
def Ajouter_magasin():

    return render_template("Magasin/Ajouter_magasin.html")

@app.route("/Succes_ajout_mag/" , methods=['POST'])
def Succes_ajout_mag():

    # cursor = conn.cursor()
    # Récupération des données du formulaire
    NomMagasin = request.form["NomMagasin"]
    AdresseMagasin = request.form["AdresseMagasin"]
    Telephone = request.form["Telephone"]
    Mail = request.form["Mail"]
    # Traitement des données
    list = {
        "NomMagasin": NomMagasin,
        "AdresseMagasin": AdresseMagasin,
        "Telephone": Telephone,
        "Mail": Mail
    }
    # Exécution de la requête d'insertion
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO Magasin (NomMagasin, AdresseMagasin, Telephone, Mail) VALUES ('{list['NomMagasin']}', '{list['AdresseMagasin']}', '{list['Telephone']}', '{list['Mail']}')"
    )
    # Commit des modifications
    conn.commit()
    cursor = conn.cursor()
    cursor.execute( "SELECT IdMagasin, NomMagasin, AdresseMagasin, Telephone, Mail FROM Magasin ")
    list = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()
    flash(f"Magasin ajouter avec succès!", 'success')
    return redirect(url_for('Magasin', list=list))
    # return render_template("Magasin/Succes_ajout_mag.html")

@app.route("/Modifier_magasin/<int:IdMagasin>", methods=['GET', 'POST'])
def Modifier_magasin(IdMagasin):
    _id = int(IdMagasin)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Magasin WHERE IdMagasin = ?", _id)
    list = cursor.fetchall() 
    conn.commit()  
    return render_template("Magasin/Modifier_magasin.html", list=list, _id=_id)

@app.route("/Succes_modif_mag/<int:IdMagasin>", methods=['GET', 'POST'])
def Succes_modif_mag(IdMagasin):
    _id = int(IdMagasin)
     # cursor = conn.cursor()
    # Récupération des données du formulaire
    NomMagasin = request.form["NomMagasin"]
    AdresseMagasin = request.form["AdresseMagasin"]
    Telephone = request.form["Telephone"]
    Mail = request.form["Mail"]
    # Traitement des données
    cursor = conn.cursor()
    cursor.execute( 
        "UPDATE Magasin SET NomMagasin =?, AdresseMagasin =?, Telephone =?, Mail =? WHERE IdMagasin=?",
        (NomMagasin,AdresseMagasin,Telephone, Mail, _id))
    conn.commit()
    # cursor.close()
    flash(f"Magasin modifier avec succès!", 'warning')
    return redirect(url_for('Magasin', _id=_id))
    # return render_template("Magasin/Succes_modif_mag.html")

@app.route("/Supprimer_magasin/<int:IdMagasin>", methods=['GET', 'POST'])
def Supprimer_magasin(IdMagasin):
    _id = int(IdMagasin)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Magasin WHERE IdMagasin = ?", _id)
    list = cursor.fetchall() 
    conn.commit() 
    return render_template("Magasin/Supprimer_magasin.html", list=list, _id=_id)

@app.route("/Succes_supp_mag/<int:IdMagasin>", methods=['GET', 'POST'])
def Succes_supp_mag(IdMagasin):
    _id = int(IdMagasin)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Magasin WHERE IdMagasin = ?", (_id,))
    conn.commit()
    flash(f"Magasin Supprimer avec succès!", 'danger')
    return redirect(url_for('Magasin', _id=_id))
    # return render_template("Magasin/Succes_supp_mag.html")


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
    flash(f"Produit ajouter avec succès!", 'success')
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
    flash(f"Produit modifier avec succès!", 'warning')
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
    flash(f"Produit Supprimer avec succès!", 'danger')
    return redirect(url_for('Produit', _id=_id))
##Produits

# Stock 
@app.route("/Liste_tock/")
def Stock():
    # Exécution de la requête de sélection
    cursor = conn.cursor()
    cursor.execute("SELECT Idstock, NomMagasin,Mail, NomProduit,PrixUnitaire, Quantitestock FROM Stock S JOIN Produit P ON S.IdProduit=P.IdProduit JOIN Magasin M ON S.IdMagasin=M.IdMagasin")
    list = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()
    return render_template("Stock/Stock.html", list=list)

@app.route("/Ajout_stock/", methods=['GET'])
def Ajout_stock():
    # je récupère la liste des produits
    cursor = conn.cursor()
    cursor.execute( "SELECT NomProduit, IdProduit FROM Produit ")
    listPro = cursor.fetchall()
    conn.commit()

    # je récupère la liste des magasins
    cursor = conn.cursor()
    cursor.execute( "SELECT NomMagasin, IdMagasin FROM Magasin ")
    listMag = cursor.fetchall()
    conn.commit()
    return render_template("Stock/Ajout_stock.html", listPro=listPro, listMag=listMag)

@app.route("/Succes_ajout_stock/", methods=['POST'])
def Succes_ajout_stock():
    # cursor = conn.cursor()
    # Récupération des données du formulaire
    Quantitestock = request.form["Quantitestock"]
    IdProduit = request.form["IdProduit"]
    IdMagasin = request.form["IdMagasin"]
    # Traitement des données
    list = {
        "Quantitestock": Quantitestock,
        "IdProduit": IdProduit,
        "IdMagasin": IdMagasin,
    }
    
    # Exécution de la requête d'insertion    
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO Stock (Quantitestock, IdProduit, IdMagasin) VALUES ('{list['Quantitestock']}', '{list['IdProduit']}', '{list['IdMagasin']}')"
    )

    # Commit des modifications
    conn.commit()

    cursor = conn.cursor()
    cursor.execute( "SELECT Idstock, Quantitestock, IdProduit, IdMagasin FROM Stock ")
    list = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()
    # return render_template("Produit/Succes_ajout_produit.html", list=list)
    flash(f"Stock ajouter avec succès!", 'success')
    return redirect(url_for('Stock', list=list))

@app.route("/Modifier_stock/<int:Idstock>", methods=['GET', 'POST'])
def Modifier_stock(Idstock):
    _id = int(Idstock)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Stock WHERE Idstock = ?", _id)
    list = cursor.fetchall() 
    conn.commit()
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Produit ")
    listPro = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Magasin ")
    listMag = cursor.fetchall()
    # Commit des modifications
    conn.commit()
    # conn.close()  
    return render_template("Stock/Modifier_stock.html", listPro=listPro, listMag=listMag, list=list, _id=_id)

@app.route("/Succes_modif_stock/<int:Idstock>", methods=['GET', 'POST'])
def Succes_modif_stock(Idstock):
    _id = int(Idstock)
    Quantitestock = request.form["Quantitestock"]
    IdProduit = request.form["IdProduit"]
    IdMagasin = request.form["IdMagasin"]
    # Traitement des données
    cursor = conn.cursor()
    cursor.execute( 
        "UPDATE Stock SET Quantitestock =?, IdProduit =?, IdMagasin =? WHERE Idstock=?",
        (Quantitestock,IdProduit,IdMagasin, _id))
    conn.commit()
    # cursor.close()
    flash(f"Stock modifier avec succès!", 'warning')
    return redirect(url_for('Stock', _id=_id))

@app.route("/Supprimer_stock/<int:Idstock>", methods=['GET', 'POST'])
def Supprimer_stock(Idstock):
    _id = int(Idstock)
    cursor = conn.cursor()
    cursor.execute( "SELECT * FROM Stock WHERE Idstock = ?", _id)
    list = cursor.fetchall()
    conn.commit()
    return render_template("Stock/Supprimer_Stock.html", list=list,  _id=_id)

@app.route("/Succes_supp_stock/<int:Idstock>", methods=['GET', 'POST'])
def Succes_supp_stock(Idstock):
    _id = int(Idstock)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Stock WHERE Idstock = ?", (_id,))
    conn.commit()
    flash(f"Stock Supprimer avec succès!", 'danger')
    return redirect(url_for('Stock', _id=_id))
# Stock 

if __name__ == "__main__":
    app.secret_key= 'admin123'
    app.run(debug=True)