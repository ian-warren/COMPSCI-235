import abc
from typing import List

from people_web_app.domain.model import Person


repo_instance = None


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self) -> Person:
        raise NotImplementedError

    @abc.abstractmethod
    def get_person(self, id: int):
        raise NotImplementedError


class PeopleRepository(AbstractRepository):
    def __init__(self, *args):
        self._people: List[Person] = list()

        for person in args:
            self._people.append(person)

    def __iter__(self):
        self._current = 0
        return self

    def __next__(self):
        if self._current >= len(self._people):
            raise StopIteration
        else:
            self._current += 1
            return self._people[self._current-1]

    def get_person(self, id: int):
        return next((person for person in self._people if person.id_number == id), None)
