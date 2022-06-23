import requests
import logging
import callback
import config

logging.basicConfig(level = logging.INFO)

class GitLabAPIs:
    def __init__(self):
        self.request_url = config.request_url
        self.api_root = config.api_root
        self.token = config.token
        self.header = {'PRIVATE-TOKEN': self.token, 'Content-Type': 'application/json'}

    def request_code(self, api_name):
        return "{0}{1}/{2}".format(self.request_url, self.api_root, api_name)

    def request_any_get(self, url_str, timeout, callback_func):
        try:
            response = requests.get(url = url_str, headers = self.header, timeout = timeout)
            if response.status_code == 200:
                return callback_func(response.json())
        except requests.exceptions.ReadTimeout:
            return ["-1 GET request ReadTimeout"]
        except requests.exceptions.ConnectionError:
            return ["-1 GET requests ConnectionError"]
        except:
            return ["-1 GET requests ERROR"]


    def request_version(self):
        return self.request_any_get(
                url_str = self.request_code("/version"), 
                timeout = 2,
                callback_func =  callback.version)

    def request_mr(self):
        return self.request_any_get(
                url_str = self.request_code("/merge_requests?state=opened&scope=assigned_to_me"), 
                timeout = 0.5,
                callback_func =  callback.mr)


# PUBLIC APIs
gitlab = GitLabAPIs()
def mr(): return gitlab.request_mr()
