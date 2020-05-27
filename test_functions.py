import re


pattern = re.compile("^([A-Z0-9]){64}")  # pattern for check response as reference_number


def AssertNotEmptyOrError(self, status, result):
    self.assertTrue(status, "Status or request: " + str(status))
    self.assertTrue(result != "", "Failed of request execution: empty result")
    self.assertTrue("Error" not in str(result), "Error: " + str(result))


def AssertResultIsRefNum(self, status, result):
    self.assertTrue(status, "Status or request: " + str(status))
    self.assertTrue(result != "", "Failed of request execution: empty result")
    self.assertTrue(pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")


def AssertResultIsTrue(self, status, result):
    self.assertTrue(status, "Status or request: " + str(status))
    self.assertTrue(result, "Result is: " + str(result))
