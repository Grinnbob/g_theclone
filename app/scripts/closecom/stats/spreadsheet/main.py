import gspread
from app.core.config import settings
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import pandas as pd
from app.scripts.globals import *
# 'https://docs.google.com/spreadsheets/d/1qiDMg0gKzA2ebZ54gnArakCjPDGQTEhkBBrTOPrzgn4/'

class GspreadProvider():
    def __init__(self):
        self.service = gspread.service_account_from_dict(info=settings.PUB_SUB_KEY)

    def create(self, customer):
        self.spreadsheet = self.service.create(f"{customer}-outreach-stats")

        print(f"SPREADSHEET CREATED for {customer}  url={self.spreadsheet.url}")
        self.spreadsheet.share('ks.shilov@gmail.com', perm_type='user', role='writer')

    def open(self, url):
        self.spreadsheet = self.service.open_by_url(url)
        print(f"SPREADSHEET OPENED  url={self.spreadsheet.url}")

    def update(self,
               sheet_title,
               data):
        if not self.spreadsheet:
            raise Exception("Call open/create spreadsheet first")

        sheet = self._create_or_clear(sheet_title)

        if isinstance(data, list):
            count = 1
            for d in data:
                set_with_dataframe(sheet,
                                   d,
                                   row=count,
                                   include_index=True)
                count = count + len(d.index) + 3
        else:
            set_with_dataframe(sheet,
                               data,
                               include_index=True)

        print(f"{sheet_title} updated")

    def _create_or_clear(self,
                         sheet_title):

        sheet = None

        try:
            sheet = self.spreadsheet.worksheet(sheet_title)
            if sheet:
                sheet.clear()
        except Exception as e:
            print(str(e))
            sheet = self.spreadsheet.add_worksheet(title=sheet_title, rows="1000", cols="100")

        return sheet

async def update_spreadsheet(customer,
                             total_dataframe,
                             daily_dataframe,
                             best_sequences_dataframe,
                             sequence_dataframe,
                             best_segments_dataframe,
                             segment_dataframe,
                             emails_dataframe):

    provider = GspreadProvider()
    url = customer_to_spreadsheet.get(customer, None)
    if not url:
        provider.create(customer)
    else:
        provider.open(url)

    provider.update(sheet_title="total",
                    data=total_dataframe)

    provider.update(sheet_title="daily",
                    data=daily_dataframe)

    provider.update(sheet_title="sequences total",
                    data=best_sequences_dataframe)

    provider.update(sheet_title="sequences/templates",
                    data=sequence_dataframe)

    provider.update(sheet_title="segments total",
                    data=best_segments_dataframe)

    provider.update(sheet_title="segments/sequences/templates",
                    data=segment_dataframe)

    provider.update(sheet_title="emails",
                    data=emails_dataframe)
