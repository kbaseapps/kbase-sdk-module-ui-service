# -*- coding: utf-8 -*-
from UIServiceTest import UIServiceTest

class UIServiceTest_test_get_alert(UIServiceTest):
    # TESTS
    def test_get_alert(self):

        # TEST: correct error for missing id in param
        param = {
            'idx': 'should_not_exist'
        }

        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assert_error(ret, err, 'input', 'missing')
        self.assertEquals(err['info']['key'], 'id')

        # TEST: wrong type for id in param
        param = {
            'id': 1
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assert_error(ret, err, 'input', 'wrong-type')
        self.assertEquals(err['info']['key'], 'id')

        # TEST: Not found
        param = {
            'id': 'abc123'
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assertIsNone(ret)
        self.assertIsNone(err)
        # self.assert_error(ret, err, 'data', 'notfound')
        # self.assertEquals(err['info']['id'], 'abc123')

        # TEST: success
        # presumes this alert is already present.
        alert_title, alert_id = self.add_random_alert()
        param = {
            'id': alert_id
        }
        ret, err = self.getImpl().get_alert(self.getContext(), param)
        self.assertIsNotNone(ret)
        self.assertIsNone(err)
        self.assertIsInstance(ret, dict)
