import unittest

from project import app

class BasicTests(unittest.TestCase):

    ############################
    # setup and teardown #######
    ############################
    def setUp(self):
        print("SETUP")

    def tearDown(self):
        print("TEAR DOWN")

    ###############
    # tests ######
    ###############
    def test_simple_endpoint(self):
        app.testing = True
        client = app.test_client()

        r = client.get('/json')
        assert r.status_code == 200
        assert r.json == {'one': 1, 'two': 2, 'three': 3}


if __name__ == "__main__":
    unittest.main()
