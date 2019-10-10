import unittest
import json
import time
import re
import api
import settings
import pandas as pd

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
    getInvoicesParams = '{ "cardId": "", "invoiceId": "", "pk": "", "transactionId": "", "status": "", "startDateTime": "", "endDateTime": "", "referenceNumber": "" }'
    
    def setUp(self):        
        self.status = False        
    
    #def test_joinChannel_repeater(self):
    #    for x in range(0, 100):
    #       #self.u.joinChannel("3EEF8E7C57A96049ABFDAEBBB275F05B", "")
    #       #self.u.leaveChannel("3EEF8E7C57A96049ABFDAEBBB275F05B")
    #       self.u.sendChannelMessage("3EEF8E7C57A96049ABFDAEBBB275F05B", "Message:" + str(x) + " of 100 from Python api test")

    #def test_unsSearchByNick(self):
    #    self.status, self.result = self.u.unsSearchByNick('AJLL66GIG2UPA2MSXPUUDIDB95S0ZGT5')
    #    s_res = self.result
    #    for uns in s_res:
    #        flds = str(uns).split(', ')
    #        for fld in flds:
    #            print(fld)
    #        print("\n")
    @unittest.skip("1")
    def test_getLicenses(self):
        self.status, self.result = self.u.getLicenses()        
        for l in self.result:
            print(l)
            print()
    @unittest.skip("2")
    def test_getContactLicenses(self):
        self.status, self.result = self.u.getContactLicenses('F91C81CED60CC8E741F590E9317C47AC0D055C10727E54EE30CC7954E09C7621')  
        print(self.status)
        print(self.result)
        for l in self.result:
            print(l)
            print()
    @unittest.skip("3")
    def test_getuNS_Count_in_api_and_UI(self):
        self.status, uns_list = self.u.unsSearchByNick("d")
        #print(len(uns_list))
        print(uns_list[0])
        uns_columns = ['channelId', 'isBlocked', 'isPrimary', 'issued', 'nick', 'pk', 'valid']
        uns_data = [[]]
        for uns in uns_list:
            row = [uns['channelId'], uns['isBlocked'], uns['isPrimary'], uns['issued'], uns['nick'], uns['pk'], uns['valid']]
            uns_data.append(row)
        df = pd.DataFrame(columns = uns_columns, data = uns_data)
        print(df['issued'])

    def test_compare_channels(self):
        channel_ids = ['4EBA22A7071E993FFFE4443AB3F0BC43', '4828F7218EBFB038427DDCEEF30ED1A4', '2EDF424F4EA0677C23939E7ECE86A317', '436C376F7E61E72D40C97C7A042CFEB9']
        channels_data = []
        channels_columns = ['HideInCommonList', 'created', 'description', 'geotag', 'hashtags', 'languages', 'modified', 'owner', 'readonly', 'readonly_privacy', 'title', 'type']
        for id in channel_ids:
            self.status, channel = self.u.getChannelInfo(id)
            row = [channel['HideInCommonList'], channel['created'], channel['description'], channel['geotag'], channel['hashtags'], channel['languages'], channel['modified'], channel['owner'], channel['readonly'], channel['readonly_privacy'], channel['title'], channel['type']]
            channels_data.append(row)
        #print(len(uns_list))
        df = pd.DataFrame(columns = channels_columns, data = channels_data)
        #print(df['readonly'])
        for column in channels_columns:
            print(df[column])
            print()
               
    def tearDown(self):
        try:
            self.assertFalse('error' in str(self.result))
        except Exception:
            time.sleep(0.001)
        self.assertTrue(bool(self.status), "Status of request execution is False")

if __name__ == "__main__":
    unittest.main(testRunner=unittest.TextTestRunner(resultclass=MyTestResult))
