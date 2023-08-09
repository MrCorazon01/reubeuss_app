from .models import *
from flask import request, render_template, redirect, url_for, session
from datetime import datetime


from functools import wraps
from flask import abort
from flask_login import current_user, logout_user



def director_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('403.html')
        user = Users.query.get(session['user_id'])
        if user.id_role != 2:
            return render_template('403.html')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('403.html')
        user = Users.query.get(session['user_id'])
        if user.id_role not in [1, 2]:
            return render_template('403.html')
        return f(*args, **kwargs)
    return decorated_function


def personnel_l1_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('403.html')
        user = Users.query.get(session['user_id'])
        if user.id_role not in [1, 2, 3]:
            return render_template('403.html')
        return f(*args, **kwargs)
    return decorated_function


def personnel_l2_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return render_template('403.html')
        user = Users.query.get(session['user_id'])
        if user.id_role not in [1, 2, 3, 4]:
            return render_template('403.html')
        return f(*args, **kwargs)
    return decorated_function



# la page d'accueil

@app.route('/')
def index():
    return render_template('index.html')


# Affichage de la vue detenu
@app.route('/detenu')
@personnel_l2_required
def detenu():
    return render_template('Detenu.html')

# Affichage de la vue ajouter_detenu
@app.route('/detenu/ajout_detenu')
@personnel_l1_required
def ajout_detenu():
    data = request.form
    cellules = Cellules.query.all()
    return render_template('detenu/ajout.html', form_data=data, cellules=cellules)


def cellule_est_pleine(id_cellule):
    cellule = Cellules.query.filter_by(id_cellule=id_cellule).first()
    capacite = cellule.capacite

    detenus_dans_cellule = Detenus.query.filter_by(id_cellule=id_cellule).all()

    return len(detenus_dans_cellule) == capacite


def modifier_statut_cellule(id_cellule):
    cellule = Cellules.query.filter_by(id_cellule=id_cellule).first()
    capacite = cellule.capacite

    detenus_dans_cellule = Detenus.query.filter_by(id_cellule=id_cellule).all()

    if len(detenus_dans_cellule) + 1 == capacite:
        cellule.statut = 'Pleine'
    else:
        cellule.statut = 'Libre'
    db.session.commit()


# Processus gérant l'ajout d'un detenu

@app.route('/detenu/ajouter_detenu', methods=['POST'])
def ajouter_detenu():
    data = request.form
    cellules = Cellules.query.all()

    # Conversion de la date au bon format
    try:
        date_incarceration = datetime.strptime(data['date_incarceration'], '%Y-%m-%d')
        date_liberation = datetime.strptime(data['date_liberation'], '%Y-%m-%d')
    except ValueError:
        error = 'Veuillez entrer une date valide'
        return render_template('detenu/ajout.html', error=error, form_data=data, cellules=cellules)

    # Verifier que tout les champs ont bien été remplis
    if any(data[key] == '' for key in ['numero_detenu', 'nom', 'date_incarceration', 'date_liberation', 'motif_detention', 'id_cellule']):
        error = 'les informations entrées doivent être completes'
        return render_template('detenu/ajout.html', error=error, form_data=data, cellules=cellules)

    # Vérifier si le detenu existe dans la base de données
    existing_detenu = Detenus.query.filter_by(numero_detenu=data['numero_detenu']).first()
    if existing_detenu:
        error = 'Le numéro d\'identification {} est déjà utilisé.'.format(data['numero_detenu'])
        return render_template('detenu/ajout.html', error=error, form_data=data, cellules=cellules)

    # Modifier le statut de la cellule
    modifier_statut_cellule(data['id_cellule'])

    # Vérifier que la cellule n'est pas pleine
    if cellule_est_pleine(data['id_cellule']):
        error = 'La cellule est pleine'
        return render_template('detenu/ajout.html', error=error, form_data=data, cellules=cellules)

    # Creation d'un instance de detenu
    nouveau_detenu = Detenus(numero_detenu=data['numero_detenu'], nom=data['nom'], date_incarceration=date_incarceration, date_liberation=date_liberation, motif_detention=data['motif_detention'], id_cellule=data['id_cellule'])

    # Ajout du detenu dans la base de données
    db.session.add(nouveau_detenu)
    db.session.commit()

    message = "Détenu Ajouter avec success"

    return render_template('detenu/ajout.html', message=message, form_data=data, cellules=cellules)


# Affichage de la liste des detenus
@app.route("/detenu/liste_detenu", methods=['GET'])
@personnel_l2_required
def liste_detenu():
    data = Detenus.query.all()
    return render_template("detenu/liste.html", data=data)


# Affichage de la page suppression des détenus
@app.route("/detenu/action_detenu")
@personnel_l1_required
def action_detenu():
    data = Detenus.query.all()
    message = session.pop('message', None)
    return render_template("detenu/action_detenu.html", data=data, message=message)


@app.route("/detenu/suppression_detenu/<numero_detenu>", methods=['POST', 'DELETE'])
@personnel_l1_required
def supprimer_detenu(numero_detenu):
    if request.method == 'POST':
        detenu = Detenus.query.filter_by(numero_detenu=numero_detenu).first()
        db.session.delete(detenu)
        db.session.commit()
        data = Detenus.query.all()

        # Mettre à jour le statut de la cellule
        if cellule_est_pleine(detenu.id_cellule) == False:
            cellule = Cellules.query.filter_by(id_cellule=detenu.id_cellule).first()
            cellule.statut = 'Libre'
            db.session.commit()

        session['message'] = "Détenu supprimé avec success"

        return redirect(url_for('action_detenu'))
    else:
        data = Detenus.query.all()
        error = "Echec lors de la suppression, réessayer plus tard"
        return render_template("detenu/action_detenu.html", error=error, data=data)


@app.route("/detenu/modification_detenu/<numero_detenu>")
@personnel_l1_required
def modification_detenu(numero_detenu):
    data = Detenus.query.filter_by(numero_detenu=numero_detenu).first()
    cellules = Cellules.query.all()
    cellule = Cellules.query.filter_by(id_cellule=data.id_cellule).first()
    return render_template('detenu/modification_detenu.html', form_data=data, current_cellule=cellule, cellules=cellules)


@app.route('/detenu/modifier_detenu/<int:id>', methods=['GET', 'POST'])
@personnel_l1_required
def modifier_detenu(id):
    detenu = Detenus.query.filter_by(numero_detenu=id).first()
    cellules = Cellules.query.all()
    cellule = Cellules.query.filter_by(id_cellule=detenu.id_cellule).first()

    if request.method == 'POST':
        data = request.form

        # Conversion de la date au bon format
        try:
            date_incarceration = datetime.strptime(data['date_incarceration'], '%Y-%m-%d')
            date_liberation = datetime.strptime(data['date_liberation'], '%Y-%m-%d')
        except ValueError:
            error = 'Veuillez entrer une date valide'
            return render_template('detenu/modification_detenu.html', error=error, form_data=data, cellules=cellules, current_cellule=cellule)

        # Verifier que tout les champs ont bien été remplis
        if any(data[key] == '' for key in ['numero_detenu', 'nom', 'date_incarceration', 'date_liberation', 'motif_detention', 'id_cellule']):
            error = 'les informations entrées doivent être completes'
            return render_template('detenu/modification_detenu.html', error=error, form_data=data, cellules=cellules, current_cellule=cellule)

        print("***********mmmmmmmmmm", data['id_cellule'], detenu.id_cellule)
        # Modifier le statut de la cellule
        if data['id_cellule'] != detenu.id_cellule:
            print("***********mmmmmmmmmm", data['id_cellule'], detenu.id_cellule)
            modifier_statut_cellule(data['id_cellule'])
            modifier_statut_cellule(detenu.id_cellule)

        # Modification des informations du detenu
        detenu.numero_detenu = data['numero_detenu']
        detenu.nom = data['nom']
        detenu.date_incarceration = date_incarceration
        detenu.date_liberation = date_liberation
        detenu.motif_detention = data['motif_detention']
        detenu.id_cellule = data['id_cellule']

        # Enregistrer les modifications dans la base de données
        db.session.commit()

        session['message'] = "Détenu modifié avec succès"
        return redirect(url_for('action_detenu'))




@app.route('/cellule', methods=['GET'])
@personnel_l2_required
def cellule():
    data = Cellules.query.all()
    return render_template('Cellule.html', data=data)

@app.route('/cellule/info_cellule/<id_cellule>')
def info_cellule(id_cellule):
    detenus = Detenus.query.filter_by(id_cellule=id_cellule)
    cellule = Cellules.query.filter_by(id_cellule=id_cellule).first()

    return render_template('cellule/info_cellule.html', detenus=detenus, cellule=cellule)


@app.route('/login')
def authentification():
    return render_template('login.html')

@app.route('/login/process', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Si le nom d'utilisateur et le mot de passe sont corrects
            # on enregistre l'utilisateur connecté
            session['user_id'] = user.id_user
            return redirect(url_for('index'))
        else:
            # Sinon, on affiche un message d'erreur
            error = "Nom d'utilisateur ou mot de passe incorrect."
            return render_template('login.html', error=error)

        return render_template('login.html')
   



@app.route('/authentification/administration')
@admin_required
def administration():
    return render_template('administration/administration.html')


@app.route('/user')
@admin_required
def user():
    return render_template('user.html')

@app.route('/user/ajout_user')
@admin_required
def ajout_user():
    return render_template('user/ajout.html')

@app.route('/user/ajouter_user', methods=["POST"])
@admin_required
def ajouter_user():
    data = request.form
    #if request.method == "POST":
    username = data['username']
    nom_role = data['role']

    role = Roles.query.filter_by(nom=nom_role).first()

    perso = Users(username=username, id_role=role.id_role)

    perso.set_password(data["password"])

    db.session.add(perso)
    db.session.commit()

    message = "user ajouter avec success"

    return render_template('user/ajout.html', message=message)



# Affichage de la page suppression des détenus
@app.route("/user/action_user")
@admin_required
def action_user():
    data = db.session.query(Users.id_user, Users.username, Roles.nom).join(Roles).filter(Users.id_role == Roles.id_role).all()
    
    message = session.pop('message', None)
    return render_template("user/action_user.html", data=data, message=message)


@app.route("/user/suppression_user/<id_user>", methods=['POST', 'DELETE'])
@admin_required
def supprimer_user(id_user):
    if request.method == 'POST':
        user = Users.query.filter_by(id_user=id_user).first()
        db.session.delete(user)
        db.session.commit()
        data = Users.query.all()


        session['message'] = "User supprimé avec success"

        return redirect(url_for('action_user'))
    else:
        data = Detenus.query.all()
        error = "Echec lors de la suppression, réessayer plus tard"
        return render_template("user/action_user.html", error=error, data=data)


@app.route("/user/modification_user/<id_user>")
@admin_required
def modification_user(id_user):
    data = Users.query.filter_by(id_user=id_user).first()
    
    return render_template('user/modification_detenu.html', form_data=data)


@app.route('/user/id_user/<int:id>', methods=['GET', 'POST'])
@admin_required
def modifier_user(id):
    user = Users.query.filter_by(id_user=id).first()
   

    if request.method == 'POST':
        data = request.form

        username = data['username']
        nom_role = data['role']

        role = Roles.query.filter_by(nom=nom_role).first()

        user = Users(username=username, id_role=role.id_role)

        user.set_password(data["password"])


        # Enregistrer les modifications dans la base de données
        db.session.commit()

        session['message'] = "Détenu modifié avec succès"
        return redirect(url_for('action_user'))








login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()

    return render_template("/login.html")



# ----------------------------------------------------------------------------------------------------------------
#                                       *****GESTION DES VISITES*****
# ----------------------------------------------------------------------------------------------------------------

# Affichage de la  vue Visites
@app.route("/visites")
@personnel_l2_required
def visites():
    return render_template('Visiteurs.html')



# Affichage de la vue ajouter_visiteur
@app.route('/visiteurs/ajout_visiteur')
@personnel_l2_required
def ajout_visiteur():
    data = request.form
    return render_template('visites/visiteurs/ajout_visiteur.html', form_data=data)


"""

# Processus gérant l'ajout d'un visiteur
@app.route('/visiteurs/ajouter_visiteur', methods=['POST'])
def ajouter_visiteur():
    data = request.form

    # Conversion de la date au bon format
    try:
        heure_visite = datetime.strptime(data['heure_visite'], '%Y-%m-%d')
    except ValueError:
        error = 'Veuillez entrer une date valide'
        return render_template('visites/visiteurs/ajout_visiteur.html', error=error, form_data=data)

    # Verifier que tout les champs ont bien été remplis
    if any(data[key] == '' for key in
           ['id_visiteur', 'nom', 'lien_detenu', 'heure_visite', 'numero_detenu']):
        error = 'les informations entrées doivent être completes'
        return render_template('visites/visiteurs/ajout_visiteur.html', error=error, form_data=data)

    # Vérifier si le visiteurs existe dans la base de données
    existing_visitor = Visiteur.query.filter_by(id_visiteur=data['id_visiteur']).first()
    if existing_visitor:
        error = 'L\'id d\'identification {} est déjà utilisé.'.format(data['id_visiteur'])
        return render_template('visites/visiteurs/ajout_visiteur.html', error=error, form_data=data)

    # Creation d'un instance de visiteur
    nouveau_visiteur = Visiteur(id_visiteur=data['id_visiteur'], nom=data['nom'],
                                lien_detenu=data['lien_detenu'], heure_visite=heure_visite,
                                numero_detenu=data['numero_detenu'])

    # Ajout du detenu dans la base de données
    db.session.add(nouveau_visiteur)
    db.session.commit()

    message = "Visiteur Ajouté avec success"

    return render_template('visites/visiteurs/ajout_visiteur.html', message=message, form_data=data)

"""


# Affichage de la vue transfert
@app.route("/transfert")
@personnel_l2_required
def transfert():
    return render_template('Transfert.html')

# Affichage de la vue ajouter_transfert
@app.route('/transfert/ajout_transfert')
@personnel_l1_required
def ajout_transfert():
    data = request.form
    return render_template('transfert/ajout.html', form_data=data)


# Processus gérant l'ajout d'un transfert
@app.route('/transfert/ajouter_transfert', methods=['POST'])
@personnel_l1_required
def ajouter_transfert():
    data = request.form

    # Conversion de la date au bon format
    try:
        data_transfert = datetime.strptime(data['data_transfert'], '%Y-%m-%d')
    except ValueError:
        error = 'Veuillez entrer une date valide'
        return render_template('transfert/ajout.html', error=error, form_data=data)

    # Verifier que tout les champs ont bien été remplis
    if any(data[key] == '' for key in
           ['id_transfert', 'numero_detenu', 'data_transfert', 'lieu_destination', 'motif']):
        error = 'les informations entrées doivent être completes'
        return render_template('transfert/ajout.html', error=error, form_data=data)

    # Vérifier si le transfert existe dans la base de données
    existing_trans = Transfert.query.filter_by(id_transfert=data['id_transfert']).first()
    if existing_trans:
        error = 'L\'id d\'identification {} est déjà utilisé.'.format(data['id_transfert'])
        return render_template('transfert/ajout.html', error=error, form_data=data)

    # Creation d'une instance de transfert
    nouveau_transfert = Transfert(id_transfert=data['id_transfert'], numero_detenu=data['numero_detenu'],
                                 data_transfert=data_transfert, lieu_destination=data['lieu_destination'],
                                 motif=data['motif'])

    # Ajout du transfert dans la base de données
    db.session.add(nouveau_transfert)
    db.session.commit()

    message = "Transfert ajouté avec success"

    return render_template('transfert/ajout.html', message=message, form_data=data)


# Affichage de la liste des transferts
@app.route("/transfert/liste", methods=['GET'])
@personnel_l2_required
def liste_transferts():
    data = Transfert.query.all()
    return render_template("transfert/liste.html", data=data)




# Affichage de la vue ajouter_visite
@app.route('/visite/ajout_visite')
@personnel_l2_required
def ajout_visite():
    data = request.form
    return render_template('visites/visite/ajout.html', form_data=data)


# Ajout de la visite
@app.route('/visite/ajouter_visite', methods=['POST'])
@personnel_l2_required
def ajouter_visite():
    data = request.form
     # Conversion de la date au bon format
    try:
        date_visite = datetime.strptime(data['date_visite'], '%Y-%m-%d')
    except ValueError:
        error = 'Veuillez entrer une date valide'
        return render_template('visites/visiteurs/ajout_visiteur.html', error=error, form_data=data)

    
    # Verifier que tout les champs ont bien été remplis
    if any(data[key] == '' for key in
           ['id_visite', 'id_visiteur', 'date_visite', 'nom_visiteur', 'lien_detenu', 'numero_detenu']):
        error = 'les informations entrées doivent être completes'
        return render_template('visites/visiteurs/ajout_visiteur.html', error=error, form_data=data)

    # Vérifier si le visiteurs existe dans la base de données
    existing_visite = visite.query.filter_by(id_visite=data['id_visite']).first()
    if existing_visite:
        error = 'L\'id d\'identification {} est déjà utilisé.'.format(data['id_visite'])
        return render_template('visites/visiteurs/ajout_visiteur.html', error=error, form_data=data)

     # Creation d'un instance de  et visite
    nouveau_visite = visite(id_visite=data['id_visite'], id_visiteur=data['id_visiteur'],
                                date_visite=date_visite, nom_visiteur=data['nom_visiteur'])

    nouveau_visiteur = Visiteur(id_visiteur=data['id_visiteur'], nom=data['nom_visiteur'],
                                 lien_detenu=data['lien_detenu'], heure_visite=date_visite, 
                                 numero_detenu=data['numero_detenu'])

     # Ajout de la visite dans la base de données
    db.session.add_all([nouveau_visiteur, nouveau_visite])
    db.session.commit()

    
    

    message = "Visite Ajouté avec success"

    return render_template('visites/visiteurs/ajout_visiteur.html', message=message, form_data=data)
        

# Affichage de la liste des visites
@app.route("/visite/liste", methods=['GET'])
@personnel_l2_required
def liste_visite():
    
    data = db.session.query(visite.id_visite, Visiteur.id_visiteur, Visiteur.nom, visite.date_visite, Visiteur.numero_detenu, Visiteur.lien_detenu).join(Visiteur).filter(visite.id_visiteur == Visiteur.id_visiteur).all()

    return render_template("visites/visite/liste.html", data=data)


# --------------------------------------------------------------------------------------#
#                                Dossier Administratif
# --------------------------------------------------------------------------------------#



# Affichage de la vue dossier -----------------------------------------------------
@app.route('/administration')
@personnel_l1_required
def dossier():
    return render_template('administration.html')
# ---------------------------------------------------------------------------------

# Formulaire de la vue Ad -------------------------------------------------
@app.route('/administrationForm')
@personnel_l1_required
def administrationForm():
    form_data=request.form
    return render_template('dossier/ajout.html', form_data=form_data)
# ---------------------------------------------------------------------------------

# Processus gérant l'ajout d'un dossier --------------------------------------------
@app.route('/administration/ajout_dossier', methods=['GET', 'POST'])
@personnel_l1_required
def ajouter_dossier():
    form_data=request.form
    # Récupération des données du formulaire
    id_dosser = request.form.get('id_dosser')
    numero_detenu = request.form.get('numero_detenu')
    etat_civil = request.form.get('etat_civil')
    antecedant_judiciaire = request.form.get('antecedant_judiciaire')
    dossier = None # Initialisation de la variable "dossier" à "None"

    # Vérification des erreurs
    error = None
    if not id_dosser or not numero_detenu or not etat_civil or not antecedant_judiciaire:
        error = 'Veuillez remplir tous les champs.'

        return render_template('dossier/ajout.html', error=error, form_data=form_data)

    
    existing_detenu = Detenus.query.filter_by(numero_detenu=form_data['numero_detenu']).first()
    if existing_detenu is None:
        error = 'Le numéro d\'identification {} ne correspond à aucun detenu ! Veiller enregistrer le détenu dabord.'.format( form_data['numero_detenu'])
        return render_template('dossier/ajout.html', error=error, form_data=form_data)
    # -------------------------------------------------------------------------------------------------
    existing_detenu_dossier = Dossiers.query.filter_by(numero_detenu=form_data['numero_detenu']).first()
    if existing_detenu_dossier:
        error = "le detenu ayant pour numero d'identification {} dispose déjà d'un dossier administratif enregistré dans notre base de données.".format( form_data['numero_detenu'])
        return render_template('dossier/ajout.html', error=error, form_data=form_data)
    # ----
       
    # Vérifier si le dossier existe dans la base de données---------------------------------------------
    existing_dossier = Dossiers.query.filter_by(id_dosser=form_data['id_dosser']).first()
    if existing_dossier:
        error = 'Le numéro d\'identification {} du dossier est déjà utilisé.'.format(form_data['id_dosser'])
        return render_template('dossier/ajout.html', error=error, form_data=request.form)
        # -------------------------------------------------------------------------------------------------
    


    # Traitement des données si aucune erreur n'a été trouvée
    if error is None:
            
        # Creation d'un instance de dossier ---------------------------------------------------------------
        nouveau_dossier = Dossiers(id_dosser=id_dosser, numero_detenu=numero_detenu, etat_civil=etat_civil, antecedant_judiciaire=antecedant_judiciaire,)
         
        # Ajout du dossier dans la base de données ---------------------------------------------------------
        db.session.add(nouveau_dossier)
        db.session.commit()
        message = "Dossier Ajouter avec success"
        #-------------------------------------------------------------------------------------------------
        return render_template('dossier/ajout.html', error=error, form_data=request.form,message=message)

     
    # Affichage de la page d'ajout avec le message d'erreur

    return render_template('dossier/ajout.html', error=error, form_data=request.form)

   
# Affichage de la liste des dossiers -------------------------------------------------------------------
@app.route("/administration/liste_dossier", methods=['GET'])
@personnel_l1_required
def liste_pdossier():
    data = Dossiers.query.all()
    return render_template("dossier/liste.html", data=data)
#-------------------------------------------------------------------------------------------------


# Affichage de la page suppression des dossiers----------------------------------------------------
@app.route("/dossier/action_dossier")
@personnel_l1_required
def action_dossier():
    data = Dossiers.query.all()
    message = session.pop('message', None)
    return render_template("dossier/action_dossier.html", data=data, message=message)
#-------------------------------------------------------------------------------------------------


@app.route("/dossier/suppression_dossier/<id_dosser>", methods=['POST', 'DELETE'])#-------------
@personnel_l1_required
def supprimer_dossier(id_dosser):
    if request.method == 'POST':
        dossier = Dossiers().query.filter_by(id_dosser=id_dosser).first()
        db.session.delete(dossier)
        db.session.commit()
        data = dossier.query.all()
        session['message'] = "dossier supprimé avec success"

        return redirect(url_for('action_dossier'))
    else:
        data = Dossiers.query.all()
        error = "Echec lors de la suppression, réessayer plus tard"
        return render_template("dossier/action_dossier.html", error=error, data=data)
#-------------------------------------------------------------------------------------------------

@app.route("/dossier/modification_dossier/<id_dosser>")#----------------------------------------
@personnel_l1_required
def modification_dossier(id_dosser):

    dossier = Dossiers.query.filter_by(id_dosser=id_dosser).first()
    detenu = Detenus.query.filter_by(numero_detenu=dossier.numero_detenu).first()
    
    return render_template('dossier/modification_dossier.html', form_data=dossier, detenu=detenu)
#-------------------------------------------------------------------------------------------------


@app.route('/dossier/modifier_dossier/<int:id>', methods=['GET', 'POST'])#--------------------------
@personnel_l1_required
def modifier_dossier(id):
    dossier = Dossiers.query.filter_by(id_dosser=id).first()

    if request.method == 'POST':
        data = request.form

        # Modification des informations du personnel
        dossier.identifiant_personnel = data['id_dosser']
        dossier.numero_detenu = data['numero_detenu']
        dossier.etat_civil = data['etat_civil']
        dossier.antecedant_judiciaire = data['antecedant_judiciaire']
    

        # Enregistrer les modifications dans la base de données
        db.session.commit()

        session['message'] = "dosser modifié avec succès"

        return render_template('dossier/dossier_personnelle.html', form_data=dossier)

#-------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------#
#                                    Personnelle
# --------------------------------------------------------------------------------------#

# Affichage de la vue Personnelle -------------------------------------------------

@app.route('/personnelle')
@personnel_l1_required
def personnelle():
    return render_template('personnelle.html')
# ---------------------------------------------------------------------------------

# Formulaire de la vue Personnelle -------------------------------------------------
@app.route('/personnelleForm')
def personelleForm():
    form_data=request.form
    return render_template('personnelle/ajout.html', form_data=form_data)
# ---------------------------------------------------------------------------------


# Processus gérant l'ajout d'un personnel --------------------------------------------
@app.route('/personnelle/ajout_personnelle', methods=['GET', 'POST'])
@personnel_l1_required
def ajouter_personnelle():
    form_data=request.form
    # Récupération des données du formulaire
    numero_personnel = request.form.get('numero_personnel')
    nom = request.form.get('nom')
    poste = request.form.get('poste')
    fonction = request.form.get('fonction')
    personnel = None # Initialisation de la variable "personnel" à "None"

    # Vérification des erreurs
    error = None
    if not numero_personnel or not nom or not poste or not fonction:
        error = 'Veuillez remplir tous les champs.'
    elif poste == "directeur" and fonction != "responsable":
        error = "Le directeur ne peut être qu'un responsable."
    elif poste == "administrateur" and fonction != "admin":
        error = "Un administrateur ne peut être qu'un admin."
    elif poste == "travailleur social" and fonction not in ("niveau1", "niveau2"):
        error = "Un travailleur social ne peut être qu'un personnel de niveau 1 ou 2."
    elif poste == "surveillant" and fonction not in ("niveau1", "niveau2"):
        error = "Un surveillant  ne peut être qu'un personnel de niveau 1 ou 2."
    
      
    # Vérifier si il y a deja un directeur---------------------------------------------
    existing_directeur = Personnels.query.filter_by(poste=f"directeur").first()
    if existing_directeur:
        error = 'Le directeur a deja été enregistrer'
        return render_template('personnelle/ajout.html', error=error, form_data=request.form)
        # -------------------------------------------------------------------------------------------------
    


       
    # Vérifier si le personnel existe dans la base de données---------------------------------------------
    existing_personnelle = Personnels.query.filter_by(numero_personnel=form_data['numero_personnel']).first()
    if existing_personnelle:
        error = 'Le numéro d\'identification {} est déjà utilisé.'.format(form_data['numero_personnel'])
        return render_template('personnelle/ajout.html', error=error, form_data=request.form)
        # -------------------------------------------------------------------------------------------------
    


    # Traitement des données si aucune erreur n'a été trouvée
    if error is None:
            
        # Creation d'un instance de personnel ---------------------------------------------------------------
        nouveau_personnel = Personnels(numero_personnel=numero_personnel, nom=nom, poste=poste, fonction=fonction)
         
        # Ajout du personnel dans la base de données ---------------------------------------------------------
        db.session.add(nouveau_personnel)
        db.session.commit()
        message = "personnelle Ajouter avec success"
        #-------------------------------------------------------------------------------------------------

        return redirect(url_for('liste_personnelle'))
     
    # Affichage de la page d'ajout avec le message d'erreur

    return render_template('personnelle/ajout.html', error=error, form_data=request.form)


    
# Affichage de la liste des personnels -------------------------------------------------------------------
@app.route("/personnelle/liste_personnelle", methods=['GET'])
@personnel_l1_required
def liste_personnelle():
    data = Personnels.query.all()
    return render_template("personnelle/liste.html", data=data)
#-------------------------------------------------------------------------------------------------


# Affichage de la page suppression des personneles----------------------------------------------------
@app.route("/personnelle/action_personnelle")
@personnel_l1_required
def action_personnelle():
    data = Personnels.query.all()
    message = session.pop('message', None)
    return render_template("personnelle/action_personnelle.html", data=data, message=message)
#-------------------------------------------------------------------------------------------------


@app.route("/personnelle/suppression_personnelle/<identifiant_personnel>", methods=['POST', 'DELETE'])#-------------
@personnel_l1_required
def supprimer_personnelle(identifiant_personnel):
    if request.method == 'POST':
        personelle = Personnels().query.filter_by(numero_personnel=identifiant_personnel).first()
        db.session.delete(personelle)
        db.session.commit()
        data = personelle.query.all()
        session['message'] = "personnel supprimé avec success"

        return redirect(url_for('action_personnelle'))
    else:
        data = Personnels.query.all()
        error = "Echec lors de la suppression, réessayer plus tard"
        return render_template("personelle/action_personnelle.html", error=error, data=data)
#-------------------------------------------------------------------------------------------------

@app.route("/personnelle/modification_personnelle/<numero_personnel>")#----------------------------------------
@personnel_l1_required
def modification_personnelle(numero_personnel):

    personnelle = Personnels.query.filter_by(numero_personnel=numero_personnel).first()
    
    return render_template('personnelle/modification_personnelle.html', form_data=personnelle)
#-------------------------------------------------------------------------------------------------


@app.route('/personnelle/modifier_personnelle/<int:id>', methods=['GET', 'POST'])#--------------------------
@personnel_l1_required
def modifier_personnelle(id):
    personnelle = Personnels.query.filter_by(numero_personnel=id).first()

    if request.method == 'POST':
        data = request.form

        # Modification des informations du personnel
        id_dosser = request.form.get('id_dosser')
        numero_detenu = request.form.get('numero_detenu')
        etat_civil = request.form.get('etat_civil')
        antecedant_judiciaire = request.form.get('antecedant_judiciaire')
        dossier = None # Initialisation de la variable "dossier" à "None"

    

        # Enregistrer les modifications dans la base de données
        db.session.commit()

        session['message'] = "personnel modifié avec succès"

        return render_template('personnelle/modification_personnelle.html', form_data=personnelle)

#-------------------------------------------------------------------------------------------------
