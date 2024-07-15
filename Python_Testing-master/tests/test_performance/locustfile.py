from locust import HttpUser, task, between, TaskSet


class BaseUserBehavior(TaskSet):
    def on_start(self):
        self.email = ""
        self.club = ""

    @task
    def index(self):
        with self.client.get("/", catch_response=True) as response:
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            assert response.elapsed.total_seconds() <= 5, f"Request took too long: {response.elapsed.total_seconds()}s"

    @task
    def show_summary(self):
        with self.client.post("/showSummary", {"email": self.email}, catch_response=True) as response:
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            assert response.elapsed.total_seconds() <= 2, f"Request took too long: {response.elapsed.total_seconds()}s"

    @task
    def book_competition(self):
        with self.client.get(f"/book/JO/{self.club}", catch_response=True) as response:
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            assert response.elapsed.total_seconds() <= 5, f"Request took too long: {response.elapsed.total_seconds()}s"

    @task
    def purchase_places(self):
        with self.client.post("/purchasePlaces", {
            "competition": "JO",
            "club": self.club,
            "places": "2"
        }, catch_response=True) as response:
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            assert response.elapsed.total_seconds() <= 2, f"Request took too long: {response.elapsed.total_seconds()}s"

    @task
    def points_board(self):
        with self.client.get("/pointsBoard", catch_response=True) as response:
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
            assert response.elapsed.total_seconds() <= 5, f"Request took too long: {response.elapsed.total_seconds()}s"


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
