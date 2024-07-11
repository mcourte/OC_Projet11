from locust import HttpUser, task, between, TaskSet

class BaseUserBehavior(TaskSet):
    def on_start(self):
        self.email = ""
        self.club = ""
    
    @task
    def index(self):
        response = self.client.get("/")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @task
    def show_summary(self):
        response = self.client.post("/showSummary", {"email": self.email})
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    @task
    def book_competition(self):
        response = self.client.get(f"/book/JO/{self.club}")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    @task
    def purchase_places(self):
        response = self.client.post("/purchasePlaces", {
            "competition": "JO",
            "club": self.club,
            "places": "2"
        })
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    @task
    def points_board(self):
        response = self.client.get("/pointsBoard")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

class SimplyLiftUser(HttpUser):
    wait_time = between(1, 5)
    tasks = [BaseUserBehavior]

    def on_start(self):
        self.tasks[0].email = "simplylift@example.com"
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
