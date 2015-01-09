import os, sys
import sys
from locust import HttpLocust, TaskSet

def login(l):
    print "Attempt login"
    r = l.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml'\
                    , {"loginForm:credentialsContainer2:0:credValue":"pete"
                    , "loginForm:credentialsContainer2:1:sCredValue":"pete"\
                    , "loginForm:loginSystemSelect" : "builtin"\
                    #, "loginForm" : "loginForm"\
                    })
    print 'status code: %s' % r.status_code
    if r.text.find('data-toggle="dropdown">Pete Privileged') == -1:
        print '----- LOGIN FAILED ------'
        fname_failed_info = 'failed_info.html'
        open(fname_failed_info, 'wb').write(r.text.encode('utf-8'))
        print 'failed page html written to file: %s' % fname_failed_info
        sys.exit(0)
    else:
        print 'LOGIN SUCCESS :):):)'
                
def index(l):
    response = l.client.get('/')
    #print dir(response)
    #print 'type: %s' % type(response)
    
def profile(l):
    l.client.get("/dataverseuser.xhtml" )

class UserBehavior(TaskSet):
    tasks = {login:1, index:1, profile:1}
    #tasks = {index:1, election_dataverse:1, election_data:1, index:1}

    def on_start(self):
        pass
        #login(self)

class WebsiteUser(HttpLocust):
    host = 'https://dvn-build.hmdc.harvard.edu'
    #host = 'https://dataverse-demo.iq.harvard.edu'
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
