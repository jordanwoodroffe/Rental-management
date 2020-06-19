import unittest
import requests
import responses
from unittest.mock import Mock, patch


URL = "http://127.0.0.1:5000/"


class TestApp(unittest.TestCase):

    def test_404(self):
        result = requests.get(
            "{}{}".format(URL, "/page_not_found")
        )
        self.assertEquals(result.status_code, 404)

    @responses.activate
    def test_403(self):
        responses.add(responses.GET, "{}{}".format(URL, "/forbidden"),
                      json={'error': 'forbidden'}, status=403)

        result = requests.get(
            "{}{}".format(URL, "/forbidden")
        )
        self.assertEquals(result.status_code, 403)

    @responses.activate
    def test_500(self):
        responses.add(responses.GET, "{}{}".format(URL, "/server_error"),
                      json={'error': 'forbidden'}, status=500)

        result = requests.get(
            "{}{}".format(URL, "/server_error")
        )
        self.assertEquals(result.status_code, 500)


if __name__ == '__main__':
    unittest.main()
