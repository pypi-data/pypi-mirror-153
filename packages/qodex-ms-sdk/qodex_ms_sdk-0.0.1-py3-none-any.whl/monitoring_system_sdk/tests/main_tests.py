import unittest
from monitoring_system_sdk import main


class TestCase(unittest.TestCase):
    inst = main.MonitoringSystemWorker()

    def test_auth(self):
        auth_result = self.inst.authorize()
        self.assertIn('access_token', auth_result.json())

    def test_ping_apps(self):
        ping_result = self.inst.ping_all_apps()
        self.assertIsInstance(ping_result.json(), dict)

    def test_get_all_apps(self):
        all_apps = self.inst.get_all_apps().json()
        self.assertIsInstance(all_apps, list)

    def test_get_deep_analze(self):
        res = self.inst.get_deep_analyze(2).json()
        #self.assertIsInstance(res.j)

    def test_get_global_analyze(self):
        result = self.inst.get_global_deep_analyze()
        print(result)


if __name__ == '__main__':
    unittest.main()
