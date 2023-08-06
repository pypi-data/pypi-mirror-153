from datetime import datetime

from severino.sdk.helpers.http_requests import Http
from severino.settings import SEVERINO_API_URL


class RescissionWorkflow:
    def __init__(self):
        self.http = Http()
        self.severino_api_url = SEVERINO_API_URL
        self.path = "/rescission-workflow"

    def create(
        self,
        process_code: int = None,
        process_status: int = None,
        start_date: datetime = None,
        completion_date: datetime = None,
        applicant_name: str = None,
        target_company_code: int = None,
        target_enrollment: int = None,
        target_name: str = None,
        effective_position_description: str = None,
        rescission_date: datetime = None,
        notice_date: datetime = None,
        target_admission_date: datetime = None,
        code_reason_rescission: int = None,
        activity_name: str = None,
        recision_time: datetime = None,
        face_to_face_communication: str = None,
        email_corp_witness_1: str = None,
        email_corp_witness_2: str = None,
        workplace: str = None,
        zip_code: str = None,
        complete_address: str = None,
        private_email: str = None,
        private_phone: str = None,
        corporate_cell_phone: str = None,
        corporate_email: str = None,
        return_computer: bool = None,
        return_chair: bool = None,
        return_other_items: bool = None,
        access_data_center: bool = None,
        servicenow_sys_id: str = None,
        servicenow_ticket_number: str = None,
    ):
        return self.http.post(
            url=f"{self.severino_api_url}{self.path}/",
            data={
                "process_code": process_code,
                "process_status": process_status,
                "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
                "completion_date": completion_date.strftime("%Y-%m-%d")
                if completion_date
                else None,
                "applicant_name": applicant_name,
                "target_company_code": target_company_code,
                "target_enrollment": target_enrollment,
                "target_name": target_name,
                "effective_position_description": effective_position_description,
                "rescission_date": rescission_date.strftime("%Y-%m-%d")
                if rescission_date
                else None,
                "notice_date": notice_date.strftime("%Y-%m-%d")
                if notice_date
                else None,
                "target_admission_date": target_admission_date.strftime("%Y-%m-%d")
                if target_admission_date
                else None,
                "code_reason_rescission": code_reason_rescission,
                "activity_name": activity_name,
                "recision_time": recision_time.strftime("%Y-%m-%d %H:%M:%S")
                if recision_time
                else None,
                "face_to_face_communication": face_to_face_communication,
                "email_corp_witness_1": email_corp_witness_1,
                "email_corp_witness_2": email_corp_witness_2,
                "workplace": workplace,
                "zip_code": zip_code,
                "complete_address": complete_address,
                "private_email": private_email,
                "private_phone": private_phone,
                "corporate_cell_phone": corporate_cell_phone,
                "corporate_email": corporate_email,
                "return_computer": return_computer,
                "return_chair": return_chair,
                "return_other_items": return_other_items,
                "access_data_center": access_data_center,
                "servicenow_sys_id": servicenow_sys_id,
                "servicenow_ticket_number": servicenow_ticket_number,
            },
        )

    def read(self, rescission_uuid: str):
        return self.http.get(
            url=f"{self.severino_api_url}{self.path}/{rescission_uuid}/"
        )

    def list(self, filters: dict = {}):
        """List

        Args:
            filters (dict, optional): List of filters: private_email, private_phone, corporate_cell_phone, corporate_email, servicenow_sys_id, servicenow_ticket_number. E.g: {"private_email": "severino@gmail.com"}
        """
        return self.http.get(url=f"{self.severino_api_url}{self.path}/", params=filters)

    def update(
        self,
        rescission_uuid: str,
        process_code: int = None,
        process_status: int = None,
        start_date: datetime = None,
        completion_date: datetime = None,
        applicant_name: str = None,
        target_company_code: int = None,
        target_enrollment: int = None,
        target_name: str = None,
        effective_position_description: str = None,
        rescission_date: datetime = None,
        notice_date: datetime = None,
        target_admission_date: datetime = None,
        code_reason_rescission: int = None,
        activity_name: str = None,
        recision_time: datetime = None,
        face_to_face_communication: str = None,
        email_corp_witness_1: str = None,
        email_corp_witness_2: str = None,
        workplace: str = None,
        zip_code: str = None,
        complete_address: str = None,
        private_email: str = None,
        private_phone: str = None,
        corporate_cell_phone: str = None,
        corporate_email: str = None,
        return_computer: bool = None,
        return_chair: bool = None,
        return_other_items: bool = None,
        access_data_center: bool = None,
        servicenow_sys_id: str = None,
        servicenow_ticket_number: str = None,
    ):
        return self.http.put(
            url=f"{self.severino_api_url}{self.path}/{rescission_uuid}/",
            data={
                "process_code": process_code,
                "process_status": process_status,
                "start_date": start_date.strftime("%Y-%m-%d") if start_date else None,
                "completion_date": completion_date.strftime("%Y-%m-%d")
                if completion_date
                else None,
                "applicant_name": applicant_name,
                "target_company_code": target_company_code,
                "target_enrollment": target_enrollment,
                "target_name": target_name,
                "effective_position_description": effective_position_description,
                "rescission_date": rescission_date.strftime("%Y-%m-%d")
                if rescission_date
                else None,
                "notice_date": notice_date.strftime("%Y-%m-%d")
                if notice_date
                else None,
                "target_admission_date": target_admission_date.strftime("%Y-%m-%d")
                if target_admission_date
                else None,
                "code_reason_rescission": code_reason_rescission,
                "activity_name": activity_name,
                "recision_time": recision_time.strftime("%Y-%m-%d %H:%M:%S")
                if recision_time
                else None,
                "face_to_face_communication": face_to_face_communication,
                "email_corp_witness_1": email_corp_witness_1,
                "email_corp_witness_2": email_corp_witness_2,
                "workplace": workplace,
                "zip_code": zip_code,
                "complete_address": complete_address,
                "private_email": private_email,
                "private_phone": private_phone,
                "corporate_cell_phone": corporate_cell_phone,
                "corporate_email": corporate_email,
                "return_computer": return_computer,
                "return_chair": return_chair,
                "return_other_items": return_other_items,
                "access_data_center": access_data_center,
                "servicenow_sys_id": servicenow_sys_id,
                "servicenow_ticket_number": servicenow_ticket_number,
            },
        )

    def delete(self, rescission_uuid):
        return self.http.delete(
            url=f"{self.severino_api_url}{self.path}/{rescission_uuid}/"
        )
