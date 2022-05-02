import os
def userHomeDir():
    return str(Path.home())

# Server constants
SERVER_IP = '127.0.0.1'
SERVER_PORT = 41000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
SERVER_BUFFER_SIZE = 65536

# Gui Combo boxes values
REPORT_OUT_PATH = os.path.join('html', 'index.html')
COMBOBOX_BACKUP_SERVER=["TLV1","MEDSAFE","BYNET"]
LOCAL_DB_FOLDER = "Z:\\barak\\DATA-NEW\\"
DBFolder = 'C:\\Users\\Eldad\\Documents\\barak\\DATA\\'
DB_main_file_name = 'climain.DBF'
DB_file_name = 'climain.dbf'
TB = DBFolder+DB_file_name #full path to db file include db file
DB_files = []