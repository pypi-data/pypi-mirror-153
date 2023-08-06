import traceback

from monitoring_system_sdk import mixins


class MonitoringSystemWorker(mixins.UrlWorker, mixins.AuthMe,
                             mixins.MethodsHandler):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.ms_auth_username = username
        self.ms_auth_password = password
        self.auth_url = self.get_full_url('token')
        self.token = self.get_token()
        self.ping_all_url = self.get_full_url('check_all_apps_availability')
        self.get_all_apps_url = self.get_full_url('get_all_gravities')
        self.get_deep_analyze_url = self.get_full_url('deep_analyze')

    def get_global_deep_analyze(self):
        all_apps = self.get_all_apps().json()
        result = {}
        for app in all_apps:
            if not app:
                continue
            try:
                result[app['name']] = self.get_deep_analyze(app['id']).json()
            except:
                result[app['name']] = traceback.format_exc()
        return result
