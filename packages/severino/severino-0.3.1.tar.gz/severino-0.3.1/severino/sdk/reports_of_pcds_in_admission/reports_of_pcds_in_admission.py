from datetime import datetime

from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class ReminderReportsOfPcdsInAdmission:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/reports-of-pcds-in-admission/reminder"

    def create(
        self,
        candidate_id: str = "",
        candidate_name: str = "",
        candidate_cpf: str = "",
        status_code: str = "",
        status_name: str = "",
    ):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "candidate_cpf": candidate_cpf,
                "status_code": status_code,
                "status_name": status_name,
            },
        )

    def read(self, movement_uuid: str):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{movement_uuid}/")

    def list(self, filters: dict = {}):
        """List

        Args:
            filters (dict, optional): List of filters: candidate_id, candidate_cpf, status_code, status_name. E.g: {"candidate_cpf": "99999999999"}.

        Returns:
            _type_: _description_
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/", params=filters)

    def update(
        self,
        movement_uuid: str,
        last_mail_sent_at: datetime = None,
        reminders_sent: int = 0,
        candidate_id: str = "",
        candidate_name: str = "",
        candidate_cpf: str = "",
        status_code: str = "",
        status_name: str = "",
    ):
        data = {
            "candidate_id": candidate_id,
            "reminders_sent": reminders_sent,
            "candidate_name": candidate_name,
            "candidate_cpf": candidate_cpf,
            "status_code": status_code,
            "status_name": status_name,
        }

        if last_mail_sent_at:
            data["last_mail_sent_at"] = last_mail_sent_at

        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{movement_uuid}/",
            data=data,
        )

    def delete(self, movement_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{movement_uuid}/"
        )
