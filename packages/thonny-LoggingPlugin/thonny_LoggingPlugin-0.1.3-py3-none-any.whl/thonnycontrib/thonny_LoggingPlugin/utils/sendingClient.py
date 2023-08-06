import requests
from thonnycontrib.thonny_LoggingPlugin.utils.xAPI_creation import convert_to_xAPI

class SendingClient():
    """
    This class is used to send data to the LRS API
    For the moment the only thing that can be send is statements, wich are converted by this class from data dicts
    """

    def __init__(self,server_addr):
        self.server_addr = server_addr
        self.stored_data = []

    def send_statement(self,data):
        """
        Convert data to the xAPI format, and send it to the LRS

        Args :
            data (object: dict()): dict of the data in a basic format
        """
        xAPI_statement = convert_to_xAPI(data)
        self.send(xAPI_statement,"/statements/")

    def send(self,data,server_path):
        """
        Try to send the data to the LRS and catch the exceptions

        Args : 
            data (object: dict()): the data in the xAPI format
            server_path (str) the server address with the right folder

        Return :
            The API's response
        """
        try :
            response = requests.post(self.server_addr+server_path,json = data)
            return response

        except requests.exceptions.RequestException as e:
            print(e)


    def change_server_addr(self,server_addr):
        """
        Change the class attribute server_addr

        Args :
            server_addr (str) the server address
        """
        self.server_addr = server_addr