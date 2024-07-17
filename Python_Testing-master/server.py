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


def get_future_competitions(competitions):
    now = datetime.now()
    return [comp for comp in competitions if datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S") > now]


def get_past_competitions(competitions):
    now = datetime.now()
    return [comp for comp in competitions if datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S") <= now]


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
        club = next(club for club in clubs if club["email"] == request.form["email"])
    except StopIteration:
        if request.form["email"] == "":
            flash("Veuillez entrer une adresse e-mail.", "error")
        else:
            flash("Il n'existe pas de compte rattache a cet e-mail.", "error")
        return render_template("index.html"), 401
    future_competitions = get_future_competitions(competitions)
    past_competitions = get_past_competitions(competitions)
    return render_template(
            "welcome.html",
            club=club,
            future_competitions=future_competitions,
            past_competitions=past_competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = next(c for c in clubs if c["name"] == club)

        foundCompetition = next(c for c in competitions if c["name"] == competition)
    except StopIteration:
        flash("Un probleme est survenu, merci de reessayer", "error")
        return (
            render_template("welcome.html", club=club, competitions=get_future_competitions(competitions)),
            400)
    if foundClub and foundCompetition:
        competition_date = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S")
        if competition_date < datetime.now():
            flash("Erreur : Vous ne pouvez pas vous inscrire a une competition deja passee", "error")
            return (render_template("welcome.html", club=foundClub,
                                    competitions=get_future_competitions(competitions)), 404)

        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Un probleme est survenu, merci de reessayer", "error")
        return (
            render_template("welcome.html", club=foundClub, competitions=get_future_competitions(competitions)), 400)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
        club = next((c for c in clubs if c['name'] == request.form['club']), None)

        if not competition or not club:
            flash("Erreur : Compétition ou club invalide.")
            return (render_template("welcome.html", club=club, competitions=get_future_competitions(competitions)),
                    400)

        placesRemaining = int(competition["numberOfPlaces"])
        placesRequired = int(request.form["places"])

        # Initialize or retrieve the total places reserved for this club
        if 'club_booking' not in competition:
            competition['club_booking'] = {}

        club_booking = competition['club_booking']
        PlacesReserved = club_booking.get(club['name'], 0)

        if placesRequired <= 0:
            flash("Erreur : Vous ne pouvez pas réserver un nombre d'athlètes négatif ou nul.", "error")
            return render_template("booking.html", club=club, competition=competition), 403

        if placesRequired > int(club['points']):
            flash("Erreur : Vous n'avez pas assez de points disponibles.", "error")
            return render_template("booking.html", club=club, competition=competition), 403

        if placesRequired > placesRemaining:
            flash("Erreur : Il ne reste pas assez de places disponibles dans la compétition.", "error")
            return render_template("booking.html", club=club, competition=competition), 403

        if placesRequired > 12:
            flash("Erreur : Vous ne pouvez pas réserver plus de 12 athlètes à une compétition.", "error")
            return render_template("booking.html", club=club, competition=competition), 403

        if PlacesReserved + placesRequired > 12:
            flash("Erreur : Vous ne pouvez pas réserver plus de 12 athlètes au total pour cette compétition.", "error")
            return render_template("booking.html", club=club, competition=competition), 403

        # Deduct points and update remaining places
        club['points'] = int(club['points']) - placesRequired
        competition['numberOfPlaces'] = placesRemaining - placesRequired

        # Update the club_booking dictionary
        club_booking[club['name']] = PlacesReserved + placesRequired
        competition['club_booking'] = club_booking

        with open("clubs.json", "w") as f:
            json.dump({"clubs": clubs}, f, indent=4)
        with open("competitions.json", "w") as f:
            json.dump({"competitions": competitions}, f, indent=4)

        flash("Super! Réservation enregistrée", "error")
        future_competitions = get_future_competitions(competitions)
        past_competitions = get_past_competitions(competitions)
        return render_template(
            "welcome.html",
            club=club,
            future_competitions=future_competitions,
            past_competitions=past_competitions)
    except Exception as e:
        flash(f"Erreur inattendue: {str(e)}", "error")
        return render_template("welcome.html", club=club, competitions=get_future_competitions(competitions)), 500


@app.route("/pointsBoard")
def pointsBoard():
    """
    Display the points board.
    """
    club_list = sorted(clubs, key=lambda club: int(club["points"]), reverse=True)
    return render_template("points_board.html", clubs=club_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
