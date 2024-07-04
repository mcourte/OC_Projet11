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
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    competition_date = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash(
            "Erreur : Vous ne pouvez pas réserver de place pour une compétition passée",
            "error",
            )
        return (
                render_template(
                    "welcome.html",
                    club=foundClub,
                    competitions=competitions,
                    clubs=clubs,
                ),
                400,
            )
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)
    # Rajouter une condition pour vérifié la date de la compétition. Si date passée : return error 400


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)
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
