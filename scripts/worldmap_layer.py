import requests
import json

from msg_util import *

def update_layer(datafile_id, json_layer_info):
    
    url = 'http://localhost:8080/api/worldmap/layer-update/%s?key=pete' % (datafile_id)
    
    # auth
    #dv_auth = ('pete', 'pete') # username/pw
    
    # prepare headers
    headers = {'Content-Type': 'application/json'}

    # open file
    #file_data = json.dumps(json_layer_info) #open(atom_entry_fname, 'rb').read()        
    
    # format requests    
    r = requests.post(url, headers=headers, data=json_layer_info)#, auth=dv_auth)
    
    print (r.text)
    print (r.status_code)
    
    
if __name__=='__main__':
    d = dict(layerName='geonode:boston_census_blocks_zip_cr9'\
            , layerLink='http://localhost:8000/data/geonode:boston_census_blocks_zip_cr9'\
            #, embed_map_link='http://localhost:8000/maps/embed/?layer=geonode:boston_census_blocks_zip_cr9'\
            , embedMapLink='blah-haha'\
            , worldmapUsername='dv_pete'
            )
    #d = dict(layer_name='geonode:boston_census_blocks_zip_cr9')
    json_info = json.dumps(d) 
    msgt("json_info: %s" % json_info)
    msgt("json_info: %s" % type(json_info))
    
    update_layer(25, json_info)
"""
private String layerName;
  
  @Column(nullable=false)
  @NotBlank(message = "Please specify a layer link.")
  private String layerLink;
  
  @Column(nullable=false)
  @NotBlank(message = "Please specify am embedded map link.")
  private String embedMapLink;
  
  @Column(nullable=false)
  @NotBlank(message = "Please specify a WorldMap username.")
  private String worldmapUsername;
 

"""