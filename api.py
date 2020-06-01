#!/usr/bin/env python
import requests
import json
import threading
from array import array
import logging
import binascii
import time
#==============================    
        
class Utopia(object):

    def __init__(self, APIURL, token, delay = 0.5):
        self.APIURL = APIURL
        self.token = token
        self.delay = delay
        
        self.GENERICFILTER={"sortBy": "" , "offset": "", "limit": ""}             

    #==============================
    def send_request(self, data):
        
        try:
            time.sleep(self.delay)
            self.EXTRAINFO=''
            headers = {}
            data["token"]= self.token
            
            req = requests.post(self.APIURL, json.dumps(data).encode("utf-8"),headers=headers)
            
            logging.debug( req.status_code)
            logging.debug( req.reason)
            if (req.status_code != 200):
                logging.error( u'Too Many Requests' )
                return False , "Too Many Requests"
                
            j = json.loads(req.text)
            
            if ( "result" not in j):
                logging.debug( u'Wrong response data')
                return False, j["error"]
            else:
                self.EXTRAINFO = j["resultExtraInfo"]
                return True , j["result"]
            
        except Exception as e:
            logging.error( u'This is an exception. Message:' )
            logging.error( e )
            return False , ""
        
    
    #==============================
    def genericFilter(self, sortBy, offset, limit):
        self.GENERICFILTER = {
                            "sortBy": sortBy,
							"offset": offset,
							"limit": limit
                            }
     
    #====================
   
    def genericFilterClear(self):
        self.GENERICFILTER = { "sortBy": "","offset": "", "limit": "" }

    #====================
	
    def getExtraInfo(self):
        return self.EXTRAINFO
           #====================  
    def getSystemInfo(self): 
        data={"jsonrpc": "2.0",
            "method":"getSystemInfo",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getSystemInfo method call' )
        return self.send_request(data)
    #====================  
    def getProfileStatus(self): 
        data={"jsonrpc": "2.0",
            "method":"getProfileStatus",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getProfileStatus method call' )
        return self.send_request(data)
    #====================  
    def setProfileStatus(self, status, mood): 
        data={"jsonrpc": "2.0",
            "method":"setProfileStatus",
            "params": {
                'status' : status,
                'mood' : mood                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'setProfileStatus method call' )
        return self.send_request(data)
    #====================  
    def getOwnContact(self): 
        data={"jsonrpc": "2.0",
            "method":"getOwnContact",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getOwnContact method call' )
        return self.send_request(data)
    #====================  
    def getContacts(self, filter): 
        data={"jsonrpc": "2.0",
            "method":"getContacts",
            "params": {
                'filter' : filter                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getContacts method call' )
        return self.send_request(data)
    #====================  
    def getContactAvatar(self, pk, coder, format): 
        data={"jsonrpc": "2.0",
            "method":"getContactAvatar",
            "params": {
                'pk' : pk,
                'coder' : coder,
                'format' : format                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getContactAvatar method call' )
        return self.send_request(data)
    #====================  
    def getChannelAvatar(self, channelid, coder, format): 
        data={"jsonrpc": "2.0",
            "method":"getChannelAvatar",
            "params": {
                'channelid' : channelid,
                'coder' : coder,
                'format' : format                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelAvatar method call' )
        return self.send_request(data)
    #====================  
    def setContactGroup(self, contactPublicKey, groupName): 
        data={"jsonrpc": "2.0",
            "method":"setContactGroup",
            "params": {
                'contactPublicKey' : contactPublicKey,
                'groupName' : groupName                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'setContactGroup method call' )
        return self.send_request(data)
    #====================  
    def setContactNick(self, contactPublicKey, newNick): 
        data={"jsonrpc": "2.0",
            "method":"setContactNick",
            "params": {
                'contactPublicKey' : contactPublicKey,
                'newNick' : newNick                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'setContactNick method call' )
        return self.send_request(data)
    #====================  
    def sendInstantMessage(self, tohex, text): 
        data={"jsonrpc": "2.0",
            "method":"sendInstantMessage",
            "params": {
                'to' : tohex,
                'text' : text                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendInstantMessage method call' )
        return self.send_request(data)
    #====================  
    def sendInstantQuote(self, tohex, text, id_message): 
        data={"jsonrpc": "2.0",
            "method":"sendInstantQuote",
            "params": {
                'to' : tohex,
                'text' : text,
                'id_message' : id_message                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendInstantQuote method call' )
        return self.send_request(data)
    #====================  
    def getStickerCollections(self): 
        data={"jsonrpc": "2.0",
            "method":"getStickerCollections",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getStickerCollections method call' )
        return self.send_request(data)
    #====================  
    def getStickerNamesByCollection(self, collection_name): 
        data={"jsonrpc": "2.0",
            "method":"getStickerNamesByCollection",
            "params": {
                'collection_name' : collection_name                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getStickerNamesByCollection method call' )
        return self.send_request(data)
    #====================  
    def getImageSticker(self, collection_name, sticker_name, coder): 
        data={"jsonrpc": "2.0",
            "method":"getImageSticker",
            "params": {
                'collection_name' : collection_name,
                'sticker_name' : sticker_name,
                'coder' : coder                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getImageSticker method call' )
        return self.send_request(data)
    #====================  
    def sendInstantSticker(self, tohex, collection, name): 
        data={"jsonrpc": "2.0",
            "method":"sendInstantSticker",
            "params": {
                'to' : tohex,
                'collection' : collection,
                'name' : name                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendInstantSticker method call' )
        return self.send_request(data)
    #====================  
    def sendInstantBuzz(self, tohex, comments): 
        data={"jsonrpc": "2.0",
            "method":"sendInstantBuzz",
            "params": {
                'to' : tohex,
                'comments' : comments                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendInstantBuzz method call' )
        return self.send_request(data)
    #====================  
    def sendInstantInvitation(self, tohex, channelid, description, comments): 
        data={"jsonrpc": "2.0",
            "method":"sendInstantInvitation",
            "params": {
                'to' : tohex,
                'channelid' : channelid,
                'description' : description,
                'comments' : comments                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendInstantInvitation method call' )
        return self.send_request(data)
    #====================  
    def removeInstantMessages(self, hex_contact_public_key): 
        data={"jsonrpc": "2.0",
            "method":"removeInstantMessages",
            "params": {
                'hex_contact_public_key' : hex_contact_public_key                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'removeInstantMessages method call' )
        return self.send_request(data)
    #====================  
    def getContactMessages(self, pk): 
        data={"jsonrpc": "2.0",
            "method":"getContactMessages",
            "params": {
                'pk' : pk                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getContactMessages method call' )
        return self.send_request(data)
    #====================  
    def sendEmailMessage(self, tohex, subject, body, attachmentFileId): 
        data={"jsonrpc": "2.0",
            "method":"sendEmailMessage",
            "params": {
                'to' : tohex,
                'subject' : subject,
                'body' : body,
                'attachmentFileId' : attachmentFileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendEmailMessage method call' )
        return self.send_request(data)
    #====================  
    def sendPayment(self, tohex, comment, cardid, amount): 
        data={"jsonrpc": "2.0",
            "method":"sendPayment",
            "params": {
                'to' : tohex,
                'comment' : comment,
                'cardid' : cardid,
                'amount' : amount                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendPayment method call' )
        return self.send_request(data)
    #====================  
    def getEmailFolder(self, folderType, filter): 
        data={"jsonrpc": "2.0",
            "method":"getEmailFolder",
            "params": {
                'folderType' : folderType,
                'filter' : filter                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getEmailFolder method call' )
        return self.send_request(data)
    #====================  
    def getEmails(self, folderType, filter): 
        data={"jsonrpc": "2.0",
            "method":"getEmails",
            "params": {
                'folderType' : folderType,
                'filter' : filter                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getEmails method call' )
        return self.send_request(data)
    #====================  
    def abortAttachment(self, emailId, fileId): 
        data={"jsonrpc": "2.0",
            "method":"abortAttachment",
            "params": {
                'emailId' : emailId,
                'fileId' : fileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'abortAttachment method call' )
        return self.send_request(data)
    #====================  
    def acceptAttachment(self, emailId, fileId): 
        data={"jsonrpc": "2.0",
            "method":"acceptAttachment",
            "params": {
                'emailId' : emailId,
                'fileId' : fileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'acceptAttachment method call' )
        return self.send_request(data)
    #====================  
    def getEmailById(self, id): 
        data={"jsonrpc": "2.0",
            "method":"getEmailById",
            "params": {
                'id' : id                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getEmailById method call' )
        return self.send_request(data)
    #====================  
    def deleteEmail(self, id): 
        data={"jsonrpc": "2.0",
            "method":"deleteEmail",
            "params": {
                'id' : id                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'deleteEmail method call' )
        return self.send_request(data)
    #====================  
    def sendReplyEmailMessage(self, id, body, subject, attachmentFileId): 
        data={"jsonrpc": "2.0",
            "method":"sendReplyEmailMessage",
            "params": {
                'id' : id,
                'body' : body,
                'subject' : subject,
                'attachmentFileId' : attachmentFileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendReplyEmailMessage method call' )
        return self.send_request(data)
    #====================  
    def sendForwardEmailMessage(self, id, tohex, body, subject, attachmentFileId): 
        data={"jsonrpc": "2.0",
            "method":"sendForwardEmailMessage",
            "params": {
                'id' : id,
                'to' : tohex,
                'body' : body,
                'subject' : subject,
                'attachmentFileId' : attachmentFileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendForwardEmailMessage method call' )
        return self.send_request(data)
    #====================  
    def getFinanceSystemInformation(self): 
        data={"jsonrpc": "2.0",
            "method":"getFinanceSystemInformation",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getFinanceSystemInformation method call' )
        return self.send_request(data)
    #====================  
    def getBalance(self): 
        data={"jsonrpc": "2.0",
            "method":"getBalance",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getBalance method call' )
        return self.send_request(data)
    #====================  
    def getFinanceHistory(self, filters, referenceNumber, fromDate, toDate, batchId, fromAmount, toAmount): 
        data={"jsonrpc": "2.0",
            "method":"getFinanceHistory",
            "params": {
                'filters' : filters,
                'referenceNumber' : referenceNumber,
                'fromDate' : fromDate,
                'toDate' : toDate,
                'batchId' : batchId,
                'fromAmount' : fromAmount,
                'toAmount' : toAmount                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getFinanceHistory method call' )
        return self.send_request(data)
    #====================  
    def getCards(self): 
        data={"jsonrpc": "2.0",
            "method":"getCards",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getCards method call' )
        return self.send_request(data)
    #====================  
    def addCard(self, color, name, preorderNumberInCard): 
        data={"jsonrpc": "2.0",
            "method":"addCard",
            "params": {
                'color' : color,
                'name' : name,
                'preorderNumberInCard' : preorderNumberInCard                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'addCard method call' )
        return self.send_request(data)
    #====================  
    def deleteCard(self, cardId): 
        data={"jsonrpc": "2.0",
            "method":"deleteCard",
            "params": {
                'cardId' : cardId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'deleteCard method call' )
        return self.send_request(data)
    #====================  
    def enableMining(self, enable): 
        data={"jsonrpc": "2.0",
            "method":"enableMining",
            "params": {
                'enable' : enable                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'enableMining method call' )
        return self.send_request(data)
    #====================  
    def enablePoS(self, enable): 
        data={"jsonrpc": "2.0",
            "method":"enablePoS",
            "params": {
                'enable' : enable                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'enablePoS method call' )
        return self.send_request(data)
    #====================  
    def enableHistoryMining(self, enable): 
        data={"jsonrpc": "2.0",
            "method":"enableHistoryMining",
            "params": {
                'enable' : enable                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'enableHistoryMining method call' )
        return self.send_request(data)
    #====================  
    def statusHistoryMining(self): 
        data={"jsonrpc": "2.0",
            "method":"statusHistoryMining",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'statusHistoryMining method call' )
        return self.send_request(data)
    #====================  
    def getMiningBlocks(self): 
        data={"jsonrpc": "2.0",
            "method":"getMiningBlocks",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getMiningBlocks method call' )
        return self.send_request(data)
    #====================  
    def getMiningInfo(self): 
        data={"jsonrpc": "2.0",
            "method":"getMiningInfo",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getMiningInfo method call' )
        return self.send_request(data)
    #====================  
    def getVouchers(self): 
        data={"jsonrpc": "2.0",
            "method":"getVouchers",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getVouchers method call' )
        return self.send_request(data)
    #====================  
    def createVoucher(self, amount): 
        data={"jsonrpc": "2.0",
            "method":"createVoucher",
            "params": {
                'amount' : amount                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'createVoucher method call' )
        return self.send_request(data)
    #====================  
    def useVoucher(self, voucherid): 
        data={"jsonrpc": "2.0",
            "method":"useVoucher",
            "params": {
                'voucherid' : voucherid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'useVoucher method call' )
        return self.send_request(data)
    #====================  
    def deleteVoucher(self, voucherid): 
        data={"jsonrpc": "2.0",
            "method":"deleteVoucher",
            "params": {
                'voucherid' : voucherid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'deleteVoucher method call' )
        return self.send_request(data)
    #====================  
    def getInvoices(self, parameters): 
        data={"jsonrpc": "2.0",
            "method":"getInvoices",
            "params": {
                'parameters' : parameters                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getInvoices method call' )
        return self.send_request(data)
    #====================  
    def getInvoiceByReferenceNumber(self, referenceNumber): 
        data={"jsonrpc": "2.0",
            "method":"getInvoiceByReferenceNumber",
            "params": {
                'referenceNumber' : referenceNumber                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getInvoiceByReferenceNumber method call' )
        return self.send_request(data)
    #====================  
    def getTransactionIdByReferenceNumber(self, referenceNumber): 
        data={"jsonrpc": "2.0",
            "method":"getTransactionIdByReferenceNumber",
            "params": {
                'referenceNumber' : referenceNumber                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getTransactionIdByReferenceNumber method call' )
        return self.send_request(data)
    #====================  
    def sendInvoice(self, comment, cardid, amount): 
        data={"jsonrpc": "2.0",
            "method":"sendInvoice",
            "params": {
                'comment' : comment,
                'cardid' : cardid,
                'amount' : amount                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendInvoice method call' )
        return self.send_request(data)
    #====================  
    def acceptInvoice(self, invoiceid): 
        data={"jsonrpc": "2.0",
            "method":"acceptInvoice",
            "params": {
                'invoiceid' : invoiceid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'acceptInvoice method call' )
        return self.send_request(data)
    #====================  
    def declineInvoice(self, invoiceid): 
        data={"jsonrpc": "2.0",
            "method":"declineInvoice",
            "params": {
                'invoiceid' : invoiceid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'declineInvoice method call' )
        return self.send_request(data)
    #====================  
    def cancelInvoice(self, invoiceid): 
        data={"jsonrpc": "2.0",
            "method":"cancelInvoice",
            "params": {
                'invoiceid' : invoiceid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'cancelInvoice method call' )
        return self.send_request(data)
    #====================  
    def requestUnsTransfer(self, name, hexNewOwnerPk): 
        data={"jsonrpc": "2.0",
            "method":"requestUnsTransfer",
            "params": {
                'name' : name,
                'hexNewOwnerPk' : hexNewOwnerPk                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'requestUnsTransfer method call' )
        return self.send_request(data)
    #====================  
    def acceptUnsTransfer(self, requestId): 
        data={"jsonrpc": "2.0",
            "method":"acceptUnsTransfer",
            "params": {
                'requestId' : requestId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'acceptUnsTransfer method call' )
        return self.send_request(data)
    #====================  
    def declineUnsTransfer(self, requestId): 
        data={"jsonrpc": "2.0",
            "method":"declineUnsTransfer",
            "params": {
                'requestId' : requestId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'declineUnsTransfer method call' )
        return self.send_request(data)
    #====================  
    def incomingUnsTransfer(self): 
        data={"jsonrpc": "2.0",
            "method":"incomingUnsTransfer",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'incomingUnsTransfer method call' )
        return self.send_request(data)
    #====================  
    def outgoingUnsTransfer(self): 
        data={"jsonrpc": "2.0",
            "method":"outgoingUnsTransfer",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'outgoingUnsTransfer method call' )
        return self.send_request(data)
    #====================  
    def storageWipe(self): 
        data={"jsonrpc": "2.0",
            "method":"storageWipe",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'storageWipe method call' )
        return self.send_request(data)
    #====================  
    def sendAuthorizationRequest(self, pk, message): 
        data={"jsonrpc": "2.0",
            "method":"sendAuthorizationRequest",
            "params": {
                'pk' : pk,
                'message' : message                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendAuthorizationRequest method call' )
        return self.send_request(data)
    #====================  
    def acceptAuthorizationRequest(self, pk, message): 
        data={"jsonrpc": "2.0",
            "method":"acceptAuthorizationRequest",
            "params": {
                'pk' : pk,
                'message' : message                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'acceptAuthorizationRequest method call' )
        return self.send_request(data)
    #====================  
    def rejectAuthorizationRequest(self, pk, message): 
        data={"jsonrpc": "2.0",
            "method":"rejectAuthorizationRequest",
            "params": {
                'pk' : pk,
                'message' : message                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'rejectAuthorizationRequest method call' )
        return self.send_request(data)
    #====================  
    def deleteContact(self, pk): 
        data={"jsonrpc": "2.0",
            "method":"deleteContact",
            "params": {
                'pk' : pk                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'deleteContact method call' )
        return self.send_request(data)
    #====================  
    def getChannels(self, filter, channel_type): 
        data={"jsonrpc": "2.0",
            "method":"getChannels",
            "params": {
                'filter' : filter,
                'channel_type' : channel_type                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannels method call' )
        return self.send_request(data)
    #====================  
    def sendChannelMessage(self, channelid, message): 
        data={"jsonrpc": "2.0",
            "method":"sendChannelMessage",
            "params": {
                'channelid' : channelid,
                'message' : message                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendChannelMessage method call' )
        return self.send_request(data)
    #====================  
    def sendChannelPicture(self, channelid, base64_image, filename_image): 
        data={"jsonrpc": "2.0",
            "method":"sendChannelPicture",
            "params": {
                'channelid' : channelid,
                'base64_image' : base64_image,
                'filename_image' : filename_image                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendChannelPicture method call' )
        return self.send_request(data)
    #====================  
    def joinChannel(self, ident, password): 
        data={"jsonrpc": "2.0",
            "method":"joinChannel",
            "params": {
                'ident' : ident,
                'password' : password                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'joinChannel method call' )
        return self.send_request(data)
    #====================  
    def leaveChannel(self, channelid): 
        data={"jsonrpc": "2.0",
            "method":"leaveChannel",
            "params": {
                'channelid' : channelid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'leaveChannel method call' )
        return self.send_request(data)
    #====================  
    def getChannelContacts(self, channelid): 
        data={"jsonrpc": "2.0",
            "method":"getChannelContacts",
            "params": {
                'channelid' : channelid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelContacts method call' )
        return self.send_request(data)
    #====================  
    def getChannelMessages(self, channelid): 
        data={"jsonrpc": "2.0",
            "method":"getChannelMessages",
            "params": {
                'channelid' : channelid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelMessages method call' )
        return self.send_request(data)
    #====================  
    def getChannelInfo(self, channelid): 
        data={"jsonrpc": "2.0",
            "method":"getChannelInfo",
            "params": {
                'channelid' : channelid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelInfo method call' )
        return self.send_request(data)
    #====================  
    def getChannelModerators(self, channelid): 
        data={"jsonrpc": "2.0",
            "method":"getChannelModerators",
            "params": {
                'channelid' : channelid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelModerators method call' )
        return self.send_request(data)
    #====================  
    def getChannelModeratorRight(self, channelid, moderator): 
        data={"jsonrpc": "2.0",
            "method":"getChannelModeratorRight",
            "params": {
                'channelid' : channelid,
                'moderator' : moderator                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelModeratorRight method call' )
        return self.send_request(data)
    #====================  
    def createChannel(self, channel_name, description, read_only, read_only_privacy, password, languages, hashtags, geoTag, base64_avatar_image, hide_in_UI): 
        data={"jsonrpc": "2.0",
            "method":"createChannel",
            "params": {
                'channel_name' : channel_name,
                'description' : description,
                'read_only' : read_only,
                'read_only_privacy' : read_only_privacy,
                'password' : password,
                'languages' : languages,
                'hashtags' : hashtags,
                'geoTag' : geoTag,
                'base64_avatar_image' : base64_avatar_image,
                'hide_in_UI' : hide_in_UI                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'createChannel method call' )
        return self.send_request(data)
    #====================  
    def modifyChannel(self, channelid, description, read_only, read_only_privacy, password, languages, hashtags, geoTag, base64_avatar_image, hide_in_UI): 
        data={"jsonrpc": "2.0",
            "method":"modifyChannel",
            "params": {
                'channelid' : channelid,
                'description' : description,
                'read_only' : read_only,
                'read_only_privacy' : read_only_privacy,
                'password' : password,
                'languages' : languages,
                'hashtags' : hashtags,
                'geoTag' : geoTag,
                'base64_avatar_image' : base64_avatar_image,
                'hide_in_UI' : hide_in_UI                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'modifyChannel method call' )
        return self.send_request(data)
    #====================  
    def modifyChannelTitle(self, channelid, newTitle, password): 
        data={"jsonrpc": "2.0",
            "method":"modifyChannelTitle",
            "params": {
                'channelid' : channelid,
                'newTitle' : newTitle,
                'password' : password                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'modifyChannelTitle method call' )
        return self.send_request(data)
    #====================  
    def modifyChannelPassword(self, channelid, newPassword, password): 
        data={"jsonrpc": "2.0",
            "method":"modifyChannelPassword",
            "params": {
                'channelid' : channelid,
                'newPassword' : newPassword,
                'password' : password                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'modifyChannelPassword method call' )
        return self.send_request(data)
    #====================  
    def deleteChannel(self, channelid, password): 
        data={"jsonrpc": "2.0",
            "method":"deleteChannel",
            "params": {
                'channelid' : channelid,
                'password' : password                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'deleteChannel method call' )
        return self.send_request(data)
    #====================  
    def getChannelSystemInfo(self): 
        data={"jsonrpc": "2.0",
            "method":"getChannelSystemInfo",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelSystemInfo method call' )
        return self.send_request(data)
    #====================  
    def unsCreateRecordRequest(self, nick, valid, isPrimary, channelId): 
        data={"jsonrpc": "2.0",
            "method":"unsCreateRecordRequest",
            "params": {
                'nick' : nick,
                'valid' : valid,
                'isPrimary' : isPrimary,
                'channelId' : channelId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'unsCreateRecordRequest method call' )
        return self.send_request(data)
    #====================  
    def unsModifyRecordRequest(self, nick, valid, isPrimary, channelId): 
        data={"jsonrpc": "2.0",
            "method":"unsModifyRecordRequest",
            "params": {
                'nick' : nick,
                'valid' : valid,
                'isPrimary' : isPrimary,
                'channelId' : channelId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'unsModifyRecordRequest method call' )
        return self.send_request(data)
    #====================  
    def unsDeleteRecordRequest(self, nick): 
        data={"jsonrpc": "2.0",
            "method":"unsDeleteRecordRequest",
            "params": {
                'nick' : nick                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'unsDeleteRecordRequest method call' )
        return self.send_request(data)
    #====================  
    def unsSearchByPk(self, filter): 
        data={"jsonrpc": "2.0",
            "method":"unsSearchByPk",
            "params": {
                'filter' : filter                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'unsSearchByPk method call' )
        return self.send_request(data)
    #====================  
    def unsSearchByNick(self, filter): 
        data={"jsonrpc": "2.0",
            "method":"unsSearchByNick",
            "params": {
                'filter' : filter                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'unsSearchByNick method call' )
        return self.send_request(data)
    #====================  
    def getUnsSyncInfo(self): 
        data={"jsonrpc": "2.0",
            "method":"getUnsSyncInfo",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getUnsSyncInfo method call' )
        return self.send_request(data)
    #====================  
    def unsRegisteredNames(self): 
        data={"jsonrpc": "2.0",
            "method":"unsRegisteredNames",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'unsRegisteredNames method call' )
        return self.send_request(data)
    #====================  
    def summaryUnsRegisteredNames(self, fromDate, toDate): 
        data={"jsonrpc": "2.0",
            "method":"summaryUnsRegisteredNames",
            "params": {
                'fromDate' : fromDate,
                'toDate' : toDate                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'summaryUnsRegisteredNames method call' )
        return self.send_request(data)
    #====================  
    def getNetworkConnections(self): 
        data={"jsonrpc": "2.0",
            "method":"getNetworkConnections",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getNetworkConnections method call' )
        return self.send_request(data)
    #====================  
    def getProxyMappings(self): 
        data={"jsonrpc": "2.0",
            "method":"getProxyMappings",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getProxyMappings method call' )
        return self.send_request(data)
    #====================  
    def createProxyMapping(self, srcHost, srcPort, dstHost, dstPort, enabled): 
        data={"jsonrpc": "2.0",
            "method":"createProxyMapping",
            "params": {
                'srcHost' : srcHost,
                'srcPort' : srcPort,
                'dstHost' : dstHost,
                'dstPort' : dstPort,
                'enabled' : enabled                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'createProxyMapping method call' )
        return self.send_request(data)
    #====================  
    def enableProxyMapping(self, mappingId): 
        data={"jsonrpc": "2.0",
            "method":"enableProxyMapping",
            "params": {
                'mappingId' : mappingId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'enableProxyMapping method call' )
        return self.send_request(data)
    #====================  
    def disableProxyMapping(self, mappingId): 
        data={"jsonrpc": "2.0",
            "method":"disableProxyMapping",
            "params": {
                'mappingId' : mappingId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'disableProxyMapping method call' )
        return self.send_request(data)
    #====================  
    def removeProxyMapping(self, mappingId): 
        data={"jsonrpc": "2.0",
            "method":"removeProxyMapping",
            "params": {
                'mappingId' : mappingId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'removeProxyMapping method call' )
        return self.send_request(data)
    #====================  
    def lowTrafficMode(self): 
        data={"jsonrpc": "2.0",
            "method":"lowTrafficMode",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'lowTrafficMode method call' )
        return self.send_request(data)
    #====================  
    def setLowTrafficMode(self, enabled): 
        data={"jsonrpc": "2.0",
            "method":"setLowTrafficMode",
            "params": {
                'enabled' : enabled                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'setLowTrafficMode method call' )
        return self.send_request(data)
    #====================  
    def getWhoIsInfo(self, owner): 
        data={"jsonrpc": "2.0",
            "method":"getWhoIsInfo",
            "params": {
                'owner' : owner                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getWhoIsInfo method call' )
        return self.send_request(data)
    #====================  
    def requestTreasuryPoSRates(self): 
        data={"jsonrpc": "2.0",
            "method":"requestTreasuryPoSRates",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'requestTreasuryPoSRates method call' )
        return self.send_request(data)
    #====================  
    def getTreasuryPoSRates(self): 
        data={"jsonrpc": "2.0",
            "method":"getTreasuryPoSRates",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getTreasuryPoSRates method call' )
        return self.send_request(data)
    #====================  
    def requestTreasuryTransactionVolumes(self): 
        data={"jsonrpc": "2.0",
            "method":"requestTreasuryTransactionVolumes",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'requestTreasuryTransactionVolumes method call' )
        return self.send_request(data)
    #====================  
    def getTreasuryTransactionVolumes(self): 
        data={"jsonrpc": "2.0",
            "method":"getTreasuryTransactionVolumes",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getTreasuryTransactionVolumes method call' )
        return self.send_request(data)
    #====================  
    def ucodeEncode(self, hex_code, size_image, coder, format): 
        data={"jsonrpc": "2.0",
            "method":"ucodeEncode",
            "params": {
                'hex_code' : hex_code,
                'size_image' : size_image,
                'coder' : coder,
                'format' : format                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'ucodeEncode method call' )
        return self.send_request(data)
    #====================  
    def ucodeDecode(self, base64_image): 
        data={"jsonrpc": "2.0",
            "method":"ucodeDecode",
            "params": {
                'base64_image' : base64_image                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'ucodeDecode method call' )
        return self.send_request(data)
    #====================  
    def getWebSocketState(self): 
        data={"jsonrpc": "2.0",
            "method":"getWebSocketState",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getWebSocketState method call' )
        return self.send_request(data)
    #====================  
    def setWebSocketState(self, enabled, port): 
        data={"jsonrpc": "2.0",
            "method":"setWebSocketState",
            "params": {
                'enabled' : enabled,
                'port' : port                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'setWebSocketState method call' )
        return self.send_request(data)
    #====================  
    def clearTrayNotifications(self): 
        data={"jsonrpc": "2.0",
            "method":"clearTrayNotifications",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'clearTrayNotifications method call' )
        return self.send_request(data)
    #====================  
    def getContactGroups(self): 
        data={"jsonrpc": "2.0",
            "method":"getContactGroups",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getContactGroups method call' )
        return self.send_request(data)
    #====================  
    def getContactsByGroup(self, groupName): 
        data={"jsonrpc": "2.0",
            "method":"getContactsByGroup",
            "params": {
                'groupName' : groupName                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getContactsByGroup method call' )
        return self.send_request(data)
    #====================  
    def renameContactGroup(self, oldGroupName, newGroupName): 
        data={"jsonrpc": "2.0",
            "method":"renameContactGroup",
            "params": {
                'oldGroupName' : oldGroupName,
                'newGroupName' : newGroupName                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'renameContactGroup method call' )
        return self.send_request(data)
    #====================  
    def deleteContactGroup(self, groupName): 
        data={"jsonrpc": "2.0",
            "method":"deleteContactGroup",
            "params": {
                'groupName' : groupName                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'deleteContactGroup method call' )
        return self.send_request(data)
    #====================  
    def getTransfersFromManager(self): 
        data={"jsonrpc": "2.0",
            "method":"getTransfersFromManager",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getTransfersFromManager method call' )
        return self.send_request(data)
    #====================  
    def getFilesFromManager(self): 
        data={"jsonrpc": "2.0",
            "method":"getFilesFromManager",
            "params": {
                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getFilesFromManager method call' )
        return self.send_request(data)
    #====================  
    def abortTransfers(self, transferId): 
        data={"jsonrpc": "2.0",
            "method":"abortTransfers",
            "params": {
                'transferId' : transferId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'abortTransfers method call' )
        return self.send_request(data)
    #====================  
    def hideTransfers(self, transferId): 
        data={"jsonrpc": "2.0",
            "method":"hideTransfers",
            "params": {
                'transferId' : transferId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'hideTransfers method call' )
        return self.send_request(data)
    #====================  
    def getFile(self, fileId): 
        data={"jsonrpc": "2.0",
            "method":"getFile",
            "params": {
                'fileId' : fileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getFile method call' )
        return self.send_request(data)
    #====================  
    def deleteFile(self, fileId): 
        data={"jsonrpc": "2.0",
            "method":"deleteFile",
            "params": {
                'fileId' : fileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'deleteFile method call' )
        return self.send_request(data)
    #====================  
    def sendFileByMessage(self, tohex, fileId): 
        data={"jsonrpc": "2.0",
            "method":"sendFileByMessage",
            "params": {
                'to' : tohex,
                'fileId' : fileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendFileByMessage method call' )
        return self.send_request(data)
    #====================  
    def getChannelBannedContacts(self, channelid): 
        data={"jsonrpc": "2.0",
            "method":"getChannelBannedContacts",
            "params": {
                'channelid' : channelid                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'getChannelBannedContacts method call' )
        return self.send_request(data)
    #====================  
    def applyChannelBannedContacts(self, channelid, newList): 
        data={"jsonrpc": "2.0",
            "method":"applyChannelBannedContacts",
            "params": {
                'channelid' : channelid,
                'newList' : newList                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'applyChannelBannedContacts method call' )
        return self.send_request(data)
    #====================  
    def uploadFile(self, fileDataBase64, fileName): 
        data={"jsonrpc": "2.0",
            "method":"uploadFile",
            "params": {
                'fileDataBase64' : fileDataBase64,
                'fileName' : fileName                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'uploadFile method call' )
        return self.send_request(data)
    #====================  
    def sendFileByMessage(self, tohex, fileId): 
        data={"jsonrpc": "2.0",
            "method":"sendFileByMessage",
            "params": {
                'to' : tohex,
                'fileId' : fileId                },
            "filter": self.GENERICFILTER
        }
        logging.info( u'sendFileByMessage method call' )
        return self.send_request(data)
