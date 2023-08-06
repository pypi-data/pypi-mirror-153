from unittest import mock
from unittest import TestCase

from mercuryclient.api import MercuryApi
from mercuryclient.types.insurance.request import (
    AdditionalInfo,
    InsuranceRequest,
    LoanData,
    PersonData,
    Premium,
    Customer,
    Insured,
    AccountData,
    Nominee,
)


class InsuranceMixinTest(TestCase):
    def setUp(self):
        self.client = MercuryApi(
            {
                "username": "username",
                "password": "password",
                "url": "https://mercury-dev.esthenos.in",
            }
        )
        self.request_obj = InsuranceRequest(
            plan="esthenos_creditshield",
            partner_id="esthenos",
            plan_type=2,
            reference_id="jsdjvbsjdvl001",
            category="loan",
            premium=Premium(amount=1180),
            customer=Customer(
                id="CUST001",
                name="Bittu",
                phone="9646432812",
                email="bittu.kumar_testi_blr@acko.tech",
                state="Karnataka",
            ),
            loan=LoanData(
                amount=100000,
                provider_id=2,
                provider_name="Lorem Ipsum",
                start_date="2022-05-23T12:22:27.873593Z",
                end_date="2025-03-28T12:22:27.873593Z",
                emi_amount=1200,
                hospicash_amount=1000,
                disbursement_date="2022-05-22T12:22:27.873593Z",
                account_number="ACC01",
                tenure_in_months=34,
                type="car_loan",
                family_type="1A",
                application_number="ACC01",
                person=[
                    PersonData(
                        insured=Insured(
                            name="Bittu",
                            phone="9646432812",
                            email="bittu.kumar_tesi_blr@acko.tech",
                            pincode="111111",
                            city="sample_city",
                            address="sample_address",
                            gender="Male",
                            occupation="salaried",
                            age=27,
                            dob="1995-02-05",
                            account=AccountData(
                                number="9646432812",
                                ifsc="HDFC0123456",
                                category="Regular",
                            ),
                        ),
                        nominee=Nominee(
                            name="Temp",
                            relationship="mother",
                            phone="9988509343",
                            dob="1991-08-14",
                        ),
                    )
                ],
            ),
            additional_info=AdditionalInfo(
                declaration_health="Y", assignment_clause="Y", collection_status="Y"
            ),
        )

        self.request_dict = {
            "profile": "some_profile",
            "plan": "esthenos_creditshield",
            "partner_id": "esthenos",
            "plan_type": 2,
            "reference_id": "jsdjvbsjdvl001",
            "category": "loan",
            "premium": {"amount": 1180},
            "customer": {
                "id": "CUST001",
                "name": "Bittu",
                "phone": "9646432812",
                "email": "bittu.kumar_testi_blr@acko.tech",
                "state": "Karnataka",
            },
            "loan": {
                "amount": 100000,
                "provider_id": 2,
                "provider_name": "Lorem Ipsum",
                "start_date": "2022-05-23T12:22:27.873593Z",
                "end_date": "2025-03-28T12:22:27.873593Z",
                "emi_amount": 1200,
                "hospicash_amount": 1000,
                "disbursement_date": "2022-05-22T12:22:27.873593Z",
                "account_number": "ACC01",
                "tenure_in_months": 34,
                "type": "car_loan",
                "family_type": "1A",
                "application_number": "ACC01",
                "person": [
                    {
                        "insured": {
                            "name": "Bittu",
                            "phone": "9646432812",
                            "email": "bittu.kumar_tesi_blr@acko.tech",
                            "pincode": "111111",
                            "city": "sample_city",
                            "address": "sample_address",
                            "gender": "Male",
                            "occupation": "salaried",
                            "age": 27,
                            "dob": "1995-02-05",
                            "account": {
                                "number": "9646432812",
                                "ifsc": "HDFC0123456",
                                "category": "Regular",
                            },
                        },
                        "nominee": {
                            "name": "Temp",
                            "relationship": "mother",
                            "phone": "9988509343",
                            "dob": "1991-08-14",
                        },
                    }
                ],
            },
            "additional_info": {
                "declaration_health": "Y",
                "assignment_clause": "Y",
                "collection_status": "Y",
            },
        }
        self.post_api_mock = mock.patch(
            "mercuryclient.api.MercuryApi._post_json_http_request"
        ).start()
        self.addCleanup(self.post_api_mock.stop)

    def test_request_insurance_policy(self):

        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        self.client.create_insurance_policy(self.request_obj, "some_profile")

        self.post_api_mock.assert_called_with(
            path="api/v1/insurance/create_insurace/",
            data=self.request_dict,
            send_request_id=True,
            add_bearer_token=True,
        )

    def test_request_exception_raised_if_status_code_error(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 401
        self.post_api_mock.return_value = ("random_string", mock_response)

        with self.assertRaises(Exception):
            self.client.create_insurance_policy(self.request_obj, "some_profile")

    def test_request_api_succeeds_if_status_code_success(self):
        mock_response = mock.MagicMock()
        mock_response.status_code = 201
        self.post_api_mock.return_value = ("random_string", mock_response)

        request_id = self.client.create_insurance_policy(
            self.request_obj, "some_profile"
        )
        self.assertEqual(request_id["request_id"], "random_string")
