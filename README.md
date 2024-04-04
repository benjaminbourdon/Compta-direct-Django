# Compta Direct Django

Site web Django destiné à proposer une interface permettant l'import de données comptables
depuis l'outil AssoConnect. En particulier, l'objectif est d'assurer le suivi des comptes
auxiliaires débiteurs et de suivre les relances avec envoi de courriels aux personnes
concernées.

## Paramétrage

Votre compte d'envoi de courriel (serveur SMTP) doit être indiqué dans le fichier settings.py
du dossier intranet_compta.
Les informations suivantes sont requises :
- EMAIL_HOST
- EMAIL_PORT 
- EMAIL_HOST_USER 
- EMAIL_HOST_PASSWORD 
Il est conseillé d'utiliser un fournisseur externe (SendInBleu ou autre) 
pour une meilleur délivrabilité. 

## Mise en route

Les dépendances sont disponibles dans le fichier Pipfile. 
Elles peuvent être installée avec la commande pipenv install.

Le serveur Django peut être lancé avec la commande 
python .\manage.py runserver

Lors de la première utilisation, la base de données doit être mise à jour avec
python .\manage.py migrate

## Page principales

- /admin pour le panneau d'admin
- /list pour lister les membres et leur situation comptable
- /import pour importer les données exportées depuis AssoConnect
    + liste des membres au format .csv
    + liste des transactions 
        depuis la page web d'Assoconnect, transformé en .json à l'aide d'un script JS
        disponible dans le dossier tools
    + liste des balances initiales au format .csv
- /debt pour envoyer un courriel de rappel aux personnes sélectionnées
    + le template de courriel est actuellement "en dur" :
    suivi_operations/templates/suivi_operations/emails/debt_message.html