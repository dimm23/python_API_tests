import unittest
import json
import time
import re
import api
from settings import *
import pandas as pd
from test_functions import *


class MyTestResult(unittest.TestResult):
    def addFailure(self, test, err):
        # print(str(test) + ": " + str(err))
        test_name = str(test).split(" ")[0]
        print(str(test_name) + ": Failed")
        super(MyTestResult, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = str(test).split(" ")[0]
        print(str(test_name) + ": " + str(err[1]))
        super(MyTestResult, self).addError(test, err)


class All_api_methods_testing(unittest.TestCase):
    u = api.Utopia("http://127.0.0.1:"+API_PORT+"/api/1.0", TOKEN)
    pattern = re.compile("^([A-Z0-9]){32}")   
    getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", ' \
                        '"startDateTime": "", "endDateTime": "", "referenceNumber": "" }'
    
    def setUp(self):        
        self.status = False

    def test_cancelInvoice(self) -> 'reference_number':
        """Method cancelInvoice allows to cancel the already created invoice. The method is called with mandatory
        'InvoiceId' parameter. Parameter InvoiceId contains the ID value for the invoice that needs to be declined.
        To get the ID of the required invoice it is mandatory to call the getInvoices method for receiving the
        list of invoices with their detailed information. In response the declineInvoice method returns in the
        Response block the results of completing this request."""

        invoice = None

        # Action
        _, awaiting_requests = self.u.getFinanceHistory("AWAITING_REQUESTS", "", "", "", "", "", "")
        if len(awaiting_requests) < 5:
            _, invoice_ref_num = self.u.sendInvoice("API request", CONTACT_CARD, 10)
            time.sleep(3)  # wait for network confirmation
            _, invoice = self.u.getInvoiceByReferenceNumber(invoice_ref_num)
        else:
            invoice = awaiting_requests[0]
        status, result = self.u.cancelInvoice(invoice["invoiceid"])
        time.sleep(3)  # wait for network confirmation

        # Assertion
        AssertResultIsRefNum(self, status, result)

    # def tearDown(self):
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
