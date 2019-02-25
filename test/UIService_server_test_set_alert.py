# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest
from UIService.UIServiceModel import UIServiceModel

class UIServiceTest_test_set_alert(UIServiceTest):
    def test_set_alert(self):
        a_random_string, alert_id = self.add_random_alert()
        alert = self.get_alert(alert_id)
        alert_id = alert['id']
        another_random_string = self.generate_random_string()
        input = {
            'alert': {
                'id': alert_id,
                'title': 'title_' + another_random_string,
                'message': 'message_' + another_random_string,
                'status': 'status_' + another_random_string,
                'start_at': UIServiceModel.iso_to_iso('2019-01-01T00:00:00Z'),
                'end_at': UIServiceModel.iso_to_iso('2019-01-02T00:00:00Z'),
            }
        }
        ret, err = self.getImpl().set_alert(self.getContext(), input)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)

        alert2 = self.get_alert(alert_id)
        self.assertEquals(alert2['title'], input['alert']['title'])
        self.assertEquals(alert2['message'], input['alert']['message'])

        self.assertNotEquals(alert2['title'], alert['title'])
        self.assertNotEquals(alert2['message'], alert['message'])

  
