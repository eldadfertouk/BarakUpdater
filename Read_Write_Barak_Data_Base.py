import sys
import dbfpy3
from dbfread import DBF
import os
import requests
import read_barak_excel_file



LOCAL_DB_FOLDER = "Z:\\barak\\DATA-NEW\\"
DBFolder = 'C:\\Users\\Eldad\\Documents\\barak\\DATA\\'
DB_main_file_name = 'climain.DBF'
tb = DBFolder+DB_main_file_name
DB_files = []

BACKUP_SERVERS = {'TLV':'http://tlv1.terrasafe.com/obs/api/GetUser.do?',
                'MEDSAFE':'http://www.medsafe.co.il/obs/api/GetUser.do?',
                'BYNET':'http://www.terrasafe-binat.com/obs/api/GetUser.do?'}
payload = {'SysUser':'terrasafeobsadmin','SysPwd':'8$x3t%f7you','LoginName':'Apax'}
#my_table = Table(DB_file_name,encoding='cp850',px_encoding='ascii',px_decode_errors='strict')


def extract_data_from_record(reco,field):
    col_name = field
    record_set = []
    for r in reco:
        #print('FROM REC',r)
        record_set.append(r[col_name])
        #if s_rec.startswith('b\'.''              '):
         #   record_set.remove(reco.index(r))
            #d = s_rec
            #yield d
    return record_set


def str_to_int(s):
    #print("s: ",s)
    size = 0
    de = 1
    new_s = reversed(s.strip('"'))
    for c in new_s:
        m = ord(c)-48
        n = m * de
        size = size + n
        de *= 10
    return int(size)


def valid_respons(respo):
    return '<err>' in respo


def build_connection_string(reco):
    new_qouta_list = []
    con_str_list = []
    con_str_dict = {'srv-name':'MEDSAFE','data':'data'}
    for r in reco:
        login_name = str(r['PROD_SN'],'utf-8').strip(' ')
        dsrname = str(r['PROD_GRUP1'],'UTF-8').strip(' ')
        if dsrname == 'ZAHAV' or dsrname == 'OFEKCLOUD':
            pass
        elif dsrname == 'TLV' or dsrname == 'MEDSAFE' or dsrname == 'BYNET':
            srv_name = BACKUP_SERVERS[dsrname]
            payload['LoginName'] = login_name
            con_str_dict['srv-name'] = srv_name
            con_str_dict['data'] = payload
            con_str_list.append(con_str_dict)
        req = get_data(con_str_dict['srv-name'], con_str_dict['data'])
        values = req.split(' ')
        if len(values) > 7 :
            quota_value = values[8].split('=')
            s = quota_value[1]
            if len(s)>1:
                sint = str_to_int(s)
                #print(sint)
                new_qouta_list.append(sint)
            else:
                pass
        else:
            pass
    return new_qouta_list


def get_dbf_table_files():
    files_list = os.listdir(DBFolder)
    for f in files_list:
        if str(f).endswith('DBF'):
            DB_files.append(f)
    return DB_files


def remove_empty_fields_from_record_set(record_set):
    clean_record_set = []
    for rec in record_set:
        i = len(rec)
        txt = str(rec)
        while ' '*i not in txt:
            clean_record_set.append(txt)
    return clean_record_set


def get_table_records(path,db_file_name,*args,**kwargs):
    p = path
    fn = db_file_name
    while kwargs:
        current_tb_path = kwargs['path']+kwargs['db_file_name']
        rec = DBF(current_tb_path, load=True, encoding='UTF-8', char_decode_errors='strict', raw=True)
        print('Table fields: ',rec.fields)
        return rec
    current_tb_path = p+fn
    rec = DBF(current_tb_path,load=True,encoding='UTF-8',char_decode_errors='strict',raw=True)
    for field in rec.fields:
        print('FIELDS: ',field)
    #print('Table fields: ', rec.fields)
    my_rec = rec.records
    return my_rec



#for record in DBF(tb,load=True,char_decode_errors='strict',raw=True):
 #   print(record)

def remove_ofek_from_recorset(record_set):
    clean_record_set = record_set
    for t in record_set:
        if 'OFEK CLOUD' in t:
            clean_record_set.remove(t)
    return clean_record_set


def update_record(table_to_update,data,cul_name):
    local_table = table_to_update
    for r in local_table:
        rec_no = local_table.index(r)
        with local_table[rec_no] as upd_rec:
            upd_rec[cul_name] = data


def get_data(srv,user_data):
    server_name = srv
    payload = user_data
    try:
        resp = requests.post(server_name,params=payload)
        if valid_respons(resp):
            return 'USER NOT FOUND'
        else:
            return resp.text
    except ConnectionError as e:
        print(str(e))
    return e


def get_client_login_name():
    loin_dict = read_barak_excel_file.read_excel_hiyuv_file()
    return loin_dict


def create_list_of_tables():
    files_list = os.listdir(DBFolder)
    for f in files_list:
        if str(f).endswith('DBF'):
            DB_files.append(f)
    return DB_files


def gui_start():
    tabels_list = get_dbf_table_files()
    for fl in tabels_list:
        num = tabels_list.index(fl)
        print('tabels #: ',num,fl)
    tbn = 41
    tb_rec = get_table_records(DBFolder, tabels_list[tbn])
    return tb_rec


def main():
    tabels_list = get_dbf_table_files()
    for fl in tabels_list:
        num = tabels_list.index(fl)
        print('tabels #: ',num,fl)
    #tbn = int(input(print('choose table number')))
    tbn = 41 # todo: build button option to choose from
    tb_rec = get_table_records(DBFolder, tabels_list[tbn])
#    client_number_list = extract_data_from_record(tb_rec,'CLI_NO')
    c_s = build_connection_string(tb_rec)
    print(len(c_s))


if __name__ == "__main__":
    main()
