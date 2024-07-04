import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():

    try:
        club = [
            club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
        )
    except IndexError:
        if request.form["email"] == "":
            flash("Veuillez entrer une adresse e-mail.", "error")
        else:
            flash("Il n'existe pas de compte rattaché à cet e-mail.", "error")
        return render_template("index.html"), 401


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Un problème est servenu, merci de réessayer")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            400)
    if foundClub and foundCompetition:
        competition_date = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
        if competition_date < datetime.now():
            flash("Erreur:Vous ne pouvez pas vous inscrire a une competition deja passee")
            return (render_template("welcome.html", club=foundClub, competitions=competitions),
                    200)
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Un problème est servenu, merci de réessayer")
        return (
            render_template("welcome.html", club=foundClub, competitions=competitions, clubs=clubs),
            400)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    placesRequired = int(request.form["places"])

    if placesRequired > 12:
        flash("Erreur : Vous ne pouvez pas vous inscrire plus de 12 athlètes à une compétition.")
        return (render_template("booking.html", club=club, competition=competition),403)
    
    competition["numberOfPlaces"] = (int(competition["numberOfPlaces"]) - placesRequired)
    club["points"] = int(club["points"]) - placesRequired
    
    flash("La réservation a été effectuée!")

    return render_template("welcome.html", club=club, competitions=competitions)
    # Rajouter des conditions pour :
    # empêcher de réserver plus de 12 places
    # empêcher de réserver plus de places qu'on a de points
    # empêcher de réserver un nombre de place négative
    # message d'erreur si nombre de place choisie = 0
    # empêcher de réserver plus de places qu'il y a de places disponible
    # !!! : si un club réserve une fois 9 places, il ne peut pas en réserver + de 3 derrière! Faire un historique ?
    # Rajouter la méthodo pour dimininuer le nombre de points du club


# Ajouter le tableau sur /showSummary qui indique le nombre de points restants pour chaque club


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
