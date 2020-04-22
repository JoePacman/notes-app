import unittest
from unittest import mock
from project.main import app
from project.service import datastore
from project import main
from google.cloud.datastore.entity import Entity
from flask import json

# for a good tutorial on python mocking run through
# https://medium.com/python-pandemonium/python-mocking-you-are-a-tricksy-beast-6c4a1f8d19b2


class MainTests(unittest.TestCase):

    ############################
    # setup and teardown #######
    ############################
    def setUp(self):
        print("Setup before EACH test")
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        print("Tear down after EACH test")

    ###############
    # tests ######
    ###############
    @mock.patch("project.service.datastore.DatastoreService")
    def test_mock_datastore_get(self, mock_datastore_service):
        entity = Entity()
        entity.update({'title': 'Example Title', 'note_text': 'Example text', 'user': 'joe.blogs@gmail.com',
                       'last_modified_date': '', 'created_date': ''})
        entities = list()
        entities.append(entity)
        mock_datastore_service.return_value.get.return_value = entities
        main.datastore = datastore.DatastoreService()  # instantiate a new DatastoreService so it is replaced with mock
        r = self.app.post('/note/get', data=json.dumps({
            'user': 'joe.blogs@gmail.com'
        }), headers={'Content-Type': 'application/json'})
        assert r.status_code == 200
        assert r.json == {'matches':[
                {'title': 'Example Title',
                 'note_text': 'Example text',
                 'last_modified_date': ''}]}


if __name__ == "__main__":
    unittest.main()
