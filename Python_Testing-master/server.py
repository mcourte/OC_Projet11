import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


# Charge la liste des clubs
def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


# Charge la liste des compétitions
def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


# Selectionne les compétitions à venir : date > date du jour
def get_future_competitions(competitions):
    now = datetime.now()
    return [
        comp
        for comp in competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") > now
    ]


# Selectionne les compétitions passées : date < date du jour
def get_past_competitions(competitions):
    now = datetime.now()
    return [
        comp
        for comp in competitions
        if datetime.strptime(comp["date"], "%Y-%m-%d %H:%M:%S") <= now
    ]


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    """Permet de se connecter ou d'afficher le Tableau des points"""
    return render_template("index.html")


@app.route("/showSummary", methods=["POST", "GET"])
def show_summary():
    """Permet de voir les compétitions & d'être redigérer vers la page de réservation"""
    if request.method == "GET":
        return redirect(url_for("index"))
    try:
        club = [
            club for club in clubs if club["email"] == request.form["email"]
        ][0]
        future_competitions = get_future_competitions(competitions)
        past_competitions = get_past_competitions(competitions)
        return render_template(
            "welcome.html",
            club=club,
            future_competitions=future_competitions,
            past_competitions=past_competitions,
        )
    except IndexError:
        if request.form["email"] == "":
            flash("Veuillez entrer une adresse e-mail.", "error")
        else:
            flash("Il n'existe pas de compte rattache a cet e-mail.", "error")
        return render_template("index.html"), 401


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Permet de choisir le nombre de place que l'on veut réserver"""
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [
            c for c in competitions if c["name"] == competition
        ][0]
    except IndexError:
        flash("Un probleme est survenu, merci de reessayer")
        return (
            render_template(
                "welcome.html",
                club=club,
                competitions=get_future_competitions(competitions),
            ),
            400,
        )
    if foundClub and foundCompetition:
        competition_date = datetime.strptime(
            foundCompetition["date"], "%Y-%m-%d %H:%M:%S"
        )
        if competition_date < datetime.now():
            flash(
                "Erreur : Vous ne pouvez pas vous inscrire a une competition deja passee"
            )
            return (
                render_template(
                    "welcome.html",
                    club=foundClub,
                    competitions=get_future_competitions(competitions),
                ),
                200,
            )

        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Un probleme est survenu, merci de reessayer")
        return (
            render_template(
                "welcome.html",
                club=foundClub,
                competitions=get_future_competitions(competitions),
            ),
        )


@app.route("/purchasePlaces", methods=["POST", "GET"])
def purchasePlaces():
    """Permet de valider le nombre de place que l'user veut réserver"""
    if request.method == "GET":
        return redirect(url_for("index"))
    competition = next(
        (c for c in competitions if c["name"] == request.form["competition"]),
        None,
    )
    club = next((c for c in clubs if c["name"] == request.form["club"]), None)

    if not competition or not club:
        flash("Erreur : Compétition ou club invalide.")
        return (
            render_template(
                "welcome.html",
                club=club,
                competitions=get_future_competitions(competitions),
            ),
            400,
        )

    placesRemaining = int(competition["numberOfPlaces"])
    placesRequired = int(request.form["places"])

    # Si pas de places déjà reservée par le club, initialise à 0
    if "club_booking" not in competition:
        competition["club_booking"] = {}

    club_booking = competition["club_booking"]
    PlacesReserved = club_booking.get(club["name"], 0)

    if placesRequired < 0:
        flash(
            "Erreur : Vous ne pouvez pas réserver un nombre d'athlètes négatif."
        )
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            403,
        )

    if placesRequired > int(club["points"]):
        flash("Erreur : Vous n'avez pas assez de points disponibles.")
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            403,
        )

    if placesRequired > placesRemaining:
        flash(
            "Erreur : Il ne reste pas assez de places disponibles dans la compétition."
        )
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            403,
        )

    if placesRequired > 12:
        flash(
            "Erreur : Vous ne pouvez pas réserver plus de 12 athlètes à une compétition."
        )
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            403,
        )

    if PlacesReserved + placesRequired > 12:
        flash(
            "Erreur : Vous ne pouvez pas réserver plus de 12 athlètes au total pour cette compétition."
        )
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            403,
        )

    # Déduit le nombre de points du club & les places restantes dans la compétition
    club["points"] = int(club["points"]) - placesRequired
    competition["numberOfPlaces"] = placesRemaining - placesRequired

    # Met à jour le nombre de place déjà reservée par le club
    club_booking[club["name"]] = PlacesReserved + placesRequired
    competition["club_booking"] = club_booking

    # Sauvegarde les nouvelles valeurs dans les JSON
    with open("clubs.json", "w") as f:
        json.dump({"clubs": clubs}, f, indent=4)
    with open("competitions.json", "w") as f:
        json.dump({"competitions": competitions}, f, indent=4)

    future_competitions = get_future_competitions(competitions)
    past_competitions = get_past_competitions(competitions)

    flash("Super! Réservation enregistrée")
    return render_template(
        "welcome.html",
        club=club,
        future_competitions=future_competitions,
        past_competitions=past_competitions,
    )


@app.route("/pointsBoard")
def pointsBoard():
    """
    Display the points board.
    """
    club_list = sorted(
        clubs, key=lambda club: int(club["points"]), reverse=True
    )
    return render_template("points_board.html", clubs=club_list)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
