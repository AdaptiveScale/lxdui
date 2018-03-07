from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def info(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self):
        raise NotImplementedError()

    @abstractmethod
    def delete(self):
        raise NotImplementedError()

    @abstractmethod
    def start(self):
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        raise NotImplementedError()

    @abstractmethod
    def restart(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()

    @abstractmethod
    def move(self):
        raise NotImplementedError()

    @abstractmethod
    def clone(self):
        raise NotImplementedError()

    @abstractmethod
    def snapshot(self):
        raise NotImplementedError()
