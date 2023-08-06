from severino.sdk.store_data import StoreData


class StoreDataTmp(StoreData):
    def __init__(self):
        super().__init__()
        self.path = "/store-data/store/tmp/"

    def create(self, airflow_dag_id: str, json_data: dict, runtime_id: str = ""):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}",
            data={
                airflow_dag_id: airflow_dag_id,
                json_data: json_data,
                runtime_id: runtime_id,
            },
        )
