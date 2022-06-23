import requests
import logging
import callback
import vim
import os

logging.basicConfig(level = logging.INFO)

class GitLabAPIs:
    def __init__(self):
        self.db_path = os.path.dirname(os.path.abspath(__file__)) + '/.db'
        if not os.path.exists(self.db_path):
            os.mkdir(self.db_path)

        try:
            with open(self.db_path + '/token', 'r') as token_file:
                self.token = token_file.readline()
        except:
            self.token = ""

        try:
            with open(self.db_path + '/url', 'r') as url_file:
                self.request_url = url_file.readline()
        except:
            self.request_url = ""


        self.header = {'PRIVATE-TOKEN': self.token, 'Content-Type': 'application/json'}


    def request_code(self, api_name):
        return "{0}/{1}".format(self.request_url, api_name)

    def request_any_get(self, url_str, timeout, callback_func):
        try:
            response = requests.get(url = url_str, headers = self.header, timeout = timeout)
            return callback_func(response)
        except requests.exceptions.ReadTimeout:
            return ["-1 GET request ReadTimeout"]
        except requests.exceptions.ConnectionError:
            return ["-1 GET requests ConnectionError"]
        except:
            return ["-1 GET requests ERROR"]

    def request_ping(self):
        global_token = vim.eval("g:Lf_GitlabToken")
        try:
            with open(self.db_path + '/token', 'w') as token_file:
                token_file.write(global_token)
        except:
            print("Write token on .db/token failed.")
            return False
        global_url = vim.eval("g:Lf_GitlabURL")
        try:
            with open(self.db_path + '/url', 'w') as url_file:
                url_file.write(global_url)
        except:
            print("Write url on .db/url failed.")
            return False

        try:
            self.header['PRIVATE-TOKEN'] = global_token
            self.request_url = global_url
            response = requests.get(url = self.request_code("/version"), headers = self.header, timeout = 0.5)
            return callback.version(response)
        except:
            return False


    def request_mr(self):
        return self.request_any_get(
                url_str = self.request_code("/merge_requests?state=opened&scope=assigned_to_me"), 
                timeout = 0.5,
                callback_func =  callback.mr)

# PUBLIC APIs
gitlab = GitLabAPIs()
def mr(): return gitlab.request_mr()
def ping(): return gitlab.request_ping()
