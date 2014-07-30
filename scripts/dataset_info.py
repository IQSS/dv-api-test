import os, sys
import csv

class DatasetManager:
    def __init__(self, datafile):
        self.datafile = datafile
        self.datasets = []      # list of DatasetInfo objects
        
    def process_rows(self):     
        if not os.path.isfile(self.datafile):
            raise Exception('This file does not exist! %s' % self.datafile)
        
        with open(self.datafile, 'rb') as csvfile:
            dataset_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            cnt = 0
            current_dataset = None
            for row in dataset_reader:
                cnt +=1
                if cnt==1: continue     # skip header row
                new_ds = DatasetInfo(row)
                if current_dataset is None:
                    current_dataset = new_ds
                    continue
                    
                if DatasetInfo.are_datasets_same_except_author(current_dataset, new_ds):
                    # Same dataset, additional author, add the author to the current dataset
                    current_dataset.add_author(new_ds)
                else:
                    # New dataset, save the old one
                    self.datasets.append(current_dataset)
                    # Set the new one
                    current_dataset = new_ds
        print len(self.datasets)
            
            
class DatasetInfo:
    table_attrs = ["protocol", "study_id", "version", "authority", "studyid", "abstract_text", "author", "author_affiliation", "title",  "unf",  "releasetime", "producer_name", "producer_affiliation"]
    
    AUTHOR_ATTRIBUTE_NAME = 'author'

    def __init__(self, row):
        if not type(row) is list:
            raise Exception('row is not a list')
        
        self.authors = []
        
        for idx, attr in enumerate(self.table_attrs):
            if attr == DatasetInfo.AUTHOR_ATTRIBUTE_NAME:
                self.authors.append(row[idx])
                
            if (idx+1) > len(row): 
                self.__dict__[attr] = None
            else:
                self.__dict__[attr] = row[idx]
    
    def add_author(self, dataset_info):
        if dataset_info is None:
            return None
        author_name = dataset_info.__dict__.get(DatasetInfo.AUTHOR_ATTRIBUTE_NAME, None)
        if author_name is None:
            return
        self.authors.append(author_name)
        
    @staticmethod
    def are_datasets_same_except_author(ds1, ds2):
        compare_attrs = ["protocol", "study_id", "version", "authority", "studyid", "abstract_text"]
        for attr in compare_attrs:
            if not ds1.__dict__.get(attr) == ds2.__dict__.get(attr):
                return False
        return True
        
        
    