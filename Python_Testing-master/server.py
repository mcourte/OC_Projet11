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
    if placesRequired < 0:
        flash("Erreur : Vous ne pouvez pas vous inscrire un nombre d'athletes negatif.")
        return render_template("booking.html", club=club, competition=competition), 403
    if placesRequired == 0:
        flash("Erreur : Vous ne pouvez pas vous inscrire un nombre d'athletes nul.")
        return render_template("booking.html", club=club, competition=competition), 403
    if placesRequired > int(club['points']):
        flash("Erreur : Vous n'avez pas assez de points disponible.")
        return render_template("booking.html", club=club, competition=competition), 403
    if placesRequired > 12:
        flash("Erreur : Vous ne pouvez pas inscrire plus de 12 athletes a une competition.")
        return render_template("booking.html", club=club, competition=competition), 403

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    club["points"] = int(club["points"]) - placesRequired

    with open("clubs.json", "w") as f:
        json.dump({"clubs": clubs}, f, indent=4)

    flash("La réservation a été effectuée!")
    return render_template("welcome.html", club=club, competitions=competitions)

    # Rajouter des conditions pour :
    # !!! : si un club réserve une fois 9 places, il ne peut pas en réserver + de 3 derrière! Faire un historique ?

@app.route("/pointsBoard")
def pointsBoard():
    """
    Display the points board.
    """
    club_list = sorted(clubs, key=lambda club: int(club["points"]), reverse=True)
    return render_template("pointsBoard.html", clubs=club_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
