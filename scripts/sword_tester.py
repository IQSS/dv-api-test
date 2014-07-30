
from jinja2 import Template
from jinja2 import Environment, PackageLoader


class SwordTester:
    
    def __init__(self):
        self.jinja_env = Environment(loader=PackageLoader('scripts', 'templates'))


    def get_atom_feed(self, study):
        template = self.jinja_env.get_template('atom-entry-template.xml')
            
        template_params = { 'study' : study\
                """            , 'creators' : study.creators\
                            , 'related_issues' : related_issue_str\
                            , 'child_issues_original' : original_children_str\
                            , 'child_issues_github' : github_children_str\
                   """         
                            }

        updated_description = template.render(template_params)
        