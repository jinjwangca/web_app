import unittest
from components.DatabaseGateway import DatabaseGateway

class TestDatabaseGateway(unittest.TestCase):
    '''
    setUp function is used to instantiate the object we are testing.
    '''
    def setUp(self):
        self.databaseGateway = DatabaseGateway()

    '''
    Test the add_data function.
    '''
    def test_add_data(self):
        id = "TestID"
        data = "TestData"
        collection = 'TestCollection'
        self.databaseGateway.delete_all_data(collection)
        result = self.databaseGateway.add_data(id,data,collection)
        assert result == id

    '''
    Test the get_data function.
    '''
    def test_get_data(self):
        id = "TestID"
        data = "TestData"
        collection = 'TestCollection'
        self.databaseGateway.delete_all_data(collection)
        self.databaseGateway.add_data(id,data,collection)
        result = self.databaseGateway.get_data(id, collection)
        assert result == data

    '''
    Test the delete_data function.
    '''
    def test_delete_data(self):
        id = "TestID"
        data = "TestData"
        collection = 'TestCollection'
        self.databaseGateway.delete_all_data(collection)
        self.databaseGateway.add_data(id,data,collection)
        result = self.databaseGateway.delete_data(id, collection)
        assert result == 1

    '''
    Test the delete_all_data function.
    '''
    def test_delete_all_data(self):
        id = "TestID"
        data = "TestData"
        collection = 'TestCollection'
        self.databaseGateway.delete_all_data(collection)
        self.databaseGateway.add_data(id,data,collection)
        result = self.databaseGateway.delete_all_data(collection)
        assert result == 1

if __name__ == '__main__':
    unittest.main()
