CREATE database Zoro_E_magasin

CREATE TABLE Produit (
IdProduit INT NOT NULL PRIMARY KEY IDENTITY(1,1),
NomProduit VARCHAR(20) NOT NULL,
CatProduit VARCHAR(20) NOT NULL,
PrixUnitaire FLOAT NOT NULL, 
Descriptions text 
);
CREATE TABLE Utilisateurs (
Id INT NOT NULL PRIMARY KEY IDENTITY(1,1),
Nom VARCHAR(15) NOT NULL,
Prenoms VARCHAR(30) NOT NULL,
Ville VARCHAR(30) NOT NULL, 
E_mail VARCHAR(30) NOT NULL unique,
Mot_de_passe VARCHAR(255) NOT NULL
);
ALTER TABLE Utilisateurs
ADD Roles varchar(20)

select * from Utilisateurs
delete from Utilisateurs
Truncate table Utilisateurs
drop table Utilisateurs

CREATE TABLE Magasin(
IdMagasin INT NOT NULL PRIMARY KEY IDENTITY(1,1),
NomMagasin VARCHAR(20) NOT NULL,
AdresseMagasin VARCHAR(50) NOT NULL,
Telephone VARCHAR(16) NOT NULL,
Mail VARCHAR(30) NOT NULL
);

CREATE TABLE Stock (
Idstock INT NOT NULL PRIMARY KEY IDENTITY(1,1),
Quantitestock INT NOT NULL,
IdProduit INT NOT NULL,
IdMagasin INT NOT NULL,
FOREIGN KEY  (IdProduit) REFERENCES Produit (IdProduit),
FOREIGN KEY (IdMagasin) REFERENCES Magasin (IdMagasin)
)

CREATE TABLE Vente (
IdVente INT NOT NULL PRIMARY KEY IDENTITY(1,1),
Quantitevendu INT NOT NULL,
Prixtotal FLOAT,
Datevente DATE NOT NULL,
IdProduit INT NOT NULL,
IdMagasin INT NOT NULL,
FOREIGN KEY  (IdProduit) REFERENCES Produit (IdProduit),
FOREIGN KEY (IdMagasin) REFERENCES Magasin (IdMagasin)
)