import os
import time
import pytest
import requests
import json
from time import sleep
from conftest import Test_Varibles
from pytest_html_reporter import attach

CurrentPath = os.path.realpath(__file__)
BaseName = os.path.basename(__file__)
Test_Case_No = BaseName.replace('.py', '')
print(Test_Case_No)



class Test_DeviceRegistration:
    
    def test_method_1_QCC2CPLAT_T1(self, supply_url):
        url = supply_url[0] + "device-request-processor/v1/device/registration"
        headers = supply_url[1]
        with open("device_registration.json") as inputFile:
            payload = json.load(inputFile)
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        attach(data=self.driver.get_screenshot_as_png())
        assert (response.status_code == 200)
        print(response.text)
        response_body = response.json()
        assert (response_body["responseCode"] == str(2001))
        assert (response_body["responseMessage"] == "SUCCESS")
        Test_Varibles.request_id = response_body["responseData"]["requestId"]
        assert (response_body["responseData"]["status"] == "SUBMITTED")
        assert (response_body["responseData"]["message"] == "Request Submitted for registration!")
        

    def test_method_1_QCC2CPLAT_T2(self, supply_url):
        final_url = supply_url[2] + str(Test_Varibles.request_id)
        print(final_url)
        time.sleep(10)
        response = requests.get(final_url)
        print(response.status_code, response.json())
        attach(data=self.driver.get_screenshot_as_png())
        assert (response.status_code == 200)
        
        response_body = response.json()
        assert (response_body["responseCode"] == str(2001))
        assert (response_body["responseMessage"] == "SUCCESS")
        request_id = response_body["responseData"]["requestId"]
        assert Test_Varibles.request_id == request_id
        assert (response_body["responseData"]["status"] == "In Progress")
        assert (response_body["responseData"]["successCount"] == 1)
        assert (response_body["responseData"]["failCount"] == 0)
        assert (response_body["responseData"]["totalCount"] == 1)
        assert (response_body["responseData"]["message"] == "")
        

    def test_method_1_QCC2CPLAT_T3(self, supply_url):
            url = supply_url[3] + str(Test_Varibles.request_id) + "/" + "devices"
            print(url)
            time.sleep(10)
            response_data = requests.get(url)
            print(response_data.status_code, response_data.json())
            attach(data=self.driver.get_screenshot_as_png())
            assert (response_data.status_code == 200)
            attach(data=self.driver.get_screenshot_as_png())

