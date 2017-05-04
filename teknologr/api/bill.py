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
        r = requests.post(self.api_url + "add?type=user&id=%s" % username, auth=(self.user, self.password))
        try:
            number = int(r.text)
        except ValueError:
            # Returned value not a BILL code or error code
            raise BILLException("BILL returned error: " + r.text)
        if number < 0:
            raise BILLException("BILL returned error code: " + r.text)
        return number

    def delete_bill_account(self, bill_code):
        r = requests.post(self.api_url + "del?type=user&acc=%s" % bill_code, auth=(self.user, self.password))
        try:
            number = int(r.text)
        except ValueError:
            # Returned value not a number, unknown error occurred
            raise BILLException("BILL returned error: " + r.text)
        if number == 0:
            pass  # All is good
        else:
            raise BILLException("BILL returned error code: %d" % number)

    def get_bill_info(self, bill_code):
        import json
        r = requests.get(self.api_url + "get?type=user&acc=%s" % bill_code, auth=(self.user, self.password))
        # BILL API does not use proper http status codes
        try:
            error = int(r.text)
        except ValueError:
            # The returned string is not an integer, so presumably we have the json we want
            return json.loads(r.text)
        raise BILLException("BILL returned error code: " + r.text)
