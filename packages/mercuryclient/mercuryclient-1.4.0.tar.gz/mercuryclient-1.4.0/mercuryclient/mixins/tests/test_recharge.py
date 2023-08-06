from unittest import TestCase, mock
from mercuryclient.api import MercuryApi


class RechargeMixinTest(TestCase):
    def setUp(self):

        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )

        self.request_dict = {"operator": 1, "number": 9876543210, "amount": 10}

        self.expected_dict = {
            "operator": 1,
            "number": 9876543210,
            "amount": 10,
            "profile": "some_profile",
        }
        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_request_recharge(self):

        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        self.client.make_recharge(self.request_dict, "some_profile")
        self.post_api_mock.assert_called_with(
            path="api/v1/mobile_recharge/recharge/",
            data=self.expected_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)
        with self.assertRaises(Exception):
            self.client.make_recharge(self.request_dict, "some_profile")

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)
        request_id = self.client.make_recharge(self.request_dict, "some_profile")
        self.assertEqual(request_id["request_id"], "random_string")
