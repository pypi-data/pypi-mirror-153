import json
from mercuryclient.types.insurance.request import InsuranceRequest


class InsuranceMixin:
    def create_insurance_policy(self, request_obj: InsuranceRequest, profile: str):

        """
        Create Insurance policy using the mercury service

        :param: request_obj: InsuranceRequest
        :param profile: An existing profile in Mercury.
        :return: (request_id, status,plicy data )
        """

        api = "api/v1/insurance/create_insurace/"

        request_dict = json.loads(request_obj.json(exclude_unset=True))
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
            "Error while sending Insurance Request Status: {}, Response is {}".format(
                r.status_code, response_json
            )
        )
