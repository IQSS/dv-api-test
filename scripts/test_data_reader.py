import os
import random
from os.path import isfile, join, isdir, abspath
from slugify import slugify


# -------------------------
# Test data
# -------------------------
# csv data
TEST_DATA_DIRECTORY = '../data_in'

# Test files directory - created as needed
TEST_DATA_DIRECTORY_FAKE_FILES = join(TEST_DATA_DIRECTORY, 'fake-files')
if not isdir(TEST_DATA_DIRECTORY_FAKE_FILES):
    os.makedirs(TEST_DATA_DIRECTORY_FAKE_FILES)


class TestDataReader:

    def __init__(self):
        pass

    def get_test_data_file_path(self, fname, content):
        """
        Create a test file and return its path
        """
        assert fname is not None, 'fname cannot be None'
        assert content is not None, 'content cannot be None'

        upload_file_path = abspath(join(TEST_DATA_DIRECTORY_FAKE_FILES, fname))
        fh = open(upload_file_path, 'w')
        fh.write(content)
        fh.close()

        return upload_file_path


    def get_test_song_dataset_params(self):
        """
        Pull random row from song list
        """
        fname = join(TEST_DATA_DIRECTORY, 'songs', 'top3000-song-list.csv')
        assert isfile(fname), 'Input file not found: %s' % fname

        cline = random.choice(open(fname, 'rU').readlines())
        citems = [unicode(x.strip().replace('"', '')) for x in cline.split(',')]

        print len(citems)
        position, artist, song_name, year = citems[:4]

        # title, description, contact
        title = '%s %s (%s)' % (song_name, artist, year)
        description = '%s by %s in %s' % (song_name, artist, year)
        datasetContact = '%s@%s.com' % (slugify(song_name), slugify(artist))

        upload_file_path = self.get_test_data_file_path('%s.txt' % slugify(title), description)

        return dict(title=song_name,
                     author=artist,
                     datasetContact=datasetContact,
                     dsDescription=description,
                     upload_file_path=upload_file_path,
                    )

    def get_test_animal_dataverse_params(self):
        fname = join(TEST_DATA_DIRECTORY, 'animals', 'list_of_endangered_species_of_mammals_and_birds-1252j.csv')
        assert isfile(fname), 'Input file not found: %s' % fname

        cline = random.choice(open(fname, 'rU').readlines())
        citems = [unicode(x.strip()) for x in cline.split(',')]
        id, name, scientific_name, home_range = citems[:4]

        dv_name = name
        alias = slugify(dv_name)#.replace('-', '')
        return dict(name=dv_name,
                alias=alias,
                description='%s. Endangered species.  Range: %s' % (scientific_name, home_range),
                category='RESEARCH_PROJECTS',
                dataverseContacts=[ dict(contactEmail='info@%s.org' % alias)],
                permissionRoot=True,
                affiliation='Testing')

    def get_test_car_dataverse_params(self):
        fname = join(TEST_DATA_DIRECTORY, 'songs', 'carlist.csv')
        assert isfile(fname), 'Input file not found: %s' % fname

        cline = random.choice(open(fname, 'rU').readlines())
        citems = [x.strip() for x in cline.split(',')]
        year, make, model, horsepower, cylinders = citems

        dv_name = '%s %s %s (%s hp)' % (year, make, model, horsepower)
        alias = slugify(unicode(dv_name))
        return dict(name=dv_name,
                alias=alias,
                description='US EPA Car Information',
                category='RESEARCH_PROJECTS',
                contact_email='info@%s.dot' % alias
                )
