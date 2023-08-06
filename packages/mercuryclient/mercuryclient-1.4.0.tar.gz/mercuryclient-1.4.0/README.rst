===========
Mercury SDK
===========

Mercury SDK can be used in projects that interface with the mercury service
that provides common internal functionality.

Initializing the client
-------------------------------
::

  from mercuryclient import MercuryApi
  # Setup connection parameters
  conn_params = {'username': 'mercury_username', 'password':'password', 'url':'https://mercury-url.com'}
  m = MercuryApi(conn_params)
  m.send_mail(['recipent@email.com'],'Test mail', 'Mail body','ses','ses_profile')

Available APIs:
----------------------
- send_mail
- send_sms
- request_experian_report
- get_experian_response
- fetch_experian_report
- request_cibil_report
- get_cibil_response
- fetch_cibil_report
- request_highmark_report
- get_highmark_response
- fetch_highmark_report
- request_verify_id
- get_verify_id_result
- request_bank_statement
- get_bank_statement_result
- verify_webhook
- insurance
- secure_patyment_recharge
  - get_operators_list
  - make_recharge
  - get_recharge_status
  - get_recharge_wallet_balance
  - get_recharge_ip

Types:
------
For complex requests like CIBIL, Experian or Highmark, you can construct the request
JSON using the provided pydantic models. The types are available at *mercury.types.<request_type>.request*.

Example using models for generating Highmark Request::

  from mercuryclient.types.highmark.request import Applicant, HighmarkRequest
  applicant = Applicant(name="Example Name" ...)
  request_obj = HighmarkRequest(
      applicant=applicant,
      inquiry_reference_number="ABCDE",
      ...
  )
  # After generating your request, pass the object to the corresponding request
  m.fetch_highmark_report(request_obj, profile="sample_profile)

Testing:
-------------
Tests are run under *tox*

You can install tox with

>>> pip install tox

If using pyenv - you can do the following steps before running tox
(patch version will depend on your installations - tox only considers the major version)

>>> pyenv local 3.7.3 3.6.8 3.8.1

Without this step - tox will not be able to find the interpreters

Run tests using the following command

>>> tox
