import csv
import os, sys

from jinja2 import Template
from jinja2 import Environment, PackageLoader
import requests

from msg_util import *
from dataverse_api_link import DataverseAPILink
from dataset_info import DatasetManager, DatasetInfo

class DatasetMaker:
    
    def __init__(self, dv_server, dv_auth, data_fname, dataverse_alias):
        self.jinja_env = Environment(loader=PackageLoader('dataset_maker', 'templates'))
        
        self.dv_server = dv_server
        self.dv_auth = dv_auth
        self.data_fname = data_fname
        self.dataverse_alias = dataverse_alias
        
        self.dataset_manager = None
        if not os.path.isfile(data_fname):
            raise Exception('This file does not exist! %s' % data_fname)
        self.load_data()
        
    def load_data(self):
        if not os.path.isfile(self.data_fname):
            raise Exception('This file does not exist! %s' % self.data_fname)
        
        self.dataset_manager = DatasetManager(self.data_fname)
        self.dataset_manager.process_rows()
        
    def create_dataset(self, atom_xml, parent_dataverse_alias=None):

        if not atom_xml:
            msg('No atom_xml')
            return

        # Format the url
        url = '%s/dvn/api/data-deposit/v1/swordv2/collection/dataverse' % (self.dv_server)    
        if parent_dataverse_alias: 
            url = '%s/%s' % (url, parent_dataverse_alias)

        # prepare headers
        headers = {'Content-Type': 'application/atom+xml'}

        # format requests    
        r = requests.post(url, headers=headers, data=atom_xml, auth=self.dv_auth)

        # check response
        if r.status_code == 201:
            #prettyprint_xml(r.text)
            msg(r.text)
            msg(r.status_code)
        else:
            msg('ERROR')
            msg(r.status_code)
            msg(r.text)        
    
    def get_atom_xml(self, dataset_info):
        if dataset_info is None:
            return None
            
        template = self.jinja_env.get_template('atom-entry-template.xml')

        template_params = { 'study' : dataset_info\
       
                            }

        atom_xml = template.render(template_params)
        return atom_xml
    
    def get_num_datasets(self):
        if self.dataset_manager and self.dataset_manager.datasets:
            return len(self.dataset_manager.datasets)
        return 0
        
    def add_datasets(self, start_cnt=0, end_cnt=100):
        if not self.dataset_manager:
            raise Exception('dataset_manager is None')

        ds_cnt = 0
        msgt('Number of datasets: %s' % len(self.dataset_manager.datasets))
        #return
        for ds in self.dataset_manager.datasets:
            ds_cnt +=1
            msgt('(%s) %s %s' % (ds_cnt, ds.title, ds.authors))
            if ds_cnt < start_cnt: 
                msg('skip dataset')
                continue
            if ds_cnt > end_cnt: 
                msg('stop here')
                break
            
            #print (ds.title, ds.authors)
            atom_xml = self.get_atom_xml(ds)
            #msgt(atom_xml)
            self.create_dataset(atom_xml, self.dataverse_alias)
            
       
            
if __name__=='__main__':

    dm = DatasetMaker(dv_server='http://dvn-build.hmdc.harvard.edu'\
                        , dv_auth=('pete', 'pete')\
                        , data_fname = os.path.join('..', 'data_in', 'dataset_info7.csv')\
                        , dataverse_alias='root'
                    )
    print (dm.get_num_datasets())
    #msgx('done')
    #dm.add_datasets(1,500)
    for x in range(1, 2):
        dm.add_datasets(1,500)
    #    dm.add_datasets(1,70)
    
    
    