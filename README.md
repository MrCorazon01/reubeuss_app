
# Reubeuss Prison Manager APP

# Documentation du Projet - Flask

## **Introduction**

Ce projet vise à développer un système de gestion d'une prison, qui permettra de gérer les informations relatives aux détenus, aux transferts, aux visites, aux dossiers administratifs et au personnel de la prison. Le système offre des fonctionnalités pour ajouter, modifier et supprimer des enregistrements, ainsi que pour afficher des listes de données.

## **Technologies utilisées**

Le système de gestion de la prison est développé en utilisant les technologies suivantes:

- Python: Le langage de programmation principal pour le développement de la logique de l'application.
- Flask: Un framework Web pour la création des routes, la gestion des requêtes HTTP et la génération de pages HTML dynamiques.
- SQLAlchemy: Une bibliothèque Python pour l'interaction avec la base de données et la manipulation des objets.
- SQLite: Un système de gestion de base de données relationnelle léger utilisé pour stocker les données de l'application.

## **Architecture du projet**

Le projet suit une architecture MVC (Modèle-Vue-Contrôleur) pour organiser le code de manière modulaire et faciliter la maintenance et l'extension du système. Voici une brève description des différents composants de l'architecture:

relations entre les entités du système. Ils sont responsables de l'interaction avec la base de données et de la manipulation des données. Dans ce projet, les modèles incluraient des classes telles que "Detenu", "Transfert", "Visite", "DossierAdministratif" et "Personnel", avec des attributs correspondant aux différentes informations nécessaires.

1. Vues (Views): Les vues sont chargées de l'interface utilisateur du système. Elles affichent les données et reçoivent les entrées de l'utilisateur. Dans ce projet, les vues seraient des pages HTML dynamiques générées à l'aide du framework Flask, avec des formulaires pour l'ajout, la modification et la suppression d'enregistrements, ainsi que des tableaux pour afficher les listes de données.
2. Contrôleurs (Controllers): Les contrôleurs agissent comme des intermédiaires entre les modèles et les vues. Ils gèrent les requêtes des utilisateurs, effectuent les opérations nécessaires sur les modèles et renvoient les données aux vues pour affichage. Les contrôleurs dans ce projet seraient des fonctions Python qui sont appelées en fonction des actions de l'utilisateur, telles que l'ajout d'un détenu, la modification d'une visite, etc.
3. Base de données: Le système utilise une base de données SQLite pour stocker les données de manière persistante. SQLite est un choix approprié pour ce projet en raison de sa simplicité et de sa légèreté. Les modèles interagissent avec la base de données à l'aide de la bibliothèque SQLAlchemy, qui facilite les opérations de requête et de manipulation des données.

## ****Installation et execution****

```bash
$ git clone https://github.com/MrCorazon01/reubeuss_app.git
$ cd reubeuss_app
$ pip install -r requirements.txt
$ python run.py
```

## Documentation

<aside>
📌

# Documentation de la classe `Detenus` :

- La classe **`Detenus`** est un modèle de base de données qui représente les détenus. Elle contient les attributs suivants :
    - **`numero_detenu`**: le numéro du détenu (entier, clé primaire)
    - **`nom`**: le nom du détenu (chaîne de caractères, non nullable)
    - **`date_incarceration`**: la date d'incarcération du détenu (date, non nullable)
    - **`date_liberation`**: la date de libération prévue du détenu (date, non nullable)
    - **`motif_detention`**: le motif de la détention du détenu (texte, non nullable)
    - **`id_cellule`**: l'identifiant de la cellule dans laquelle le détenu est détenu (entier, clé étrangère)
- La fonction **`detenu`** est une vue qui affiche la vue **`Detenu.html`**.
- La fonction **`ajout_detenu`** est une vue qui affiche la vue **`ajout.html`** pour ajouter un détenu. Elle récupère les données du formulaire et les affiche dans le modèle **`ajout.html`**. Elle utilise la méthode HTTP GET.
- La fonction **`ajouter_detenu`** est une vue qui traite la soumission du formulaire d'ajout de détenu. Elle récupère les données du formulaire et effectue les validations nécessaires. Si les données sont valides, elle crée une nouvelle instance de **`Detenus`** avec les données fournies, l'ajoute à la base de données et affiche un message de réussite. Sinon, elle affiche un message d'erreur avec les données fournies. Elle utilise la méthode HTTP POST.
- La fonction **`liste_detenu`** est une vue qui affiche la liste des détenus. Elle récupère tous les enregistrements de la table **`Detenus`** à partir de la base de données et les affiche dans le modèle **`liste.html`**. Elle utilise la méthode HTTP GET.
- La fonction **`action_detenu`** est une vue qui affiche la page pour effectuer des actions sur les détenus. Elle récupère tous les enregistrements de la table **`Detenus`** à partir de la base de données et les affiche dans le modèle **`action_detenu.html`**.
- La fonction **`supprimer_detenu`** est une vue qui traite la suppression d'un détenu. Si la méthode HTTP est POST, elle supprime le détenu avec le numéro spécifié de la base de données, met à jour le statut de la cellule correspondante et affiche un message de réussite. Si la méthode HTTP est DELETE, elle affiche un message d'erreur. Elle utilise les méthodes HTTP POST et DELETE.
- La fonction **`modification_detenu`** est une vue qui affiche le formulaire de modification d'un détenu spécifié par son numéro. Elle récupère les données du détenu à partir de la base de données et les affiche dans le modèle **`modification_detenu.html`**.
- La fonction **`modifier_detenu`** est une vue qui traite la soumission du formulaire de modification d'un détenu. Elle récupère les données du formulaire, effectue les validations nécessaires et met à jour les informations du détenu dans la base de données. Elle utilise les méthodes HTTP GET et POST.

### Services de l'API :

- **`GET /detenu`**: Affiche la vue **`Detenu.html`**.
- **`GET /detenu/ajout_detenu`**: Affiche la vue **`ajout.html`** pour ajouter un détenu.
- `POST /detenu/ajouter_detenu: Traite la soumission du formulaire d'ajout de détenu. Les données du formulaire doivent être envoyées via la méthode HTTP POST.
- **`GET /detenu/liste_detenu`**: Affiche la liste des détenus.
- **`GET /detenu/action_detenu`**: Affiche la page pour effectuer des actions sur les détenus.
- **`POST /detenu/suppression_detenu/<numero_detenu>`**: Supprime le détenu avec le numéro spécifié. Les données doivent être envoyées via la méthode HTTP POST.
- **`DELETE /detenu/suppression_detenu/<numero_detenu>`**: Affiche une erreur car la méthode HTTP DELETE n'est pas utilisée pour la suppression des détenus.
- **`GET /detenu/modification_detenu/<numero_detenu>`**: Affiche le formulaire de modification du détenu avec le numéro spécifié.
- **`GET /detenu/modifier_detenu/<int:id>`**: Affiche le formulaire de modification du détenu avec l'ID spécifié.
- **`POST /detenu/modifier_detenu/<int:id>`**: Traite la soumission du formulaire de modification du détenu avec l'ID spécifié. Les données du formulaire doivent être envoyées via la méthode HTTP POST.

### Manuel d'utilisation :

1. Accéder à la page d'accueil de l'application.
2. Pour afficher la vue des détenus, accéder à l'URL **`/detenu`**.

1. Pour ajouter un détenu, accéder à l'URL **`/detenu/ajout_detenu`** et remplir le formulaire avec les informations requises.
2. Pour visualiser la liste des détenus, accéder à l'URL **`/detenu/liste_detenu`**.
3. Pour effectuer des actions sur les détenus, accéder à l'URL **`/detenu/action_detenu`**.
4. Pour supprimer un détenu, accéder à l'URL **`/detenu/suppression_detenu/<numero_detenu>`** et confirmer la suppression.
5. Pour modifier les informations d'un détenu, accéder à l'URL **`/detenu/modification_detenu/<numero_detenu>`** ou **`/detenu/modifier_detenu/<int:id>`** selon le numéro ou l'ID du détenu, et modifier les informations dans le formulaire.

**Remarque** : Certains des services nécessitent une authentification en tant que personnel de niveau 1 ou niveau 2 pour y accéder.

</aside>

<aside>
📌

## Documentation de la classe **`Dossiers`** :

La classe **`Dossiers`** représente les dossiers administratifs des détenus dans l'application. Elle a les attributs suivants :

- **`id_dosser`** : Un entier qui représente l'identifiant unique du dossier administratif (clé primaire).
- **`numero_detenu`** : Un entier qui représente le numéro du détenu associé à ce dossier (clé étrangère faisant référence à la table **`detenus`**).
- **`etat_civil`** : Une chaîne de caractères qui représente l'état civil du détenu.
- **`antecedant_judiciaire`** : Une chaîne de caractères qui représente les antécédents judiciaires du détenu.

La méthode **`__repr__`** est définie pour afficher une représentation sous forme de chaîne du dossier, en affichant l'identifiant et le numéro du détenu.

### API des services de la classe **`Dossiers`** :

- **`GET /administration`** : Affiche la vue de l'administration.
- **`GET /administrationForm`** : Affiche le formulaire pour ajouter un nouveau dossier administratif.
- **`POST /administration/ajout_dossier`** : Traite l'ajout d'un nouveau dossier administratif à partir des données du formulaire.
- **`GET /administration/liste_dossier`** : Affiche la liste de tous les dossiers administratifs.
- **`GET /dossier/action_dossier`** : Affiche la page pour effectuer des actions sur les dossiers administratifs.
- **`POST /dossier/suppression_dossier/<id_dosser>`** : Supprime un dossier administratif avec l'identifiant spécifié.
- **`GET /dossier/modification_dossier/<id_dosser>`** : Affiche la page de modification d'un dossier administratif avec l'identifiant spécifié.
- **`POST /dossier/modifier_dossier/<id>`** : Modifie un dossier administratif avec l'identifiant spécifié à partir des données du formulaire.

### Manuel d'utilisation :

1. Accéder à la page d'accueil de l'application.
2. Pour accéder à la vue d'administration, accéder à l'URL **`/administration`**. Il est nécessaire d'être authentifié en tant que personnel de niveau 1 pour accéder à cette vue.
3. Sur la vue d'administration, vous pouvez choisir parmi différentes actions liées aux dossiers administratifs.
4. Pour ajouter un nouveau dossier administratif, accéder à l'URL **`/administrationForm`** pour afficher le formulaire d'ajout.
5. Remplir tous les champs du formulaire (identifiant du dossier, numéro du détenu, état civil et antécédents judiciaires) et soumettre le formulaire. Le dossier sera ajouté à la base de données.
6. Pour afficher la liste de tous les dossiers administratifs, accéder à l'URL **`/administration/liste_dossier`**.
7. Pour effectuer des actions supplémentaires sur les dossiers administratifs, accéder à l'URL **`/dossier/action_dossier`**.
8. Sur la page d'actions des dossiers, vous pouvez supprimer un dossier administratif en cliquant sur le bouton de suppression correspondant à l'identifiant du dossier.
9. Pour modifier un dossier administratif, cliquer sur le bouton de modification correspondant à l'identifiant du dossier sur la page d'actions des dossiers.

</aside>

<aside>
📌

## Documentation de la classe **`Cellules`** :

La classe **`Cellules`** représente les cellules de détention dans l'application. Elle a les attributs suivants :

- **`id_cellule`** : Un entier qui représente l'identifiant unique de la cellule (clé primaire).
- **`numero`** : Une chaîne de caractères qui représente le numéro de la cellule.
- **`capacite`** : Un entier qui représente la capacité maximale de la cellule.
- **`statut`** : Une chaîne de caractères qui représente le statut actuel de la cellule.

La méthode **`__repr__`** est définie pour afficher une représentation sous forme de chaîne de la cellule, en affichant l'identifiant et la capacité.

### API des services de la classe **`Cellules`** :

- **`GET /cellule`** : Récupère la liste de toutes les cellules de détention. Requiert l'authentification en tant que personnel de niveau 2.
- **`GET /cellule/info_cellule/<id_cellule>`** : Affiche les informations détaillées sur la cellule avec l'ID spécifié. Les informations comprennent la liste des détenus actuellement dans la cellule et les détails de la cellule elle-même.

### Manuel d'utilisation :

1. Accéder à la page d'accueil de l'application.
2. Pour afficher la vue des cellules, accéder à l'URL **`/cellule`**. Il est nécessaire d'être authentifié en tant que personnel de niveau 2 pour accéder à cette vue.
3. Pour obtenir des informations détaillées sur une cellule spécifique, accéder à l'URL **`/cellule/info_cellule/<id_cellule>`**, où **`<id_cellule>`** est l'identifiant de la cellule.
4. Les informations affichées pour chaque cellule comprennent le numéro de la cellule, sa capacité et son statut actuel.
5. Pour chaque cellule, la liste des détenus qui y sont actuellement détenus est également affichée.

**Remarque** : L'accès à certains services de la classe **`Cellules`** nécessite une authentification en tant que personnel de niveau 2.

</aside>

<aside>
📌

## Documentation de la classe **`Personnels`** :

La classe **`Personnels`** représente les informations sur le personnel dans l'application. Elle a les attributs suivants :

- **`numero_personnel`** : Un entier qui représente l'identifiant unique du personnel (clé primaire).
- **`nom`** : Une chaîne de caractères qui représente le nom du personnel.
- **`poste`** : Une chaîne de caractères qui représente le poste du personnel.
- **`fonction`** : Une chaîne de caractères qui représente la fonction du personnel.

La méthode **`__repr__`** est définie pour afficher une représentation sous forme de chaîne du personnel, en affichant l'identifiant, le nom et la fonction.

### API des services de la classe **`Personnels`** :

- **`GET /personnelle`** : Récupère la liste de tout le personnel enregistré. Requiert l'authentification en tant que personnel de niveau 1.
- **`GET /personnelleForm`** : Affiche le formulaire pour ajouter un nouveau personnel.
- **`POST /personnelle/ajout_personnelle`** : Ajoute un nouveau personnel à la base de données. Requiert l'authentification en tant que personnel de niveau 1.
- **`GET /personnelle/liste_personnelle`** : Affiche la liste de tout le personnel enregistré.
- **`GET /personnelle/action_personnelle`** : Affiche la page pour effectuer des actions sur le personnel (par exemple, la suppression).
- **`POST /personnelle/suppression_personnelle/<identifiant_personnel>`** : Supprime le personnel avec l'identifiant spécifié. Requiert l'authentification en tant que personnel de niveau 1.
- **`GET /personnelle/modification_personnelle/<numero_personnel>`** : Affiche la page de modification du personnel avec l'identifiant spécifié.
- **`POST /personnelle/modifier_personnelle/<id>`** : Modifie les informations du personnel avec l'identifiant spécifié. Requiert l'authentification en tant que personnel de niveau 1.

### Manuel d'utilisation :

1. Accéder à la page d'accueil de l'application.
2. Pour afficher la vue du personnel, accéder à l'URL **`/personnelle`**. Il est nécessaire d'être authentifié en tant que personnel de niveau 1 pour accéder à cette vue.
3. Pour ajouter un nouveau personnel, accéder à l'URL **`/personnelleForm`** et remplir le formulaire.
4. Les champs obligatoires à remplir sont le numéro du personnel, le nom, le poste et la fonction.
5. Lors de l'ajout d'un nouveau personnel, diverses vérifications sont effectuées, notamment la validation des champs, les contraintes de poste et de fonction, et la vérification de l'existence d'un directeur.
6. Pour afficher la liste de tout le personnel enregistré, accéder à l'URL **`/personnelle/liste_personnelle`**.
7. Pour effectuer des actions sur le personnel, accéder à l'URL **`/personnelle/action_personnelle`**, où vous pouvez supprimer le personnel en cliquant sur le bouton de suppression correspondant à chaque personne.
8. Pour modifier les informations d'un personnel spécifique, accéder à l'URL **`/personnelle/modification_personnelle/<numero_personnel>`**, où **`<numero_personnel>`** est l'identifiant du personnel.
9. Remplir le formulaire de modification avec les nouvelles informations et cliquer sur le bouton de modification pour enregistrer les modifications.
10. Les modifications apportées aux informations du personnel seront enregistrées en accédant à l'URL **`/personnelle/modifier_personnelle/<id>`**, où **`<id>`** est l'identifiant du personnel.
10. Les modifications seront enregistrées uniquement si toutes les vérifications sont réussies, telles que la validation des champs et les contraintes de poste et de fonction.
11. Une fois les modifications enregistrées avec succès, un message de confirmation sera affiché.
12. Vous pouvez continuer à effectuer d'autres actions sur le personnel en naviguant sur les différentes vues et en utilisant les fonctionnalités fournies.

</aside>

<aside>
📌

## Documentation des classes **`Visiteur`** et **`visite`** :

La classe **`Visiteur`** représente les visiteurs dans l'application. Elle a les attributs suivants :

- **`id_visiteur`** : Un entier qui représente l'identifiant unique du visiteur (clé primaire).
- **`nom`** : Une chaîne de caractères qui représente le nom du visiteur.
- **`lien_detenu`** : Une chaîne de caractères qui représente le lien entre le visiteur et le détenu visité.
- **`heure_visite`** : Un objet **`DateTime`** qui représente l'heure de la visite.
- **`numero_detenu`** : Un entier qui représente le numéro du détenu visité (clé étrangère faisant référence à la table **`detenus`**).

La méthode **`__repr__`** est définie pour afficher une représentation sous forme de chaîne du visiteur, en affichant l'identifiant, le nom et le numéro du détenu concerné.

La classe **`visite`** représente les visites effectuées par les visiteurs dans l'application. Elle a les attributs suivants :

- **`id_visite`** : Un entier qui représente l'identifiant unique de la visite (clé primaire).
- **`id_visiteur`** : Un entier qui représente l'identifiant du visiteur associé à cette visite (clé étrangère faisant référence à la table **`visiteur`**).
- **`date_visite`** : Un objet **`DateTime`** qui représente la date de la visite.
- **`nom_visiteur`** : Une chaîne de caractères qui représente le nom du visiteur.

Les API des services des classes **`Visiteur`** et **`visite`** sont les suivantes :

- **`GET /visites`** : Affiche la vue des visites.
- **`GET /visiteurs/ajout_visiteur`** : Affiche la vue pour ajouter un nouveau visiteur.
- **`GET /visite/ajout_visite`** : Affiche la vue pour ajouter une nouvelle visite.
- **`POST /visite/ajouter_visite`** : Traite l'ajout d'une nouvelle visite à partir des données du formulaire.
- **`GET /visite/liste`** : Affiche la liste de toutes les visites effectuées.

### Manuel d'utilisation :

1. Accéder à la page d'accueil de l'application.
2. Pour accéder à la vue des visites, accéder à l'URL **`/visites`**. Il est nécessaire d'être authentifié en tant que personnel de niveau 2 pour accéder à cette vue.
3. Sur la vue des visites, vous pouvez choisir parmi différentes actions liées aux visiteurs et aux visites.
4. Pour ajouter un nouveau visiteur, accéder à l'URL **`/visiteurs/ajout_visiteur`** pour afficher le formulaire d'ajout.
5. Remplir tous les champs du formulaire (identifiant du visiteur, nom, lien avec le détenu, heure de visite et numéro du détenu) et soumettre le formulaire. Le visiteur sera ajouté à la base de données.
6. Pour ajouter une nouvelle visite, accéder à l'URL **`/visite/ajout_visite`** pour afficher le formulaire d'ajout.
7. Remplir tous les champs du formulaire (identifiant de la visite, identifiant du visiteur, date de visite et nom du visiteur) et soumettre le formulaire.
</aside>

<aside>
📌

## Documentation de la classe **`Transfert`** :

La classe **`Transfert`** représente les transferts de détenus dans l'application. Elle a les attributs suivants :

- **`id_transfert`** : Un entier qui représente l'identifiant unique du transfert (clé primaire).
- **`numero_detenu`** : Un entier qui représente le numéro du détenu concerné par le transfert (clé étrangère faisant référence à la table **`detenus`**).
- **`date_transfert`** : Un objet **`Date`** qui représente la date du transfert.
- **`lieu_destination`** : Une chaîne de caractères qui représente le lieu de destination du transfert.
- **`motif`** : Une chaîne de caractères qui représente le motif du transfert.

La méthode **`__repr__`** est définie pour afficher une représentation sous forme de chaîne du transfert, en affichant l'identifiant, le nom du détenu et la destination.

### Les API des services de la classe **`Transfert`** sont les suivantes :

- **`GET /transfert`** : Affiche la vue des transferts.
- **`GET /transfert/ajout_transfert`** : Affiche la vue pour ajouter un nouveau transfert.
- **`POST /transfert/ajouter_transfert`** : Traite l'ajout d'un nouveau transfert à partir des données du formulaire.
- **`GET /transfert/liste`** : Affiche la liste de tous les transferts effectués.

### Manuel d'utilisation :

1. Accéder à la page d'accueil de l'application.
2. Pour accéder à la vue des transferts, accéder à l'URL **`/transfert`**. Il est nécessaire d'être authentifié en tant que personnel de niveau 2 pour accéder à cette vue.
3. Sur la vue des transferts, vous pouvez choisir parmi différentes actions liées aux transferts.
4. Pour ajouter un nouveau transfert, accéder à l'URL **`/transfert/ajout_transfert`** pour afficher le formulaire d'ajout.
5. Remplir tous les champs du formulaire (identifiant du transfert, numéro du détenu, date du transfert, lieu de destination et motif) et soumettre le formulaire. Le transfert sera ajouté à la base de données.
6. Pour afficher la liste de tous les transferts, accéder à l'URL **`/transfert/liste`**. Vous verrez la liste des transferts effectués.
</aside>

<aside>
📌

# Documentation de la classe **`Users`** :

La classe **`Users`** représente les utilisateurs de l'application. Elle a les attributs suivants :

- **`id_user`** : Un entier qui représente l'identifiant unique de l'utilisateur (clé primaire).
- **`username`** : Une chaîne de caractères qui représente le nom d'utilisateur de l'utilisateur. Ce champ est unique et obligatoire.
- **`password`** : Une chaîne de caractères qui représente le mot de passe de l'utilisateur. Ce champ est obligatoire.
- **`id_role`** : Un entier qui représente l'identifiant du rôle de l'utilisateur (clé étrangère faisant référence à la table **`roles`**).

La méthode **`__repr__`** est définie pour afficher une représentation sous forme de chaîne de l'utilisateur, en affichant son nom d'utilisateur.

La classe **`Users`** comprend également les méthodes suivantes :

- **`set_password(password)`** : Cette méthode prend un mot de passe en paramètre et définit le mot de passe de l'utilisateur en utilisant le hachage bcrypt.
- **`check_password(password)`** : Cette méthode prend un mot de passe en paramètre et vérifie s'il correspond au mot de passe haché de l'utilisateur.

### Les API des services de la classe **`Users`** sont les suivantes :

- **`GET /user`** : Affiche la vue des utilisateurs.
- **`GET /user/ajout_user`** : Affiche la vue pour ajouter un nouvel utilisateur.
- **`POST /user/ajouter_user`** : Traite l'ajout d'un nouvel utilisateur à partir des données du formulaire.
- **`GET /user/action_user`** : Affiche la page d'action sur les utilisateurs, y compris la liste des utilisateurs existants.
- **`POST /user/suppression_user/<id_user>`** : Supprime un utilisateur avec l'identifiant spécifié.
- **`GET /user/modification_user/<id_user>`** : Affiche la vue pour modifier les informations d'un utilisateur spécifié.
- **`POST /user/id_user/<id>`** : Traite la modification des informations d'un utilisateur avec l'identifiant spécifié à partir des données du formulaire.

### Manuel d'utilisation :

1. Accéder à la page d'accueil de l'application.
2. Pour accéder à la vue des utilisateurs, accéder à l'URL **`/user`**. Il est nécessaire d'être authentifié en tant qu'administrateur pour accéder à cette vue.
3. Sur la vue des utilisateurs, vous pouvez choisir parmi différentes actions liées aux utilisateurs.
4. Pour ajouter un nouvel utilisateur, accéder à l'URL **`/user/ajout_user`** pour afficher le formulaire d'ajout.
5. Remplir tous les champs du formulaire (nom d'utilisateur, mot de passe et rôle) et soumettre le formulaire. L'utilisateur sera ajouté à la base de données.
6. Pour effectuer des actions sur les utilisateurs (suppression, modification), accéder à l'URL **`/user/action_user`**. Vous verrez la liste des utilisateurs existants et vous pourrez sélectionner l'action à effectuer.
7. Pour supprimer un utilisateur, cliquer sur le bouton de suppression correspondant à l'utilisateur que vous souhaitez supprimer. L'utilisateur sera supprimé de la base de données.
8. Pour modifier les informations d'un utilisateur, cliquer sur le bouton de modification correspondant à l'utilisateur que vous souhaitez modifier. Vous serez redirigé vers la vue de modification
</aside>

[data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2738%27%20height=%2738%27/%3e](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2738%27%20height=%2738%27/%3e)

[data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2738%27%20height=%2738%27/%3e](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%2738%27%20height=%2738%27/%3e)

## **Conclusion**

Cette documentation fournit une vue d'ensemble de l'API de gestion des visites, y compris les services offerts, les endpoints, les méthodes HTTP, les entrées et les sorties. En suivant le manuel d'utilisation, les utilisateurs pourront interagir avec l'API et gérer les visites aux détenus de manière efficace.
