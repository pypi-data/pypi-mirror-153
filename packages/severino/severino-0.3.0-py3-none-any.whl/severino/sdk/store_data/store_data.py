from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class StoreData:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/store-data/store"

    def create(self, airflow_dag_id: str, json_data: dict):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={"airflow_dag_id": airflow_dag_id, "json_data": json_data},
        )

    def read(self, store_data_id: str):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{store_data_id}/")

    def update(self, store_data_id: str, airflow_dag_id: str, json_data: dict):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{store_data_id}/",
            data={"airflow_dag_id": airflow_dag_id, "json_data": json_data},
        )

    def delete(self, store_data_id):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{store_data_id}"
        )
