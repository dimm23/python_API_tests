import pytest
import json
import time
import api
from settings import *
from datetime import datetime
from test_functions import *
from pprint import pprint

report_file = "../test_report.txt"
report_recipients = "31033EA6DD56AF6BD07B6DB4721A00BE9756084F2E76C17281FDDC57D73C0B09"

u = api.Utopia("http://127.0.0.1:" + API_PORT + "/api/1.0", TOKEN)
getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", ' \
                    '"startDateTime": "", "endDateTime": "", "referenceNumber": "" } '


def test_getSystemInfo() -> json:
    """Method getSystemInfo returns information about current packaging
    version of the Utopia application in the Response block.
    The method is called without using any parameters."""

    # Action
    status, result = u.getSystemInfo()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getBalance() -> str:
    """Method getBalance returns in the Response field the amount of cryptons on the primary balance,
    without considering the balance on cards. Method is called without using any parameters."""

    # Action
    status, result = u.getBalance()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getCards() -> json:
    """Method getCards returns in the Response field the current list of cards and their
    detailed information from uWallet. Method is called without using any parameters."""

    # Action
    status, result = u.getCards()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getVouchers() -> json:
    """Method getVouchers returns to the Response field the information about existing vouchers as a list.
    The method is called without using any parameters."""

    # Action
    status, result = u.getVouchers()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getInvoices() -> json:
    """Method getInvoices returns to the Response field the list of active invoices.
    The method is called with using any optional parameters."""

    # Action
    status, result = u.getInvoices(getInvoicesParams)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getProfileStatus() -> json:
    """Method getProfileStatus returns the profile status"""

    # Action
    status, result = u.getProfileStatus()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getContacts(filtr: str = "") -> json:
    """Method getContacts returns to the Response field the list of contacts, it is possible to search by
    full or partial matching of the Public Key and Nickname. As a parameter it is possible to specify
    Filter that transfers the text line to search for contacts ( has to contain full or partial matching
    with Public Key or Nickname of the searched contact).The Filter "#owner#" will return information
    about your"""

    # Action
    status, result = u.getContacts(filtr)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getContactAvatar(contact_pk: str = CONTACT_PK) -> json:
    """Method getContactAvatar returns to the Response field the avatar of the selected user in the base64
    or hex format. As a parameter the method uses Public Key of the contact."""

    # Action
    status, result = u.getContactAvatar(contact_pk, "BASE64", "JPG")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendCorrectInstantMessage(contact_pk: str = CONTACT_PK) -> json:
    """Method sendInstantMessage sends personal message(IM) to the selected contact from the contact list.
    The method is called by using the To parameter, that passes on the Public Key or Nickname to whom
    the message would be sent (Public Key can be recognized by using the getContacts method) and Text,
    which contains the text of the message. In the Response field the status of completion
    of the operation is displayed."""

    # Action
    txt_message = "API method sendInstantMessage testing \n ======================= \n Python unittest"
    status, result = u.sendInstantMessage(contact_pk, txt_message)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendBlankInstantMessageIsFailed(contact_pk: str = CONTACT_PK) -> json:
    """Проверяем что невозможно отправить пустое сообщение"""

    # Action
    txt_message = ""
    status, result = u.sendInstantMessage(contact_pk, txt_message)

    # Assertion
    AssertResultIsZero(status, result)


def test_sendSingleSpaceInstantMessageIsFailed(contact_pk: str = CONTACT_PK) -> json:
    """Проверяем что невозможно отправить сообщение только из одного символа пробела"""

    # Action
    txt_message = " "
    status, result = u.sendInstantMessage(contact_pk, txt_message)

    # Assertion
    AssertResultIsZero(status, result)


def test_sendEmailMessage(contacts_pk: tuple = (CONTACT_PK,), attachId: str = "") -> json:
    """Method sendEmailMessage sends uMail to the selected contact in the Utopia network.
    The method is called by using the To parameter, which passes on the Public Key or Nickname
    to which the uMail would be sent (Public Key can be recognized by using the getContacts method);
    Subject, that determines the subject of the email; and Body, which passes on the text in the body
    of the uMail. In the Response field the status of completion of the operation is displayed."""

    # Action
    body_text = "This is a Python api body"
    subject_text = "This is a Python api subject"

    status, result = u.sendEmailMessage(contacts_pk, subject_text, body_text, attachId)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendPaymentToPk(recipient: str = CONTACT_PK,
                         _card: str = "",
                         amount: int = 0.001) -> 'reference_number':
    """Method sendPayment sends cryptons transfer for the specified amount to the contact or to the card.
    The method is called by using the To parameters (nick, pk, cardid), which pass on the Public Key,
    Nickname or the card number of the user to whom the transfer would be sent (Public Key can be recognized
    by using the getContacts method); Amount, which transfers the amount of transfer (the number needs to be
    greater than 0 and contain no more than 9 character after coma); Comment is optional, which contains
    the text of the comment (up to 148 characters); as well as the optional 'From card' field can be specified,
    that passes on the card number from which the cryptons will be taken from. If the parameter is empty,
    then cryptons would be deducted from the main account. In the Response field the status of completion
    of the operation is displayed."""

    # Test data
    comment = "payment from pk to pk"

    # Action
    status, result = u.sendPayment(recipient, comment, _card, amount)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_sendPaymentToCard(recipient: str = CONTACT_CARD,
                           _card: str = "",
                           amount: int = 0.002) -> 'reference_number':
    """Method sendPayment sends cryptons transfer for the specified amount to the contact or to the card.
    The method is called by using the To parameters (nick, pk, cardid), which pass on the Public Key,
    Nickname or the card number of the user to whom the transfer would be sent (Public Key can be recognized
    by using the getContacts method); Amount, which transfers the amount of transfer (the number needs to be
    greater than 0 and contain no more than 9 character after coma); Comment is optional, which contains
    the text of the comment (up to 148 characters); as well as the optional 'From card' field can be specified,
    that passes on the card number from which the cryptons will be taken from. If the parameter is empty,
    then cryptons would be deducted from the main account. In the Response field the status of completion
    of the operation is displayed."""

    # Action
    comment = "payment from pk to card"

    status, result = u.sendPayment(recipient, comment, _card, amount)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_sendPaymentFromCard(recipient: str = CONTACT_PK,
                             _card: str = SELF_CARD,
                             amount: int = 0.003) -> 'reference_number':
    """Method sendPayment sends cryptons transfer for the specified amount to the contact or to the card.
    The method is called by using the To parameters (nick, pk, cardid), which pass on the Public Key,
    Nickname or the card number of the user to whom the transfer would be sent (Public Key can be recognized
    by using the getContacts method); Amount, which transfers the amount of transfer (the number needs to be
    greater than 0 and contain no more than 9 character after coma); Comment is optional, which contains
    the text of the comment (up to 148 characters); as well as the optional 'From card' field can be specified,
    that passes on the card number from which the cryptons will be taken from. If the parameter is empty,
    then cryptons would be deducted from the main account. In the Response field the status of completion
    of the operation is displayed."""

    # Action
    comment = "payment from card to pk"

    status, result = u.sendPayment(recipient, comment, _card, amount)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_sendPaymentMoreThenBalanceFailed(recipient: str = CONTACT_PK,
                                          _card: str = "") -> 'reference_number':
    """Негативный тест который проверяет возможность совершить транзакцию превышающйю баланс"""

    # Action
    comment = "payment more then balance"
    _, balance = u.getBalance()
    status, result = u.sendPayment(recipient, comment, _card, int(balance) + 100)
    AssertErrorInResult(status, result)


def test_createVoucher(amount: int = 10) -> 'reference_number':
    """Method createVoucher with the mandatory parameter 'amount' creates new voucher for the selected amount
    in the list of own vouchers. The amount for the vouchers is taken from the main account balance.
    Amount, which transfers the amount of transfer (the number needs to be greater than 0 and contain
    no more than 9 character after coma);"""

    # Action
    status, result = u.createVoucher(amount)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_useVoucher() -> 'reference_number':
    """Method useVoucher allows to use the selected voucher with adding its amount to your main account.
    The method is called with mandatory 'VoucherId' parameter in which the number of the voucher is specified."""

    # SetUp
    _, vouchers = u.getVouchers()
    if len(vouchers) == 0 or 'Error' in vouchers:
        u.createVoucher(10)
        time.sleep(3)
        _, vouchers = u.getVouchers()

    # Action
    status, result = u.useVoucher(vouchers[0]['voucherid'])

    # Assertion
    AssertResultIsRefNum(status, result)


def test_deleteVoucher(amount: int = 10) -> 'reference_number':
    """Method deleteVoucher allows to remove your own voucher from the existing list with having the amount
    refunded back to your account. The method is called with mandatory 'VoucherId' parameter in which
    the number of the voucher is specified. In the Response field the status of completion of the
    operation is displayed."""

    # SetUp
    _, result = u.getVouchers()
    if len(result) == 0:
        u.createVoucher(amount)
        time.sleep(3)
        _, result = u.getVouchers()

    # Action
    status, result = u.deleteVoucher(result[0]["voucherid"])

    # Assertion
    AssertResultIsRefNum(status, result)


def test_sendInvoice(recipient: str = CONTACT_CARD, amount: int = 10) -> 'reference_number':
    """Method sendInvoice sends invoice (Request Cryptons) for deduction of specified amount from specified card.
    In the parameters of the method, the card number of the request recipient is specified (CardId).
    In the second parameter the 'Amount' is specified which transfers the amount of transfer (the number needs
    to be greater than 0 and contain no more than 9 character after coma), and the third parameter is optional,
    where 'Comment is optional, which contains the text of the comment (up to 148 characters)."""

    # Action
    status, result = u.sendInvoice("sendInvoice to contact card", recipient, amount)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_getInvoiceByReferenceNumber() -> json:
    """Method getInvoiceByReferenceNumber allows to receive 'batchid' of the invoice using the ReferenceNumber.
    In the Response field, batchid is returned, which is considered a successful status for completion
    of the operation."""

    # Action
    _, invoices = u.getFinanceHistory(filters='ALL_REQUESTS', referenceNumber='', fromDate='', toDate='',
                                      batchId='', fromAmount='', toAmount='')
    if len(invoices) > 0 and 'Error' not in invoices:
        status, result = u.getInvoiceByReferenceNumber(invoices[0]['referenceNumber'])
    else:
        raise Exception("There is no invoices or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getTransactionIdByReferenceNumber() -> json:
    """Method getTransactionIdByReferenceNumber allows to receive 'batchid' of the transaction by using
    the ReferenceNumber. In the Response field, batchid is returned, which is considered a successful status
    for completion of the operation."""

    # Action
    _, transactions = u.getFinanceHistory(filters='ALL_REQUESTS', referenceNumber='', fromDate='', toDate='',
                                          batchId='', fromAmount='', toAmount='')
    if len(transactions) > 0 and 'Error' not in transactions:
        status, result = u.getTransactionIdByReferenceNumber(transactions[0]['referenceNumber'])
    else:
        raise Exception("There is no transactions or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_acceptInvoice() -> 'reference_number':
    """Method acceptInvoice performs payment of the incoming invoice. The method is called with mandatory
    'InvoiceId' parameter in which the ID of the invoice that needs to be rejected. For receiving ID of the
    needed invoice it is needed to call getInvoices for receiving the list of invoices with their detailed
    information. In response the acceptInvoice method returns in the Response block the results of completing
    this request."""

    # Setup
    status = False
    result = ""

    # Action
    _, invoices = u.getInvoices(getInvoicesParams)
    incoming_invoices = [invoice for invoice in invoices if invoice['direction'] == 'Incoming'
                         and invoice['status'] == 'Awaiting']
    if len(incoming_invoices) > 0 and 'Error' not in incoming_invoices:
        status, result = u.acceptInvoice(incoming_invoices[0]['invoiceid'])
    else:
        raise Exception("There is no incoming invoices or got Error on request")

    # Assertion
    AssertResultIsRefNum(status, result)


def test_cancelInvoice() -> 'reference_number':
    """Method cancelInvoice allows to cancel the already created invoice. The method is called with mandatory
    'InvoiceId' parameter. Parameter InvoiceId contains the ID value for the invoice that needs to be declined.
    To get the ID of the required invoice it is mandatory to call the getInvoices method for receiving the
    list of invoices with their detailed information. In response the declineInvoice method returns in the
    Response block the results of completing this request."""

    invoiceid = ''

    # Action
    _, awaiting_requests = u.getFinanceHistory("AWAITING_REQUESTS", "", "", "", "", "", "")

    if len(awaiting_requests) < 5:
        _, invoice_ref_num = u.sendInvoice("API request", CONTACT_CARD, 10)
        time.sleep(4)  # wait for network confirmation
        _, invoice = u.getInvoiceByReferenceNumber(invoice_ref_num)
        invoiceid = invoice['invoiceid']
    else:
        invoiceid = awaiting_requests[0]['id']

    status, result = u.cancelInvoice(invoiceid)
    time.sleep(3)  # wait for network confirmation

    # Assertion
    AssertResultIsRefNum(status, result)


def test_declineInvoice() -> 'reference_number':
    """Method declineInvoice sends request for declining the payment for the incoming invoice. The method is
    called with mandatory the 'InvoiceId' parameter. Parameter InvoiceId contains the ID value for the invoice
    that needs to be declined. To get the ID of the required invoice it is mandatory to call the getInvoices
     method for receiving the list of invoices with their detailed information. In response the declineInvoice
     method returns in the Response block the results of completing this request."""

    # Setup
    status = ""
    result = ""

    # Action
    _, invoices = u.getInvoices(getInvoicesParams)
    incoming_invoices = [invoice for invoice in invoices if invoice['direction'] == 'Incoming'
                         and invoice['status'] == 'Awaiting']
    if len(incoming_invoices) > 0 and 'Error' not in incoming_invoices:
        status, result = u.declineInvoice(incoming_invoices[0]['invoiceid'])
    else:
        raise Exception("There is no incoming invoices or got Error on request")

    # Assertion
    AssertResultIsRefNum(status, result)


@pytest.fixture(params=[0, 1, 2, 3, 4, 5, 6],
                ids=["All", "Recent", "My", "Friends", "Bookmarked", "Joined", "Opened"])
def channel_type(request):
    return request.param


def test_getChannels(channel_type) -> json:
    """Тест принимает на вход 7 параметров типов каналов и проверяет что для каждого параметра возвращается
    список каналов"""

    # Setup
    filters = ''
    channel_type = channel_type

    # Action
    status, result = u.getChannels(filters, channel_type)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendChannelMessage(channel_id: str = CHANNEL_ID,
                            message: str = "Python api test") -> json:
    """Method sendChannelMessage creates and sends message in the selected channel (to send the message the user
    should have joined this channel and needs to have status 'online'). To enter the channel, use joinChannel
    method. As a parameter the method is using the ChannelId, which passes on the id of the channel in which the
    message is being sent (finding the id of the channel is possible by using the getChannels method) and Message,
    which contains the text of the message being sent. In the Response field the status of completion of
    the operation is displayed."""

    # Action
    status, result = u.sendChannelMessage(channel_id, message)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_leaveChannel(channel_id: str = "C160AB99F292C98746C3EA6ABB6AC7CD", passwd: str = "utopia9") -> bool:
    """Method leaveChannel executes the exit from the selected channel. As a parameter the method takes the
    ChannelId, which passes on the id of the channel in which the message is being sent (finding the id of the
    channel is possible by using the getChannels method ."""

    # Action
    status, result = u.leaveChannel(channel_id)
    u.joinChannel(channel_id, passwd)

    # Assert
    AssertResultIsTrue(status, result)


def test_joinChannel(channel_id: str = "C160AB99F292C98746C3EA6ABB6AC7CD",
                     channel_password: str = "utopia9") -> bool:
    """Method joinChannel executes an entry into selected channel. The following parameters are specified:
    ChannelId, which passes on the id of the channel in which the message is being sent (finding the id of the
    channel is possible by using the getChannels method); when needed the parameter Password is specified,
    which passes on the password for entry into the channel (if left empty, no password is required).
    In the Response field the status of completion of the operation is displayed."""

    # Action
    status, result = u.joinChannel(channel_id, channel_password)

    # Assert
    AssertResultIsTrue(status, result)


def test_deleteContact(pk: str = CONTACT_PK) -> bool:
    """Method deleteContact allows to perform the operation of removing selected user from the list of contacts.
    The method is called with mandatory use of 'Public Key' parameter that represents Public key of the to be
    removed contact. In the Response field the status of completion of such operation is displayed."""

    # Action
    status, result = u.deleteContact(pk)

    # Cleanup steps (return contact to contact list)
    u.sendAuthorizationRequest(pk, 'autotest request')
    u.acceptAuthorizationRequest(pk, 'autotest accept request')

    # Assert
    AssertResultIsTrue(status, result)


def test_sendAuthorizationRequest(pk: str = CONTACT_PK, message: str = 'autotest request') -> bool:
    """Method sendAuthorizationRequest allows to send the authorization request to add the user to the contact
    list. The method is called with mandatory use of 'Public Key' and 'Message' parameters. The Public Key
    parameter represents the Public Key of the person being added. The message parameter represents it
    the text message with the request to be authorized. In the Response field the status of completion of
    sending such request is displayed."""

    # Action
    status, result = u.sendAuthorizationRequest(pk, message)

    # Assert
    AssertResultIsTrue(status, result)


def test_rejectAuthorizationRequest(pk: str = CONTACT_PK, message: str = 'autotest reject request') -> bool:
    """Method rejectAuthorizationRequest declines the incoming authorization request from user with Public key,
    which is specified as first parameter (Public Key) of the rejectAuthorizationRequest method. The second
    parameter of the method is Message row, that represents it the response message the user who`s
    authorization is rejected. In the Response field the status of completion of such request is displayed."""

    # Action
    status, result = u.rejectAuthorizationRequest(pk, message)
    u.sendAuthorizationRequest(pk, "autotest request")
    u.acceptAuthorizationRequest(pk, "autotest accept request")

    # Assert
    AssertResultIsTrue(status, result)


def test_acceptAuthorizationRequest(pk: str = CONTACT_PK, message: str = 'autotest accept request') -> bool:
    """Method acceptAuthorizationRequest accepts the incoming authorization request to add user to contacts.
    The method is called with mandatory use of 'Public Key' and 'Message' parameters. The Public Key parameter
    represents the Public Key of the person who send the authorization request. The message parameter represents
    it the text message. In the Response field the status of completion of sending such request is displayed."""

    # Action
    status, result = u.acceptAuthorizationRequest(pk, message)

    # Assert
    AssertResultIsTrue(status, result)


def test_getUnsSyncInfo() -> json:
    """Method getUnsSyncInfo returns statistics value of sync process."""

    # Action
    status, result = u.getUnsSyncInfo()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_unsCreateRecordRequest(nick: str = random_uns, validTo: str = "2100-07-20",
                                is_primary: str = "false", channel_id: str = '') -> 'reference_number':
    """unsCreateRecordRequest method sends a request to register a uNS name in the Utopia ecosystem for specific
    time period. In addition to uNS name which is used as a parameter (the name contains characters (A-Z),
    numbers (0-9), a dash (-) character, a period (.) and can be up to 32 characters long.), other parameters
    include: expiration date (yyyy -mm-dd ) which is a final valid date of the uNS (6 months by default),
    isPrimary, indicating whether the uNS name is primary, ChannelId, which passes the channel identifier
    uNS will be associated with (channel identifier can be found out using the getChannels method).
    The Response field displays the status of the completed operation."""

    # Action
    status, result = u.unsCreateRecordRequest(nick, validTo, is_primary, channel_id)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_unsDeleteRecordRequest() -> 'reference_number':
    """Method unsDeleteRecordRequest sends request for deletion of uNS name of the current user. As a parameter
    the uNS name is used ( uNS name can be found by using the unsRegisteredNames method). In the Response field
    the status of completion of the operation is displayed."""

    _, unss = u.unsRegisteredNames()
    if len(unss) > 0 and 'Error' not in unss:
        status, result = u.unsDeleteRecordRequest(unss[-1]["nick"])

        # Assertion
        AssertResultIsRefNum(status, result)
    else:
        raise Exception("There is no UNS, or got Error on request")


def test_unsSearchByPk(pk: str = CONTACT_PK) -> json:
    """Method unsSearchByPk returns in the Response field the list of all uNS names with selected 'Filter'
    parameter (contains full or partial matching with the searched uNS name. The name can contain symbols (A-Z),
    numbers (0-9), dash symbol (-) and period (.) and can be no greater than 32 symbols in length.)."""

    # Action
    status, result = u.unsSearchByPk(pk)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_unsSearchByNick(nick: str = CONTACT_NAME) -> json:
    """Method unsSearchByNick returns the list of uNS names by partial or full matching with selected 'Filter'
    parameter (contains full or partial matching with the searched uNS name. The name can contain symbols (A-Z),
    numbers (0-9), dash symbol (-) and period (.) and can be no greater than 32 symbols in length.)."""

    # Action
    status, result = u.unsSearchByNick(nick)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_unsRegisteredNames() -> json:
    """Method unsRegisteredNames returns in the Response field the list of all registered uNS for current user.
    The method is called without using any parameters."""

    # Action
    status, result = u.unsRegisteredNames()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_unsModifyRecordRequest() -> 'reference_number':
    """unsModifyRecordRequest method sends a request to modify the uNS name in the Utopia ecosystem for specific
    time period. In addition to uNS name which is used as a parameter (the name contains characters (A-Z), numbers
    (0-9), a dash (-) character, a period (.) and can be up to 32 characters long.), other parameters include:
    expiration date (yyyy -mm-dd ) which is a final valid date of the uNS (6 months by default), isPrimary,
    indicating whether the uNS name is primary, ChannelId, which passes the channel identifier uNS will be
    associated with (channel identifier can be found out using the getChannels method). The Response field displays
    the status of the completed operation."""

    # Actions
    _, unss = u.unsRegisteredNames()
    if len(unss) > 0 and 'Error' not in unss:
        status, result = u.unsModifyRecordRequest(unss[-1]['nick'], "2100-07-20", False, "")

        # Assertion
        AssertResultIsRefNum(status, result)
    else:
        raise Exception("There is no UNS, or got Error on request")


def test_setContactGroup(pk: str = CONTACT_PK, group_name: str = "PyAPI") -> bool:
    """Method setContactGroup creates group or transfers selected contact into the group in the contact list.
    The method is called by using the Public Key parameters, which pass the Public Key of the contact (Public Key
    can be recognized by using the getContacts method) and Group Name, which passes the group name for creation
    or transfer (up to 32 symbols). In the Response field the status of completion of the operation is displayed."""

    # Action
    status, result = u.setContactGroup(pk, group_name)

    # Assert
    AssertResultIsTrue(status, result)


def test_setContactNick(pk: str = CONTACT_PK, new_name: str = CONTACT_NAME) -> bool:
    """Method setContactNick sets the selected value for the Nickname field for the selected contact. The method
    is called by using the Public Key parameters, which pass on the Public Key for the contact (Public Key can be
    recognized by using the getContacts method) and New Nick, which passes on the new Nickname (up to 32 symbols).
    Empty value to be set as the Nickname Public Key of the contact. In the Response field the status of completion
     of the operation is displayed."""

    # Action
    status, result = u.setContactNick(pk, new_name)

    # Assert
    AssertResultIsTrue(status, result)


def test_getEmailFolder(folder_type: int = 1, fltr: str = "") -> json:
    """Method getEmailFolder returns to the Response block the list of identifications of uMail emails in the
    selected folder by using specified search filter. The method is called by using the FolderType parameters,
    which pass on the number of the folder from which the list should be taken (numbers of the folders 1-Inbox,
    2-Drafts, 4-Sent, 8-Outbox, 16-Trash) and it is possible to specify the Filter parameter, which passes on the
    text value for the search of emails in uMail (has to contain the full or partial match with the Public Key,
    Nickname or the text of email)."""

    # Action
    status, result = u.getEmailFolder(folder_type, fltr)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getEmailById() -> json:
    """Method getEmailById returns the information based on the selected email in uMail. The method is called by
    using the Id parameter, which passes on the id of the email (id of the email can be found by using
    getEmailFolder method)."""

    # Action
    _, emails = u.getEmailFolder(1, "")
    if len(emails) > 0 and 'Error' not in emails:
        status, result = u.getEmailById(emails[0])
    else:
        raise Exception("There is no emails, or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_deleteEmail() -> json:
    """Method deleteEmail deletes email in uMail. First deletion will move email to the Trash, subsequent will
    remove from the database. The method is called by using the Id parameter which passes on the id of the email
    (id of the email can be found by using getEmailFolder method). In the Response field the status of completion
    of the operation is displayed."""

    # Action
    _, emails = u.getEmailFolder(1, "")  # 1 - Inbox folder
    if len(emails) > 0 and 'Error' not in emails:
        status, result = u.deleteEmail(emails[-1])
    else:
        raise Exception("There is no emails, or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_clearTrayNotifications() -> bool:
    """Method clearTrayNotifications allows to drop all existing notifications in the tray of the operating system.
     The method is called without using any parameters. In the Response field the status of completion of the
     operation is displayed."""

    # Action
    status, result = u.clearTrayNotifications()

    # Assert
    AssertResultIsTrue(status, result)


def test_getContactMessages(pk: str = CONTACT_PK) -> json:
    """Method getContactMessages returns in the Response block the history of communication from personal chat
    with selected contact. The method is called by using the Public Key parameter, that passes on the Public Key
    of the contact (Public Key can be recognized by using the getContacts method)"""

    # Action
    status, result = u.getContactMessages(pk)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendReplyEmailMessage() -> json:
    """Method sendReplyEmailMessage creates response email in uMail for the incoming email and sends it to the
    contact with new message. The method is called by using the Id parameters, which pass on the id of the email
    (id of the email can be found by using getEmailFolder method) and Body, which passes on the text of the email
    in uMail. In the Response field the status of completion of the operation is displayed."""
    # SetUp
    subject = 'This is a Reply email by Python API test'
    body = 'This is a python api test'
    attachId = ''
    status = False
    result = ''

    # Action
    _, emails = u.getEmailFolder(1, "")
    if len(emails) > 0 and 'Error' not in emails:
        status, result = u.sendReplyEmailMessage(emails[-1], body, subject, attachId)
    else:
        raise Exception("There is no emails, or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendForwardEmailMessage() -> json:
    """Method sendForwardEmailMessage creates response email for an incoming email in uMail and sends it to the
    selected contact with the new message. The method is called by using the 'Id' parameter, which passes on the
    id of the email (id of the email can be found by using getEmailFolder method); 'To', which passes on the
    Public Key or Nickname of the user to which the email will be sent; and 'Body', which passes on the text in
    uMail. In the Response field the status of completion of the operation is displayed."""

    # SetUp
    recipient = CONTACT_PK
    body = 'This is a Forward email by Python API test'
    subject = 'This is a Python api test'
    attachId = ""
    status = False
    result = ''

    # Action
    _, emails = u.getEmailFolder(1, "")
    if len(emails) > 0 and 'Error' not in emails:
        status, result = u.sendForwardEmailMessage(emails[-1], recipient, body, subject, attachId)
    else:
        raise Exception("There is no emails, or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getFinanceHistory(filters: str = "ALL_TRANSACTIONS",
                           referenceNumber: str = "",
                           fromDate: str = "",
                           toDate: str = "",
                           batchId: str = "",
                           fromAmount: int = None,
                           toAmount: int = None) -> json:
    """Method getFinanceHistory allows to receive the history of financial transactions based on the
    specifications in the parameters of the filter."""

    # Action
    status, result = u.getFinanceHistory(filters, referenceNumber, fromDate, toDate,
                                         batchId, fromAmount, toAmount)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_requestUnsTransfer(pk: str = CONTACT_PK) -> 'reference_number':
    """Проверка что метод requestUnsTransfer при успешном вызове возвращает reference number"""

    # Setup
    status = False
    result = ''

    # Action
    # Получаем список всех uns, исходящих uns и uns на которые настроен мапинг
    _, unss = u.unsRegisteredNames()
    _, outgoing_unss = u.outgoingUnsTransfer()
    _, uns_in_maps = u.getProxyMappings()

    # Если в списке всех uns есть те которые уже в списке исходящих, то удаляем их из списка
    for out_uns in outgoing_unss:
        uns = [uns for uns in unss if uns['nick'] == out_uns['nick'].lower()]
        if len(uns) > 0:
            unss.remove(uns[0])

    # Если в списке всех uns есть те на которые настроен мапинг, то удаляем их из списка
    for m in uns_in_maps:
        uns = [uns for uns in unss if uns['nick'] == m['incomingAddress'].lower()]
        if len(uns) > 0:
            unss.remove(uns[0])

    if len(unss) > 0 and 'Error' not in unss:
        status, result = u.requestUnsTransfer(unss[-1]['nick'], pk)
    else:
        u.unsCreateRecordRequest(nick=random_uns, valid='', isPrimary='false', channelId='')
        time.sleep(3)  # wait for network confirmation
        _, unss = u.unsRegisteredNames()
        status, result = u.requestUnsTransfer(unss[-1]['nick'], pk)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_try_to_transfer_outgoing_uns(pk: str = '31033EA6DD56AF6BD07B6DB4721A00BE9756084F2E76C17281FDDC57D73C0B09'):
    """Проверяем что невозможно повторно отправить uns которая уже в статусе отправки"""
    status = True
    result = ''

    _, outgoing_unss = u.outgoingUnsTransfer()

    if len(outgoing_unss) > 0:
        status, result = u.requestUnsTransfer(outgoing_unss[0]['nick'], pk)
        AssertErrorInResult(status, result)
    else:
        raise ValueError("No outgoing UNS")


def test_incomingUnsTransfer() -> json:
    """Method incomingUnsTransfer returns in the Response field the list of all incoming uNS transfer records with
    their detailed information. The method is called without using any parameters."""

    # Action
    status, result = u.incomingUnsTransfer()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_acceptUnsTransfer() -> 'reference_number':
    """Method acceptUnsTransfer allows to accept the incoming record of the uNS transfer. The method is called
    with the mandatory 'RequestId' parameter, which represents the id of the incoming uNS transfer. To receive the
    id of incoming transfers it is necessary to call the incomingUnsTransfer method, which returns the list of
    incoming uNS transfer. In the Response field the status of completion of the acceptUnsTransfer operation
    is displayed."""

    # Setup
    status = False
    result = ''

    # Action
    _, incoming_unses = u.incomingUnsTransfer()
    if len(incoming_unses) > 0 and 'Error' not in incoming_unses:
        status, result = u.acceptUnsTransfer(incoming_unses[0]['id'])
    else:
        raise Exception("There is no incoming UNS transfers")

    # Assertion
    AssertResultIsRefNum(status, result)


def test_declineUnsTransfer() -> 'reference_number':
    """Method declineUnsTransfer allows to decline the incoming record of the uNS transfer. The method is called
    with the mandatory 'RequestId' parameter, which represents the id of the incoming uNS transfer. To receive the
    id of incoming transfers it is necessary to call the incomingUnsTransfer method, which returns the list of
    incoming uNS transfer. In the Response field the status of completion of the declineUnsTransfer operation
    is displayed."""

    # Setup
    status = False
    result = ''

    # Action
    _, incoming_unses = u.incomingUnsTransfer()
    if len(incoming_unses) > 0 and 'Error' not in incoming_unses:
        status, result = u.declineUnsTransfer(incoming_unses[0]['id'])
    else:
        raise Exception("There is no incoming UNS transfers")

    # Assertion
    AssertResultIsRefNum(status, result)


def test_outgoingUnsTransfer() -> json:
    """Method outgoingUnsTransfer returns in the Response field the list of all outgoing uNS transfer records with
    their detailed information. The method is called without using any parameters."""

    # Action
    status, result = u.outgoingUnsTransfer()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getNetworkConnections() -> json:
    """Method getNetworkConnections returns in Response block detailed information about all current network
    connections. The method is called without using any parameters."""

    # Action
    status, result = u.getNetworkConnections()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getProxyMappings() -> json:
    """Method getProxyMappings returns in Response block the list of all configured proxy mappings. The method
    is called without using any parameters."""

    # Action
    status, result = u.getProxyMappings()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_createProxyMapping(
        srcHost: str = "uns",
        srcPort: str = "80",
        dstHost: str = "81.19.72.36",
        dstPort: str = "80",
        enabled: str = "true") -> json:
    """Тестирование метода createProxyMapping на возможность добавления мапинга"""

    # Setup
    status = False
    result = ''

    # Action
    # Получаем список своих Uns записей и список настроенных мапингов
    _, unss = u.unsRegisteredNames()
    _, maps = u.getProxyMappings()

    if len(unss) > 0 and 'Error' not in unss:
        # Проходимся по всем мапингам и проверяем есть ли в списке моих uns
        # мапинг с таким же ником, то удаляем его из списка unss
        for m in maps:
            uu = [uns for uns in unss if uns['nick'] == m['incomingAddress'].lower()]
            if len(uu) != 0:
                unss.remove(uu[0])
        # Из списка оставшихся uns берём первый и создаём на него новый мапинг
        srcHost = unss[0]["nick"]
        status, result = u.createProxyMapping(srcHost, srcPort, dstHost, dstPort, enabled)

        # Clear step
        u.removeProxyMapping(result)
    else:
        raise Exception("There is no UNS records, or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_enableProxyMapping() -> json:
    """Method enableProxyMapping allows to turn on the ability to use the connection with specified 'MappingId' as
    a parameter when calling this method. To receive the 'MappingId' of the needed connection it is necessary to
    call the getProxyMappings method. In the Response field the status of completion of operation of turning on
    the connection is displayed."""

    # Setup
    status = False
    result = ''

    # Action
    _, proxy_mappings = u.getProxyMappings()
    if len(proxy_mappings) > 0 and 'Error' not in proxy_mappings:
        status, result = u.enableProxyMapping(proxy_mappings[0]['id'])
    else:
        raise Exception("There is no mappings or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_disableProxyMapping() -> json:
    """Method disableProxyMapping allows to turn off the ability to use the connection with specified 'MappingId'
    as a parameter when calling this method. To receive the 'MappingId' of the needed connection it is necessary
    to call the getProxyMappings method. In the Response field the status of completion of operation of turning
    off the connection is displayed."""

    # Setup
    status = False
    result = ''

    # Action
    _, proxy_mappings = u.getProxyMappings()
    if len(proxy_mappings) > 0 and 'Error' not in proxy_mappings:
        status, result = u.disableProxyMapping(proxy_mappings[0]['id'])
    else:
        raise Exception("There is no mappings or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_removeProxyMapping() -> json:
    """Method removeProxyMapping allows to remove the selected configured of proxy mappings. The method is called
    by using the MappingId parameter, which represents the id of the configured proxy connection. In the Response
    field the status of completion of operation of removing the mapping is displayed."""

    # Setup
    status = False
    result = ''

    # Action
    _, proxy_mappings = u.getProxyMappings()
    if len(proxy_mappings) > 0 and 'Error' not in proxy_mappings:
        status, result = u.removeProxyMapping(proxy_mappings[0]['id'])
    else:
        raise Exception("There is no mappings or got Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_addCard(color: str = "#FBEDC0",
                 card_name: str = "API card",
                 preferred_number: str = "") -> 'reference_number':
    """Method addCard sends the request for creation of new card in uWallet. The method is called by using the
    following parameters: Name, which passes on the name of the new card (can contain between 1 and 32 symbols),
    Color, which passes on the color of the card ( in RGB format, for example '#FFFFFF') and also can specify the
    First 4 numbers of the card for customization ( it is possible to change only 4 first symbols, can contain
    symbols (A-F) and numbers (0-9)). In the Response field the status of completion of the operation
    is displayed."""

    # Action
    status, result = u.addCard(color, card_name, preferred_number)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_deleteCard() -> 'reference_number':
    """Method deleteCard deletes the existing card from uWallet. The amount from card will be returned to the main
    balance. The following parameter is specified: CardId, which passes on the card number ( CardId can be found
    by using the getCards method). In the Response field the status of completion of the operation is displayed."""

    # Action
    _, cards = u.getCards()
    status = False
    result = ""

    if len(cards) > 0 and 'Error' not in cards:
        card = [card for card in cards if card['name'] == 'API card' or card['name'] == 'DefaultCardName']
        if len(card) == 0:
            _, new_card_refNum = u.addCard("#FBEDC0", "API card", "")
            _, transaction = u.getFinanceHistory("", new_card_refNum, "", "", "", "", "")
            if transaction[0]['state'] != 0:
                raise Exception("New card is not created")
            _, cards = u.getCards()
            card = [card for card in cards if card['name'] == 'API card' or card['name'] == 'DefaultCardName']
        if len(card) > 0:
            status, result = u.deleteCard(card[0]['cardid'])
            timer = 10
            while result == '' and timer != 0:
                time.sleep(1)
                timer -= 1
                print(timer)
        else:
            raise Exception("Cant choose card for deleting")

        # Assertion
        AssertResultIsRefNum(status, result)


def test_getFinanceSystemInformation() -> json:
    """Method getFinanceSystemInformation returns in the Response field the information about Utopia financial
    system (information about fees and limits). Method is called without using any parameters."""

    # Action
    status, result = u.getFinanceSystemInformation()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getMiningBlocks() -> json:
    """Method getMiningBlocks returns to the Response field the information about the mining blocks for which the
    reward has been paid. The method is called without using any parameters."""

    # Action
    status, result = u.getMiningBlocks()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_enableMining(enabled: str = "true") -> bool:
    """Method enableMining turns on the mining in the Utopia client (mining is available only for x64 client). As
    a parameter the Status (true/false) is specified, which turns on or off the mining process. In the Response
    field the status of completion of the operation is displayed."""

    # Action
    status, result = u.enableMining(enabled)

    # Assertion
    AssertResultIsTrue(status, result)


def test_enablePoS(enabled: str = "true") -> bool:
    """Calling the enablePoS method turns on and off the PoS on the remaining irreducible account balance. As a
    parameter, one of the two statuses, true or false is selected. In the Response field the status of completion
    of turning on or off the operation is displayed."""

    # Prepare step
    _, res = u.enablePoS('false')  # Switch off pos
    if res != "":
        time.sleep(5)  # wait for network response

    # Action
    status, result = u.enablePoS(enabled)

    # Assertion
    AssertResultIsRefNum(status, result)


def test_enableHistoryMining(enabled: str = "true") -> bool:
    """Calling the enableHistoryMining method changes the option of the automatic reading of the mining history from
     the financial server. As a parameter of the method, the status of true or false is specified. In the Response
    field the status of completion of turning on or off the operation is displayed."""

    # Action
    status, result = u.enableHistoryMining(enabled)

    # Assertion
    AssertResultIsTrue(status, result)


def test_statusHistoryMining() -> json:
    """Calling the statusHistoryMining method returns in the Response block the status of mining history poll.
    Method is called without using any parameters.
    Meaning of different states:
    0 = STATE_EMPTY
    1 = STATE_IN_PROGRESS
    2 = STATE_RECEIVED_RESPONSE"""

    # Action
    status, result = u.statusHistoryMining()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_lowTrafficMode() -> json:
    """Method lowTrafficMode returns in Response block the status of low Traffic mode. The method is called
    without using any parameters."""

    # Action
    status, result = u.lowTrafficMode()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_setLowTrafficMode(enabled: str = "false") -> json:
    """Method setLowTrafficMode allows to turn on or off the low Traffic mode. The method is called by using the
    enabled parameter, which represents it a status of true or false that is being set
    for this particular mode."""

    # Action
    status, result = u.setLowTrafficMode(enabled)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getWhoIsInfo(pk: str = CONTACT_PK) -> json:
    """Method getWhoIsInfo returns in Response block the detailed information about selected user. As a parameter
    of the method, the Public key of the particular user can be used, or his nickname, if such contact was added
    to the contact list."""

    # Action
    status, result = u.getWhoIsInfo(pk)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getChannelInfo(channel_id: str = CHANNEL_ID) -> json:
    """Method getChannelInfo returns in the Response field the information about the channel ( the response
    contains following parameters: HideInCommonList, description, geotag, hashtags, languages, readonly, title,
    type, private). As a parameter the method is using the ChannelId for which the user is trying to find more
    information (finding the id of the channel is possible by using the getChannels method)."""

    # Action
    status, result = u.getChannelInfo(channel_id)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getChannelModerators(channel_id: str = CHANNEL_ID) -> json:
    """Method getChannelModerators returns in the Response field the list of Public Keys of moderators. As a
    parameter the ChannelId is used (finding the id of the channel is possible by using the getChannels method)."""

    # Action
    status, result = u.getChannelModerators(channel_id)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getChannelModeratorRight(channel_id: str = CHANNEL_ID) -> json:
    """Method getChannelModeratorRight returns in the Response field the list of moderator rights in the channel
    ( the response contains parameters as ban, delete, promote). As a parameter the method uses: ChannelId from
    which it is needed to get the list of moderator rights (finding the id of the channel is possible by using the
    getChannels method) and Public Key of the channel moderator (finding Public Key(pk) of the channel moderator
    is possible by using the getChannelModerators method)."""

    # Setup
    status = False
    result = ''

    # Action
    _, moderators = u.getChannelModerators(channel_id)
    if len(moderators) > 0 and "Error" not in moderators:
        status, result = u.getChannelModeratorRight(channel_id, moderators[0])
    else:
        raise Exception("There is no moderators or Error on request")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_setProfileStatus(status: str = "Available", mood: str = "QA Engineer") -> json:
    """Method setProfileStatus sets the new status, as well as the mood message in the Utopia Ecosystem. The method
     is called by using Status parameter line with possible options: (Available, Away, DoNotDisturb, Invisible,
     Offline) and if desired Mood which contains mood message text (up to 130 symbols). In the Response field, the
     status of completed operation is displayed."""

    # Action
    status, result = u.setProfileStatus(status, mood)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getEmails(folder_type: int = 1, fltr: str = "") -> json:
    """Method getEmails returns to the Response block the list of detailed of uMail emails in the selected folder
    by using specified search filter. The method is called by using the FolderType parameters, which pass on the
    number of the folder from which the list should be taken (numbers of the folders 1-Inbox, 2-Drafts, 4-Sent,
    8-Outbox, 16-Trash) and it is possible to specify the Filter parameter, which passes on the text value for the
    search of emails in uMail (has to contain the full or partial match with the Public Key, Nickname or the text
    of email)"""

    # Action
    status, result = u.getEmails(folder_type, fltr)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getChannelMessages(channel_id: str = CHANNEL_ID) -> json:
    """Method getChannelMessages returns in the Response block the history of communication from selected channel.
    The method is called by using the channelid parameter, that passes on id of channel."""
    # Action
    # status, result = u.getChannelMessages("B4EF14CFE2782C1E94E82631F9B782E2")
    status, result = u.getChannelMessages(channel_id)

    # Assertion
    AssertNotEmptyOrError(status, result)


# @unittest.skip("просьба не трогать ушан")
def test_createChannel() -> json:
    """Testing of channel creation using correct data"""

    # Test data
    channel_name = "Test Channel |+_)(*&^%$#@!~"
    description = "description _)(*?:%;№"
    read_only = "false"
    read_only_privacy = ""
    password = ""
    languages = ""
    hash_tags = "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x"
    geo_tag = "10.000, 20.000"
    avatar = ""
    hide_in_ui = "false"
    status = False
    myChannel = ''

    # Action
    _, my_channels = u.getChannels(filter="", channel_type=2)
    if len(my_channels) < 10:
        status, myChannel = u.createChannel(channel_name, description, read_only, read_only_privacy, password,
                                            languages, hash_tags, geo_tag, avatar, hide_in_ui)
        time.sleep(3)  # wait for uchan database sync ends
        u.deleteChannel(myChannel, password)  # cleanup step

        # Assertion
        AssertNotEmptyOrError(status, myChannel)
    else:
        raise Exception("There are 10 channels. Cant create more")


def test_getOwnContact() -> json:
    """Method getOwnContact returns information about your"""

    # Action
    status, result = u.getOwnContact()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getChannelAvatar(channel_id: str = CHANNEL_ID, coder: str = "BASE64", format: str = "JPG") -> json:
    """Method getChannelAvatar returns to the Response field the avatar of the selected channel
    in the base64 or hex format."""

    # Action
    status, result = u.getChannelAvatar(channel_id, coder, format)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendInstantQuote(pk: str = CONTACT_PK) -> json:
    """Method sendInstantQuote sends quote personal message(IM) to the selected contact from the contact list
    on message by id_message"""

    # Action
    _, contact_msgs = u.getContactMessages(pk)
    if len(contact_msgs) == 0:
        u.sendInstantMessage(pk, "Send Instant Quote Test")
        _, contact_msgs = u.getContactMessages(pk)
    status, result = u.sendInstantQuote(pk, "this is python unittest quote message",
                                        contact_msgs[0]["id"])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getStickerCollections() -> json:
    """Method getStickerCollections returns collection names of stickers."""

    # Action
    status, result = u.getStickerCollections()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getStickerNamesByCollection() -> json:
    """Method getStickerNamesByCollection returns available names from corresponded collection."""

    # Action
    _, sticker_collection = u.getStickerCollections()
    status, result = u.getStickerNamesByCollection(sticker_collection[0])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getImageSticker() -> json:
    """Method getImageSticker returns image by sticker name from corresponded collection in coder that can be
    equal "BASE64"."""

    # Action
    _, sticker_collection = u.getStickerCollections()
    _, all_stickers = u.getStickerNamesByCollection(sticker_collection[0])
    status, result = u.getImageSticker(sticker_collection[0], all_stickers[0], "BASE64")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendInstantSticker(contact_pk: str = CONTACT_PK) -> json:
    """Method sendInstantSticker sends sticker personal message(IM) to the selected contact from the contact list
    a sticker from collection by name."""

    # Action
    _, sticker_collection = u.getStickerCollections()
    _, all_stickers = u.getStickerNamesByCollection(sticker_collection[0])
    status, result = u.sendInstantSticker(contact_pk, sticker_collection[0], all_stickers[0])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendInstantBuzz(contact_pk: str = CONTACT_PK) -> json:
    """Method sendInstantBuzz sends buzz personal message(IM) to the selected contact from the contact list with
    comments."""

    # Action
    status, result = u.sendInstantBuzz(contact_pk, "Python Buzz")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendInstantInvitation(pk: str = CONTACT_PK, channel_id: str = CHANNEL_ID) -> json:
    """Method sendInstantInvitation sends invitation personal message(IM) to the selected contact from the contact
    list with description and comments on channel_id."""

    # Action
    status, result = u.sendInstantInvitation(pk, channel_id,
                                             "Python invite description", "Python invite comment")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_removeInstantMessages(contact_pk: str = CONTACT_PK) -> json:
    """Method removeInstantMessages removes all personal messages(IM) of the selected contact from the contact
    list."""

    # Action
    status, result = u.removeInstantMessages(contact_pk)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getMiningInfo() -> json:
    """Method getMiningInfo returns statistics value of mining process."""

    # Action
    status, result = u.getMiningInfo()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendChannelPicture(channel_id: str = "81B8CA0B8E2A5C87C468927953BEB674",
                            pic: str = PICTURE) -> json:
    """Method sendChannelPicture creates and sends message with picture in base64 format"""

    # Action
    status, result = u.sendChannelPicture(channel_id, pic, "image.jpg")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_modifyChannel() -> 'reference_number':
    """Method modifyChannel changes uchan record properties."""

    # Test data
    channel_name = "Test Channel |+_)(*&^%$#@!~"
    description = "description _)(*?:%;№"
    read_only = "false"
    read_only_privacy = ""
    password = ""
    languages = ""
    hash_tags = "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x"
    geo_tag = "10.000, 20.000"
    avatar = ""
    hide_in_ui = "false"
    status = False
    result = ''

    # Action
    _, my_channels = u.getChannels(filter="", channel_type=2)
    myChannel = ""
    if len(my_channels) < 10:
        _, myChannel = u.createChannel(channel_name, description, read_only, read_only_privacy, password,
                                       languages, hash_tags, geo_tag, avatar, hide_in_ui)
        time.sleep(3)  # wait for uchan data base sync process ends
    else:
        myChannel = [channel["channelid"] for channel in my_channels if channel["name"] != "testing_dev"][0]
    if myChannel:
        status, result = u.modifyChannel(myChannel, "edited on:" + str(datetime.today()), read_only,
                                         read_only_privacy, password, languages, hash_tags, geo_tag,
                                         avatar, hide_in_ui)
    else:
        raise Exception("Cant choose channel for modify")
    u.deleteChannel(myChannel, password)  # cleanup step

    # Assertion
    AssertResultIsTrue(status, result)


@pytest.mark.skip("Have no channels for testing")
def test_deleteChannel() -> 'reference_number':
    """Method deleteChannel deletes uchan record."""

    # Test data
    channel_name = "Test Channel |+_)(*&^%$#@!~"
    description = "description _)(*?:%;№"
    read_only = "false"
    read_only_privacy = ""
    password = ""
    languages = ""
    hash_tags = "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x"
    geo_tag = "10.000, 20.000"
    avatar = ""
    hide_in_ui = "false"
    status = False
    result = ''

    # Action
    _, my_channels = u.getChannels(filter="", channel_type=2)
    myChannel = ""
    if len(my_channels) < 9:
        _, myChannel = u.createChannel(channel_name, description, read_only, read_only_privacy,
                                       password, languages, hash_tags, geo_tag, avatar, hide_in_ui)
    else:
        channels_for_del = [channel["channelid"] for channel in my_channels
                            if channel["name"] != "testing_dev" and channel["name"] != "hidden channel"]
        myChannel = channels_for_del[0]
    status, result = u.deleteChannel(myChannel, password)  # main action step

    # Assertion
    AssertResultIsTrue(status, result)


def test_getChannelSystemInfo() -> json:
    """Method getChannelSystemInfo returns system properties of channels."""

    # Action
    status, result = u.getChannelSystemInfo()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_summaryUnsRegisteredNames() -> json:
    """Method summaryUnsRegisteredNames returns the list count of uNS names by each day"""

    # Action
    status, result = u.summaryUnsRegisteredNames(fromDate="", toDate="")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_requestTreasuryPoSRates() -> json:
    """Method requestTreasuryPoSRates makes request to obtain treasury PoS rate data"""

    # Action
    status, result = u.requestTreasuryPoSRates()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getTreasuryPoSRates() -> json:
    """Method getTreasuryPoSRates returns in Response block the detailed information about treasury PoS rate"""

    # Action
    status, result = u.getTreasuryPoSRates()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_requestTreasuryTransactionVolumes() -> json:
    """Method requestTreasuryTransactionVolumes makes request to obtain treasury transaction volume data"""

    # Action
    status, result = u.requestTreasuryTransactionVolumes()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getTreasuryTransactionVolumes() -> json:
    """Method getTreasuryTransactionVolumes returns in Response block the detailed information about treasury
    transaction volume"""

    # Action
    status, result = u.getTreasuryTransactionVolumes()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_get_treasury_transaction_volumes_with_filter() -> json:
    """Тест проверяет применение фильтра к выводу полученных данных"""

    limit = 3

    # Action
    u.genericFilter('transactions,amount:1', '', limit)
    u.requestTreasuryTransactionVolumes()
    status, result = u.getTreasuryTransactionVolumes()
    amount_list = [transaction['amount'] for transaction in result['transactions']]
    amount_list_sorted = sorted(amount_list, reverse=True)
    u.genericFilterClear()

    # Assertion
    assert status
    assert amount_list == amount_list_sorted
    assert len(result['transactions']) == limit


def test_ucodeEncode(contact_pk: str = CONTACT_PK) -> json:
    """Method ucodeEncode returns image of ucode in size_image with public key from hex_code"""

    # Action
    status, result = u.ucodeEncode(contact_pk, size_image="200", coder="BASE64", format="JPG")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_ucodeDecode(image: str = UCODE) -> json:
    """Method ucodeDecode returns hex public key from image in base64 format."""

    # Action
    status, result = u.ucodeDecode(image)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getWebSocketState() -> json:
    """Method getWebSocketState returns WSS Notifications state, 0 - disabled or active listening port number."""

    # Action
    status, result = u.getWebSocketState()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_setWebSocketState() -> json:
    """Тест проверяет возможность установить статус и порт веб сокета"""
    status = ''
    result = ''

    # Action
    status, result = u.setWebSocketState(enabled=True, port='20001')

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getContactGroups() -> json:
    """Method setContactGroup creates group or transfers selected contact into the group in the contact list.
    The method is called by using the Public Key parameters, which pass the Public Key of the contact (Public Key
    can be recognized by using the getContacts method) and Group Name, which passes the group name for creation or
    transfer (up to 32 symbols). In the Response field the status of completion of the operation is displayed."""

    # Action
    status, result = u.getContactGroups()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getContactsByGroup() -> json:
    """Method getContactsByGroup returns to the Response field the list of contacts from group with corresponded
    name."""

    # Action
    _, groups = u.getContactGroups()
    status, result = u.getContactsByGroup(groups[0])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_deleteContactGroup() -> json:
    """Method deleteContactGroup delete corresponded group name, all contacts are moved under default group."""

    # Action
    _, groups = u.getContactGroups()
    group = list(filter(lambda g:
                        g != "DEV Group™" and
                        g != "██▓▓▒▒░░Вожди░░▒▒▓▓██" and
                        g != "<h1>Отдел тестирования</h1>11111" and
                        g != "MSK Teem" and
                        g != "beta.u.is" and
                        g != "Freedom Society" and
                        g != "", groups))
    # if DEBUG:
    print("test_deleteContactGroup, group name: " + str(group[0]))
    status, result = u.deleteContactGroup(group[0])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getTransfersFromManager() -> json:
    """Method getTransfersFromManager returns list of file transfer."""

    # Action
    status, result = u.getTransfersFromManager()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getFilesFromManager() -> json:
    """Тест проверяет что выполнение запроса getFilesFromManager возвращает список файлов в json формате и ответ
    не является пустым и не содержит сообщения об ошибке"""

    # Action
    status, result = u.getFilesFromManager()

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_abortTransfers() -> json:
    """Method abortTransfers abort transfer with selected ID."""

    # Action
    _, transfers = u.getTransfersFromManager()
    tr_id = ""
    try:
        active_transfers = [t["transferId"] for t in transfers if t["percentCompleted"] < 100]
        tr_id = active_transfers[0]
    except:
        tr_id = transfers[0]["transferId"]

    status, result = u.abortTransfers(tr_id)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_hideTransfers() -> json:
    """Method hideTransfers hide transfer with selected ID."""

    # Action
    _, transfers = u.getTransfersFromManager()
    tr_id = ""
    try:
        active_transfers = [t["transferId"] for t in transfers if t["percentCompleted"] < 100]
        tr_id = active_transfers[0]
    except:
        tr_id = transfers[0]["transferId"]

    status, result = u.hideTransfers(tr_id)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getFile() -> json:
    """Method getFile return file with selected ID."""

    # Action
    _, files = u.getFilesFromManager()
    status, result = u.getFile(files[0]["id"])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_deleteFile():
    # Action
    _, files = u.getFilesFromManager()
    status, result = u.deleteFile(files[0]["id"])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_sendFileByMessage(pk: str = CONTACT_PK) -> json:
    """Method sendFileByMessage send file with selected address."""

    # Action
    _, files = u.getFilesFromManager()
    status, result = u.sendFileByMessage(pk, files[0]["id"])

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_getChannelBannedContacts(channel_id: str = CHANNEL_ID) -> json:
    """Method getChannelBannedContacts returns list banned contacts on corresponded channel with id channelid."""

    # Action
    status, result = u.getChannelBannedContacts(channel_id)

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_applyChannelBannedContacts(channel_id: str = CHANNEL_ID, pk: str = CONTACT_PK) -> json:
    """
    Method applyChannelBannedContacts apply and send new banned list for corresponded channel with id channelid.
    """

    # Action
    u.applyChannelBannedContacts(channel_id, "[" + pk + "]")
    status, result = u.applyChannelBannedContacts(channel_id, "[]")  # clear ban list

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_uploadFile(pic: str = PICTURE) -> str:
    """Method uploadFile upload data in base64 format and returns id of new file."""

    # Action
    status, result = u.uploadFile(pic, "Дулин.png")

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_acceptAttachment() -> bool:
    """Тест проверяет возможность ододрить загружку вложенных во входящее письмо файлов.
    Сначала получаем список всех входящих писем, потом отбираем из них те, у которых есть attachments со статусом
    waiting. Потом берём id этого письма и id аттача и вызываем метод
    acceptAttachment чтобы загрузить вложение. Далее проверяем что пришло в ответ в result."""

    # Action
    _, all_incoming_umails = u.getEmails(1, "")

    ids = [{"mail_id": umail['id'], "attach_id": attach['id']}
           for umail in all_incoming_umails if 'attachments' in umail.keys()
           for attach in umail['attachments'] if 'waiting' in attach.values()]

    try:
        status, result = u.acceptAttachment(ids[0]["mail_id"], ids[0]["attach_id"])
        AssertResultIsTrue(status, result)
    except:
        raise Exception("There is no incoming emails with attachments")


def test_abortAttachment() -> bool:
    """Тест проверяет возможность отменить загружку вложенных во входящее письмо файлов.
    Сначала получаем список всех входящих писем, потом генератором отбираем из них те, у которых есть attachments
    со статусом waiting. Сохраняем id письма и id его аттача в статусе waiting в список словарей.
    Берём id этого письма и id аттача и вызываем метод abortAttachment чтобы отменить загрузку вложения.
    Далее проверяем что result не пустой, в нём нет сообщения об ошибке Error и он имеет значение True"""

    # Action
    _, all_incoming_umails = u.getEmails(1, "")

    ids = [{"mail_id": umail['id'], "attach_id": attach['id']}
           for umail in all_incoming_umails if 'attachments' in umail.keys()
           for attach in umail['attachments'] if 'waiting' in attach.values()]

    try:
        status, result = u.abortAttachment(ids[0]["mail_id"], ids[0]["attach_id"])
        AssertResultIsTrue(status, result)
    except:
        pprint(ids)
        raise Exception("There is no incoming emails with attachments in status waiting")


def test_pinInstantMessage() -> bool:
    """Тест проверяет возможность закрепить сообщение в чате с контактом"""

    # Action
    _, contact_messages = u.getContactMessages(CONTACT_PK)
    _, pinned_messages = u.getPinnedMessages(CONTACT_PK)

    for msg in contact_messages:
        if msg not in pinned_messages and msg['messageType'] != 6:
            status, result = u.pinInstantMessage(CONTACT_PK, msg['id'], 'true')
            AssertResultIsTrue(status, result)
            break


def test_UnPinInstantMessage() -> bool:
    """Тест проверяет возможность открепить сообщение в чате с контактом"""

    # Setup
    status = ''
    result = ''

    # Action
    _, contact_messages = u.getContactMessages(CONTACT_PK)
    _, pinned_messages = u.getPinnedMessages(CONTACT_PK)

    if len(pinned_messages) == 0:
        for msg in contact_messages:
            if msg not in pinned_messages and msg['messageType'] != 6:
                u.pinInstantMessage(CONTACT_PK, msg['id'], 'true')
                break

    _, pinned_messages = u.getPinnedMessages(CONTACT_PK)

    for msg in pinned_messages:
        status, result = u.pinInstantMessage(CONTACT_PK, msg['id'], 'false')
        AssertResultIsTrue(status, result)


def test_sendEmailInvitation() -> bool:
    """Тест проверят возможность отправки инвайта письмом"""

    # Action
    status, result = u.sendEmailInvitation(CHANNEL_ID, CONTACT_PK, 'This is description', 'This is comment')

    # Assertion
    AssertResultIsTrue(status, result)


def test_emptyEmailsTrash() -> bool:
    """Тест проверят возможность очистки корзины в списке писем"""

    # Action
    status, result = u.emptyEmailsTrash()

    # Assertion
    AssertResultIsTrue(status, result)


def test_setChannelAsBookmarked() -> bool:
    """Тест проверяет возможность добвления канала в закладки"""

    # Setup
    status = False
    result = ''
    channel_in = False

    # Action
    _, bookmarked_channels = u.getChannels(filter="", channel_type=4)  # Get my bookmarked channels

    for channel in bookmarked_channels:
        if channel['channelid'] == CHANNEL_ID:
            channel_in = True

    if channel_in:
        status, result = u.setChannelAsBookmarked(CHANNEL_ID, "false")
    else:
        status, result = u.setChannelAsBookmarked(CHANNEL_ID, "true")

    # Assertion
    AssertResultIsTrue(status, result)


def test_getSettingInfo() -> json:
    """Тест проверяет корректность возвращаемых данных о настройках методом getSettingInfo"""

    # Action
    status, result = u.getSettingInfo(settingId='')

    # Assertion
    AssertNotEmptyOrError(status, result)


def test_setSettingInfo() -> bool:
    """Тест проверяет возможность установки настроек"""

    # Action
    status, result = u.setSettingInfo(settingId='TrayIconMode', newValue='Always')

    # Assertion
    AssertResultIsTrue(status, result)


def test_try_to_get_ReleaseNotes():
    """Тест проверяет возможность получения информации Release Notes"""

    # Action
    status, result = u.getReleaseNotes()

    # Assertion
    AssertResultIsNotEmpty(status, result)


def test_send_channel_quote_for_valid_message_id():
    """Тест проверят возможность отправки цитаты в канал"""

    _, messages = u.getChannelMessages(CHANNEL_ID)
    message_id = messages[0]['topicId']
    status, result = u.sendChannelQuote(CHANNEL_ID, "This is a python api test quote", message_id)
    AssertResultIsNotEmpty(status, result)


def test_send_channel_quote_for_invalid_message_id():
    """Тест проверят возможность отправки цитаты в канал"""

    message_id = 0
    status, result = u.sendChannelQuote(CHANNEL_ID, "This is a python api test quote", message_id)
    AssertResultIsZero(status, result)


def test_unable_to_send_channel_quote_for_invalid_channel():
    """Тест проверят возможность отправки цитаты в канал"""

    message_id = 0
    channel_id = 0
    status, result = u.sendChannelQuote(channel_id, "This is a python api test quote", message_id)
    AssertUnableToExecute(status, result)


def test_remove_valid_channel_message():
    """Тест проверят возможность удаления сообщений в канале"""

    _, messages = u.getChannelMessages(CHANNEL_ID)
    message_id = messages[0]['topicId']
    status, result = u.removeChannelMessage(CHANNEL_ID, message_id)
    AssertResultIsNotEmpty(status, result)


def test_remove_invalid_channel_message():
    """Тест проверят возможность удаления сообщений в канале если указан не верный ID"""

    message_id = 0
    status, result = u.removeChannelMessage(CHANNEL_ID, message_id)
    AssertResultIsZero(status, result)


def test_cant_remove_channel_message_from_other_channel():
    """Тест проверят возможность удаления сообщений в чужом канале.
    Сначала я получаю свой PK, потом получаю список всех каналов и извлекаю из него
    новый список ID каналов в которых owner не я. А потом перебераю ID из списка
    и проверю есть ли сообщения в канале и пробую удалить одно сообщение"""

    _, own_contact = u.getOwnContact()
    my_pk = own_contact['pk']
    _, channels = u.getChannels('', 0)
    channel_id = [channel['channelid'] for channel in channels if
                  channel['owner'] != my_pk and channel['isprivate'] is False]
    messages = []
    for ch_id in channel_id:
        u.joinChannel(ch_id, '')
        _, messages = u.getChannelMessages(ch_id)
        u.leaveChannel(ch_id)
        if len(messages) > 0:
            break
    message_id = messages[0]['topicId']
    status, result = u.removeChannelMessage(channel_id[0], message_id)
    AssertResultIsZero(status, result)


def test_enable_channel_notification_for_valid_channel():
    """Тест проверят возможность включения уведомлений о новых событиях на канале"""

    status, result = u.enableChannelNotification(CHANNEL_ID, "true")
    AssertResultIsTrue(status, result)


def test_disable_channel_notification_for_valid_channel():
    """Тест проверят возможность отключения уведомлений о новых событиях на канале"""

    status, result = u.enableChannelNotification(CHANNEL_ID, "false")
    u.enableChannelNotification(CHANNEL_ID, "true")  # return setting to enabled state
    AssertResultIsTrue(status, result)
