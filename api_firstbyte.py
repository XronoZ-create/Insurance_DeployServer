import requests
from urllib.parse import quote

class ApiFirstByte:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def get_servers(self, with_pass=False):
        self.r = requests.get(f"https://billing.firstbyte.ru/billmgr?authinfo={quote(self.login)}:{quote(self.password)}&func=vds&out=json")
        self.r_json = self.r.json()

        self.server_info = {}
        for self.one in self.r_json["doc"]["elem"]:
            self.id_one = self.one["id"]["$"]
            if with_pass:
                self.one_pass = self.get_pass(id=self.id_one)
            else:
                self.one_pass = None
            self.server_info[self.one["ip"]["$"]] = {"id": self.id_one, "password": self.one_pass}
        return self.server_info

    def get_pass(self, id):
        self.req_pass = requests.get(f"https://billing.firstbyte.ru/billmgr?authinfo={quote(self.login)}:{quote(self.password)}&func=vds.edit&elid={id}")
        self.req_pass_json = self.req_pass.json()

        self.pass_server = self.req_pass_json["form"][0]["formItems"][8][0]["value"]
        return self.pass_server