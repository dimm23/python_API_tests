import re


pattern = re.compile("^([A-Z0-9]){64}")  # pattern for check response as reference_number


def AssertNotEmptyOrError(self, status, result):
    """Ожидание что result, возвращаемый вызовом метода, не пустой и не содержит слово Error"""

    self.assertTrue(status, "Status or request: " + str(status) + "; Result: " + str(result))
    self.assertTrue(result != "", "Failed of request execution: empty result")
    self.assertTrue("Error" not in str(result), "Error: " + str(result))


def AssertResultIsRefNum(self, status, result):
    """Ожидание что result, возвращённый вызовом метода, представляет собой reference number"""

    self.assertTrue(status, "Status or request: " + str(status) + "; Result: " + str(result))
    self.assertTrue(result != "", "Failed of request execution: empty result")
    self.assertTrue(pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")


def AssertResultIsTrue(self, status, result):
    """Ожидание что result, возвращённый вызовом апи метода, представляет собой булево значение True"""

    self.assertTrue(status, "Status or request: " + str(status) + "; Result: " + str(result))
    self.assertTrue(result != "", "Failed of request execution: empty result")
    self.assertTrue(result, "Result is: " + str(result))
