from datetime import datetime

from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class VagasDotComBot:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/vagas-dot-com/bot"

    def create(
        self,
        vagas_job_id: int = "",
        gh_job_id: int = "",
        last_migration_at: datetime = "",
    ):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "vagas_job_id": vagas_job_id,
                "gh_job_id": gh_job_id,
                "last_migration_at": last_migration_at,
            },
        )

    def read(self, migration_uuid: str):
        return self.http.get(
            url=f"{self.severino_api_url}{self.path}/{migration_uuid}/"
        )

    def list(self, filters: dict = {}):
        """List

        Args:
            filters (dict, optional): List of filters: vagas_job_id, gh_job_id, last_migration_at E.g: {"vagas_job_id": 999999}.

        Returns:
            _type_: _description_
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/", params=filters)

    def update(
        self,
        migration_uuid: str,
        vagas_job_id: int = "",
        gh_job_id: int = "",
        last_migration_at: datetime = "",
    ):
        data = {
            "vagas_job_id": vagas_job_id,
            "gh_job_id": gh_job_id,
            "last_migration_at": last_migration_at,
        }

        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{migration_uuid}/",
            data=data,
        )

    def delete(self, migration_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{migration_uuid}/"
        )
