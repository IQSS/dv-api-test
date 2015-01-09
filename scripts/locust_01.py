import sys
from locust import HttpLocust, TaskSet

def login(l):
    l.client.post('/loginpage.xhtml'\
                    , {"loginForm:credentialsContainer2:0:credValue":"pete"
                    , "loginForm:credentialsContainer2:0:j_idt138":"xpete"})

def index(l):
    response = l.client.get('/')
    
def election_dataverse(l):
    l.client.get('/dataverse.xhtml?id=9')

def election_data(l):
    l.client.get('/dataset.xhtml?id=27&versionId=18')
    
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
