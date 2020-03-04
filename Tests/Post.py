from tornado import testing
from tornado.testing import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
import main
import json


class TestPost(testing.AsyncHTTPTestCase):
    def get_app(self):
        return main.Api(run_for_tests=True)

    # def setUp(self):
    #     super(TestPost, self).setUp()

    @testing.gen_test()
    def testing_post(self):
        body = {
                "id": "999",
                "name": "userTest"
                }
        request = HTTPRequest(url="http://localhost:8080/api/users", method="POST", body=json.dumps(body))
        client = AsyncHTTPClient()
        resp = yield client.fetch(request, self.stop)
        self.assertEqual(resp.code, 200)

    # def tearDown(self):
    #     super(TestPost, self).tearDown()


if __name__ == "__main__":
    testing.main(verbosity=2)
