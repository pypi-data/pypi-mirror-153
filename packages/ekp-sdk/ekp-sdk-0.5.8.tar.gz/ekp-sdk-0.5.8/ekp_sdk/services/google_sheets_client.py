from ekp_sdk.services import CacheService
import os
from google.oauth2 import service_account
from apiclient import discovery


class GoogleSheetsClient:

    def __init__(
        self,
        credentials_file: str
        ):
        scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/spreadsheets"
        ]
        secret_file = os.path.join(os.getcwd(), credentials_file)
        credentials = service_account.Credentials.from_service_account_file(
            secret_file,
            scopes=scopes
        )
        self.service = discovery.build('sheets', 'v4', credentials=credentials)

    def get_range(self, sheet_id, range):
        sheet = self.service.spreadsheets()

        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=range
        ).execute()

        return result.get('values', [])
