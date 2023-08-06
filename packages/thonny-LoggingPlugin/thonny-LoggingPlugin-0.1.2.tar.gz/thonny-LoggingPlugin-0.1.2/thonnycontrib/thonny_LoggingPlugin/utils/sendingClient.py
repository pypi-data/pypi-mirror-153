import requests
from thonnycontrib.thonny_LoggingPlugin.utils.xAPI_creation import convert_to_xAPI

class SendingClient():

    def __init__(self,server_addr):
        self.server_addr = server_addr
        self.stored_data = []

    def send_statement(self,data):
        xAPI_statement = convert_to_xAPI(data)
        self.send(xAPI_statement,"/statements/")

    def send(self,data,server_path):
        try :
            response = requests.post(self.server_addr+server_path,json = data)
            return response

        except requests.exceptions.RequestException as e:
            print(e)


    def change_server_addr(self,server_addr):
        self.server_addr = server_addr