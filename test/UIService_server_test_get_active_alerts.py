# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_test_search_alerts(UIServiceTest):
    # TESTS
    def test_get_active_alert(self):
        # TODO: we need to populate the db with different cases of 
        #       active and inactive alerts.
        ret, err = self.getImpl().get_active_alerts(self.getContext())
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, list)

