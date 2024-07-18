from locust import HttpUser, task, between, TaskSet


class BaseUserBehavior(TaskSet):
    def on_start(self):
        self.email = ""
        self.club = "Simply Lift"

    @task
    def index(self):
        self.client.get(
            "/",
        )

    @task
    def show_summary(self):
        self.client.post(
            "showSummary",
            data={"email": "john@simplylift.co"},
        )

    @task
    def book_competition(self):
        self.client.get(
            f"book/JO/{self.club}",
        )

    @task
    def purchase_places(self):
        self.client.post(
            "purchasePlaces",
            data={
                "places": 0,
                "club": "Simply Lift",
                "competition": "JO",
            },
        )

    @task
    def points_board(self):
        self.client.get(
            "pointsBoard",
        )


class SimplyLiftUser(HttpUser):
    wait_time = between(1, 5)
    tasks = [BaseUserBehavior]

    def on_start(self):
        self.tasks[0].email = "john@simplylift.co"
        self.tasks[0].club = "Simply Lift"


class IronTempleUser(HttpUser):
    wait_time = between(1, 5)
    tasks = [BaseUserBehavior]

    def on_start(self):
        self.tasks[0].email = "admin@irontemple.com"
        self.tasks[0].club = "Iron Temple"


class SheLiftsUser(HttpUser):
    wait_time = between(1, 5)
    tasks = [BaseUserBehavior]

    def on_start(self):
        self.tasks[0].email = "kate@shelifts.co.uk"
        self.tasks[0].club = "She Lifts"
