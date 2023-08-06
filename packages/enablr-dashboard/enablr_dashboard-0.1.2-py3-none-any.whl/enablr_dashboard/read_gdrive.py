import traceback

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from loguru import logger
import io
import shutil
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'security/simple-object-detector-5fe1e5265981.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

topFolderId = '1Abny-aJj6E0AmNYfRFU4BMrdyIJwDFBS'  # Please set the folder of the top folder ID.


def read_folder(top_folder_id):
    items = []
    pageToken = ""
    while pageToken is not None:
        response = service.files().list(q="'" + top_folder_id + "' in parents", pageSize=1000, pageToken=pageToken, fields="nextPageToken, files(id, name)").execute()
        items.extend(response.get('files', []))
        pageToken = response.get('nextPageToken')
    return items


def get_file(file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    logger.info("Downloading {}".format(file_name))
    while done is False:
        try:
            status, done = downloader.next_chunk()
            fh.seek(0)
            # Write the received data to the file
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)
            logger.info("Download %s %d%%." % (file_name, int(status.progress() * 100)))
        except Exception as err:
            logger.error(traceback.format_exc())
            logger.error(err)
            break
    return


def main(topFolderId, date_cutoff=None):
    logger.info("Start read gdrive")
    client_folders = read_folder(topFolderId)
    for row in client_folders:
        sub_folders = read_folder(row['id'])
        if sub_folders:
            try:
                os.mkdir("tmp/" + row['name'])
            except Exception as err:
                pass

            for data in sub_folders:
                # subfolder harusnya berisi tanggal
                file_ids = read_folder(data['id'])
                if file_ids:
                    if data['name'] != date_cutoff:
                        continue
                    new_date_folder = "tmp/" + row['name'] + "/" + date_cutoff
                    try:
                        os.mkdir(new_date_folder)
                    except Exception as err:
                        pass
                    for file in file_ids:
                        filename = "{}/{}/{}/{}".format("tmp", row['name'], data['name'], file['name'])
                        get_file(file['id'], filename)
                else:
                    filename = "{}/{}/{}".format("tmp", row['name'], data['name'])
                    get_file(data['id'], filename)
        else:
            filename = "{}/{}".format("tmp", row['name'])
            get_file(row['id'], filename)
    logger.info("Finish download all files")
    return


if __name__ == '__main__':
    main(topFolderId)
