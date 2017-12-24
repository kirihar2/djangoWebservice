__author__ = 'jurankirihara'
import unittest
from os import path,makedirs,remove,rmdir,listdir,getcwd
from JsonSerialize.AttributeToJson import JsonSerialize
from sklearn.linear_model import LogisticRegression,LinearRegression
class JsonSerializeUnitTests(unittest.TestCase):
    #create directory JsonTest and store it as variable
    def setUp(self):
        print("Setting up")
        self.filename="sampleJsonAttributes"
        self.directory=path.join(getcwd(),'JsonTest')
        self.fullpath = path.join(self.directory, self.filename)
        if not path.exists(self.directory):
            makedirs(self.directory)

    def testConstructionValid(self):
        ser = JsonSerialize(self.fullpath)
        self.assertEqual(ser.file, self.fullpath+'.json')
    def testConstructionWithRename(self):
        ser = JsonSerialize(self.fullpath)
        ser.data_to_json(LinearRegression())
        ser.data_to_json(LinearRegression())
        self.assertEqual(ser.file, self.fullpath+'_1.json')


    #tear down the test variable
    def tearDown(self):
        print("Tearing down")
        for file in listdir(self.directory):
            remove(path.join(self.directory,file))
        rmdir(self.directory)
if __name__ == '__main__':
    unittest.main()
