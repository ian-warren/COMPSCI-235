# hello_jinja Web Application

## Description

A minimal Web application to introduce Jinja fundamentals. 

## Installation

**Installation via requirements.txt**

```shell
$ cd hello_jinja
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:hello_jinja' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *hello_jinja* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

The terminal window will display the IP address and port of the Web server running the simple Web app, e.g. http://127.0.0.1:5000. Try out the Web application using a Web browser by typing the following URLs:

http://127.0.0.1:5000/greet/<your name>

http://127.0.0.1:5000/people

http://127.0.0.1:5000/parent

http://127.0.0.1:5000/child

http://127.0.0.1:5000/grandchild

http://127.0.0.1:5000/whole

http://127.0.0.1:5000/part

 