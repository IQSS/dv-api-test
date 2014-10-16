from locust import HttpLocust, TaskSet

def login(l):
    l.client.post('/loginpage.xhtml'\
                    , {"loginForm:credentialsContainer2:0:credValue":"pete"
                    , "loginForm:credentialsContainer2:0:j_idt138":"pete"})

def index(l):
    l.client.get('/')

def profile(l):
    l.client.get("/dataverseuser.xhtml" )

class UserBehavior(TaskSet):
    tasks = {index:2, profile:1}

    def on_start(self):
        login(self)

class WebsiteUser(HttpLocust):
    host = 'https://dvn-build.hmdc.harvard.edu'
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
