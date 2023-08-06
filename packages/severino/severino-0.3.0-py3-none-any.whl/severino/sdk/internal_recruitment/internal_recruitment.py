from datetime import datetime

from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class Movement:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/internal-recruitment/movement"

    def create(
        self, from_stage_short_code: str, to_stage_short_code: str, candidate: str
    ):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "from_stage_short_code": from_stage_short_code,
                "to_stage_short_code": to_stage_short_code,
                "candidate": candidate,
            },
        )

    def read(self, movement_uuid: str):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{movement_uuid}/")

    def list(self):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/")

    def update(
        self,
        movement_uuid: str,
        from_stage_short_code: str,
        to_stage_short_code: str,
        candidate: str,
    ):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{movement_uuid}/",
            data={
                "from_stage_short_code": from_stage_short_code,
                "to_stage_short_code": to_stage_short_code,
                "candidate": candidate,
            },
        )

    def delete(self, movement_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{movement_uuid}/"
        )


class Stage:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/internal-recruitment/stage"

    def create(self, name: str, short_code: str, stage_id: int):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={"name": name, "short_code": short_code, "stage_id": stage_id},
        )

    def read(self, stage_uuid: str):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{stage_uuid}/")

    def read_by_short_code(self, short_code: str):
        return self.http.get(
            url=f"{self.severino_api_url}{self.path}/short-code/{short_code}/"
        )

    def list(self):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/")

    def update(self, stage_uuid: str, name: str, short_code: str, stage_id: int):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{stage_uuid}/",
            data={"name": name, "short_code": short_code, "stage_id": stage_id},
        )

    def delete(self, stage_uuid):
        return self.http.delete(url=f"{self.severino_api_url}{self.path}/{stage_uuid}/")


class MindsightReminder:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/internal-recruitment/mindsight-reminder"

    def create(
        self, candidate_id: str, reminders_sent: int, last_mail_sent_at: datetime
    ):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "candidate": candidate_id,
                "reminders_sent": reminders_sent,
                "last_mail_sent_at": last_mail_sent_at.strftime("%Y-%m-%d %H:%M:%S")
                if last_mail_sent_at
                else None,
            },
        )

    def read(self, reminder_uuid: str):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/{reminder_uuid}/")

    def list(self):
        return self.http.get(url=f"{self.severino_api_url}{self.path}/")

    def update(
        self,
        reminder_uuid: str,
        candidate_id: str,
        reminders_sent: int,
        last_mail_sent_at: datetime,
    ):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{reminder_uuid}/",
            data={
                "candidate": candidate_id,
                "reminders_sent": reminders_sent,
                "last_mail_sent_at": last_mail_sent_at.strftime("%Y-%m-%d %H:%M:%S")
                if last_mail_sent_at
                else None,
            },
        )

    def delete(self, reminder_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{reminder_uuid}/"
        )
