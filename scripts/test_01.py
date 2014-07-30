from __future__ import print_function
import os, sys
import requests
import getpass
from lxml import etree
import xmltodict
import pprint as pp

from jinja2 import Template
from jinja2 import Environment, PackageLoader


def msg(s): print(s)
def dashes(): msg(40*'-')
def msgt(s): dashes(); msg(s); dashes()
def msgx(s): msgt(s); sys.exit(0)

def print_dict(pydict, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""
    for key, value in pydict.iteritems():
        if isinstance(value, dict):
            print('%s%s%s%s' %(ident,braces*'[',key,braces*']') )
            print_dict(value, ident+'  ', braces+1)
        else:
            print( ident+'%s = %s' %(key, value))
            

def open_service_doc(fname):
    """Open an XML file and convert it to a python dictionary"""
    xml_content = open(fname, 'r').read()
    
    service_dict = xmltodict.parse(xml_content)
    
    print_dict(service_dict)
    #keys = service_dict.keys()
    #while keys:
    #    msg('keys: %s' % keys)
    
        
def create_dataset(dv_server, dv_auth, atom_entry_fname, parent_dataverse_alias=None):
    
    if not os.path.isfile(atom_entry_fname):
        msg('File not found!  %s' % atom_entry_fname)
        return
    
    # Format the url
    url = 'https://%s/dvn/api/data-deposit/v1/swordv2/collection/dataverse' % (dv_server)    
    if parent_dataverse_alias: 
        url = '%s/%s' % (url, parent_dataverse_alias)

    # prepare headers
    headers = {'Content-Type': 'application/atom+xml'}

    # open file
    file_data = open(atom_entry_fname, 'rb').read()        

    # format requests    
    r = requests.post(url, headers=headers, data=file_data, auth=dv_auth)
    
    # check response
    if r.status_code == 201:
        prettyprint_xml(r.text)
        msg(r.status_code)
    else:
        msg('ERROR')
        msg(r.status_code)
        msg(r.text)        
        
    
def prettyprint_xml(xml_str):
    """Pretty print an XML string"""

    if not xml_str:
        msg('No XML found')
    
    try:
        root = etree.fromstring(xml_str)
    except:
        msg('No XML found')
        return
    msg(etree.tostring(root, pretty_print=True))

def get_service_document(dv_server, dv_auth, output_fname):
    """Retrieve the SWORD service document"""
    
    # format the url
    url = 'https://%s/dvn/api/data-deposit/v1/swordv2/service-document' % (dv_server)
    
    # prepare the requests
    r = requests.get(url, auth=dv_auth)
    if not r.status_code == 200:
        msg(r.text  )
        msg('Failed, status code: %s' % r.status_code)
        return
    
    prettyprint_xml(r.text)
    msg(r.status_code)
    
    # save file
    open(output_fname, 'w').write(r.text)
    msg('file written: %s' % output_fname)


if __name__=='__main__':

    dv_server = 'apitest.dataverse.org'     
       
    dv_auth = ('pete', getpass('Enter password')) # username/pw
    
    # Open the service document and write it to a specified file
    service_doc_fname = 'data/service_doc.sml'   # file path that across OS's (windows, etc) -> os.path.join('data', 'service_doc.xml')  
    get_service_document(dv_server, dv_auth, output_fname=service_doc_fname)

    # Create a dataset from an atom file
    create_dataset(dv_server, dv_auth, 'data/atom-entry-study.xml', 'testapi')

    # Open XML file and convert it to a python dict
    #open_service_doc(service_doc_fname)
"""
curl -s --insecure --data-binary @data/atom-entry-study2.xml -H "Content-Type: application/atom+xml" -u pete:pete https://apitest.dataverse.org/dvn/api/data-deposit/v1/swordv2/collection/dataverse/testapi | xmllint -format -


"""
