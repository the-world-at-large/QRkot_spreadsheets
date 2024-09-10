from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from constants import COLUMN_NUMBER, ROW_NUMBER, SHEET_ID_NUMBER

FORMAT = '%Y/%m/%d %H:%M:%S'

SPREADSHEET_BODY = {
    'properties': {'title': '',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': SHEET_ID_NUMBER,
                               'title': 'Лист1',
                               'gridProperties': {
                                   'rowCount': ROW_NUMBER,
                                   'columnCount': COLUMN_NUMBER}}}],
}


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
) -> str:
    SPREADSHEET_BODY['properties']['title'] = (
        'Отчёт от {}'.format(datetime.now().strftime(FORMAT))
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle,
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id',
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle,
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчёт от', now_date_time],
        ['Рейтинг проектов по скорости выполнения'],
        ['Название проекта', 'Время выполнения проекта', 'Описание проекта']
    ]

    for proj in projects:
        new_row = [str(proj['name']),
                   str(proj['project_timeline']),
                   str(proj['description'])]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
