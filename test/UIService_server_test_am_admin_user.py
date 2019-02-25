# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_am_admin_user(UIServiceTest):
    # TESTS
    def test_am_admin_user(self):
        ret, err = self.getImpl().am_admin_user(self.getContext())
        self.assertIsNone(err)
        self.assertIsInstance(ret, bool)
        self.assertEquals(ret, True)
