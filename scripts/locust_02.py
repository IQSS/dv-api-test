from locust import HttpLocust, TaskSet

def index(l):
    l.client.get('/')

def predict(l):
    l.client.get('/predict/upload-data/')
    #                , {"id_first_name":"test"
    #                , "id_last_name":"test2"})

def map(l):
    l.client.get('/maps/tb-map/')
    
def services(l):
    l.client.get('/pages/services')

def governing(l):
    l.client.get('/people/hwpi-role/governing-board')
    
class UserBehavior(TaskSet):
    #tasks = {index:1, predict:1, map:1, index:1 }
    tasks = { index:1, services:1, governing:1, index:1}

class WebsiteUser(HttpLocust):
    host = 'http://hwp.harvard.edu'
    #host = 'http://tb.datascience.iq.harvard.edu'
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
