# hello_flask Web Application

## Description

A minimal Web application to introduce Python's Flask framework. 

## Installation

**Installation via requirements.txt**

```shell
$ cd hello_flask
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:hello_flask' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *hello_flask* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

The terminal window will display the IP address and port of the Web server running the simple Web app, e.g. http://127.0.0.1:5000. Try out the Web application using a Web browser by typing the following URLs:

http://127.0.0.1:5000

http://127.0.0.1:5000/hello

http://127.0.0.1:5000/user/<your-name>

http://127.0.0.1:5000/post<id>

http://127.0.0.1:5000/path/<path>

http://127.0.0.1:5000/news


## Testing

Run the *tests/test_app.py* script. 

 