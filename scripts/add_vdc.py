import csv
import os, sys
from msg_util import *
from dataverse_api_link import DataverseAPILink

class DvInfo:
    attrs = ["id", "name", "alias", "visibility", "dvndescription", "lastname", "firstname", "affiliation"]
    def __init__(self, row):
        if not type(row) is list:
            raise Exception('row is not a list')
        
        
        for idx, attr in enumerate(self.attrs):
            if (idx+1) > len(row): 
                self.__dict__[attr] = None
            else:
                self.__dict__[attr] = row[idx]
    
    def get_params(self):
        desc = self.dvndescription
        if not desc:
            desc = 'Dataverse for %s' % self.name
        if not self.affiliation:
            self.affiliation = 'Project Dataverse [default description]'
            
        dv_params = { 
                        "alias": self.alias,
                        "name": self.name,
                        "affiliation": self.affiliation,
                        "contactEmail":"test@dvtest.org",
                        "permissionRoot":True,
                        "description":desc
                        }
        return dv_params
    

def delete_dataverses(server_with_api, start_cnt=0, end_cnt=100):
    #DELETE http://{{SERVER}}/api/dvs/{{id}}?key={{username}}
    dat = DataverseAPILink(server_with_api, use_https=False, apikey='pete')
    
    vdc_input = os.path.join('..', 'data_in', 'vdc.csv')
    with open(vdc_input, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        cnt = 0
        for row in spamreader:
            cnt +=1
            if cnt==1: continue     # skip header row
            
            dv = DvInfo(row)
            
            msg('name: %s alias: %s description: %s ' % (dv.name, dv.alias, dv.dvndescription))
                #print ', '.join(row)
            
            if cnt >= start_cnt:
                print dat.delete_dataverse_by_id(dv.alias)
            if cnt==end_cnt:
                break
    
    
    
def add_dataverses(server_with_api, start_cnt=0, end_cnt=100):

    dat = DataverseAPILink(server_with_api, use_https=False, apikey='pete')
    
    vdc_input = os.path.join('..', 'data_in', 'vdc.csv')
    with open(vdc_input, 'rb') as csvfile:
        vdc_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        cnt = 0
        for row in vdc_reader:
            cnt +=1
            if cnt==1: continue     # skip header row
            
            dv = DvInfo(row)
            
            msg('name: %s alias: %s description: %s ' % (dv.name, dv.alias, dv.dvndescription))
                #print ', '.join(row)
            
            if cnt >= start_cnt:
                print dat.create_dataverse('root', dv.get_params())
            if cnt==end_cnt:
                break
            
if __name__=='__main__':
    server_with_api = 'https://dvn-build.hmdc.harvard.edu'
    add_dataverses(server_with_api, 1, 610)
    #delete_dataverses(server_with_api, 3,700)