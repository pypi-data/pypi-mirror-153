import logging

logger = logging.getLogger(__name__)


class RechargeMixin:
    def get_operators_list(self, profile: str):

        """
        Get oparators list using the mercury service
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,result )
        """
        api = "api/v1/mobile_recharge/get_providers/"
        request_dict = {}
        request_dict["profile"] = profile
        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )
        if r.status_code == 201:
            return {"request_id": request_id, "data": r.content}
        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending get provider Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def make_recharge(self, rechagre_data, profile):

        """
        Make recharge using mercury service
        :param rechagre_data: data for recharge
        :param Profile: An existing profile in Mercury.
        """
        api = "api/v1/mobile_recharge/recharge/"
        rechagre_data["profile"] = profile
        request_id, r = self._post_json_http_request(
            path=api, data=rechagre_data, send_request_id=True, add_bearer_token=True
        )
        if r.status_code == 201:
            return {"request_id": request_id, "data": r.content}
        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending get provider Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_recharge_status(self, status_data, profile):

        """
        Make recharge using mercury service
        :param status_data: data for recharge
        :param Profile: An existing profile in Mercury.
        """
        api = "api/v1/mobile_recharge/status/"
        status_data["profile"] = profile
        request_id, r = self._post_json_http_request(
            path=api, data=status_data, send_request_id=True, add_bearer_token=True
        )
        if r.status_code == 201:
            return {"request_id": request_id, "data": r.content}
        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending get provider Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_recharge_wallet_balance(self, profile):

        """
        check wallet balance using mercury service
        :param Profile: An existing profile in Mercury.
        """
        api = "api/v1/mobile_recharge/balance/"
        request_dict = {}
        request_dict["profile"] = profile
        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )
        if r.status_code == 201:
            return {"request_id": request_id, "data": r.content}
        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending get rechagre balance Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_recharge_ip(self, profile):

        """
        get ip of securepayment using mercury service
        :param Profile: An existing profile in Mercury.
        """
        api = "api/v1/mobile_recharge/ip/"
        request_dict = {}
        request_dict["profile"] = profile
        request_id, r = self._post_json_http_request(
            path=api, data=request_dict, send_request_id=True, add_bearer_token=True
        )
        print(f"Error {request_dict} {r} {r.status_code}")
        if r.status_code == 201:
            return {"request_id": request_id, "data": r.content}
        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending fetching IP Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )

    def get_recharge_plans(self, operator, profile):
        """
        Make recharge using mercury service
        :param operator: data for recharge
        :param Profile: An existing profile in Mercury.
        """
        api = "api/v1/mobile_recharge/plans/"
        operator["profile"] = profile
        request_id, r = self._post_json_http_request(
            path=api, data=operator, send_request_id=True, add_bearer_token=True
        )
        if r.status_code == 201:
            return {"request_id": request_id, "data": r.content}
        try:
            response_json = r.json()
        except Exception:
            response_json = {}
        raise Exception(
            "Error while sending get provider Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )
