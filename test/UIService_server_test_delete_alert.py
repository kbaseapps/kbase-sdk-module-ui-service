# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_test_delete_alert(UIServiceTest):
    def test_delete_alert(self):
        a_random_string, _id = self.add_random_alert()
        alerts = self.get_alert_by_title(a_random_string)
        alert_id = alerts[0]['id']
        ret, err = self.getImpl().delete_alert(self.getContext(), alert_id)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
