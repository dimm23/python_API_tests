import re


reference_number = re.compile("^([A-Z0-9]){64}")  # pattern for check response as reference_number


def AssertNotEmptyOrError(status, result):
    """Ожидание что result, возвращаемый вызовом метода, не пустой и не содержит слово Error"""

    assert status, "Status or request: " + str(status) + "; Result: " + str(result)
    assert result != "" and str(result) != "0", "Failed of request execution: empty result"
    assert "Error" not in str(result), "Error: " + str(result)


def AssertResultIsRefNum(status, result):
    """Ожидание что result, возвращённый вызовом метода, представляет собой reference number"""

    assert status, "Status or request: " + str(status) + "; Result: " + str(result)
    assert result != "", "Failed of request execution: empty result"
    assert reference_number.match(str(result)), "Result '" + str(result) + "' is not reference number"


def AssertResultIsTrue(status, result):
    """Ожидание что result, возвращённый вызовом апи метода, представляет собой булево значение True"""

    assert status, "Status or request: " + str(status) + "; Result: " + str(result)
    assert result != "", "Failed of request execution: empty result"
    assert result, "Result is: " + str(result)


def AssertResultIsNotEmpty(status, result):
    """Ожиданое что result не пустой"""
    assert status, "Status or request: " + str(status) + "; Result: " + str(result)
    assert result != "" and str(result) != "0", "Failed of request execution: empty result"


def AssertErrorInResult(status, result):
    """Ожидание что в result будет слово Error"""
    assert status, "Status or request: " + str(status) + "; Result: " + str(result)
    assert 'Error' in result, "Operation with errors"


def AssertResultIsZero(status, result):
    """Ожидание того что результат равен нулю"""
    assert status, "Status or request: " + str(status) + "; Result: " + str(result)
    assert str(result) == "0", "Operation without errors"


def AssertUnableToExecute(status, result):
    """Ожидание что status будет False а result будет содержать текст Unable to execute api request"""
    assert status is False
    assert "Unable to execute api request" in result
