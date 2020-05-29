import unittest
import json
import time
import api
from settings import *
from datetime import datetime
from test_functions import *

report_file = "test_report.txt"
report_recipients = "31033EA6DD56AF6BD07B6DB4721A00BE9756084F2E76C17281FDDC57D73C0B09"


class MyTestResult(unittest.TestResult):
    def addFailure(self, test, err):
        test_name = str(test).split(" ")[0]
        with open(report_file, "a") as f:
            f.write(str(test_name) + ": Failed" + "; " + str(err[1]) + "\n")
        super(MyTestResult, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = str(test).split(" ")[0]
        with open(report_file, "a") as f:
            f.write(str(test_name) + ": Error: " + str(err[1]) + "\n")
        super(MyTestResult, self).addError(test, err)


class AllApiMethodsTesting(unittest.TestCase):
    u = api.Utopia("http://127.0.0.1:" + API_PORT + "/api/1.0", TOKEN)
    getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", ' \
                        '"startDateTime": "", "endDateTime": "", "referenceNumber": "" } '

    @classmethod
    def setUpClass(cls):
        """Create report_file if not exist or clear"""

        with open(report_file, "w"):
            print("Python API autotests report")

    def test_getSystemInfo(self) -> json:
        """Method getSystemInfo returns information about current packaging
        version of the Utopia application in the Response block.
        The method is called without using any parameters."""

        # Action
        status, result = self.u.getSystemInfo()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getBalance(self) -> str:
        """Method getBalance returns in the Response field the amount of cryptons on the primary balance,
        without considering the balance on cards. Method is called without using any parameters."""

        # Action
        status, result = self.u.getBalance()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getCards(self) -> json:
        """Method getCards returns in the Response field the current list of cards and their
        detailed information from uWallet. Method is called without using any parameters."""

        # Action
        status, result = self.u.getCards()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getVouchers(self) -> json:
        """Method getVouchers returns to the Response field the information about existing vouchers as a list.
        The method is called without using any parameters."""

        # Action
        status, result = self.u.getVouchers()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getInvoices(self) -> json:
        """Method getInvoices returns to the Response field the list of active invoices.
        The method is called with using any optional parameters."""

        # Action
        status, result = self.u.getInvoices(self.getInvoicesParams)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getProfileStatus(self) -> json:
        """Method getProfileStatus returns the profile status"""

        # Action
        status, result = self.u.getProfileStatus()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getContacts(self, filtr: str = "") -> json:
        """Method getContacts returns to the Response field the list of contacts, it is possible to search by
        full or partial matching of the Public Key and Nickname. As a parameter it is possible to specify
        Filter that transfers the text line to search for contacts ( has to contain full or partial matching
        with Public Key or Nickname of the searched contact).The Filter "#owner#" will return information
        about yourself."""

        # Action
        status, result = self.u.getContacts(filtr)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getContactAvatar(self, contact_pk: str = CONTACT_PK) -> json:
        """Method getContactAvatar returns to the Response field the avatar of the selected user in the base64
        or hex format. As a parameter the method uses Public Key of the contact."""

        # Action
        status, result = self.u.getContactAvatar(contact_pk, "BASE64", "JPG")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendInstantMessage(self, contact_pk: str = CONTACT_PK) -> json:
        """Method sendInstantMessage sends personal message(IM) to the selected contact from the contact list.
        The method is called by using the To parameter, that passes on the Public Key or Nickname to whom
        the message would be sent (Public Key can be recognized by using the getContacts method) and Text,
        which contains the text of the message. In the Response field the status of completion
        of the operation is displayed."""

        # Action
        txt_message = "API method sendInstantMessage testing \n ======================= \n Python unittest"

        status, result = self.u.sendInstantMessage(contact_pk, txt_message)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendEmailMessage(self, contacts_pk: tuple = (CONTACT_PK,)) -> json:
        """Method sendEmailMessage sends uMail to the selected contact in the Utopia network.
        The method is called by using the To parameter, which passes on the Public Key or Nickname
        to which the uMail would be sent (Public Key can be recognized by using the getContacts method);
        Subject, that determines the subject of the email; and Body, which passes on the text in the body
        of the uMail. In the Response field the status of completion of the operation is displayed."""

        # Action
        body_text = "This is a Python api body"
        subject_text = "This is a Python api subject"

        status, result = self.u.sendEmailMessage(contacts_pk, subject_text, body_text)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendPaymentToPk(self, recipient: str = CONTACT_PK,
                             self_card: str = "",
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
        self.status, result = self.u.sendPayment(recipient, comment, self_card, amount)

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_sendPaymentToCard(self, recipient: str = CONTACT_CARD,
                               self_card: str = "",
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

        self.status, result = self.u.sendPayment(recipient, comment, self_card, amount)

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_sendPaymentFromCard(self, recipient: str = CONTACT_PK,
                                 self_card: str = SELF_CARD,
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

        self.status, result = self.u.sendPayment(recipient, comment, self_card, amount)

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_createVoucher(self, amount: int = 10) -> 'reference_number':
        """Method createVoucher with the mandatory parameter 'amount' creates new voucher for the selected amount
        in the list of own vouchers. The amount for the vouchers is taken from the main account balance.
        Amount, which transfers the amount of transfer (the number needs to be greater than 0 and contain
        no more than 9 character after coma);"""

        # Action
        self.status, result = self.u.createVoucher(amount)

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_useVoucher(self) -> 'reference_number':
        """Method useVoucher allows to use the selected voucher with adding its amount to your main account.
        The method is called with mandatory 'VoucherId' parameter in which the number of the voucher is specified."""

        # SetUp
        _, vouchers = self.u.getVouchers()
        if len(vouchers) == 0 or 'Error' in vouchers:
            self.u.createVoucher(10)
            time.sleep(3)
            _, vouchers = self.u.getVouchers()

        # Action
        self.status, result = self.u.useVoucher(vouchers[0]['voucherid'])

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_deleteVoucher(self, amount: int = 10) -> 'reference_number':
        """Method deleteVoucher allows to remove your own voucher from the existing list with having the amount
        refunded back to your account. The method is called with mandatory 'VoucherId' parameter in which
        the number of the voucher is specified. In the Response field the status of completion of the
        operation is displayed."""

        # SetUp
        _, result = self.u.getVouchers()
        if len(result) == 0:
            self.u.createVoucher(amount)
            time.sleep(3)
            _, result = self.u.getVouchers()

        # Action
        self.status, result = self.u.deleteVoucher(result[0]["voucherid"])

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_sendInvoice(self, recipient: str = CONTACT_CARD, amount: int = 10) -> 'reference_number':
        """Method sendInvoice sends invoice (Request Cryptons) for deduction of specified amount from specified card.
        In the parameters of the method, the card number of the request recipient is specified (CardId).
        In the second parameter the 'Amount' is specified which transfers the amount of transfer (the number needs
        to be greater than 0 and contain no more than 9 character after coma), and the third parameter is optional,
        where 'Comment is optional, which contains the text of the comment (up to 148 characters)."""

        # Action
        self.status, result = self.u.sendInvoice("sendInvoice to contact card", recipient, amount)

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_getInvoiceByReferenceNumber(self) -> json:
        """Method getInvoiceByReferenceNumber allows to receive 'batchid' of the invoice using the ReferenceNumber.
        In the Response field, batchid is returned, which is considered a successful status for completion
        of the operation."""

        # Action
        _, invoices = self.u.getFinanceHistory(filters='ALL_REQUESTS', referenceNumber='', fromDate='', toDate='',
                                               batchId='', fromAmount='', toAmount='')
        if len(invoices) > 0 and 'Error' not in invoices:
            status, result = self.u.getInvoiceByReferenceNumber(invoices[0]['referenceNumber'])
        else:
            raise Exception("There is no invoices or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getTransactionIdByReferenceNumber(self) -> json:
        """Method getTransactionIdByReferenceNumber allows to receive 'batchid' of the transaction by using
        the ReferenceNumber. In the Response field, batchid is returned, which is considered a successful status
        for completion of the operation."""

        # Action
        _, transactions = self.u.getFinanceHistory(filters='ALL_REQUESTS', referenceNumber='', fromDate='', toDate='',
                                                   batchId='', fromAmount='', toAmount='')
        if len(transactions) > 0 and 'Error' not in transactions:
            status, result = self.u.getTransactionIdByReferenceNumber(transactions[0]['referenceNumber'])
        else:
            raise Exception("There is no transactions or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_acceptInvoice(self) -> 'reference_number':
        """Method acceptInvoice performs payment of the incoming invoice. The method is called with mandatory
        'InvoiceId' parameter in which the ID of the invoice that needs to be rejected. For receiving ID of the
        needed invoice it is needed to call getInvoices for receiving the list of invoices with their detailed
        information. In response the acceptInvoice method returns in the Response block the results of completing
        this request."""

        # Action
        _, invoices = self.u.getInvoices(self.getInvoicesParams)
        incoming_invoices = [invoice for invoice in invoices if invoice['direction'] == 'Incoming'
                             and invoice['status'] == 'Awaiting']
        # incoming_invoices = list(filter(lambda x: x['direction'] == "Incoming", invoices))
        if len(incoming_invoices) > 0 and 'Error' not in incoming_invoices:
            self.status, result = self.u.acceptInvoice(incoming_invoices[0]['invoiceid'])
        else:
            raise Exception("There is no incoming invoices or got Error on request")

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

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

    def test_declineInvoice(self) -> 'reference_number':
        """Method declineInvoice sends request for declining the payment for the incoming invoice. The method is
        called with mandatory the 'InvoiceId' parameter. Parameter InvoiceId contains the ID value for the invoice
        that needs to be declined. To get the ID of the required invoice it is mandatory to call the getInvoices
         method for receiving the list of invoices with their detailed information. In response the declineInvoice
         method returns in the Response block the results of completing this request."""

        # Setup
        status = ""
        result = ""

        # Action
        _, invoices = self.u.getInvoices(self.getInvoicesParams)
        incoming_invoices = [invoice for invoice in invoices if invoice['direction'] == 'Incoming'
                             and invoice['status'] == 'Awaiting']
        if len(incoming_invoices) > 0 and 'Error' not in incoming_invoices:
            status, result = self.u.declineInvoice(incoming_invoices[0]['invoiceid'])
        else:
            raise Exception("There is no incoming invoices or got Error on request")

        # Assertion
        AssertResultIsRefNum(self, status, result)

    def test_getChannels(self, filters: str = '1', channel_type: int = 0) -> json:
        """Method getChannels returns in the Response field the current list of all channels of Utopia ecosystem,
        it is possible to search by name of the channel (partial or complete matching). As a parameter, a Filter
        can be specified, which can be used for searching of the channel by name ( has to contain full or partial
        matching of the channel name)."""

        # Action
        status, result = self.u.getChannels(filters, channel_type)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendChannelMessage(self, channel_id: str = "81B8CA0B8E2A5C87C468927953BEB674",
                                message: str = "Python api test") -> json:
        """Method sendChannelMessage creates and sends message in the selected channel (to send the message the user
        should have joined this channel and needs to have status 'online'). To enter the channel, use joinChannel
        method. As a parameter the method is using the ChannelId, which passes on the id of the channel in which the
        message is being sent (finding the id of the channel is possible by using the getChannels method) and Message,
        which contains the text of the message being sent. In the Response field the status of completion of
        the operation is displayed."""

        # Action
        status, result = self.u.sendChannelMessage(channel_id, message)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_leaveChannel(self, channel_id: str = "C160AB99F292C98746C3EA6ABB6AC7CD", passwd: str = "utopia9") -> bool:
        """Method leaveChannel executes the exit from the selected channel. As a parameter the method takes the
        ChannelId, which passes on the id of the channel in which the message is being sent (finding the id of the
        channel is possible by using the getChannels method ."""

        # Action
        status, result = self.u.leaveChannel(channel_id)
        self.u.joinChannel(channel_id, passwd)

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_joinChannel(self, channel_id: str = "C160AB99F292C98746C3EA6ABB6AC7CD",
                         channel_password: str = "utopia9") -> bool:
        """Method joinChannel executes an entry into selected channel. The following parameters are specified:
        ChannelId, which passes on the id of the channel in which the message is being sent (finding the id of the
        channel is possible by using the getChannels method); when needed the parameter Password is specified,
        which passes on the password for entry into the channel (if left empty, no password is required).
        In the Response field the status of completion of the operation is displayed."""

        # Action
        status, result = self.u.joinChannel(channel_id, channel_password)

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_deleteContact(self, pk: str = CONTACT_PK) -> bool:
        """Method deleteContact allows to perform the operation of removing selected user from the list of contacts.
        The method is called with mandatory use of 'Public Key' parameter that represents Public key of the to be
        removed contact. In the Response field the status of completion of such operation is displayed."""

        # Action
        status, result = self.u.deleteContact(pk)
        s = self.u.sendAuthorizationRequest(pk, 'autotest request')
        s = self.u.acceptAuthorizationRequest(pk, 'autotest accept request')

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_sendAuthorizationRequest(self, pk: str = CONTACT_PK, message: str = 'autotest request') -> bool:
        """Method sendAuthorizationRequest allows to send the authorization request to add the user to the contact
        list. The method is called with mandatory use of 'Public Key' and 'Message' parameters. The Public Key
        parameter represents the Public Key of the person being added. The message parameter represents itself
        the text message with the request to be authorized. In the Response field the status of completion of
        sending such request is displayed."""

        # Action
        status, result = self.u.sendAuthorizationRequest(pk, message)

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_rejectAuthorizationRequest(self, pk: str = CONTACT_PK, message: str = 'autotest reject request') -> bool:
        """Method rejectAuthorizationRequest declines the incoming authorization request from user with Public key,
        which is specified as first parameter (Public Key) of the rejectAuthorizationRequest method. The second
        parameter of the method is Message row, that represents itself the response message the user who`s
        authorization is rejected. In the Response field the status of completion of such request is displayed."""

        # Action
        status, result = self.u.rejectAuthorizationRequest(pk, message)
        self.u.sendAuthorizationRequest(pk, "autotest request")
        self.u.acceptAuthorizationRequest(pk, "autotest accept request")

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_acceptAuthorizationRequest(self, pk: str = CONTACT_PK, message: str = 'autotest accept request') -> bool:
        """Method acceptAuthorizationRequest accepts the incoming authorization request to add user to contacts.
        The method is called with mandatory use of 'Public Key' and 'Message' parameters. The Public Key parameter
        represents the Public Key of the person who send the authorization request. The message parameter represents
        itself the text message. In the Response field the status of completion of sending such request is displayed."""

        # Action
        status, result = self.u.acceptAuthorizationRequest(pk, message)

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_getUnsSyncInfo(self) -> json:
        """Method getUnsSyncInfo returns statistics value of sync process."""

        # Action
        status, result = self.u.getUnsSyncInfo()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_unsCreateRecordRequest(self, nick: str = random_uns, validTo: str = "2100-07-20",
                                    is_primary: str = "false", channel_id: str = '') -> 'reference_number':
        """unsCreateRecordRequest method sends a request to register a uNS name in the Utopia ecosystem for specific
        time period. In addition to uNS name which is used as a parameter (the name contains characters (A-Z),
        numbers (0-9), a dash (-) character, a period (.) and can be up to 32 characters long.), other parameters
        include: expiration date (yyyy -mm-dd ) which is a final valid date of the uNS (6 months by default),
        isPrimary, indicating whether the uNS name is primary, ChannelId, which passes the channel identifier
        uNS will be associated with (channel identifier can be found out using the getChannels method).
        The Response field displays the status of the completed operation."""

        # Action
        self.status, result = self.u.unsCreateRecordRequest(nick, validTo, is_primary, channel_id)

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_unsDeleteRecordRequest(self) -> 'reference_number':
        """Method unsDeleteRecordRequest sends request for deletion of uNS name of the current user. As a parameter
        the uNS name is used ( uNS name can be found by using the unsRegisteredNames method). In the Response field
        the status of completion of the operation is displayed."""

        _, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and 'Error' not in unss:
            self.status, result = self.u.unsDeleteRecordRequest(unss[-1]["nick"])

            # Assertion
            AssertResultIsRefNum(self, self.status, result)
        else:
            raise Exception("There is no UNS, or got Error on request")

    def test_unsSearchByPk(self, pk: str = CONTACT_PK) -> json:
        """Method unsSearchByPk returns in the Response field the list of all uNS names with selected 'Filter'
        parameter (contains full or partial matching with the searched uNS name. The name can contain symbols (A-Z),
        numbers (0-9), dash symbol (-) and period (.) and can be no greater than 32 symbols in length.)."""

        # Action
        status, result = self.u.unsSearchByPk(pk)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_unsSearchByNick(self, nick: str = CONTACT_NAME) -> json:
        """Method unsSearchByNick returns the list of uNS names by partial or full matching with selected 'Filter'
        parameter (contains full or partial matching with the searched uNS name. The name can contain symbols (A-Z),
        numbers (0-9), dash symbol (-) and period (.) and can be no greater than 32 symbols in length.)."""

        # Action
        status, result = self.u.unsSearchByNick(nick)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_unsRegisteredNames(self) -> json:
        """Method unsRegisteredNames returns in the Response field the list of all registered uNS for current user.
        The method is called without using any parameters."""

        # Action
        status, result = self.u.unsRegisteredNames()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_unsModifyRecordRequest(self) -> 'reference_number':
        """unsModifyRecordRequest method sends a request to modify the uNS name in the Utopia ecosystem for specific
        time period. In addition to uNS name which is used as a parameter (the name contains characters (A-Z), numbers
        (0-9), a dash (-) character, a period (.) and can be up to 32 characters long.), other parameters include:
        expiration date (yyyy -mm-dd ) which is a final valid date of the uNS (6 months by default), isPrimary,
        indicating whether the uNS name is primary, ChannelId, which passes the channel identifier uNS will be
        associated with (channel identifier can be found out using the getChannels method). The Response field displays
        the status of the completed operation."""

        # Actions
        _, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and 'Error' not in unss:
            self.status, result = self.u.unsModifyRecordRequest(unss[-1]['nick'], "2100-07-20", False, "")

            # Assertion
            AssertResultIsRefNum(self, self.status, result)
        else:
            raise Exception("There is no UNS, or got Error on request")

    def test_setContactGroup(self, pk: str = CONTACT_PK, group_name: str = "PyAPI") -> bool:
        """Method setContactGroup creates group or transfers selected contact into the group in the contact list.
        The method is called by using the Public Key parameters, which pass the Public Key of the contact (Public Key
        can be recognized by using the getContacts method) and Group Name, which passes the group name for creation
        or transfer (up to 32 symbols). In the Response field the status of completion of the operation is displayed."""

        # Action
        status, result = self.u.setContactGroup(pk, group_name)

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_setContactNick(self, pk: str = CONTACT_PK, new_name: str = CONTACT_NAME) -> bool:
        """Method setContactNick sets the selected value for the Nickname field for the selected contact. The method
        is called by using the Public Key parameters, which pass on the Public Key for the contact (Public Key can be
        recognized by using the getContacts method) and New Nick, which passes on the new Nickname (up to 32 symbols).
        Empty value to be set as the Nickname Public Key of the contact. In the Response field the status of completion
         of the operation is displayed."""

        # Action
        status, result = self.u.setContactNick(pk, new_name)

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_getEmailFolder(self, folder_type: int = 1, fltr: str = "") -> json:
        """Method getEmailFolder returns to the Response block the list of identifications of uMail emails in the
        selected folder by using specified search filter. The method is called by using the FolderType parameters,
        which pass on the number of the folder from which the list should be taken (numbers of the folders 1-Inbox,
        2-Drafts, 4-Sent, 8-Outbox, 16-Trash) and it is possible to specify the Filter parameter, which passes on the
        text value for the search of emails in uMail (has to contain the full or partial match with the Public Key,
        Nickname or the text of email)."""

        # Action
        status, result = self.u.getEmailFolder(folder_type, fltr)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getEmailById(self) -> json:
        """Method getEmailById returns the information based on the selected email in uMail. The method is called by
        using the Id parameter, which passes on the id of the email (id of the email can be found by using
        getEmailFolder method)."""

        # Action
        _, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and 'Error' not in emails:
            status, result = self.u.getEmailById(emails[0])
        else:
            raise Exception("There is no emails, or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_deleteEmail(self) -> json:
        """Method deleteEmail deletes email in uMail. First deletion will move email to the Trash, subsequent will
        remove from the database. The method is called by using the Id parameter which passes on the id of the email
        (id of the email can be found by using getEmailFolder method). In the Response field the status of completion
        of the operation is displayed."""

        # Action
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and 'Error' not in emails:
            status, result = self.u.deleteEmail(emails[-1])
        else:
            raise Exception("There is no emails, or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_clearTrayNotifications(self) -> bool:
        """Method clearTrayNotifications allows to drop all existing notifications in the tray of the operating system.
         The method is called without using any parameters. In the Response field the status of completion of the
         operation is displayed."""

        # Action
        status, result = self.u.clearTrayNotifications()

        # Assert
        AssertResultIsTrue(self, status, result)

    def test_getContactMessages(self, pk: str = CONTACT_PK) -> json:
        """Method getContactMessages returns in the Response block the history of communication from personal chat
        with selected contact. The method is called by using the Public Key parameter, that passes on the Public Key
        of the contact (Public Key can be recognized by using the getContacts method)"""

        # Action
        status, result = self.u.getContactMessages(pk)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendReplyEmailMessage(self) -> json:
        """Method sendReplyEmailMessage creates response email in uMail for the incoming email and sends it to the
        contact with new message. The method is called by using the Id parameters, which pass on the id of the email
        (id of the email can be found by using getEmailFolder method) and Body, which passes on the text of the email
        in uMail. In the Response field the status of completion of the operation is displayed."""
        # SetUp
        subject = 'This is a Reply email by Python API test'
        body = 'This is a python api test'

        # Action
        _, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and 'Error' not in emails:
            status, result = self.u.sendReplyEmailMessage(emails[-1], body, subject)
        else:
            raise Exception("There is no emails, or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendForwardEmailMessage(self, recipient: str = CONTACT_PK, body: str = "", subject: str = "") -> json:
        """Method sendForwardEmailMessage creates response email for an incoming email in uMail and sends it to the
        selected contact with the new message. The method is called by using the 'Id' parameter, which passes on the
        id of the email (id of the email can be found by using getEmailFolder method); 'To', which passes on the
        Public Key or Nickname of the user to which the email will be sent; and 'Body', which passes on the text in
        uMail. In the Response field the status of completion of the operation is displayed."""

        # SetUp
        recipient = CONTACT_PK
        body = 'This is a Forward email by Python API test'
        subject = 'This is a Python api test'

        # Action
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and 'Error' not in emails:
            status, result = self.u.sendForwardEmailMessage(emails[-1], recipient, body, subject)
        else:
            raise Exception("There is no emails, or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getFinanceHistory(self, filters: str = "ALL_TRANSACTIONS",
                               referenceNumber: str = "",
                               fromDate: str = "",
                               toDate: str = "",
                               batchId: str = "",
                               fromAmount: int = None,
                               toAmount: int = None) -> json:
        """Method getFinanceHistory allows to receive the history of financial transactions based on the
        specifications in the parameters of the filter."""

        # Action
        status, result = self.u.getFinanceHistory(filters,
                                                  referenceNumber,
                                                  fromDate,
                                                  toDate,
                                                  batchId,
                                                  fromAmount,
                                                  toAmount)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_requestUnsTransfer(self, pk: str = CONTACT_PK) -> json:
        """Method requestUnsTransfer allows to transfer the uNS record to contact. The method is called with mandatory
        'Name' and 'Public Key' parameters. Name parameter is the name of the uNS record from the list of own uNS
        records. hexNewOwnerPk represents hash of the public portion of the key (as in some instances, key is now
        known, only hash is), to which the transfer is being made. In the Response field the status of completion of
        the operation is displayed."""

        # Action
        _, unss = self.u.unsRegisteredNames()
        time.sleep(1)
        if len(unss) > 0 and 'Error' not in unss:
            status, result = self.u.requestUnsTransfer(unss[-1]['nick'], pk)
        else:
            self.u.unsCreateRecordRequest(random_uns)
            time.sleep(3)  # wait for network confirmation
            _, unss = self.u.unsRegisteredNames()
            status, result = self.u.requestUnsTransfer(unss[-1]['nick'], pk)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_incomingUnsTransfer(self) -> json:
        """Method incomingUnsTransfer returns in the Response field the list of all incoming uNS transfer records with
        their detailed information. The method is called without using any parameters."""

        # Action
        status, result = self.u.incomingUnsTransfer()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_acceptUnsTransfer(self) -> 'reference_number':
        """Method acceptUnsTransfer allows to accept the incoming record of the uNS transfer. The method is called
        with the mandatory 'RequesId' parameter, which represents the id of the incoming uNS transfer. To receive the
        id of incoming transfers it is necessary to call the incomingUnsTransfer method, which returns the list of
        incoming uNS transfer. In the Response field the status of completion of the acceptUnsTransfer operation
        is displayed."""

        # Action
        _, incoming_unses = self.u.incomingUnsTransfer()
        if len(incoming_unses) > 0 and 'Error' not in incoming_unses:
            self.status, result = self.u.acceptUnsTransfer(incoming_unses[0]['id'])
        else:
            raise Exception("There is no incoming UNS transfers")

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_declineUnsTransfer(self) -> 'reference_number':
        """Method declineUnsTransfer allows to decline the incoming record of the uNS transfer. The method is called
        with the mandatory 'RequesId' parameter, which represents the id of the incoming uNS transfer. To receive the
        id of incoming transfers it is necessary to call the incomingUnsTransfer method, which returns the list of
        incoming uNS transfer. In the Response field the status of completion of the declineUnsTransfer operation
        is displayed."""

        # Action
        _, incoming_unses = self.u.incomingUnsTransfer()
        if len(incoming_unses) > 0 and 'Error' not in incoming_unses:
            self.status, result = self.u.declineUnsTransfer(incoming_unses[0]['id'])
        else:
            raise Exception("There is no incoming UNS transfers")

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_outgoingUnsTransfer(self) -> json:
        """Method outgoingUnsTransfer returns in the Response field the list of all outgoing uNS transfer records with
        their detailed information. The method is called without using any parameters."""

        # Action
        status, result = self.u.outgoingUnsTransfer()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getNetworkConnections(self) -> json:
        """Method getNetworkConnections returns in Response block detailed information about all current network
        connections. The method is called without using any parameters."""

        # Action
        status, result = self.u.getNetworkConnections()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getProxyMappings(self) -> json:
        """Method getProxyMappings returns in Response block the list of all configured proxy mappings. The method
        is called without using any parameters."""

        # Action
        status, result = self.u.getProxyMappings()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_createProxyMapping(self,
                                srcHost: str = "uns",
                                srcPort: str = "80",
                                dstHost: str = "81.19.72.36",
                                dstPort: str = "80",
                                enabled: str = "true") -> json:
        """Method createProxyMapping allows to create a 'bridge' type of connections to receive access to the external
        page by the specified ip address and port, when trying to call the inter-network address in the Utopia network
        ( usually used by Idyll browser). The method by using the mandatory parameters SrcHost,SrcPort,DstHost,DstPort,
        Enabled. The SrcHost parameters represents its own uNS name, the request of which would be executed in the
        Idyll browser. The SrcPort parameter represents the port number on which the mapping is planned to be located.
        Parameter DstHost represents itself the ip address of the page on which it will navigate, and parameters
        DstPort is the number of port on which the needed page with specified ip address is located. The Enabled
        parameter represents the activity of such connection as 'true' or 'false'. In the Response block the status of
        completion of the attempt to create a connection with specified parameters is displayed."""

        # Action
        _, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and 'Error' not in unss:
            srcHost = unss[0]["nick"]
            status, result = self.u.createProxyMapping(srcHost, srcPort, dstHost, dstPort, enabled)
        else:
            raise Exception("There is no UNS records, or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_enableProxyMapping(self) -> json:
        """Method enableProxyMapping allows to turn on the ability to use the connection with specified 'MappingId' as
        a parameter when calling this method. To receive the 'MappingId' of the needed connection it is necessary to
        call the getProxyMappings method. In the Response field the status of completion of operation of turning on
        the connection is displayed."""

        # Action
        _, proxy_mappings = self.u.getProxyMappings()
        if len(proxy_mappings) > 0 and 'Error' not in proxy_mappings:
            status, result = self.u.enableProxyMapping(proxy_mappings[0]['id'])
        else:
            raise Exception("There is no mappings or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_disableProxyMapping(self) -> json:
        """Method disableProxyMapping allows to turn off the ability to use the connection with specified 'MappingId'
        as a parameter when calling this method. To receive the 'MappingId' of the needed connection it is necessary
        to call the getProxyMappings method. In the Response field the status of completion of operation of turning
        off the connection is displayed."""

        # Action
        _, proxy_mappings = self.u.getProxyMappings()
        if len(proxy_mappings) > 0 and 'Error' not in proxy_mappings:
            status, result = self.u.disableProxyMapping(proxy_mappings[0]['id'])
        else:
            raise Exception("There is no mappings or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_removeProxyMapping(self) -> json:
        """Method removeProxyMapping allows to remove the selected configured of proxy mappings. The method is called
        by using the MappingId parameter, which represents the id of the configured proxy connection. In the Response
        field the status of completion of operation of removing the mapping is displayed."""

        # Action
        _, proxy_mappings = self.u.getProxyMappings()
        if len(proxy_mappings) > 0 and 'Error' not in proxy_mappings:
            status, result = self.u.removeProxyMapping(proxy_mappings[0]['id'])
        else:
            raise Exception("There is no mappings or got Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_addCard(self,
                     color: str = "#FBEDC0",
                     card_name: str = "API card",
                     preferred_number: str = "") -> 'reference_number':
        """Method addCard sends the request for creation of new card in uWallet. The method is called by using the
        following parameters: Name, which passes on the name of the new card (can contain between 1 and 32 symbols),
        Color, which passes on the color of the card ( in RGB format, for example '#FFFFFF') and also can specify the
        First 4 numbers of the card for customization ( it is possible to change only 4 first symbols, can contain
        symbols (A-F) and numbers (0-9)). In the Response field the status of completion of the operation
        is displayed."""

        # Action
        self.status, result = self.u.addCard(color, card_name, preferred_number)

        # Assertion
        AssertResultIsRefNum(self, self.status, result)

    def test_deleteCard(self) -> 'reference_number':
        """Method deleteCard deletes the existing card from uWallet. The amount from card will be returned to the main
        balance. The following parameter is specified: CardId, which passes on the card number ( CardId can be found
        by using the getCards method). In the Response field the status of completion of the operation is displayed."""

        # Action
        _, cards = self.u.getCards()
        result = ""

        if len(cards) > 0 and 'Error' not in cards:
            card = [card for card in cards if card['name'] == 'API card']
            if len(card) == 0:
                self.u.addCard("#FBEDC0", "API card", "")
                time.sleep(3)  # wait for network confirmation
                _, cards = self.u.getCards()
                card = [card for card in cards if card['name'] == 'API card']
            try:
                self.status, result = self.u.deleteCard(card[0]['cardid'])
            except Exception as e:
                print(e)
            finally:
                # Assertion
                AssertResultIsRefNum(self, self.status, result)

    def test_getFinanceSystemInformation(self) -> json:
        """Method getFinanceSystemInformation returns in the Response field the information about Utopia financial
        system (information about fees and limits). Method is called without using any parameters."""

        # Action
        status, result = self.u.getFinanceSystemInformation()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getMiningBlocks(self) -> json:
        """Method getMiningBlocks returns to the Response field the information about the mining blocks for which the
        reward has been paid. The method is called without using any parameters."""

        # Action
        status, result = self.u.getMiningBlocks()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_enableMining(self, enabled: str = "true") -> bool:
        """Method enableMining turns on the mining in the Utopia client (mining is available only for x64 client). As
        a parameter the Status (true/false) is specified, which turns on or off the mining process. In the Response
        field the status of completion of the operation is displayed."""

        # Action
        status, result = self.u.enableMining(enabled)

        # Assertion
        AssertResultIsTrue(self, status, result)

    def test_enablePoS(self, enabled: str = "true") -> bool:
        """Calling the enablePoS method turns on and off the PoS on the remaining irreducible account balance. As a
        parameter, one of the two statuses, true or false is selected. In the Response field the status of completion
        of turning on or off the operation is displayed."""

        # Prepare step
        self.u.enablePoS('false')  # Switch off pos
        time.sleep(3)  # wait for network response

        # Action
        status, result = self.u.enablePoS(enabled)
        time.sleep(3)  # wait for network response

        # Assertion
        AssertResultIsTrue(self, status, result)

    def test_enableHistoryMining(self, enabled: str = "true") -> bool:
        """Calling the enableHistoryMining method changes the option of the automatic reading of the mining history from
         the financial server. As a parameter of the method, the status of true or false is specified. In the Response
        field the status of completion of turning on or off the operation is displayed."""

        # Action
        status, result = self.u.enableHistoryMining(enabled)

        # Assertion
        AssertResultIsTrue(self, status, result)

    def test_statusHistoryMining(self) -> json:
        """Calling the statusHistoryMining method returns in the Response block the status of mining history poll.
        Method is called without using any parameters.
        Meaning of different states:
        0 = STATE_EMPTY
        1 = STATE_IN_PROGRESS
        2 = STATE_RECEIVED_RESPONSE"""

        # Action
        status, result = self.u.statusHistoryMining()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_lowTrafficMode(self) -> json:
        """Method lowTrafficMode returns in Response block the status of low Traffic mode. The method is called
        without using any parameters."""

        # Action
        status, result = self.u.lowTrafficMode()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_setLowTrafficMode(self, enabled: str = "false") -> json:
        """Method setLowTrafficMode allows to turn on or off the low Traffic mode. The method is called by using the
        enabled parameter, which represents itself a status of true or false that is being set
        for this particular mode."""

        # Action
        status, result = self.u.setLowTrafficMode(enabled)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getWhoIsInfo(self, pk: str = CONTACT_PK) -> json:
        """Method getWhoIsInfo returns in Response block the detailed information about selected user. As a parameter
        of the method, the Public key of the particular user can be used, or his nickname, if such contact was added
        to the contact list."""

        # Action
        status, result = self.u.getWhoIsInfo(pk)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getChannelInfo(self, channel_id: str = CHANNEL_ID) -> json:
        """Method getChannelInfo returns in the Response field the information about the channel ( the response
        contains following parameters: HideInCommonList, description, geotag, hashtags, languages, readonly, title,
        type, private). As a parameter the method is using the ChannelId for which the user is trying to find more
        information (finding the id of the channel is possible by using the getChannels method)."""

        # Action
        status, result = self.u.getChannelInfo(channel_id)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getChannelModerators(self, channel_id: str = CHANNEL_ID) -> json:
        """Method getChannelModerators returns in the Response field the list of Public Keys of moderators. As a
        parameter the ChannelId is used (finding the id of the channel is possible by using the getChannels method)."""

        # Action
        status, result = self.u.getChannelModerators(channel_id)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getChannelModeratorRight(self, channel_id: str = CHANNEL_ID) -> json:
        """Method getChannelModeratorRight returns in the Response field the list of moderator rights in the channel
        ( the response contains parameters as ban, delete, promote). As a parameter the method uses: ChannelId from
        which it is needed to get the list of moderator rights (finding the id of the channel is possible by using the
        getChannels method) and Public Key of the channel moderator (finding Public Key(pk) of the channel moderator
        is possible by using the getChannelModerators method)."""

        # Action
        _, moderators = self.u.getChannelModerators(channel_id)
        if len(moderators) > 0 and "Error" not in moderators:
            status, result = self.u.getChannelModeratorRight(channel_id, moderators[0])
        else:
            raise Exception("There is no moderators or Error on request")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_setProfileStatus(self, status: str = "Available", mood: str = "QA Engineer") -> json:
        """Method setProfileStatus sets the new status, as well as the mood message in the Utopia Ecosystem. The method
         is called by using Status parameter line with possible options: (Available, Away, DoNotDisturb, Invisible,
         Offline) and if desired Mood which contains mood message text (up to 130 symbols). In the Response field, the
         status of completed operation is displayed."""

        # Action
        status, result = self.u.setProfileStatus(status, mood)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getEmails(self, folder_type: int = 1, fltr: str = "") -> json:
        """Method getEmails returns to the Response block the list of detailed of uMail emails in the selected folder
        by using specified search filter. The method is called by using the FolderType parameters, which pass on the
        number of the folder from which the list should be taken (numbers of the folders 1-Inbox, 2-Drafts, 4-Sent,
        8-Outbox, 16-Trash) and it is possible to specify the Filter parameter, which passes on the text value for the
        search of emails in uMail (has to contain the full or partial match with the Public Key, Nickname or the text
        of email)"""

        # Action
        status, result = self.u.getEmails(folder_type, fltr)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getChannelMessages(self, channel_id: str = CHANNEL_ID) -> json:
        """Method getChannelMessages returns in the Response block the history of communication from selected channel.
        The method is called by using the channelid parameter, that passes on id of channel."""
        # Action
        # status, result = self.u.getChannelMessages("B4EF14CFE2782C1E94E82631F9B782E2")
        status, result = self.u.getChannelMessages(channel_id)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    # @unittest.skip("просьба не трогать ушан")
    def test_createChannel(self) -> json:
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

        # Action
        status, myChannel = self.u.createChannel(channel_name, description, read_only, read_only_privacy, password,
                                                      languages, hash_tags, geo_tag, avatar, hide_in_ui)
        time.sleep(3)  # wait for uchan database sync ends
        self.u.deleteChannel(myChannel, password)  # cleanup step

        # Assertion
        AssertNotEmptyOrError(self, status, myChannel)

    def test_getOwnContact(self) -> json:
        """Method getOwnContact returns information about yourself."""

        # Action
        status, result = self.u.getOwnContact()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getChannelAvatar(self, channel_id: str = CHANNEL_ID, coder: str = "BASE64", format: str = "JPG") -> json:
        """Method getChannelAvatar returns to the Response field the avatar of the selected channel
        in the base64 or hex format."""

        # Action
        status, result = self.u.getChannelAvatar(channel_id, coder, format)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendInstantQuote(self, pk: str = CONTACT_PK) -> json:
        """Method sendInstantQuote sends quote personal message(IM) to the selected contact from the contact list
        on message by id_message"""

        # Action
        _, contact_msgs = self.u.getContactMessages(pk)
        if len(contact_msgs) == 0:
            self.test_sendInstantMessage()
            _, contact_msgs = self.u.getContactMessages(pk)
        status, result = self.u.sendInstantQuote(pk, "this is python unittest quote message",
                                                 contact_msgs[0]["id"])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getStickerCollections(self) -> json:
        """Method getStickerCollections returns collection names of stickers."""

        # Action
        status, result = self.u.getStickerCollections()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getStickerNamesByCollection(self) -> json:
        """Method getStickerNamesByCollection returns available names from corresponded collection."""

        # Action
        _, sticker_collection = self.u.getStickerCollections()
        status, result = self.u.getStickerNamesByCollection(sticker_collection[0])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getImageSticker(self) -> json:
        """Method getImageSticker returns image by sticker name from corresponded collection in coder that can be
        equal "BASE64"."""

        # Action
        _, sticker_collection = self.u.getStickerCollections()
        _, all_stickers = self.u.getStickerNamesByCollection(sticker_collection[0])
        status, result = self.u.getImageSticker(sticker_collection[0], all_stickers[0], "BASE64")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendInstantSticker(self, contact_pk: str = CONTACT_PK) -> json:
        """Method sendInstantSticker sends sticker personal message(IM) to the selected contact from the contact list
        a sticker from collection by name."""

        # Action
        _, sticker_collection = self.u.getStickerCollections()
        _, all_stickers = self.u.getStickerNamesByCollection(sticker_collection[0])
        status, result = self.u.sendInstantSticker(contact_pk, sticker_collection[0], all_stickers[0])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendInstantBuzz(self, contact_pk: str = CONTACT_PK) -> json:
        """Method sendInstantBuzz sends buzz personal message(IM) to the selected contact from the contact list with
        comments."""

        # Action
        status, result = self.u.sendInstantBuzz(contact_pk, "Python Buzz")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendInstantInvitation(self, pk: str = CONTACT_PK, channel_id: str = CHANNEL_ID) -> json:
        """Method sendInstantInvitation sends invitation personal message(IM) to the selected contact from the contact
        list with description and comments on channel_id."""

        # Action
        status, result = self.u.sendInstantInvitation(pk, channel_id,
                                                      "Python invite description", "Python invite comment")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_removeInstantMessages(self, contact_pk: str = CONTACT_PK) -> json:
        """Method removeInstantMessages removes all personal messages(IM) of the selected contact from the contact
        list."""

        # Action
        status, result = self.u.removeInstantMessages(contact_pk)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getMiningInfo(self) -> json:
        """Method getMiningInfo returns statistics value of mining process."""

        # Action
        status, result = self.u.getMiningInfo()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendChannelPicture(self, channel_id: str = "81B8CA0B8E2A5C87C468927953BEB674",
                                pic: str = PICTURE) -> json:
        """Method sendChannelPicture creates and sends message with picture in base64 format"""

        # Action
        status, result = self.u.sendChannelPicture(channel_id, pic, "image.jpg")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    # @unittest.skip("просьба не трогать ушан")
    def test_modifyChannel(self) -> 'reference_number':
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
        status = ""
        result = ""

        # Action
        _, my_channels = self.u.getChannels(filter="", channel_type=2)
        myChannel = ""
        if len(my_channels) < 10:
            _, myChannel = self.u.createChannel(channel_name, description, read_only, read_only_privacy, password,
                                                languages, hash_tags, geo_tag, avatar, hide_in_ui)
            time.sleep(3)  # wait for uchan data base sync process ends
        else:
            myChannel = [channel["channelid"] for channel in my_channels if channel["name"] != "testing_dev"][0]
        if myChannel != "":
            status, result = self.u.modifyChannel(myChannel, "edited on:" + str(datetime.today()), password,
                                                  languages, hash_tags, geo_tag, avatar, hide_in_ui)
        else:
            raise Exception("Cant choose channel for modify")
        self.u.deleteChannel(myChannel, password)  # cleanup step

        # Assertion
        AssertResultIsRefNum(self, status, result)

    # @unittest.skip("просьба не трогать ушан")
    def test_deleteChannel(self) -> 'reference_number':
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

        # Action
        _, my_channels = self.u.getChannels(filter="", channel_type=2)
        myChannel = ""
        if len(my_channels) < 9:
            _, myChannel = self.u.createChannel(channel_name, description, read_only, read_only_privacy, password,
                                                languages, hash_tags, geo_tag, avatar, hide_in_ui)
        else:
            channels_for_del = [channel["channelid"] for channel in my_channels
                                if channel["name"] != "testing_dev" and channel["name"] != "hidden channel"]
            myChannel = channels_for_del[0]
        status, result = self.u.deleteChannel(myChannel, password)  # main action step

        # Assertion
        AssertResultIsTrue(self, status, result)

    def test_getChannelSystemInfo(self) -> json:
        """Method getChannelSystemInfo returns system properties of channels."""

        # Action
        status, result = self.u.getChannelSystemInfo()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_summaryUnsRegisteredNames(self) -> json:
        """Method summaryUnsRegisteredNames returns the list count of uNS names by each day"""

        # Action
        status, result = self.u.summaryUnsRegisteredNames(fromDate="", toDate="")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_requestTreasuryPoSRates(self) -> json:
        """Method requestTreasuryPoSRates makes request to obtain treasury PoS rate data"""

        # Action
        status, result = self.u.requestTreasuryPoSRates()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getTreasuryPoSRates(self) -> json:
        """Method getTreasuryPoSRates returns in Response block the detailed information about treasury PoS rate"""

        # Action
        status, result = self.u.getTreasuryPoSRates()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_requestTreasuryTransactionVolumes(self) -> json:
        """Method requestTreasuryTransactionVolumes makes request to obtain treasury transaction volume data"""

        # Action
        status, result = self.u.requestTreasuryTransactionVolumes()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getTreasuryTransactionVolumes(self) -> json:
        """Method getTreasuryTransactionVolumes returns in Response block the detailed information about treasury
        transaction volume"""

        # Action
        status, result = self.u.getTreasuryTransactionVolumes()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_ucodeEncode(self, contact_pk: str = CONTACT_PK) -> json:
        """Method ucodeEncode returns image of ucode in size_image with public key from hex_code"""

        # Action
        status, result = self.u.ucodeEncode(contact_pk, size_image="200", coder="BASE64", format="JPG")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_ucodeDecode(self, image: str = UCODE) -> json:
        """Method ucodeDecode returns hex public key from image in base64 format."""

        # Action
        status, result = self.u.ucodeDecode(image)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getWebSocketState(self) -> json:
        """Method getWebSocketState returns WSS Notifications state, 0 - disabled or active listening port number."""

        # Action
        status, result = self.u.getWebSocketState()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_setWebSocketState(self) -> json:
        """Method setWebSocketState set WSS Notification state."""

        # Action
        status, result = self.u.setWebSocketState(enabled="true", port="20001")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getContactGroups(self) -> json:
        """Method setContactGroup creates group or transfers selected contact into the group in the contact list.
        The method is called by using the Public Key parameters, which pass the Public Key of the contact (Public Key
        can be recognized by using the getContacts method) and Group Name, which passes the group name for creation or
        transfer (up to 32 symbols). In the Response field the status of completion of the operation is displayed."""

        # Action
        status, result = self.u.getContactGroups()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getContactsByGroup(self) -> json:
        """Method getContactsByGroup returns to the Response field the list of contacts from group with corresponded
        name."""

        # Action
        _, groups = self.u.getContactGroups()
        status, result = self.u.getContactsByGroup(groups[0])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_deleteContactGroup(self) -> json:
        """Method deleteContactGroup delete corresponded group name, all contacts are moved under default group."""

        # Action
        _, groups = self.u.getContactGroups()
        group = list(filter(lambda g:
                            g != "DEV Group™" or
                            g != "██▓▓▒▒░░Вожди░░▒▒▓▓██" or
                            g != "<h1>Отдел тестирования</h1>11111" or
                            g != "MSK Teem" or
                            g != "beta.u.is" or
                            g != "", groups))
        if DEBUG: print("test_deleteContactGroup, group name: " + str(group[0]))
        status, result = self.u.deleteContactGroup(group[0])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getTransfersFromManager(self) -> json:
        """Method getTransfersFromManager returns list of file transfer."""

        # Action
        status, result = self.u.getTransfersFromManager()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getFilesFromManager(self) -> json:
        """Тест проверяет что выполнение запроса getFilesFromManager возвращает список файлов в json формате и ответ
        не является пустым и не содержит сообщения об ошибке"""

        # Action
        status, result = self.u.getFilesFromManager()

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_abortTransfers(self) -> json:
        """Method abortTransfers abort transfer with selected ID."""

        # Action
        _, transfers = self.u.getTransfersFromManager()
        tr_id = ""
        try:
            active_transfers = [t["transferId"] for t in transfers if t["percentCompleted"] < 100]
            tr_id = active_transfers[0]
        except:
            tr_id = transfers[0]["transferId"]

        status, result = self.u.abortTransfers(tr_id)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_hideTransfers(self) -> json:
        """Method hideTransfers hide transfer with selected ID."""

        # Action
        _, transfers = self.u.getTransfersFromManager()
        tr_id = ""
        try:
            active_transfers = [t["transferId"] for t in transfers if t["percentCompleted"] < 100]
            tr_id = active_transfers[0]
        except:
            tr_id = transfers[0]["transferId"]

        status, result = self.u.hideTransfers(tr_id)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getFile(self) -> json:
        """Method getFile return file with selected ID."""

        # Action
        _, files = self.u.getFilesFromManager()
        status, result = self.u.getFile(files[0]["id"])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_deleteFile(self):
        # Action
        _, files = self.u.getFilesFromManager()
        status, result = self.u.deleteFile(files[0]["id"])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_sendFileByMessage(self, pk: str = CONTACT_PK) -> json:
        """Method sendFileByMessage send file with selected address."""

        # Action
        _, files = self.u.getFilesFromManager()
        status, result = self.u.sendFileByMessage(pk, files[0]["id"])

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_getChannelBannedContacts(self, channel_id: str = CHANNEL_ID) -> json:
        """Method getChannelBannedContacts returns list banned contacts on corresponded channel with id channelid."""

        # Action
        status, result = self.u.getChannelBannedContacts(channel_id)

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_applyChannelBannedContacts(self, channel_id: str = CHANNEL_ID, pk: str = CONTACT_PK) -> json:
        """
        Method applyChannelBannedContacts apply and send new banned list for corresponded channel with id channelid.
        """

        # Action
        self.u.applyChannelBannedContacts(channel_id, "[" + pk + "]")
        status, result = self.u.applyChannelBannedContacts(channel_id, "[]")  # clear ban list

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_uploadFile(self, pic: str = PICTURE) -> str:
        """Method uploadFile upload data in base64 format and returns id of new file."""

        # Action
        status, result = self.u.uploadFile(pic, "Дулин.png")

        # Assertion
        AssertNotEmptyOrError(self, status, result)

    def test_acceptAttachment(self) -> bool:
        """Тест проверяет возможность ододрить загружку вложенных во входящее письмо файлов.
        Сначала получаем список всех входящих писем, потом отбираем из них те, у которых есть attachments со статусом
        waiting. Потом берём id этого письма и id аттача и вызываем метод
        acceptAttachment чтобы загрузить вложение. Далее проверяем что пришло в ответ в result."""

        # Action
        _, all_incoming_umails = self.u.getEmails(1, "")
        umails_with_attach = [umail for umail in all_incoming_umails if 'attachments' in umail.keys()]

        if len(umails_with_attach) > 0:
            ids = [[umail['id'], attach['id']] for umail in umails_with_attach
                   for attach in umail['attachments'] if attach['status'] == 'waiting']

            status, result = self.u.acceptAttachment(ids[0][0], ids[0][1])
            AssertResultIsTrue(self, status, result)
        else:
            raise Exception("There is no incoming emails with attachments")

    def test_abortAttachment(self) -> bool:
        """Тест проверяет возможность отменить загружку вложенных во входящее письмо файлов.
        Сначала получаем список всех входящих писем, потом отбираем из них те, у которых есть attachments.
        Если их больше нуля, то отбираем со статусом waiting. Берём id этого письма и id аттача и вызываем метод
        abortAttachment чтобы отменить загрузку вложения. Далее проверяем что пришло в ответ в result."""

        # Action
        _, all_incoming_umails = self.u.getEmails(1, "")
        umails_with_attach = [umail for umail in all_incoming_umails if 'attachments' in umail.keys()]

        if len(umails_with_attach) > 0:
            ids = [[umail['id'], attach['id']] for umail in umails_with_attach
                   for attach in umail['attachments'] if attach['status'] == 'waiting']

            status, result = self.u.abortAttachment(ids[0][0], ids[0][1])
            AssertResultIsTrue(self, status, result)
        else:
            raise Exception("There is no incoming emails with attachments")

    @classmethod
    def tearDownClass(cls):
        report = ""
        with open(report_file, "r") as f:
            for row in f:
                report = report + "\n" + str(row)
        cls.u.sendEmailMessage(report_recipients, "Test Failures Report", report)


if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult))
