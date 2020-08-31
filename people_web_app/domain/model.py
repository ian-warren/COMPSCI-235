class Person:
    def __init__(self, id_number: int, firstname: str, lastname: str):
        self._id_number = id_number
        self._firstname = firstname
        self._lastname = lastname

    @property
    def id_number(self) -> int:
        return self._id_number

    @property
    def firstname(self) -> str:
        return self._firstname

    @property
    def lastname(self) -> str:
        return self._lastname
