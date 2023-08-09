from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager





app = Flask(__name__ , static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prison.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'

CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)


db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)




class Cellules(db.Model):
    id_cellule = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Text, nullable=False)
    capacite = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"numero:{self.id_cellule} \n capacité:{self.capacite}"


class Detenus(db.Model):
    numero_detenu = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    date_incarceration = db.Column(db.Date, nullable=False)
    date_liberation = db.Column(db.Date, nullable=False)
    motif_detention = db.Column(db.Text, nullable=False)
    id_cellule = db.Column(db.Integer, db.ForeignKey('cellules.id_cellule'), nullable=False)

    def __repr__(self):
        return f"Detenu(nom={self.nom} \n num_det:{self.numero_detenu})"


class Personnels(db.Model):
    numero_personnel = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    poste = db.Column(db.Text, nullable=False)
    fonction = db.Column(db.Text, nullable=False)
    

    def __repr__(self):
        return f"numero_det:{self.numero_personnel} \n nom:{self.nom} \n fonction:{self.fonction}"

    

class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    id_role = db.Column(db.Integer, db.ForeignKey("roles.id_role"), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)



class Travaux(db.Model):
    id_travail = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"id:{self.id_travail} \n nom:{self.nom} \n description:{self.description}"


class DetenuTravail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_detenu = db.Column(db.Integer, db.ForeignKey('detenus.numero_detenu'), nullable=False)
    id_travail = db.Column(db.Integer, db.ForeignKey('travaux.id_travail'), nullable=False)


class Visiteur(db.Model):
    id_visiteur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    lien_detenu = db.Column(db.Text)
    heure_visite = db.Column(db.DateTime, nullable=False)
    numero_detenu = db.Column(db.Integer, db.ForeignKey('detenus.numero_detenu'), nullable=False)

    def __repr__(self):
        return f"id:{self.id_visiteur} \n nom:{self.nom} \n detenu conerné:{self.numero_detenu}"

class visite(db.Model):
    id_visite = db.Column(db.Integer, primary_key=True)
    id_visiteur = db.Column(db.Integer, db.ForeignKey('visiteur.id_visiteur'), nullable=False)
    date_visite = db.Column(db.DateTime, nullable=False)
    nom_visiteur = db.Column(db.String, nullable=False)


class Dossiers(db.Model):
    id_dosser = db.Column(db.Integer, primary_key=True)
    numero_detenu = db.Column(db.Integer, db.ForeignKey('detenus.numero_detenu'), nullable=False)
    etat_civil = db.Column(db.Text, nullable=False)
    antecedant_judiciaire = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return  f"id:{self.id_dosser} \n nom:{self.numero_detenu}"


class Transfert(db.Model):
    id_transfert = db.Column(db.Integer, primary_key=True)
    numero_detenu = db.Column(db.Integer, db.ForeignKey('detenus.numero_detenu'), nullable=False)
    data_transfert = db.Column(db.Date, nullable=False)
    lieu_destination = db.Column(db.Text, nullable=False)
    motif = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"id:{self.id_transfert} \n nom détenu:{self.numero_detenu} \n destination:{self.lieu_destination}"



class Roles(db.Model):
    id_role = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))



class PrisonModel(ModelView):
    column_display_pk = True

class userModel(ModelView):
    column_display_pk = True
    column_list= ('username', 'password', 'id_role')


admin = Admin(app)
admin.add_view(PrisonModel(Detenus, db.session))
admin.add_view(PrisonModel(Cellules, db.session))
admin.add_view(PrisonModel(Roles, db.session))
admin.add_view(userModel(Users, db.session))
admin.add_view(PrisonModel(Transfert, db.session))
admin.add_view(PrisonModel(Visiteur, db.session))
admin.add_view(PrisonModel(visite, db.session))
admin.add_view(PrisonModel(Personnels, db.session))
admin.add_view(PrisonModel(Dossiers, db.session))



with app.app_context():
    db.create_all()