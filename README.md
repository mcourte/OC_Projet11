# Projet 11 : Améliorez une application Web Python par des tests et du débogage

[Schéma tests](https://lucid.app/lucidspark/36ed9325-f267-4986-a95a-eca7be2086e0/edit?viewport_loc=-951%2C2174%2C5754%2C2703%2C0_0&invitationId=inv_b9491f15-a409-45ab-9b92-694c9e19d640)
  

Nota : il est OBLIGATOIRE de créer un compte sur LucidApp pour avoir accès aux différents fichiers.  
  


## Etape 1 : Télécharger le code

Cliquer sur le bouton vert "<> Code" puis sur Download ZIP.  
Extraire l'ensemble des éléments dans le dossier dans lequel vous voulez stockez les datas qui seront téléchargées.  


## Etape 2 ; Installer Python et ouvrir le terminal de commande

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :  
Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   


## Etape 3 : Création de l'environnement virtuel

Se placer dans le dossier où l'on a extrait l'ensemble des documents grâce à la commande ``cd``  
Exemple :
```
cd home/magali/OpenClassrooms/Formation/Projet_4
```


Dans le terminal de commande, executer la commande suivante :
```
python3 -m venv env
```


Activez l'environnement virtuel
```
source env/bin/activate
```
> Pour les utilisateurs de Windows, la commande est la suivante : 
> ``` env\Scripts\activate.bat ```

## Etape 4 : Télécharger les packages nécessaires au bon fonctionnement du programme

Dans le terminal, taper la commande suivante :
```
pip install -r requirements.txt
```

## Etape 5 : Lancer le programme

Dans le terminal, taper la commande suivante : 

```
flask run
```

Cliquer sur le lien qui s'affiche dans le terminal

## Etape 6 : Utilisateurs

Il existe trois clubs qui sont inscrits actuellement sur le site, pour vous connecter, entrer l'une des trois adresses e-mail suivantes :  

- john@simplylift.co

- admin@irontemple.com

- kate@shelifts.co.uk


Nota : le nombre de points de chaque clubs, et le nombre de place disponible diminuent dans les JSON.  
Si vous voulez remettre les données à jour, voici les données de bases :  

```
{
    "clubs": [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "12"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "25"
        }
    ]
}
```  

```
{
    "competitions": [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "JO",
            "date": "2025-10-22 13:30:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "CDM de Crossfit",
            "date": "2024-10-26 13:30:00",
            "numberOfPlaces": "24"
        }
    ]
}
```

