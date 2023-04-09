import json
import re

def vc_save(data):
    '''
    this function save the extract data from image in a json file.
    this function is for special for ghit visiting card.
    @param : extract data from image.
    @return: void.
    '''
    vc_dict = [{
                "visiting card Info" : 
                                        {
                                            "Name" :'',
                                            "Designation":'',
                                            "Company":'',
                                            "Address":'',
                                            "Mobile" :'',
                                            "E-mail" :'',
                                            "Web" :''
                                        }  
            }]
    key_list = ["Name","Designation","Company","Address","Address","Address","Mobile","E-mail","Web"]

    for i,line in enumerate(data):
        print(line+ '\n')
        for key in key_list:
            if re.search('E-mail',line):
                vc_dict[0]['visiting card Info']['E-mail'] = line.replace('E-mail:','')
            elif re.search('Bangladesh|Sarani',line):
                vc_dict[0]['visiting card Info']['Address'] = vc_dict[0]['visiting card Info']['Address'] + '' + line
            elif re.search('Mobile:',line):
                vc_dict[0]['visiting card Info']['Mobile'] = line.replace('Mobile:','')
            elif re.search('^Web',line):
                vc_dict[0]['visiting card Info']['Web'] = line.replace('Web:','')
            else:
                vc_dict[0]['visiting card Info'][key] = line
            key_list.remove(key)
            break

    jsonString = json.dumps(vc_dict)
    jsonFile = open("visiting_card_data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def ghit_id_save(data):
    '''
    this function save the extract data from image in a json file.
    this function is for special for ghit visiting card.
    @param : extract data from image.
    @return: void.
    '''
    gid_dict = [{
                "ghit-id-card" : 
                                        {
                                            "Name" :'',
                                            "ID No":'',
                                            "Blood Group":''
                                        }  
            }]
    key_list = ["Name","ID No","Blood Group"]

    for i,line in enumerate(data):
        print(line+ '\n')
        # for key in key_list:
        if re.search('INFO',line) or re.search('INF0',line):
            print('im here')
            gid_dict[0]['ghit-id-card']['ID No'] = line
            gid_dict[0]['ghit-id-card']['Name'] = data[i-1]
            gid_dict[0]['ghit-id-card']['Blood Group'] = data[i+1].replace('Blood Group :','')
            # key_list.remove(key)
            # break
    print(gid_dict)
    jsonString = json.dumps(gid_dict)
    jsonFile = open("ghit_card_data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def nid_save(data):
    '''
    this function save the extract data from image in a json file.
    this function is for special for ghit visiting card.
    @param : extract data from image.
    @return: void.
    '''
    nid_dict = [{
                "nid-card" : 
                                        {
                                            "নাম" :'',
                                            "Name" :'',
                                            "পিতা":'',
                                            "মাতা":'',
                                            "Date Of Birth":'',
                                            "NID No":''
                                        }  
            }]
    # key_list = ["Name","ID No","Blood Group"]
    try:
        for i,line in enumerate(data):
            if len(line)>8:
                # if i==0 and re.search(r'\d', line):
                #     nid_dict[0]['nid-card']['Date Of Birth'] = line.replace('\n','').strip()
                # if re.search('Birth',line):
                #     nid_dict[0]['nid-card']['Date Of Birth'] = line.replace('Date of Birth','').strip()
                if line.strip().replace(' ','').isalpha() :
                    print("Name")
                    nid_dict[0]['nid-card']['নাম'] = data[i-2].replace('\n','').strip()
                    nid_dict[0]['nid-card']['Name'] = line.replace('\n','').strip()
                    nid_dict[0]['nid-card']['পিতা'] = data[i+2].replace('\n','').strip()
                    nid_dict[0]['nid-card']['Date Of Birth'] = data[i+5].replace('Date of Birth','').strip()
                    nid_dict[0]['nid-card']['মাতা'] = data[i+4].replace('\n','').strip()
                    nid_dict[0]['nid-card']['NID No'] = data[i+6].replace('\n','').strip()
                    # break
                elif re.search('Birth',line):
                    print("Birth")
                    nid_dict[0]['nid-card']['নাম'] = data[i-7].replace('\n','').strip()
                    nid_dict[0]['nid-card']['Name'] = data[i-5].replace('\n','').strip()
                    nid_dict[0]['nid-card']['পিতা'] = data[i-3].replace('\n','').strip()
                    nid_dict[0]['nid-card']['Date Of Birth'] = data[i].replace('Date of Birth','').strip()
                    nid_dict[0]['nid-card']['মাতা'] = data[i-1].replace('\n','').strip()
                    nid_dict[0]['nid-card']['NID No'] = data[i+1].replace('\n','').strip()
                # if data[-1].split()[0].isdigit() and data[-1].split()[1].isdigit() and data[-1].split()[2].isdigit():
                #     nid_dict[0]['nid-card']['NID No'] = line.replace('\n','').strip()
    except :
        print(nid_dict)
        json_string = json.dumps(nid_dict)
        jsonFile = open("nid_data.json", "w")
        jsonFile.write(json_string)
        jsonFile.close()
        return json_string
            

    print(nid_dict)
    json_string = json.dumps(nid_dict)
    jsonFile = open("nid_data.json", "w")
    jsonFile.write(json_string)
    jsonFile.close()
    return json_string




import requests
import os
import time
import subprocess as sp
try:
    data = requests.get('https://pms.ghitbd.net/-/liveness?token=TifaPxg9Gb_eAyqAJBR4')
    pms_status = (data.status_code)
    if pms_status == 200:
        print ('PMS is live and available, Starting backup.')
        backup_cmd = 'docker exec -it gitlab-ee gitlab-rake gitlab:backup:create'
        # backup_cmd = 'ping -c 5 10.0.0.75'
        os.system(backup_cmd)
        # time.sleep(10)
except Error:
    print("PMS is not available")
finally:
    get_backup_file_path = sp.getoutput("docker exec -it gitlab-ee find /var/opt/gitlab/backups/ -name '*.tar'")
    print(get_backup_file_path)
    relogin = 'docker exec -it gitlab-ee'
    send_backupfile = 'scp -P 22 -r ' + get_backup_file_path + ' shakiurrnd@10.0.0.77:/home/shakiurrnd/pms-backup/'
    print (send_backupfile)
    print('Sending backup file to RND Server done')
    os.system(relogin + ' ' + send_backupfile)
    print('Sending backup file to RND Server done')
    remove_backupfile = 'rm -rf ' + get_backup_file_path
    print('Removing dumped backup file from  PMS Server')
    os.system(relogin + ' ' + remove_backupfile)
    print('Removed dumped backup file from  PMS Server')