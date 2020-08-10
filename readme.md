# COVID-19 Repository

## Description

Application of the Repository pattern. This branch provides a Repository interface for the COVID-19 app, and an implementation that stores domain model objects in memory. The branch includes unit tests for the Repository.

## Installation

**Installation via requirements.txt**

```shell
$ cd COMPSCI-235
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:COMPSCI-235' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Testing

Testing requires that file *COMPSCI-235/tests/unit/test_memory_repository.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *COMPSCI-235/tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'ian', 'Documents', 'Python dev', 'COMPSCI-235', 'tests', 'data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\ian\Documents\python-dev\COMPSCI-235\tests\data`

You can then run the tests from within PyCharm or a terminal window.

