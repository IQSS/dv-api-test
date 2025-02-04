"""
Use Dataverse native APIs described here: https://github.com/IQSS/dataverse/tree/master/scripts/api

5/8/2013 - scratch work, examining API
6/5/2013 - Back to implementing some API work
6/6/2013 - Move function parameters into API_SPECS, create functions on init

Requires the python requests library:  http://docs.python-requests.org

"""
import os
import sys
from pprint import pprint
import json
import requests
from msg_util import *
from settings_helper import get_setting
from test_data_reader import TestDataReader
import types # MethodType, FunctionType
from datetime import datetime
#from single_api_spec import SingleAPISpec
import time

def msg(s): print s
def dashes(char='-'): msg(40*char)
def msgt(s): dashes(); msg(s); dashes()
def msgx(s): dashes('='); msg(s); dashes('='); sys.exit(0)

        
class DataverseAPILink:
    
    def __init__(self, server_name, apikey):
        """
        Example:
        server_name = 'https://dvn-build.hmdc.harvard.edu'
        apikey = 'an-api-key-86fd-cd973194c66b'
        """
        self.test_data_reader = TestDataReader()

        self.server_name = server_name
        if self.server_name.endswith('/'):
            self.server_name = self.server_name[:-1]
        self.apikey = apikey
        
        
    def create_dataverse(self, parent_dv_alias_or_id, dv_params):
        """Create a dataverse
        POST http://{{SERVER}}/api/dvs/{{ parent_dv_name }}?key={{username}}

        :param parent_dv_alias_or_id: str or integer, the alias or id of an existing datavese 
        :param dv_params: dict containing the parameters for the new dataverse

        Sample: Create Dataverse

        from dataverse_api import DataverseAPILink
        server_with_api = 'dvn-build.hmdc.harvard.edu'
        dat = DataverseAPILink(server_with_api, use_https=False, apikey='pete')
        dv_params = {
                    "alias":"hm_dv",
                    "name":"Home, Home on the Dataverse",
                    "affiliation":"Affiliation value",
                     "dataverseContacts": [
                                     {"contactEmail": "pete@mailinator.com"}
                                 ],                    "permissionRoot":False,
                    "description":"API testing"
                    }
        parent_dv_alias_or_id = 'root'
        print dat.create_dataverse(parent_dv_alias_or_id, dv_params)
        """
        msgt('create_dataverse')
        if not type(dv_params) is dict:
            msgx('dv_params is None')
            
        url_str = self.server_name + '/api/dataverses/%s?key=%s' % (parent_dv_alias_or_id, self.apikey)
        msg('url_str: %s' % url_str)

        headers = {'content-type': 'application/json'}
        
        r = requests.post(url_str, data=json.dumps(dv_params), headers=headers)
        print 'status code:', r.status_code
        if r.status_code == 201:
            msg('Success!!')
        else:
            dashes('- ')
            msg('Parameters used to create dataverse: %s' % dv_params)
            dashes('- ')
            msg('Response Error: %s' % r.text)
            msgx('Response Status code: %s' % r.status_code )
        #return self.make_api_call(url_str, self.HTTP_POST, params=dv_params, headers=headers)
        
        
    def publish_dataverse(self, dv_id_or_name):
        """
        Publish a dataverse based on its id or alias
        #POST http://{{SERVER}}/api/dvs/{{identifier}}/actions/:publish?key={{apikey}}
        
        :param dv_id_or_name: Dataverse id (str or int) or alias (str)
        """
        msg('\npublish_dataverse: "%s"' % dv_id_or_name)
        if dv_id_or_name is None:
            msgx('dv_id_or_name is None')
        
        url_str = self.server_name + '/api/dataverses/%s/actions/:publish?key=%s' % (dv_id_or_name, self.apikey)
        msg('url_str: %s' % url_str)
        headers = {'content-type': 'application/json'}
        
        try:
            r = requests.post(url_str, headers=headers)
        except requests.exceptions.ConnectionError as e:
            msgx('Connection error: %s' % e.message)
        except:
            msgx("Unexpected error: %s" % sys.exc_info()[0])
        
        if r.status_code == 200:
            msg('Success!  Published!')
        else:
            dashes('- ')            
            msg('ERROR: %s' % r.text)
            msgx('Status code: %s' % r.status_code )


def make_lots_of_dataverses(num_dataverses=100, parent_dv_alias='root', publish_dataverses=False):

    server_with_api = get_setting('DATAVERSE_URL')
    apikey =  get_setting('API_TOKEN')
    
    dat = DataverseAPILink(server_with_api, apikey=apikey)

    for cnt in range(1, num_dataverses+1):
        if cnt > 0 and cnt % 50 == 0:
            sleep_secs = 7
            msgt('Sleeping for %s seconds' % sleep_secs)
            time.sleep(sleep_secs)

        dv_params = dat.test_data_reader.get_test_animal_dataverse_params()
        pprint(dv_params)

        msgt('(%s) Creating dataverse: "%s" alias: %s' % (cnt, dv_params['name'], dv_params['alias'] ))
        
        
        dat.create_dataverse(parent_dv_alias, dv_params)
        if publish_dataverses:
            dat.publish_dataverse(dv_params.get('alias', 'no-alias found!'))
     
     
if __name__=='__main__':
    # EXAMPLE
    make_lots_of_dataverses(num_dataverses=1\
                            , parent_dv_alias='root'\
                            , publish_dataverses=True\
                        )
    