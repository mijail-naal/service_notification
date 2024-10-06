from abc import ABC, abstractmethod


class BaseBrokerService(ABC):
    @abstractmethod
    def send_message(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def send_to_broker(self, *args, **kwargs) -> None:
        pass