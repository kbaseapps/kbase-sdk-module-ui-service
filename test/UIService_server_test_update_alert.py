# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest
from UIService.UIServiceModel import UIServiceModel

class UIServiceTest_test_update_alert(UIServiceTest):

    def test_update_alert(self):
        a_random_string, alert_id = self.add_random_alert()
        alert = self.get_alert(alert_id)
        alert_id = alert['id']

        another_random_string = self.generate_random_string()
        test_table = [
            {
                'field': 'title',
                'value': 'title_' + another_random_string
            },
            {
                'field': 'message',
                'value': 'message_' + another_random_string
            },
            {
                'field': 'start_at',
                'value': UIServiceModel.iso_to_iso('2019-01-02T00:00:00Z')
            },
            {
                'field': 'end_at',
                'value': UIServiceModel.iso_to_iso('2019-01-03T00:00:00Z')
            }
        ]

        for test in test_table:
            field_name = test['field']
            input = {
                'alert': {
                    'id': alert_id
                }
            }
            input['alert'][field_name] = test['value']

            ret, err = self.getImpl().update_alert(self.getContext(), input)
            self.assertIsNotNone(ret)
            self.assertIsNone(err)

            alert2 = self.get_alert(alert_id)
            self.assertEquals(alert2[field_name], input['alert'][field_name])

    