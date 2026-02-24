from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass
    
    @abstractmethod
    def channel_type(self) -> str:
        pass
    
class EmailChannel(NotificationChannel):
    def __init__(self, smtp_server: str, sender_address: str) -> None:
        self.__smtp_server = smtp_server
        self.__sender_address = sender_address
    def send(self, recipient: str, message: str) -> bool:
        print(f'[EMAIL] To: {recipient} | Fron: {self.__sender_address} |  Message: {message}')
        return True
    def channel_type(self) -> str:
        return "email"
    
class SMSChannel(NotificationChannel):
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
    def send(self, recipient: str, message: str) -> bool:
        print(f'[SMS] To: {recipient} |  Message: {message}')
        return True
    def channel_type(self) -> str:
        return "sms"

class PushNotificationChannel(NotificationChannel):
    def __init__(self, app_id: str) -> None:
        self.__app_id = app_id
    def send(self, recipient: str, message: str) -> bool:
        print(f'[PUSH] To: {recipient} |  Message: {message} | AppID: {self.__app_id}')
        return True
    def channel_type(self) -> str:
        return "push"
    
class SlackChannel(NotificationChannel):
    def __init__(self, webhook_url: str) -> None:
        self.__webhook_url = webhook_url
    def send(self, recipient: str, message: str) -> bool:
        print(f'[SLACK] To: {recipient} |  Message: {message} | WebHook URL: {self.__webhook_url}')
        return True
    def channel_type(self) -> str:
        return "slack"
    
class NotificationService:
    def __init__(self, channels: list[NotificationChannel]) -> None:
        # dict to pick specific channel in O(1)
        self.__channels = {c.channel_type() : c for c in channels}
        
    def notify(self, recipient: str, message: str) -> None:
        for c in self.__channels.values():
            c.send(recipient=recipient, message=message)
    
    def notify_via(self, channel_type: str, recipient: str, message: str) -> bool:
        if channel_type not in self.__channels:
            return False
        channel = self.__channels[channel_type]
        status = channel.send(recipient=recipient, message=message)
        return status
        
    def add_channel(self, channel: NotificationChannel) -> None:
        if channel.channel_type() in self.__channels:
            self.remove_channel(channel.channel_type())
        
        self.__channels[channel.channel_type()] = channel
        
    def remove_channel(self, channel_type: str) -> None:
        if channel_type not in self.__channels:
            return
        self.__channels.pop(channel_type)