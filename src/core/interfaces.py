# src/core/interfaces.py

from abc import ABC, abstractmethod

class IUserRepository(ABC):
    @abstractmethod
    def get_next_user_id(self):
        pass

    @abstractmethod
    def create(self, user):
        pass

    @abstractmethod
    def find_by_id(self, user_id):
        pass

    @abstractmethod
    def find_by_username(self, username):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, user_id, updated_user):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass
