import os
import mws
import xml.etree.ElementTree as ET
import re
from g_sheet import main
import datetime
import unittest

class TestRegIt(unittest.TestCase):
    def test_reg_it(self):
        test_text = '{http://example.com}example_text'
        result = reg_it(test_text)
        self.assertEqual(result, 'example_text')

class TestSource(unittest.TestCase):
    def setUp(self):
        self.path = './test_dir'
        os.makedirs(self.path, exist_ok=True)
        os.environ['MWS_ACCESS_KEY'] = 'test_access_key'
        os.environ['MWS_SECRET_KEY'] = 'test_secret_key'
        os.environ['MWS_ACCOUNT_ID'] = 'test_account_id'
        os.environ['MWS_MARKETPLACE_ID'] = 'test_marketplace_id'

    def test_source(self):
        with open('ListOrders.xml', 'w') as f:
            f.write('<test>example_xml</test>')
        with open('ListOrderItems.xml', 'w') as f:
            f.write('<test>example_xml</test>')
        main.return_value = []
        source(self.path)
        self.assertTrue(os.path.exists(os.path.join(self.path, 'orders_report.txt')))
        with open(os.path.join(self.path, 'orders_report.txt')) as f:
            content = f.read()
            self.assertTrue('order-id' in content)
            self.assertTrue('price-designation' in content)
        
    def tearDown(self):
        os.remove('ListOrders.xml')
        os.remove('ListOrderItems.xml')
        os.remove(os.path.join(self.path, 'orders_report.txt'))
        os.rmdir(self.path)

if __name__ == '__main__':
    unittest.main()
