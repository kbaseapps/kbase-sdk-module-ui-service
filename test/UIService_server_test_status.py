# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_test_status(UIServiceTest):
    # TESTS
    def test_status(self):
        ret = self.getImpl().status(self.getContext())
        ret = ret[0]
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, dict)
        self.assertIn('state', ret)
        self.assertEquals(ret['state'], 'OK')
