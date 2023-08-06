from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class Airflow:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/airflow/dag"

    def create(self, dag_id: str):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/", data={"dag_id": dag_id}
        )

    def read(self, dag_id: str):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{dag_id}/")

    def list(self):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/")

    def update(self, airflow_id: str, dag_id: str):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{airflow_id}/",
            data={"dag_id": dag_id},
        )

    def delete(self, airflow_id):
        return self.http.delete(url=f"{self.severino_api_url}{self.path}/{airflow_id}")
