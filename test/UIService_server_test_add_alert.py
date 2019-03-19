# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTestAddAlert(UIServiceTest):
    def test_add_alert(self):
        a_random_string, _id = self.add_random_alert()
        alert = self.get_alert_by_title(a_random_string)
        self.assertEquals(alert[0]['title'], 'title_' + a_random_string)

        a_random_string, _id = self.add_random_alert(False)
        alert = self.get_alert_by_title(a_random_string)
        self.assertEquals(alert[0]['title'], 'title_' + a_random_string)

    