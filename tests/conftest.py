import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from covid import create_app
from covid.adapters import memory_repository, database_repository
from covid.adapters.orm import metadata, map_model_to_tables
from covid.adapters.memory_repository import MemoryRepository


#TODO: You have to adapt these paths to your file structure
TEST_DATA_PATH_MEMORY = os.path.join('E:', os.sep, '01_Repos', 'COMPSCI-235', 'tests', 'data', 'memory')
TEST_DATA_PATH_DATABASE = os.path.join('E:', os.sep, '01_Repos', 'COMPSCI-235', 'tests', 'data', 'database')


TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///covid-19-test.db'

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH_MEMORY, repo)
    return repo

@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'memory',                         # Set to 'memory' or 'database' depending on desired repository.
        'TEST_DATA_PATH': TEST_DATA_PATH_MEMORY,        # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
