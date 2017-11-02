from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# install PyDrive : pip install PyDrive
# need to store client_secrets in the same working directory

gauth = GoogleAuth()
gauth.LocalWebServerAuth()

drive = GoogleDrive(gauth)
# search for files with titles contain 'production_xmldata*'
for file_list in drive.ListFile({'q': 'title contains "production_xmldata"'}):
    for file in file_list:
        #download file - keep its original name
	file.GetContentFile(file['title'])
