import requests
from getenv import env


class BILLException(Exception):
    pass


class BILLAccountManager:

    def __init__(self):
        self.api_url = env("BILL_API_URL")
        self.user = env("BILL_API_USER")
        self.password = env("BILL_API_PW")

    def create_bill_account(self, username):
        r = requests.post(self.api_url + "add?type=user&id=%s".format(username), auth=(self.user, self.password))
        if r < 0:
            raise BILLException("BILL returned error code: " + r)
        else:
            return r

    def delete_bill_account(self, bill_code):
        r = requests.post(self.api_url + "del?type=user&acc=%s".format(bill_code), auth=(self.user, self.password))
        if r < 0:
            raise BILLException("BILL returned error code: " + r)
        else:
            return r

    def get_bill_info(self, bill_code):
        r = requests.get(self.api_url + "get?type=user&acc=%s".format(bill_code), auth=(self.user, self.password))
        if r < 0:
            raise BILLException("BILL returned error code: " + r)
        else:
            return r
