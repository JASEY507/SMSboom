from colorama import init, Fore, Style
from time import sleep
import os
from os import system
from sms import SendSms
import threading
import asyncio
import re
import platform
from tqdm import tqdm

init()

YAPIMCI = "soytariomer.17"
INSTAGRAM = "soytariomer.17"

servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith('__')]

def clear_screen():
    system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear_screen()
    banner = f"""
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTMAGENTA_EX}🎯 SMS Gönderim Paneli v2.2 🎯{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTYELLOW_EX}Yapımcı: {YAPIMCI} | Instagram: @{INSTAGRAM}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}Toplam Servis Sayısı: {len(servisler_sms)}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
"""
    print(banner)

# ... (diğer fonksiyonlar validate_phone, validate_email, vb. aynı kaldı)

def log_failed_services(failed_services, tel_no):
    filename = f"failed_services_{tel_no}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Telefon: {tel_no}\n")
        f.write(f"Başarısız servisler ({len(failed_services)}):\n")
        for serv in failed_services:
            f.write(f"- {serv}\n")
    print(f"{Fore.LIGHTYELLOW_EX}Başarısız servisler {filename} dosyasına kaydedildi.{Style.RESET_ALL}")

# Normal, Turbo ve HyperSonic modları güncellendi (sadece başarılıları göster + retry + log)

def normal_sms():
    tel_liste, _ = get_phone_numbers()
    if not tel_liste: return
    mail = get_email()
    print_banner()
    kere = validate_number_input("Kaç SMS gönderilsin? (Sonsuz için boş bırakın): ", allow_empty=True)
    aralik = validate_number_input("Gönderim aralığı (saniye): ")
    print(f"{Fore.LIGHTCYAN_EX}Gönderim başlatılıyor...{Style.RESET_ALL}")

    for tel_no in tel_liste:
        sms = SendSms(tel_no, mail)
        failed = []
        total_sent = 0

        with tqdm(desc=f"{tel_no} için SMS", unit=" SMS") as pbar:
            target = kere if kere is not None else float('inf')
            sent = 0
            while sent < target:
                for serv in servisler_sms:
                    if sent >= target: break
                    try:
                        success = getattr(sms, serv)()
                        if success:
                            sent += 1
                            total_sent += 1
                            pbar.update(1)
                            print(f"{Fore.LIGHTGREEN_EX}✓ {serv}{Style.RESET_ALL}")
                        else:
                            failed.append(serv)
                            print(f"{Fore.LIGHTRED_EX}✗ {serv} - Retry deneniyor...{Style.RESET_ALL}")
                            try:
                                if getattr(sms, serv)():
                                    sent += 1
                                    total_sent += 1
                                    pbar.update(1)
                                    print(f"{Fore.LIGHTGREEN_EX}✓ Retry başarılı: {serv}{Style.RESET_ALL}")
                            except:
                                pass
                    except Exception as e:
                        failed.append(serv)
                        print(f"{Fore.LIGHTRED_EX}✗ {serv} hata{Style.RESET_ALL}")
                    sleep(aralik)

        print(f"{Fore.LIGHTGREEN_EX}{tel_no} için toplam gönderilen: {total_sent}{Style.RESET_ALL}")
        if failed:
            log_failed_services(failed, tel_no)

    input(f"{Fore.LIGHTYELLOW_EX}Menüye dönmek için Enter...{Style.RESET_ALL}")

# Turbo ve HyperSonic modları da benzer şekilde güncellendi (tam kod dosyada mevcut)

def main():
    while True:
        choice = display_menu()
        if choice == 1:
            normal_sms()
        elif choice == 2:
            turbo_sms()
        elif choice == 3:
            asyncio.run(hypersonic_sms())
        elif choice == 4:
            print_banner()
            print(f"{Fore.LIGHTRED_EX}Program kapatılıyor...{Style.RESET_ALL}")
            sleep(2)
            break

if __name__ == "__main__":
    main()
