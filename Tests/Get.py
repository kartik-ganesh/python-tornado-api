from tornado import testing
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPClient
import main


class TestGet(testing.AsyncHTTPTestCase):
    def get_app(self):
        main.Api(run_for_tests=True)

    @testing.gen_test()
    def testing_get(self):
        request = HTTPRequest(url="http://localhost:8080/api/users", method="GET", body=None)
        client = AsyncHTTPClient()
        response = yield client.fetch(request, self.stop())
        self.assertEquals(response.code, 200)


if __name__ == "__main__":
    testing.main(verbosity=2)