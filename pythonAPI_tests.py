import unittest
import json
import time
import re
import api
import settings

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
    pattern = re.compile("^([A-Z0-9]){64}")
    getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", "startDateTime": "", "endDateTime": "", "referenceNumber": "" }'
    
    def setUp(self):        
        self.status = False

    def test_getSystemInfo(self):
        self.status, self.result = self.u.getSystemInfo()

    def test_getBalance(self):
        self.status, self.result = self.u.getBalance()

    def test_getCards(self):
        self.status, self.result = self.u.getCards()

    def test_getVouchers(self):
        self.status, self.result = self.u.getVouchers()

    def test_getInvoices(self):
        self.status, self.result = self.u.getInvoices(self.getInvoicesParams)

    def test_getProfileStatus(self):
        self.status, self.result = self.u.getProfileStatus()

    def test_getContacts(self):
        self.status, self.result = self.u.getContacts("")

    def test_getContactAvatar(self):
        self.status, self.result = self.u.getContactAvatar(settings.CONTACT_PK, "BASE64", "JPG")

    def test_sendInstantMessage(self):
        self.status = self.u.sendInstantMessage(settings.CONTACT_PK, "API method sendInstantMessage testing \n ======================= \n Python unittest")
        
    def test_sendEmailMessage(self):
        self.status = self.u.sendEmailMessage([settings.CONTACT_PK], "This is a Python api subject", "This is a Python api body")

    def test_sendPaymentToPk(self):
        s, result = self.u.sendPayment(settings.CONTACT_PK, "payment from pk to pk", "", 0.001)
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result

    def test_sendPaymentToCard(self):
        s, result = self.u.sendPayment(settings.CONTACT_CARD, "payment from pk to card", "", 0.002)
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result

    def test_sendPaymentFromCard(self):
        s, result = self.u.sendPayment(settings.contactPk, "payment from card to pk", settings.SELF_CARD,  0.003)
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result

    def test_createVoucher(self):
        s, result = self.u.createVoucher(10)
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result

    def test_useVoucher(self):
        s, vouchers = self.u.getVouchers()        
        if(len(vouchers) == 0 or 'error' in vouchers):
            s, result = self.u.createVoucher(10)
            time.sleep(3)
            s, vouchers = self.u.getVouchers()
        self.status, result = self.u.useVoucher(vouchers[0]["voucherid"])
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result
        
    def test_deleteVoucher(self):
        s, result = self.u.getVouchers()
        if(len(result) == 0):
            status, result = self.u.createVoucher(10)
            time.sleep(3)
            s, result = self.u.getVouchers()        
        self.status, result = self.u.deleteVoucher(result[0]["voucherid"])
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result
    
    def test_sendInvoice(self):
        s, result = self.u.sendInvoice("sendInvoice to contact card", settings.CONTACT_CARD, 10)
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result

    def test_getInvoiceByReferenceNumber(self):
        s, invoices = self.u.getFinanceHistory("ALL_REQUESTS", "", "", "", "", "", "")
        if(len(invoices) > 0 and not 'error' in invoices):
            self.status, self.result = self.u.getInvoiceByReferenceNumber(invoices[0]['referenceNumber'])
        else:
            raise Exception("There is no invoices or got error on request")

    def test_getTransactionIdByReferenceNumber(self):
        s, transactions = self.u.getFinanceHistory("ALL_TRANSACTIONS", "", "", "", "", "", "")
        if(len(transactions) > 0 and not 'error' in transactions):
            self.status, self.result = self.u.getTransactionIdByReferenceNumber(transactions[0]['referenceNumber'])
        else:
            raise Exception("There is no transactions or got error on request")

    def test_acceptInvoice(self):
        # костыль
        s, invoices = self.u.getInvoices(self.getInvoicesParams)
        incoming_invoices = list(filter(lambda x: x['direction'] == "Incoming", invoices))
        if(len(incoming_invoices) > 0 and not 'error' in incoming_invoices):
            s, result = self.u.acceptInvoice(incoming_invoices[0]['invoiceid'])
            if (self.pattern.match(str(result)) == None):
                self.status = False
                print("Result '" + str(result) + "' is not reference number")
            else:
                self.status = True
                self.result = result
        else:
            raise Exception("There is no incoming invoices or got error on request")
        
    def test_cancelInvoice(self):
        self.status, invoice_ref_numbr = self.u.sendInvoice("API request", settings.CONTACT_CARD,10)
        self.status, invoice = self.u.getInvoiceByReferenceNumber(invoice_ref_numbr)
        self.status = self.u.cancelInvoice(invoice['invoiceid'])

    def test_declineInvoice(self):
        s, invoices = self.u.getInvoices(self.getInvoicesParams)
        incoming_invoices = list(filter(lambda x: x['direction'] == "Incoming", invoices))
        if(len(incoming_invoices) > 0 and not 'error' in incoming_invoices):
            # result should contains reference number for decline invoice transaction
            s, result = self.u.declineInvoice(incoming_invoices[0]['invoiceid'])
            if (self.pattern.match(str(result)) == None):
                self.status = False
                print("Result '" + str(result) + "' is not reference number")
            else:
                self.status = True
                self.result = result
        else:
            raise Exception("There is no incoming invoices or got error on request")

    def test_getChannels(self):
        self.status, self.result = self.u.getChannels("1", 0)

    def test_sendChannelMessage(self):
        self.status = self.u.sendChannelMessage(settings.CHANNEL_ID, "Message from Python api test")

    def test_leaveChannel(self):
        self.status = self.u.leaveChannel(settings.CHANNEL_ID)
        s = self.u.joinChannel(settings.CHANNEL_ID, settings.CHANNEL_PWD)

    def test_joinChannel(self):
        self.status = self.u.joinChannel(settings.CHANNEL_ID, settings.CHANNEL_PWD)

    def test_deleteContact(self):
        self.status = self.u.deleteContact(settings.CONTACT_PK)
        s = self.u.sendAuthorizationRequest(settings.CONTACT_PK, "autotest request")
        s = self.u.acceptAuthorizationRequest(settings.CONTACT_PK, "autotest accept request")

    def test_sendAuthorizationRequest(self):
        self.status = self.u.sendAuthorizationRequest(settings.CONTACT_PK, "autotest request")    

    def test_rejectAuthorizationRequest(self):
        self.status = self.u.rejectAuthorizationRequest(settings.CONTACT_PK, "autotest reject request")
        s = self.u.sendAuthorizationRequest(settings.CONTACT_PK, "autotest request")
        s = self.u.acceptAuthorizationRequest(settings.CONTACT_PK, "autotest accept request")

    def test_acceptAuthorizationRequest(self):
        self.status = self.u.acceptAuthorizationRequest(settings.CONTACT_PK, "autotest accept request")

    def test_getUnsSyncInfo(self):
        self.status, self.result = self.u.getUnsSyncInfo()

    def test_unsCreateRecordRequest(self):
        s, result = self.u.unsCreateRecordRequest(settings.random_uns, "2100-07-20", "false", "")
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result

    def test_unsDeleteRecordRequest(self):
        s, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and not 'error' in unss:
            s, result = self.u.unsDeleteRecordRequest(unss[-1]["nick"])
            if (self.pattern.match(str(result)) == None):
                raise Exception("Result '" + str(result) + "' is not reference number")
            else:
                self.status = True
                self.result = result
        else:
            raise Exception("There is no UNS, or got error on request")

    def test_unsSearchByPk(self):
        self.status, self.result = self.u.unsSearchByPk(settings.CONTACT_PK)

    def test_unsSearchByNick(self):
        self.status, self.result = self.u.unsSearchByNick(settings.CONTACT_NAME)

    def test_unsRegisteredNames(self):
        self.status, self.result = self.u.unsRegisteredNames()

    def test_unsModifyRecordRequest(self):
        s, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and not 'error' in unss:
            self.status, result = self.u.unsModifyRecordRequest(unss[-1]['nick'], "2100-07-20", False, "")
            if (self.pattern.match(str(result)) == None):
                raise Exception("Result '" + str(result) + "' is not reference number")
            else:
                self.status = True
                self.result = result
        else:
            raise Exception("There is no UNS, or got error on request")

    def test_setContactGroup(self):
        self.status = self.u.setContactGroup(settings.CONTACT_PK, "PyAPI")

    def test_setContactNick(self):
        self.status = self.u.setContactNick(settings.CONTACT_PK, settings.CONTACT_NAME)

    def test_getEmailFolder(self):
        self.status, self.result = self.u.getEmailFolder(1, "")

    def test_getEmailById(self):
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status, self.result = self.u.getEmailById(emails[0])
        else:
            raise Exception("There is no emails, or got error on request")

    def test_deleteEmail(self):
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status, self.result = self.u.deleteEmail(emails[-1])
        else:
            raise Exception("There is no emails, or got error on request")

    def test_clearTrayNotifications(self):
        self.status = self.u.clearTrayNotifications()

    def test_getContactMessages(self):
        self.status, self.result = self.u.getContactMessages(settings.contactPk)

    def test_sendReplyEmailMessage(self):
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status = self.u.sendReplyEmailMessage(emails[-1], "This is a Reply email by Python API test")
        else:
            raise Exception("There is no emails, or got error on request")

    def test_sendForwardEmailMessage(self):
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status = self.u.sendForwardEmailMessage(emails[-1], "This is a Forward email by Python API test", settings.CONTACT_PK)
        else:
            raise Exception("There is no emails, or got error on request")

    def test_getFinanceHistory(self):
        self.status, self.result = self.u.getFinanceHistory("ALL_TRANSACTIONS", "", "", "" , "" , "" , "")

    def test_requestUnsTransfer(self):
        self.status, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and not 'error' in unss:
            self.status = self.u.requestUnsTransfer(unss[-1], settings.CONTACT_PK)
        else:
            self.u.unsCreateRecordRequest(settings.random_uns)
            self.status, unss = self.u.unsRegisteredNames()
            self.status = self.u.requestUnsTransfer(unss[-1], settings.CONTACT_PK)

    def test_incomingUnsTransfer(self):
        self.status, self.result = self.u.incomingUnsTransfer()

    def test_acceptUnsTransfer(self):
        self.status, incoming_unses = self.u.incomingUnsTransfer()
        if (len(incoming_unses) > 0 and not 'error' in incoming_unses):
            self.status = self.u.acceptUnsTransfer(incoming_unses[0]['id'])
        else:
            raise Exception("There is no incoming UNS transfers")

    def test_declineUnsTransfer(self):
        self.status, incoming_unses = self.u.incomingUnsTransfer()
        if (len(incoming_unses) > 0 and not 'error' in incoming_unses):
            self.status = self.u.declineUnsTransfer(incoming_unses[0]['id'])
        else:
            raise Exception("There is no incoming UNS transfers")

    def test_outgoingUnsTransfer(self):
        self.status, self.result = self.u.outgoingUnsTransfer()

    def test_getNetworkConnections(self):
        self.status, self.result = self.u.getNetworkConnections()

    def test_getProxyMappings(self):
        self.status, self.result = self.u.getProxyMappings()

    def test_createProxyMapping(self):
        self.status, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and not 'error' in unss:
            self.status = self.u.createProxyMapping(unss[0]["nick"], "80", "81.19.72.36", "80", "true")
        else:
            raise Exception("There is no UNS records, or got error on request")

    def test_enableProxyMapping(self):
        self.status, proxy_mapings = self.u.getProxyMappings()
        if len(proxy_mapings) > 0 and not 'error' in proxy_mapings:
            self.status = self.u.enableProxyMapping(proxy_mapings[0]['id'])
        else:
            raise Exception("There is no mapings or got error on request")

    def test_disableProxyMapping(self):
        self.status, proxy_mapings = self.u.getProxyMappings()
        if len(proxy_mapings) > 0 and not 'error' in proxy_mapings:
            self.status = self.u.disableProxyMapping(proxy_mapings[0]['id'])
        else:
            raise Exception("There is no mapings or got error on request")

    def test_removeProxyMapping(self):
        self.status, proxy_mapings = self.u.getProxyMappings()
        if len(proxy_mapings) > 0 and not 'error' in proxy_mapings:
            self.status = self.u.removeProxyMapping(proxy_mapings[0]['id'])
        else:
            raise Exception("There is no mapings or got error on request")

    def test_addCard(self):
        self.status, result = self.u.addCard("#FBEDC0","API card", "")
        if (self.pattern.match(str(result)) == None):
            raise Exception("Result '" + str(result) + "' is not reference number")
        else:
            self.status = True
            self.result = result

    def test_deleteCard(self):
        s, cards = self.u.getCards()
        if len(cards) > 0 and not 'error' in cards:
            card = list(filter(lambda x: x['name'] == 'API card', cards))
            if len(card) == 0:                
                self.u.addCard("#FBEDC0","API card", "")
                time.sleep(1)
                self.status, cards = self.u.getCards()
                card = list(filter(lambda x: x['name'] == 'API card', cards))                
            self.status, self.result = self.u.deleteCard(card[0]['cardid'])

    def test_getFinanceSystemInformation(self):
        self.status, self.result = self.u.getFinanceSystemInformation()

    def test_getMiningBlocks(self):
        self.status, self.result = self.u.getMiningBlocks()

    def test_enableMining(self):
        self.status = self.u.enableMining("true")

    def test_enableInterest(self):
        self.status = self.u.enableInterest("true")

    def test_enableHistoryMining(self):
        self.status = self.u.enableHistoryMining("true")

    def test_statusHistoryMining(self):
        self.status, self.result = self.u.statusHistoryMining()

    def test_lowTrafficMode(self):
        self.status, self.result = self.u.lowTrafficMode()

    def test_setLowTrafficMode(self):
        self.status = self.u.setLowTrafficMode('false')

    def test_getWhoIsInfo(self):
        self.status, self.result = self.u.getWhoIsInfo(settings.CONTACT_PK)

    def test_getChannelInfo(self):
        self.status, self.result = self.u.getChannelInfo(settings.CHANNEL_ID)

    def test_getChannelModerators(self):
        self.status, self.result = self.u.getChannelModerators(settings.CHANNEL_ID)

    def test_getChannelModeratorRight(self):
        self.status, moderators = self.u.getChannelModerators(settings.CHANNEL_ID)
        if len(moderators) > 0 and not 'error' in moderators:
            self.status, self.result = self.u.getChannelModeratorRight(settings.CHANNEL_ID, moderators[0])
        else:
            raise Exception("There is no moderators or error on request")

    def test_setProfileStatus(self):
        self.status = self.u.setProfileStatus("Available", "QA Engineer")

    def test_getEmails(self):
        self.status, self.result = self.u.getEmails(1, "")

    def test_getChannelMessages(self):
        #self.status, self.result = self.u.getChannelMessages("B4EF14CFE2782C1E94E82631F9B782E2")
        self.status, self.result = self.u.getChannelMessages(settings.CHANNEL_ID)

    @unittest.skip("просьба не трогать ушан")
    def test_createChannel(self):
        s, myChannel = self.u.createChannel("Test Channel |+_)(*&^%$#@!~", "description _)(*?:%;№", "false", "", "", "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x", "10.000, 20.000", "")
        s, self.result = self.u.deleteChannel(myChannel)        
        if self.pattern.match(str(myChannel)) != None:
            self.status = s
        else:
            raise Exception("Result: '" + str(self.result) + "'")

    def test_getOwnContact(self):
        self.status, self.result = self.u.getOwnContact()

    def test_getChannelAvatar(self):
        self.status, self.result = self.u.getChannelAvatar(settings.CHANNEL_ID, "BASE64", "JPG")

    def test_sendInstantQuote(self):
        s, contact_msgs = self.u.getContactMessages(settings.CONTACT_PK)
        if len(contact_msgs) == 0:
            self.test_sendInstantMessage()
            s, contact_msgs = self.u.getContactMessages(settings.CONTACT_PK)
        self.status, self.result = self.u.sendInstantQuote(settings.CONTACT_PK, "this is python unittest quote message", contact_msgs[0]["id"])

    def test_getStickerCollections(self):
        self.status, self.result = self.u.getStickerCollections()

    def test_getStickerNamesByCollection(self):
        s, sticker_collection = self.u.getStickerCollections()
        self.status, self.result = self.u.getStickerNamesByCollection(sticker_collection[0])

    def test_getImageSticker(self):
        s, sticker_collection = self.u.getStickerCollections()
        s, all_stickers = self.u.getStickerNamesByCollection(sticker_collection[0])
        self.status, self.result = self.u.getImageSticker(sticker_collection[0], all_stickers[0], "BASE64")

    def test_sendInstantSticker(self):
        s, sticker_collection = self.u.getStickerCollections()
        s, all_stickers = self.u.getStickerNamesByCollection(sticker_collection[0])
        self.status, self.result = self.u.sendInstantSticker(settings.CONTACT_PK, sticker_collection[0], all_stickers[0])

    def test_sendInstantBuzz(self):
        self.status, self.result = self.u.sendInstantBuzz(settings.CONTACT_PK, "Python Buzz")

    def test_sendInstantInvitation(self):
        self.status, self.result = self.u.sendInstantInvitation(settings.CONTACT_PK, settings.CHANNEL_ID, "Python invite description", "Python invite comment")

    def test_removeInstantMessages(self):
        self.status, self.result = self.u.removeInstantMessages(settings.CONTACT_PK)

    def test_getMiningInfo(self):
        self.status, self.result = self.u.getMiningInfo()

    def test_sendChannelPicture(self):
        self.status, self.result = self.u.sendChannelPicture(settings.CHANNEL_ID, settings.PICTURE, "image.jpg")

    #@unittest.skip("просьба не трогать ушан")
    def test_modifyChannel(self):
        s, my_channels = self.u.getChannels("", 2)
        myChannel = ""
        if len(my_channels) < 3:
            s, myChannel = self.u.createChannel("Test Channel |+_)(*&^%$#@!~", "description _)(*?:%;№", "false", "", "", "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x", "10.000, 20.000", "")
        else:
            for channel in my_channels:
                if channel["name"] != "testing_dev" or channel["name"] != "hidden channel":
                    myChannel = channel["ident"]
        self.status, self.result = self.u.modifyChannel(myChannel)
        s, r = self.u.deleteChannel(myChannel)
    
    #@unittest.skip("просьба не трогать ушан")
    def test_deleteChannel(self):
        s, my_channels = self.u.getChannels("", 2)
        myChannel = ""
        if len(my_channels) < 3:
            s, myChannel = self.u.createChannel("Test Channel |+_)(*&^%$#@!~", "description _)(*?:%;№", "false", "", "", "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x", "10.000, 20.000", "")
        else:
            for channel in my_channels:
                if channel["name"] != "testing_dev" or channel["name"] != "hidden channel":
                    myChannel = channel["ident"]
        self.status, self.result = self.u.deleteChannel(myChannel)

    def test_getChannelSystemInfo(self):
        self.status, self.result = self.u.getChannelSystemInfo()

    def test_summaryUnsRegisteredNames(self):
        self.status, self.result = self.u.summaryUnsRegisteredNames("", "")

    def test_requestTreasuryInterestRates(self):
        self.status, self.result = self.u.requestTreasuryInterestRates()

    def test_getTreasuryInterestRates(self):
        self.status, self.result = self.u.getTreasuryInterestRates()

    def test_requestTreasuryTransactionVolumes(self):
        self.status, self.result = self.u.requestTreasuryTransactionVolumes()

    def test_getTreasuryTransactionVolumes(self):
        self.status, self.result = self.u.getTreasuryTransactionVolumes()

    def test_ucodeEncode(self):
        self.status, self.result = self.u.ucodeEncode(settings.CONTACT_PK, "200", "BASE64", "JPG")

    def test_ucodeDecode(self):
        self.status, self.result = self.u.ucodeDecode(settings.UCODE)

    def test_getWebSocketState(self):
        self.status, self.result = self.u.getWebSocketState()

    def test_setWebSocketState(self):
        self.status, self.result = self.u.setWebSocketState("true", "20001")

    def tearDown(self):
        try:
            self.assertFalse('error' in str(self.result))
        except Exception:
            time.sleep(0.001)
        self.assertTrue(bool(self.status), "Status of request execution is False")


if __name__ == "__main__":
    #unittest.main()
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult))
