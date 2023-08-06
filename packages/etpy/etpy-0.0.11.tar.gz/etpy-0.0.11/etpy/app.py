import base64
import json
import numbers
import random
import urllib.parse
import uuid
import requests
import xmltodict
import time
from datetime import datetime, timedelta
from requests.sessions import Session
from .Cash import *
from .Normal import *

class Client:
    headers = {
        "applicationVersion": "2",
        "Content-Type": "text/xml;charset=UTF-8",
        "applicationName": "MAB",
        "Accept": "text/xml",
        "applicationPassword": Constants.application_password,
        "APP-BuildNumber": Constants.build_number,
        "APP-Version": Constants.app_version,
        "OS-Type": "Android",
        "OS-Version": "10",
        "APP-STORE": "GOOGLE",
        "Is-Corporate": "false",
        "Host": "mab.etisalat.com.eg:11003",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.12.8",
        "ADRUM_1": "isMobile:true",
        "ADRUM": "isAjax:true",
    }
    access_token = ""
    def __init__(
        self,
        phone,
        device_id=None,
        device_name=Constants.device_name,
        platform="IOS",
        os_version="15",
    ):
        """
        Creating a new instance of client Client
        Parameters:
            Required :
                phone -> your etisalat phone number
            Optional:
                device_id -> you can pass your own device id or pass a random value from uuid module
                device_name -> you can pass a device name (the device name you put here will be shown in MyEtisalat app logs)
                platform    -> IOS or Android default is Android and this parameter also will be shown in MyEtisalat application logs
                os_version  -> Operating System Version  
        """

        self.phone = phone[1:]
        self.device_id = device_id
        self.device_name = device_name
        self.platform = platform
        self.os_version = os_version
        self.device_id = "tarookissexyguy699"
        self.user : User = None
        self.gifts = []

    def xmltodict(self, xml):
        """
        Etisalat api is returning a xml response !
        this function is used to convert xml to python dict
        """
        try:
            return json.loads(
                json.dumps(
                    xmltodict.parse(xml, encoding="utf-8"), ensure_ascii=False
                ).encode("utf-8")
            )
        except Exception as error:
            print(xml, error)

    def wait_for_cash(self, amount):
        """
        this function is used to wait for specfic amount to be received in etisalat cash wallet 
        once this amount is recevied the function will return true
        """
        balance = int(float(self.cash_login(self.pincode).Balance))
        new_balance = balance + amount
        print("Waiting for balance ...")
        while True:
            balance = int(float(self.cash_login(self.pincode).Balance))
            if new_balance == balance:
                break
            time.sleep(10)
        return True

    def cash_transfer(self, phone, amount) -> TransferPaymentReply:
        """
        with this function you can transfer money to any mezaa wallet 
        """
        response = self.__post(
            "/Saytar/rest/etisalatpay/service/TRANSFER",
            data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><PaymentRequest><Amount>{amount}</Amount><BNumber>{phone[1:]}</BNumber><ClientID>1234</ClientID><ClientLanguageID>2</ClientLanguageID><MSISDN>{self.phone}</MSISDN><Password>{self.pincode}</Password><Username>{self.phone}</Username></PaymentRequest>",
        )["PaymentReply"]
        return TransferPaymentReply(**response)

    def cash_login(self, pincode) -> BalancePaymentReply:
        """
        this function must be called before starting calling any cash function 
        it's so important because it save your wallet's pen 
        """
        self.pincode = pincode
        return BalancePaymentReply(
            self.__post(
                "/Saytar/rest/etisalatpay/service/CHECK_BALANCE",
                data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><PaymentRequest><ClientLanguageID>2</ClientLanguageID><MSISDN>{self.phone}</MSISDN><Password>{pincode}</Password><Username>{self.phone}</Username></PaymentRequest>",
            )
        )

    def get_cash_transactions(self, limit=None):
        """
        getting your etisalat cash wallet transactions history 
        from date 2021-01-01T00:00:00+00:00
        until now 
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        response = self.__post(
            "/Saytar/rest/etisalatpay/service/GET_TRANSACTIONS_HISTORY",
            data=f"<PaymentRequest><BNumber></BNumber><ClientLanguageID>2</ClientLanguageID><FromDate>2021-08-20T02:52:23+02:00</FromDate><MSISDN>{self.phone}</MSISDN><PageNumber>1</PageNumber><Password>{self.pincode}</Password><ServiceCodeFilter></ServiceCodeFilter><ToDate>{now}</ToDate><Username>{self.phone}</Username></PaymentRequest>",
        )
        Transactions = [
            Transaction(**tx)
            for trc in response["PaymentReply"]["TrxHistory"]["TrxHistoryPerMonth"]
            for tx in trc["TrxHistoryRecords"]["TrxHistoryRecord"]
        ]
        if limit == None or len(Transactions) < limit:
            return Transactions
        return Transactions[:limit]

    def send_verification_code(self):
        """
        Sending a verification code to complete the first login to MyEtisalat using this package
        """
        return SendVerificationCodeResponse(**self.xmltodict(
            requests.get(
                Constants.API_ENDPOINT
                + f"/Saytar/rest/quickAccess/sendVerCodeQuickAccessV2?sendVerCodeQuickAccessRequest=<sendVerCodeQuickAccessRequest><udid>{self.device_id}</udid><dial>{self.phone}</dial></sendVerCodeQuickAccessRequest>",
                headers=self.headers,
            ).text)["sendVerCodeQuickAccessResponseV2"]
    )

    @property
    def save_session(self) -> str:
        """
        Saving Current Seession so you do not have to login every time with the verification code
        next time you will use session_login function
        """
        return self.access_token
    def session_login(self, session):
        self.headers["Authorization"] = "Basic " + session
        self.access_token = session
        response = requests.post(
            Constants.API_ENDPOINT
            + "/Saytar/rest/quickAccess/loginQuickAccessWithPlan",
            data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginWlQuickAccessRequest><firstLoginAttempt>true</firstLoginAttempt><modelType>{self.device_name}</modelType><osVersion>{self.os_version}</osVersion><platform>{self.platform}</platform><wlUdid>{self.device_id}</wlUdid></loginWlQuickAccessRequest>",
            headers=self.headers,
        )
        self.session = response.cookies["JSESSIONID"]
        self.headers["cookie"] = "JSESSIONID=" + self.session + ";"
        data = self.xmltodict(response.text)["loginResponseWithPlan"]
        self.account_number = data["accountNumber"]
        data2 = self.__get(
            f"/Saytar/rest/account/profile?req=<getCustomerProfileV4Request><nativeToken/><firstLoginAttempt>true</firstLoginAttempt><serviceClass>2094</serviceClass><thirdPartyType>firebase</thirdPartyType><versionNum>22.10.1</versionNum><billingProfileId>1-31DW-1861</billingProfileId><language>2</language><accountNumber>{self.account_number}</accountNumber><deviceId>{self.device_id}</deviceId><platform>{self.platform}</platform><versionCode>507</versionCode><deviceModelType>{self.device_name}</deviceModelType><osVersion>{self.os_version}</osVersion><notificationToken>cEcfpO9cSTCgZU-ibNyJMJ:APA91bGuTW23IvvPGzQ2CaS1tBSDdQAWDezZDLje6rJTQy4uh2R_KT-2_YyeLzmoGj0vubIZKwnMSpDBOsQDP2XdE4dzLL2FRFbpbMUTiCpzeAFB9ngfeiNucd0YhtMxGQVdVfFMa8NH</notificationToken></getCustomerProfileV4Request>"
        )["getAccountProfileResponse"]["contracts"]["contract"]
        self.user = User(**{**data,**data2})
        return True
    def login_with_code(self, user_code):
        """
        with this function you should login with the verification code sent by send_verification_code function
        """
        data = self.__post(
            "/Saytar/rest/quickAccess/verifyCodeQuickAccess",
            f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><verifyCodeQuickAccessRequest><dial>{self.phone}</dial><udid>{self.device_id}</udid><verCode>{user_code}</verCode></verifyCodeQuickAccessRequest>",
        )
        if data.get("verifyCodeQuickAccessResponse", {}).get("pass") != None:
            self.account_password = data["verifyCodeQuickAccessResponse"]["pass"]
            session = (
                self.phone + "," + str(self.device_id) + ":" + self.account_password
            )
            self.basic_auth = base64.b64encode(session.encode("utf-8")).decode("ascii")
            self.headers["Authorization"] = "Basic " + self.basic_auth
            for x in range(10):
                response = requests.post(
                    Constants.API_ENDPOINT
                    + "/Saytar/rest/quickAccess/loginQuickAccessWithPlan",
                    data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginWlQuickAccessRequest><firstLoginAttempt>true</firstLoginAttempt><modelType>{self.device_name}</modelType><osVersion>{self.os_version}</osVersion><platform>{self.platform}</platform><wlUdid>{self.device_id}</wlUdid></loginWlQuickAccessRequest>",
                    headers=self.headers,
                )
                if "JSESSIONID" in response.cookies:
                    self.session = response.cookies["JSESSIONID"]
                    self.headers["cookie"] = "JSESSIONID=" + self.session + ";"
                    data1 = self.xmltodict(response.text)["loginResponseWithPlan"]
                    self.account_number = data1["accountNumber"]
                    data2 = self.__get(
                        f"/Saytar/rest/account/profile?req=<getCustomerProfileV4Request><nativeToken/><firstLoginAttempt>true</firstLoginAttempt><serviceClass>2094</serviceClass><thirdPartyType>firebase</thirdPartyType><versionNum>22.10.1</versionNum><billingProfileId>1-31DW-1861</billingProfileId><language>2</language><accountNumber>{self.account_number}</accountNumber><deviceId>{self.device_id}</deviceId><platform>{self.platform}</platform><versionCode>507</versionCode><deviceModelType>{self.device_name}</deviceModelType><osVersion>{self.os_version}</osVersion><notificationToken>cEcfpO9cSTCgZU-ibNyJMJ:APA91bGuTW23IvvPGzQ2CaS1tBSDdQAWDezZDLje6rJTQy4uh2R_KT-2_YyeLzmoGj0vubIZKwnMSpDBOsQDP2XdE4dzLL2FRFbpbMUTiCpzeAFB9ngfeiNucd0YhtMxGQVdVfFMa8NH</notificationToken></getCustomerProfileV4Request>"
                    )["getAccountProfileResponse"]["contracts"]["contract"]
                    self.user = User(**{**data1,**data2})
                    return True
                else:
                    raise ("Error Key JSESSIONID is not found")
        return False
    def zero11_get(self):
        """
        Get the eligiable 011 offers for the current user
        """
        return self.__get(
            f"/Saytar/rest/zero11/offers?req=<dialAndLanguageRequest><subscriberNumber>{self.phone}</subscriberNumber><language>2</language></dialAndLanguageRequest>"
        )["mabCategorizedProductsResponse"]["mabCategoryList"]

    def zero11_order(self, offer_id) -> SubmitResponse:
        """
        Redeem 011 offer which is obtained by zero11_get function
        """
        return SubmitResponse(
            self.__post(
                "/Saytar/rest/zero11/submitOrder",
                f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>{self.phone}</msisdn><operation>ACTIVATE</operation><parameters><parameter><name>GIFT_FULLFILMENT_PARAMETERS</name><value>Offer_ID:{offer_id};isRTIM:Y</value></parameter></parameters><productName>DYNAMIC_OFFERING_PAY_AND_GET_MI</productName></submitOrderRequest>",
            )
        )

    def __post(self, path, data):
        return self.xmltodict(
            requests.post(
                Constants.API_ENDPOINT + path, data=data, headers=self.headers
            ).text
        )

    def __get(self, path):
        return self.xmltodict(
            requests.get(Constants.API_ENDPOINT + path, headers=self.headers).text
        )

    def gettodaydailygift(self):
        gifts = []
        if self.gifts:
            gifts = self.gifts
        else:
            gifts = self.getdailygifts()
        for gift in gifts:
            if gift.today_gift == True:
                return gift

    def getdailygifts(self):
        print(self.__get(
                f"/Saytar/rest/dailyTipsWS/dailyTipGiftV3?req=%3CdailyTipRequest%3E%3CsubscriberNumber%3E{self.phone}%3C%2FsubscriberNumber%3E%3Clanguage%3E2%3C%2Flanguage%3E%3C%2FdailyTipRequest%3E"
            )["dailyTipNewResponse"])
        gifts = [
            Gift(
                gift["dailyTips"]["dailyTip"]["params"]["param"][2]["value"],
                gift["dayNum"],
                str(gift["dailyTips"]["dailyTip"]["redeemed"]),
                gift["dailyTips"]["dailyTip"]["todayGift"],
            )
            for gift in self.__get(
                f"/Saytar/rest/dailyTipsWS/dailyTipGiftV3?req=%3CdailyTipRequest%3E%3CsubscriberNumber%3E{self.phone}%3C%2FsubscriberNumber%3E%3Clanguage%3E2%3C%2Flanguage%3E%3C%2FdailyTipRequest%3E"
            )["dailyTipNewResponse"]["dailyList"]["dailyList"]
        ]
        self.gifts = gifts
        return gifts

    def claimtodaygift(self) -> SubmitResponse:
        return SubmitResponse(
            self.__post(
                f"/Saytar/rest/dailyTipsWS/submitOrder",
                f"<dailyTipsSubmitRequest><operationId>REDEEM</operationId><params><param><name>GIFT_ID</name><value>{self.gettodaydailygift().day}</value></param><param><name>CATEGORY</name><value>DAILY_TIPS_NEW</value></param></params><productId>DAILY_TIPS_GIFT</productId><subscriberNumber>{self.phone}</subscriberNumber></dailyTipsSubmitRequest>",
            )
        )

    def getbalance(self):
        """
        Get current User Balance
        """
        return self.__get(
            f"/Saytar/rest/servicemanagement/getGenericConsumptions?requestParam=<dialAndLanguageRequest><subscriberNumber>{self.phone}</subscriberNumber><language>2</language></dialAndLanguageRequest>"
        )["getConsumptionResponse"]["balance"]

    def scratchcard(self, voucher) -> RechargeResponse:
        """
        Balance Rechange using scratch card 
        """
        return RechargeResponse(
            self.__post(
                f"/Saytar/rest/digitalIncentive/recharge",
                data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><rechargeRequest><damagedFlag>false</damagedFlag><serialNumber></serialNumber><subscriberNumber>{self.phone}</subscriberNumber><voucherNumber>{voucher}</voucherNumber></rechargeRequest>",
            )
        )

    def callingnumbers(self):
        """
        Get the calling numbers for current users
        """
        return [item["secondDial"] for item in self.callhistory()]

    def callhistory(self):
        """
        Get the call log for current user
        """
        calls = []
        for days in range(30):
            past_date = str(datetime.today() - timedelta(days=days))
            data = self.__get(
                f"/Saytar/rest/services/accountHistory?req=<getCallHistoryV2Request><fromDate>{past_date}</fromDate><toDate>{past_date}</toDate><subscriberNumber>{self.phone}</subscriberNumber><type>0</type></getCallHistoryV2Request>"
            )
            print(data)
            if data["accountHistoryResponse"]["accountHistoryList"] == None:
                continue
            if (
                type(
                    data["accountHistoryResponse"]["accountHistoryList"][
                        "accountHistoryItem"
                    ]["historyTransactionsList"]["historyTransaction"]
                )
                is list
            ):
                for item in data["accountHistoryResponse"]["accountHistoryList"][
                    "accountHistoryItem"
                ]["historyTransactionsList"]["historyTransaction"]:
                    try:
                        if item["type"] == "1":
                            calls.append(item)
                    except Exception as error:
                        pass
            else:
                if (
                    data["accountHistoryResponse"]["accountHistoryList"][
                        "accountHistoryItem"
                    ]["historyTransactionsList"]["historyTransaction"]["type"]
                    == "1"
                ):
                    calls.append(item)
        return calls
