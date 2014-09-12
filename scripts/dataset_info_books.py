import uuid
import os, sys
import csv
import string

class DatasetManager:
    
    def __init__(self, datafile, start_row=1, end_row=100):
        self.datafile = datafile
        self.datasets = []      # list of DatasetInfo objects
        self.start_row = start_row
        self.end_row = end_row
        assert(end_row > start_row)
        
    def process_rows(self):     
        # source: http://www2.informatik.uni-freiburg.de/~cziegler/BX/
        if not os.path.isfile(self.datafile):
            raise Exception('This file does not exist! %s' % self.datafile)

        with open(self.datafile, 'rb') as csvfile:
            dataset_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            cnt = 0
            for row in dataset_reader:
                cnt +=1
                if cnt==1: continue
                if cnt>=self.start_row and cnt < self.end_row:
                    new_ds = DatasetInfo(row)
                    self.datasets.append(new_ds)
                    print('(%s) added: %s' % (cnt, new_ds.title))


class DatasetInfo:
    table_attrs = """isbn title author year publisher img_sm img_med img_lg""".split() 

    def __init__(self, row):
        if not type(row) is list:
            raise Exception('row is not a list')

        for idx, attr in enumerate(self.table_attrs):
            if (idx+1) > len(row): 
                self.__dict__[attr] = None
                return

            val = self.strip_non_ascii(row[idx])#.decode('utf-8') 
            self.__dict__[attr] = val


    def strip_non_ascii(self, val):
        return filter(lambda x: x in string.printable, val)


    def get_study_obj_with_params(self):
        class StudyObj: pass
        sb = StudyObj()
        sb.__dict__.update(self.get_dataset_params())
        return sb
        
    def get_dataset_params(self):
        return dict(producer_affiliation=""\
                , study_id="78622"\
                , title=self.title
                , mock_doi=self.isbn
                , abstract_text='text datast for the book: %s' % self.title\
                , protocol="doi"\
                , authority="10.5072/FK2"\
                , studyid=uuid.uuid1()\
                , producer_name=self.publisher\
                , author_affiliation=self.publisher\
                , releasetime="2012-02-28 18:58:48.469"\
                , author=self.author\
                , version=self.year\
                , pub_year=self.year
                , unf=""\
                )
        

