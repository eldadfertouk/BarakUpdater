import requests
import xlrd
import read_barak_excel_file

SERVERS_DICT = {'TLV1':'http://tlv1.terrasafe.com/obs/api/GetUser.do?',
                'MedSafe':'http://www.medsafe.co.il/obs/api/GetUser.do?',
                'Bynet':'http://www.terrasafe-binat.com/obs/api/GetUser.do?'}

MEDSAFE_SERVER_URL = 'http://www.medsafe.co.il/obs/api/GetUser.do?'

BINAT_SERVER_URL = 'http://www.terrasafe-binat.com/obs/api/GetUser.do?'

TLV1_SERVER_URL = 'http://tlv1.terrasafe.com/obs/api/GetUser.do?'

payload = {'SysUser':'terrasafeobsadmin','SysPwd':'8$x3t%f7you','LoginName':'Apax'}



def get_data(server_name='http://www.medsafe.co.il/obs/api/GetUser.do?'):
    r=requests.post(server_name,params=payload)
    print(r.text)



def get_client_login_name():
    loin_dict = read_barak_excel_file.read_excel_hiyuv_file()
    return loin_dict



def main():
    #todo: create gui
    #todo: get user options
    #print('choose server\n')
    #print('\nMED '+MEDSAFE_SERVER_URL,'\nTERRA '+TLV1_SERVER_URL,'\nBINAT '+BINAT_SERVER_URL)
    get_data()


if __name__ == "__main__":
    main()



