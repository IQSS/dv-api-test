dv-api-test
===========

Currently "Scratch" code to use the dataverse api

### Setup 

+ pip install 

```
cd dv-api-test
pip install -r requirements/base.txt
```
+ **Recommended**: use [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation)
+ **I don't want to install pip**: try this [stackoverflow, no pip](http://stackoverflow.com/questions/9348869/how-to-install-virtualenv-without-using-sudo/15555989#15555989)
  + See [Issue #1](https://github.com/IQSS/dv-api-test/issues/1) for more details on how to do this

### Create test dataverses

```python
cd ~/dv-api-test/scripts
# This uses the dv names listed in ~/dv-api-test/data_in/vdc.csv
python add_vdc.py
``` 

### Delete the test dataverses

+ Edit the bottom of the scripts/add_vdc.py file
+ Comment out "add_dataverses(1, 700)"
+ Uncomment "delete_dataverses(3,700)"
```python

if __name__=='__main__':
   #add_dataverses(1, 700)
   delete_dataverses(3,700)
```
