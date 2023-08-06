import requests


class UrlWorker:
    host = None
    port = None

    def get_full_url(self, url):
        return f"{self.host}:{self.port}/{url}"


class AuthMe:
    auth_url = None
    ms_auth_username = None
    ms_auth_password = None

    def authorize(self):
        data_dict = {"username": self.ms_auth_username,
                     "password": self.ms_auth_password,
                     }
        return requests.post(self.auth_url,
                             data=data_dict)

    def get_token(self):
        return self.authorize().json()['access_token']


class HeaderHandler:
    token = None

    def get_headers(self):
        return {"accept": "application/json",
                "Authorization": f"Bearer {self.token}"}


class MethodsHandler(HeaderHandler):
    ping_all_url = None
    get_all_apps_url = None
    get_deep_analyze_url = None

    def get_method_result(self, url, **kwargs):
        return requests.get(url,
                            headers=self.get_headers(),
                            **kwargs)

    def ping_all_apps(self):
        return self.get_method_result(self.ping_all_url)

    def get_all_apps(self):
        return self.get_method_result(self.get_all_apps_url)

    def get_deep_analyze(self, app_id):
        return self.get_method_result(self.get_deep_analyze_url,
                                      params={'gravity_id': app_id})
