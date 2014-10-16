import csv
import os, sys
#from multiprocessing import Pool

from jinja2 import Template
from jinja2 import Environment, PackageLoader
import requests

from msg_util import *
from dataverse_api_link import DataverseAPILink
from dataset_info_books import DatasetManager, DatasetInfo

from temp_aliases import get_random_alias

class DatasetMaker:
    
    def __init__(self, dv_server, dv_auth, data_fname, dataverse_alias):
        self.jinja_env = Environment(loader=PackageLoader('dataset_maker', 'templates'))
        
        if dv_server.endswith('/'):
            dv_server = dv_server[0:-1]
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

        parent_dataverse_alias = get_random_alias()
            
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
            msg(r.text)        
            msgx(r.status_code)
    
    def get_atom_xml(self, dataset_info):
        if dataset_info is None:
            raise TypeError('dataset_info is not a DatasetInfo')
            
        template = self.jinja_env.get_template('atom-entry-template_books.xml')
        #msgt(template)
        
        #params = dataset_info.get_dataset_params()
        #msg(params)
        template_params = { 'study' : dataset_info.get_study_obj_with_params() }
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
        #pool = Pool(processes=1)              # Start a worker processes.
        for ds in self.dataset_manager.datasets:
            ds_cnt +=1
            msgt('(%s) %s %s' % (ds_cnt, ds.title, ds.author))
            if ds_cnt < start_cnt: 
                msg('skip dataset')
                continue
            if ds_cnt > end_cnt: 
                msg('stop here')
                break
            
            #print (ds.title, ds.authors)
            atom_xml = self.get_atom_xml(ds)
            #msgt(atom_xml)
            #result = pool.apply_async(self.create_dataset\
            #                , [atom_xml, self.dataverse_alias]\
            #                , callback=self.done)
            self.create_dataset(atom_xml, self.dataverse_alias)
    
    def done(self):
        msg('loaded')
            
       
            
if __name__=='__main__':
    db_server = 'http://localhost:8080'
    #db_server = 'http://dvn-build.hmdc.harvard.edu'
    dm = DatasetMaker(dv_server=db_server\
                        , dv_auth=('pete', 'pete')\
                        , data_fname = os.path.join('..', 'data_in', 'BX-CSV-Dump', 'BX-Books.csv')\
                        , dataverse_alias='root'
                    )
    
    print (dm.get_num_datasets())
    #msgx('done')
    dm.add_datasets(358,1000)
    #dm.add_datasets(26083,28000)
    #dm.add_datasets(19960,25000)
    #    dm.add_datasets(1,70)
    

