from tornado import testing
from tornado.testing import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
import main
import json


class TestPost(testing.AsyncHTTPTestCase):
    def get_app(self):
        return main.Api(run_for_tests=True)

    def setUp(self):
        super(TestPost, self).setUp()
        # body = {
        #     "id": "999",
        #     "name": "user"
        # }
        # request = HTTPRequest(url="http://localhost:8080/api/users", method="POST", body=json.dumps(body))
        # client = AsyncHTTPClient()
        # resp = yield client.fetch(request, self.stop)

    @testing.gen_test()
    def test_data_put(self):
        body = {
            "id": "999",
            "name": "user"
        }
        request = HTTPRequest(url="http://localhost:8080/api/users", method="POST", body=json.dumps(body))
        client = AsyncHTTPClient()
        resp = yield client.fetch(request, self.stop)
        body = {
                "id": "999",
                "name": "userTest"
                }
        request = HTTPRequest(url="http://localhost:8080/api/users/999", method="PUT", body=json.dumps(body))
        # client = AsyncHTTPClient()
        resp = yield client.fetch(request, self.stop)
        self.assertEqual(resp.code, 200)

        # request = HTTPRequest(url="http://localhost:8080/api/users/999", method="DELETE")
        # client = AsyncHTTPClient()
        # resp = yield client.fetch(request, self.stop)

    def tearDown(self):
        super(TestPost, self).tearDown()
        # request = HTTPRequest(url="http://localhost:8080/api/users/999", method="DELETE")
        # client = AsyncHTTPClient()
        # resp = yield client.fetch(request, self.stop)


if __name__ == "__main__":
    testing.main(verbosity=2)
