import unittest
import json
import time
import re
import api
import settings
import pandas as pd
from test_functions import *

class MyTestResult(unittest.TestResult):
    def addFailure(self, test, err):
        #print(str(test) + ": " + str(err))
        test_name = str(test).split(" ")[0]
        print(str(test_name) + ": Failed")
        super(MyTestResult, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = str(test).split(" ")[0]
        print(str(test_name) + ": " + str(err[1]))
        super(MyTestResult, self).addError(test, err)


class All_api_methods_testing(unittest.TestCase):
    u = api.Utopia("http://127.0.0.1:"+settings.API_PORT+"/api/1.0",settings.TOKEN)
    pattern = re.compile("^([A-Z0-9]){32}")   
    getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", ' \
                        '"startDateTime": "", "endDateTime": "", "referenceNumber": "" }'
    
    def setUp(self):        
        self.status = False

    def test_createChannel(self):
        # Test data
        channel_name = "Test Channel |+_)(*&^%$#@!~"
        description = "description _)(*?:%;№"
        read_only = "false"
        read_only_privacy = ""
        password = ""
        languages = ""
        hash_tags = "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x"
        geo_tag = "10.000, 20.000, 30.000trh65srt4h65srt4h564"
        avatar = ""
        hide_in_ui = "false"

        # Action
        self.status, myChannel = self.u.createChannel(channel_name, description, read_only, read_only_privacy, password,
                                                      languages, hash_tags, geo_tag, avatar, hide_in_ui)
        time.sleep(3)  # wait for uchan database sync ends
        # self.u.deleteChannel(myChannel, password)  # cleanup step
        self.result = myChannel

        # Assertion
        AssertEmptyOrError(self, self.status, myChannel)

    #def tearDown(self):
    #    print("status: " + str(self.status))
    #    try:
    #        print("result: " + str(self.result))
    #        if "error" in str(self.result):
    #            print("If result: " + str(self.result))
    #        self.assertFalse("Unable" in str(self.result), msg = "result: " + str(self.result))
    #    except Exception:
    #        time.sleep(0.001)
    #    self.assertTrue(bool(self.status), "Status of request execution is False")

if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult))
