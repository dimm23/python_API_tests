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
    
    #def setUp(self):        
    #    self.status = False

    def test_getSystemInfo(self):
        # Action
        self.status, self.result = self.u.getSystemInfo()
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getBalance(self):
        # Action
        self.status, self.result = self.u.getBalance()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getCards(self):
        # Action
        self.status, self.result = self.u.getCards()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getVouchers(self):
        # Action
        self.status, self.result = self.u.getVouchers()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getInvoices(self):
        # Action
        self.status, self.result = self.u.getInvoices(self.getInvoicesParams)

         # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getProfileStatus(self):
        # Action
        self.status, self.result = self.u.getProfileStatus()

         # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getContacts(self):
        # Action
        self.status, self.result = self.u.getContacts("")

         # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getContactAvatar(self):
        # Action
        self.status, self.result = self.u.getContactAvatar(settings.CONTACT_PK, "BASE64", "JPG")

         # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendInstantMessage(self):
        # Action
        self.status, self.result = self.u.sendInstantMessage(settings.CONTACT_PK, "API method sendInstantMessage testing \n ======================= \n Python unittest")
        
         # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendEmailMessage(self):
        # Actual
        self.status, self.result = self.u.sendEmailMessage([settings.CONTACT_PK], "This is a Python api subject", "This is a Python api body")

         # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendPaymentToPk(self):
        # Action
        self.status, result = self.u.sendPayment(settings.CONTACT_PK, "payment from pk to pk", "", 0.001)
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")            

    def test_sendPaymentToCard(self):
        # Action
        self.status, result = self.u.sendPayment(settings.CONTACT_CARD, "payment from pk to card", "", 0.002)
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")    

    def test_sendPaymentFromCard(self):
        # Action
        self.status, result = self.u.sendPayment(settings.CONTACT_PK, "payment from card to pk", settings.SELF_CARD,  0.003)
        
        # Assertion
        self.assertTrue(self.status, "Status: " + str(self.status))
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")    

    def test_createVoucher(self):
        # Action
        self.status, result = self.u.createVoucher(10)
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")    

    def test_useVoucher(self):
        # SetUp
        s, vouchers = self.u.getVouchers()        
        if(len(vouchers) == 0 or 'error' in vouchers):
            s, result = self.u.createVoucher(10)
            time.sleep(3)
            s, vouchers = self.u.getVouchers()

        # Action
        self.status, result = self.u.useVoucher(vouchers[0]["voucherid"])
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")    
        
    def test_deleteVoucher(self):
        # SetUp
        s, result = self.u.getVouchers()
        if(len(result) == 0):
            status, result = self.u.createVoucher(10)
            time.sleep(3)
            s, result = self.u.getVouchers()  
            
        # Action
        self.status, result = self.u.deleteVoucher(result[0]["voucherid"])
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")    
    
    def test_sendInvoice(self):
        # Action
        self.status, result = self.u.sendInvoice("sendInvoice to contact card", settings.CONTACT_CARD, 10)
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_getInvoiceByReferenceNumber(self):
        # Action
        s, invoices = self.u.getFinanceHistory("ALL_REQUESTS", "", "", "", "", "", "")
        if(len(invoices) > 0 and not 'error' in invoices):
            self.status, self.result = self.u.getInvoiceByReferenceNumber(invoices[0]['referenceNumber'])
        else:
            raise Exception("There is no invoices or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getTransactionIdByReferenceNumber(self):
        # Action
        s, transactions = self.u.getFinanceHistory("ALL_TRANSACTIONS", "", "", "", "", "", "")
        if(len(transactions) > 0 and not 'error' in transactions):
            self.status, self.result = self.u.getTransactionIdByReferenceNumber(transactions[0]['referenceNumber'])
        else:
            raise Exception("There is no transactions or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_acceptInvoice(self):
        # Action
        ## костыль
        s, invoices = self.u.getInvoices(self.getInvoicesParams)
        incoming_invoices = list(filter(lambda x: x['direction'] == "Incoming", invoices))
        if(len(incoming_invoices) > 0 and not 'error' in incoming_invoices):
            self.status, result = self.u.acceptInvoice(incoming_invoices[0]['invoiceid'])             
        else:
            raise Exception("There is no incoming invoices or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")
        
    def test_cancelInvoice(self):
        # Action
        s, invoice_ref_numbr = self.u.sendInvoice("API request", settings.CONTACT_CARD,10)
        time.sleep(3)
        s, invoice = self.u.getInvoiceByReferenceNumber(invoice_ref_numbr)
        self.status, result = self.u.cancelInvoice(invoice['invoiceid'])

        # Assertion
        self.assertTrue(self.status, str(self.status))
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_declineInvoice(self):
        # Action
        s, invoices = self.u.getInvoices(self.getInvoicesParams)
        incoming_invoices = list(filter(lambda x: x['direction'] == "Incoming", invoices))
        if(len(incoming_invoices) > 0 and not 'error' in incoming_invoices):
            # result should contains reference number for decline invoice transaction
            self.status, result = self.u.declineInvoice(incoming_invoices[0]['invoiceid'])            
        else:
            raise Exception("There is no incoming invoices or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_getChannels(self):
        # Action
        self.status, self.result = self.u.getChannels("1", 0)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendChannelMessage(self):
        # Action
        self.status, self.result = self.u.sendChannelMessage(settings.CHANNEL_ID, "Message from Python api test")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_leaveChannel(self):
        # Action
        self.status, self.result = self.u.leaveChannel(settings.CHANNEL_ID)
        s = self.u.joinChannel(settings.CHANNEL_ID, settings.CHANNEL_PWD)

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_joinChannel(self):
        # Action
        self.status, self.result = self.u.joinChannel(settings.CHANNEL_ID, settings.CHANNEL_PWD)

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_deleteContact(self):
        # Action
        self.status, self.result = self.u.deleteContact(settings.CONTACT_PK)
        s = self.u.sendAuthorizationRequest(settings.CONTACT_PK, "autotest request")
        s = self.u.acceptAuthorizationRequest(settings.CONTACT_PK, "autotest accept request")

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_sendAuthorizationRequest(self):
        # Action
        self.status, self.result = self.u.sendAuthorizationRequest(settings.CONTACT_PK, "autotest request")    

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_rejectAuthorizationRequest(self):
        # Action
        self.status, self.result = self.u.rejectAuthorizationRequest(settings.CONTACT_PK, "autotest reject request")
        s = self.u.sendAuthorizationRequest(settings.CONTACT_PK, "autotest request")
        s = self.u.acceptAuthorizationRequest(settings.CONTACT_PK, "autotest accept request")

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_acceptAuthorizationRequest(self):
        # Action
        self.status, self.result = self.u.acceptAuthorizationRequest(settings.CONTACT_PK, "autotest accept request")

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_getUnsSyncInfo(self):
        # Action
        self.status, self.result = self.u.getUnsSyncInfo()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_unsCreateRecordRequest(self):
        # Action
        self.status, result = self.u.unsCreateRecordRequest(settings.random_uns, "2100-07-20", "false", "")
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_unsDeleteRecordRequest(self):
        s, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and not 'error' in unss:
            self.status, result = self.u.unsDeleteRecordRequest(unss[-1]["nick"])
            
            # Assertion
            self.assertTrue(self.status)
            self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")
        else:
            raise Exception("There is no UNS, or got error on request")

    def test_unsSearchByPk(self):
        # Action
        self.status, self.result = self.u.unsSearchByPk(settings.CONTACT_PK)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_unsSearchByNick(self):
        # Action
        self.status, self.result = self.u.unsSearchByNick(settings.CONTACT_NAME)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_unsRegisteredNames(self):
        # Action
        self.status, self.result = self.u.unsRegisteredNames()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_unsModifyRecordRequest(self):
        # Actions
        s, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and not 'error' in unss:
            self.status, result = self.u.unsModifyRecordRequest(unss[-1]['nick'], "2100-07-20", False, "")
            
            # Assertion
            self.assertTrue(self.status)
            self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")
        else:
            raise Exception("There is no UNS, or got error on request")

    def test_setContactGroup(self):
        # Action
        self.status, self.result = self.u.setContactGroup(settings.CONTACT_PK, "PyAPI")

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_setContactNick(self):
        # Action
        self.status, self.result = self.u.setContactNick(settings.CONTACT_PK, settings.CONTACT_NAME)

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_getEmailFolder(self):
        # Action
        self.status, self.result = self.u.getEmailFolder(1, "")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getEmailById(self):
        # Action
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status, self.result = self.u.getEmailById(emails[0])
        else:
            raise Exception("There is no emails, or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_deleteEmail(self):
        # Action
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status, self.result = self.u.deleteEmail(emails[-1])
        else:
            raise Exception("There is no emails, or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_clearTrayNotifications(self):
        # Action
        self.status, self.result = self.u.clearTrayNotifications()

        # Assert
        self.assertTrue(self.status)
        self.assertTrue(self.result)

    def test_getContactMessages(self):
        # Action
        self.status, self.result = self.u.getContactMessages(settings.CONTACT_PK)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendReplyEmailMessage(self):
        # Action
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status, self.result = self.u.sendReplyEmailMessage(emails[-1], "This is a Reply email by Python API test", "This is a python api test")
        else:
            raise Exception("There is no emails, or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendForwardEmailMessage(self):
        # Action
        self.status, emails = self.u.getEmailFolder(1, "")
        if len(emails) > 0 and not 'error' in emails:
            self.status, self.result = self.u.sendForwardEmailMessage(emails[-1], settings.CONTACT_PK, "This is a Forward email by Python API test", "This is a Python api test")
        else:
            raise Exception("There is no emails, or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getFinanceHistory(self):
        # Action
        self.status, self.result = self.u.getFinanceHistory("ALL_TRANSACTIONS", "", "", "" , "" , "" , "")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_requestUnsTransfer(self):
        # Action
        self.status, unss = self.u.unsRegisteredNames()
        time.sleep(1)
        if len(unss) > 0 and not 'error' in unss:
            self.status, self.result = self.u.requestUnsTransfer(unss[-1], settings.CONTACT_PK)
        else:
            self.u.unsCreateRecordRequest(settings.random_uns)
            self.status, unss = self.u.unsRegisteredNames()
            self.status, self.result = self.u.requestUnsTransfer(unss[-1], settings.CONTACT_PK)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_incomingUnsTransfer(self):
        # Action
        self.status, self.result = self.u.incomingUnsTransfer()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_acceptUnsTransfer(self):
        # Action
        self.status, incoming_unses = self.u.incomingUnsTransfer()
        if (len(incoming_unses) > 0 and not 'error' in incoming_unses):
            self.status, result = self.u.acceptUnsTransfer(incoming_unses[0]['id'])
        else:
            raise Exception("There is no incoming UNS transfers")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_declineUnsTransfer(self):
        # Action
        self.status, incoming_unses = self.u.incomingUnsTransfer()
        if (len(incoming_unses) > 0 and not 'error' in incoming_unses):
            self.status, result = self.u.declineUnsTransfer(incoming_unses[0]['id'])
        else:
            raise Exception("There is no incoming UNS transfers")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_outgoingUnsTransfer(self):
        # Action
        self.status, self.result = self.u.outgoingUnsTransfer()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getNetworkConnections(self):
        # Action
        self.status, self.result = self.u.getNetworkConnections()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getProxyMappings(self):
        # Action
        self.status, self.result = self.u.getProxyMappings()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_createProxyMapping(self):
        # Action
        self.status, unss = self.u.unsRegisteredNames()
        if len(unss) > 0 and not 'error' in unss:
            self.status, self.result = self.u.createProxyMapping(unss[0]["nick"], "80", "81.19.72.36", "80", "true")
        else:
            raise Exception("There is no UNS records, or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_enableProxyMapping(self):
        # Action
        self.status, proxy_mapings = self.u.getProxyMappings()
        if len(proxy_mapings) > 0 and not 'error' in proxy_mapings:
            self.status, self.result = self.u.enableProxyMapping(proxy_mapings[0]['id'])
        else:
            raise Exception("There is no mapings or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_disableProxyMapping(self):
        # Action
        self.status, proxy_mapings = self.u.getProxyMappings()
        if len(proxy_mapings) > 0 and not 'error' in proxy_mapings:
            self.status, self.result = self.u.disableProxyMapping(proxy_mapings[0]['id'])
        else:
            raise Exception("There is no mapings or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_removeProxyMapping(self):
        # Action
        self.status, proxy_mapings = self.u.getProxyMappings()
        if len(proxy_mapings) > 0 and not 'error' in proxy_mapings:
            self.status, self.result = self.u.removeProxyMapping(proxy_mapings[0]['id'])
        else:
            raise Exception("There is no mapings or got error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_addCard(self):
        # Action
        self.status, result = self.u.addCard("#FBEDC0","API card", "")
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_deleteCard(self):
        # Action
        s, cards = self.u.getCards()
        result = ""
        if len(cards) > 0 and not 'error' in cards:
            card = list(filter(lambda x: x['name'] == 'API card', cards))
            if len(card) == 0:                
                self.u.addCard("#FBEDC0","API card", "")
                time.sleep(3)
                self.status, cards = self.u.getCards()
                card = list(filter(lambda x: x['name'] == 'API card', cards))
            try:
                self.status, result = self.u.deleteCard(card[0]['cardid'])
            except Exception as e:
                print(e)
            finally:
                # Assertion
                self.assertTrue(self.status)
                self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_getFinanceSystemInformation(self):
        # Action
        self.status, self.result = self.u.getFinanceSystemInformation()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getMiningBlocks(self):
        # Action
        self.status, self.result = self.u.getMiningBlocks()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_enableMining(self):
        # Action
        self.status, self.result = self.u.enableMining("true")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result, str(self.result))

    def test_enablePoS(self):
        # Action
        self.status, self.result = self.u.enablePoS("true")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result, str(self.result))

    def test_enableHistoryMining(self):
        # Action
        self.status, self.result = self.u.enableHistoryMining("true")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result, str(self.result))

    def test_statusHistoryMining(self):
        # Action
        self.status, self.result = self.u.statusHistoryMining()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_lowTrafficMode(self):
        # Action
        self.status, self.result = self.u.lowTrafficMode()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_setLowTrafficMode(self):
        # Action
        self.status, self.result = self.u.setLowTrafficMode('false')

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getWhoIsInfo(self):
        # Action
        self.status, self.result = self.u.getWhoIsInfo(settings.CONTACT_PK)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getChannelInfo(self):
        # Action
        self.status, self.result = self.u.getChannelInfo(settings.CHANNEL_ID)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getChannelModerators(self):
        # Action
        self.status, self.result = self.u.getChannelModerators(settings.CHANNEL_ID)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getChannelModeratorRight(self):
        # Action
        self.status, moderators = self.u.getChannelModerators(settings.CHANNEL_ID)
        if len(moderators) > 0 and not 'error' in moderators:
            self.status, self.result = self.u.getChannelModeratorRight(settings.CHANNEL_ID, moderators[0])
        else:
            raise Exception("There is no moderators or error on request")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_setProfileStatus(self):
        # Action
        self.status, self.result = self.u.setProfileStatus("Available", "QA Engineer")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getEmails(self):
        # Action
        self.status, self.result = self.u.getEmails(1, "")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getChannelMessages(self):
        # Action
        #self.status, self.result = self.u.getChannelMessages("B4EF14CFE2782C1E94E82631F9B782E2")
        self.status, self.result = self.u.getChannelMessages(settings.CHANNEL_ID)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    #@unittest.skip("просьба не трогать ушан")
    def test_createChannel(self):
        # Action
        self.status, myChannel = self.u.createChannel("Test Channel |+_)(*&^%$#@!~", "description _)(*?:%;№", "false", "", "", "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x", "10.000, 20.000", "", "false", "false")
        time.sleep(3)
        s, result = self.u.deleteChannel(myChannel)        
        
        # Assertion
        self.assertTrue(self.status, "Status: " + str(self.status))
        self.assertTrue(self.pattern.match(str(myChannel)), "Result '" + str(myChannel) + "' is not reference number")

    def test_getOwnContact(self):
        # Action
        self.status, self.result = self.u.getOwnContact()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getChannelAvatar(self):
        # Action
        self.status, self.result = self.u.getChannelAvatar(settings.CHANNEL_ID, "BASE64", "JPG")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendInstantQuote(self):
        # Action
        s, contact_msgs = self.u.getContactMessages(settings.CONTACT_PK)
        if len(contact_msgs) == 0:
            self.test_sendInstantMessage()
            s, contact_msgs = self.u.getContactMessages(settings.CONTACT_PK)
        self.status, self.result = self.u.sendInstantQuote(settings.CONTACT_PK, "this is python unittest quote message", contact_msgs[0]["id"])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getStickerCollections(self):
        # Action
        self.status, self.result = self.u.getStickerCollections()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getStickerNamesByCollection(self):
        # Action
        s, sticker_collection = self.u.getStickerCollections()
        self.status, self.result = self.u.getStickerNamesByCollection(sticker_collection[0])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getImageSticker(self):
        # Action
        s, sticker_collection = self.u.getStickerCollections()
        s, all_stickers = self.u.getStickerNamesByCollection(sticker_collection[0])
        self.status, self.result = self.u.getImageSticker(sticker_collection[0], all_stickers[0], "BASE64")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendInstantSticker(self):
        # Action
        s, sticker_collection = self.u.getStickerCollections()
        s, all_stickers = self.u.getStickerNamesByCollection(sticker_collection[0])
        self.status, self.result = self.u.sendInstantSticker(settings.CONTACT_PK, sticker_collection[0], all_stickers[0])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendInstantBuzz(self):
        # Action
        self.status, self.result = self.u.sendInstantBuzz(settings.CONTACT_PK, "Python Buzz")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendInstantInvitation(self):
        # Action
        self.status, self.result = self.u.sendInstantInvitation(settings.CONTACT_PK, settings.CHANNEL_ID, "Python invite description", "Python invite comment")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_removeInstantMessages(self):
        # Action
        self.status, self.result = self.u.removeInstantMessages(settings.CONTACT_PK)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getMiningInfo(self):
        # Action
        self.status, self.result = self.u.getMiningInfo()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendChannelPicture(self):
        # Action
        self.status, self.result = self.u.sendChannelPicture(settings.CHANNEL_ID, settings.PICTURE, "image.jpg")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    #@unittest.skip("просьба не трогать ушан")
    def test_modifyChannel(self):
        # Action
        s, my_channels = self.u.getChannels("", 2)
        myChannel = ""
        if len(my_channels) < 5:
            s, myChannel = self.u.createChannel("Test Channel |+_)(*&^%$#@!~", "description _)(*?:%;№", "false", "", "", "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x", "10.000, 20.000", "", "false", "false")
            time.sleep(2)
        else:
            for channel in my_channels:
                if channel["name"] != "testing_dev" or channel["name"] != "hidden channel":
                    myChannel = channel["channelid"]
        if myChannel != "":
            self.status, self.result = self.u.modifyChannel(myChannel, "edit on:" + str(time.strftime("%H:%M:%S", time.gmtime()).split(":")), "false", "all", "", "", "", "", "false")
        else:
            raise Exception("Cant choose channel for modify")
        s, r = self.u.deleteChannel(myChannel)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")
    
    #@unittest.skip("просьба не трогать ушан")
    def test_deleteChannel(self):
        # Action
        s, my_channels = self.u.getChannels("", 2)
        myChannel = ""
        if len(my_channels) < 3:
            s, myChannel = self.u.createChannel("Test Channel |+_)(*&^%$#@!~", "description _)(*?:%;№", "false", "", "", "hash_tag1234567890v6dg46s5d4gr6s5dg46s54h6a5d4rg56431m31x", "10.000, 20.000", "", "false", "false")
        else:
            for channel in my_channels:
                if channel["name"] != "testing_dev" or channel["name"] != "hidden channel":
                    myChannel = channel["channelid"]
        self.status, result = self.u.deleteChannel(myChannel)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.pattern.match(str(result)), "Result '" + str(result) + "' is not reference number")

    def test_getChannelSystemInfo(self):
        # Action
        self.status, self.result = self.u.getChannelSystemInfo()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_summaryUnsRegisteredNames(self):
        # Action
        self.status, self.result = self.u.summaryUnsRegisteredNames("", "")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_requestTreasuryPoSRates(self):
        # Action
        self.status, self.result = self.u.requestTreasuryPoSRates()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getTreasuryPoSRates(self):
        # Action
        self.status, self.result = self.u.getTreasuryPoSRates()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_requestTreasuryTransactionVolumes(self):
        # Action
        self.status, self.result = self.u.requestTreasuryTransactionVolumes()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getTreasuryTransactionVolumes(self):
        # Action
        self.status, self.result = self.u.getTreasuryTransactionVolumes()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_ucodeEncode(self):
        # Action
        self.status, self.result = self.u.ucodeEncode(settings.CONTACT_PK, "200", "BASE64", "JPG")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_ucodeDecode(self):
        # Action
        self.status, self.result = self.u.ucodeDecode(settings.UCODE)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getWebSocketState(self):
        # Action
        self.status, self.result = self.u.getWebSocketState()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_setWebSocketState(self):
        # Action
        self.status, self.result = self.u.setWebSocketState("true", "20001")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getContactGroups(self):
        # Action
        self.status, self.result = self.u.getContactGroups()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getContactsByGroup(self):
        # Action
        s, groups = self.u.getContactGroups()
        self.status, self.result = self.u.getContactsByGroup(groups[0])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_deleteContactGroup(self):
        # Action
        s, groups = self.u.getContactGroups()
        group = list(filter(lambda g: 
                            g != "DEV Group™" or 
                            g != "██▓▓▒▒░░Вожди░░▒▒▓▓██" or 
                            g != "<h1>Отдел тестирования</h1>11111" or
                            g != "MSK Teem" or
                            g != "beta.u.is" or
                            g != "", groups))
        if settings.DEBUG: print("test_deleteContactGroup, group name: " + str(group[0]))
        self.status, self.result = self.u.deleteContactGroup(group[0])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getTransfersFromManager(self):
        # Action
        self.status, self.result  = self.u.getTransfersFromManager()
        
        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getFilesFromManager(self):
        # Action
        self.status, self.result = self.u.getFilesFromManager()

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_abortTransfers(self):
        # Action
        s, transfers = self.u.getTransfersFromManager()
        tr_id = ""
        try:
            active_transfers = list(filter(lambda t: t["percentCompleted"] < 100))
            tr_id = active_transfers[0]["transferId"]
        except:
            tr_id = transfers[0]["transferId"]

        self.status, self.result = self.u.abortTransfers(tr_id)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_hideTransfers(self):
        # Action
        s, transfers = self.u.getTransfersFromManager()
        tr_id = ""
        try:
            active_transfers = list(filter(lambda t: t["percentCompleted"] < 100))
            tr_id = active_transfers[0]["transferId"]
        except:
            tr_id = transfers[0]["transferId"]

        self.status, self.result = self.u.hideTransfers(tr_id)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getFile(self):
        # Action
        s, files = self.u.getFilesFromManager()
        self.status, self.result = self.u.getFile(files[0]["id"])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_deleteFile(self):
        # Action
        s, files = self.u.getFilesFromManager()
        self.status, self.result = self.u.deleteFile(files[0]["id"])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_sendFileByMessage(self):
        # Action
        s, files = self.u.getFilesFromManager()
        self.status, self.result = self.u.sendFileByMessage(settings.CONTACT_PK, files[0]["id"])

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_getChannelBannedConacts(self):
        # Action
        self.status, self.result = self.u.getChannelBannedContacts(settings.CHANNEL_ID)

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_applyChannelBannedContacts(self):
        # Action
        s,r = self.u.applyChannelBannedContacts(settings.CHANNEL_ID, "["+settings.CONTACT_PK+"]")
        #print(self.u.getChannelBannedContacts(settings.CHANNEL_ID))
        self.status, self.result = self.u.applyChannelBannedContacts(settings.CHANNEL_ID, "[]")

        # Assertion
        self.assertTrue(self.status)
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

    def test_uploadFile(self):
        # Action
        self.status, self.result = self.u.uploadFile(settings.PICTURE, "Дулин.png")

        # Assertion
        self.assertTrue(self.status, str(self.status))
        self.assertTrue(self.result != "" and not "error" in str(self.result), str(self.result))

        
        
    def tearDown(self):
        if settings.DEBUG:
            print("Result: " + str(self.result))

if __name__ == "__main__":
    #unittest.main()
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult))
