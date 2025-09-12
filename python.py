import subprocess
import sys
import os
import threading
import re
from time import sleep
from os import system

# Gerekli modüller
required_modules = ["colorama", "tqdm"]
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"{module} modülü yüklü değil, yükleniyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

from colorama import init, Fore, Style
from tqdm import tqdm
from sms import SendSms  # sms.py aynı klasörde olmalı

init()

YAPIMCI = "soytariomer.17"
INSTAGRAM = "omer.17___"

# Servisleri dinamik çek
servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith("__")]

def clear_screen():
    system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear_screen()
    banner = f"""
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTMAGENTA_EX} SMS Gönderim Paneli v2.0 {Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTYELLOW_EX}Yapımcı: {YAPIMCI} | Instagram: @{INSTAGRAM}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}Toplam Servis Sayısı: {len(servisler_sms)}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
"""
    print(banner)

def validate_phone(phone):
    phone = phone.strip()
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Telefon numarası 10 haneli olmalı ve sadece rakamlardan oluşmalı!")
    return phone

def validate_email(email):
    if email == "":
        return email
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValueError("Geçersiz e-posta adresi!")
    return email

def validate_number_input(prompt, allow_empty=False):
    while True:
        value = input(f"{Fore.LIGHTYELLOW_EX}{prompt}{Style.RESET_ALL}")
        if allow_empty and value.strip() == "":
            return None
        try:
            return int(value)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Hatalı giriş! Sadece sayı giriniz.{Style.RESET_ALL}")
            sleep(2)

def display_menu():
    print_banner()
    print(f"{Fore.LIGHTBLUE_EX}[1] SMS Gönder (Normal Mod)")
    print(f"[2] SMS Gönder (Turbo Mod)")
    print(f"[3] Çıkış")
    print(f"{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}")
    return validate_number_input("Seçiminiz (1-3): ")

def get_phone_numbers():
    print_banner()
    print(f"{Fore.LIGHTGREEN_EX}Telefon numarasını girin (10 haneli, +90 olmadan):{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}Birden fazla numara için dosya yolunu girin veya boş bırakın:{Style.RESET_ALL}")
    tel_input = input(f"{Fore.LIGHTGREEN_EX}> ")

    tel_liste = []
    if tel_input.strip() == "":
        print(f"{Fore.LIGHTYELLOW_EX}Numaraların bulunduğu dosya yolunu girin:{Style.RESET_ALL}")
        dizin = input(f"{Fore.LIGHTGREEN_EX}> ")
        try:
            with open(dizin, "r", encoding="utf-8") as f:
                for line in f.read().splitlines():
                    if line.strip():
                        tel_liste.append(validate_phone(line))
            return tel_liste, True
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}Dosya bulunamadı!{Style.RESET_ALL}")
            sleep(3)
            return None, False
    else:
        try:
            tel_liste.append(validate_phone(tel_input))
            return tel_liste, False
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            sleep(3)
            return None, False

def get_email():
    print_banner()
    print(f"{Fore.LIGHTGREEN_EX}E-posta adresini girin (boş bırakabilirsiniz):{Style.RESET_ALL}")
    while True:
        try:
            return validate_email(input(f"{Fore.LIGHTGREEN_EX}> "))
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            sleep(2)

def normal_sms():
    tel_liste, _ = get_phone_numbers()
    if not tel_liste:
        return
    mail = get_email()
    print_banner()
    kere = validate_number_input("Kaç SMS gönderilsin? (Sonsuz için boş bırakın): ", allow_empty=True)
    aralik = validate_number_input("Gönderim aralığı (saniye): ")

    print(f"{Fore.LIGHTCYAN_EX}Gönderim başlatılıyor...{Style.RESET_ALL}")
    for tel_no in tel_liste:
        sms = SendSms(tel_no, mail)
        sms.adet = 0
        try:
            if kere is None:
                with tqdm(desc="Gönderilen SMS", unit=" SMS") as pbar:
                    while True:
                        for serv in servisler_sms:
                            getattr(sms, serv)()
                            sms.adet += 1
                            pbar.update(1)
                            sleep(aralik)
            else:
                with tqdm(total=kere, desc=f"{tel_no} için SMS", unit=" SMS") as pbar:
                    while sms.adet < kere:
                        for serv in servisler_sms:
                            if sms.adet >= kere:
                                break
                            getattr(sms, serv)()
                            sms.adet += 1
                            pbar.update(1)
                            sleep(aralik)
        except KeyboardInterrupt:
            print(f"{Fore.LIGHTRED_EX}\nGönderim durduruldu. Toplam: {sms.adet} SMS{Style.RESET_ALL}")
            sleep(2)
            return
    print(f"{Fore.LIGHTGREEN_EX}Gönderim tamamlandı! Toplam: {sms.adet} SMS{Style.RESET_ALL}")
    input(f"{Fore.LIGHTYELLOW_EX}Menüye dönmek için Enter tuşuna basın...{Style.RESET_ALL}")

def turbo_sms():
    tel_liste, _ = get_phone_numbers()
    if not tel_liste:
        return
    tel_no = tel_liste[0]
    mail = get_email()

    send_sms = SendSms(tel_no, mail)
    send_sms.adet = 0
    stop_event = threading.Event()

    def turbo_loop():
        with tqdm(desc="Turbo Gönderim", unit=" SMS") as pbar:
            while not stop_event.is_set():
                threads = [threading.Thread(target=getattr(send_sms, serv), daemon=True) for serv in servisler_sms]
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                    send_sms.adet += 1
                pbar.update(len(servisler_sms))

    print(f"{Fore.LIGHTCYAN_EX}Turbo gönderim başlatıldı. Durdurmak için CTRL+C tuşlayın.{Style.RESET_ALL}")
    try:
        turbo_loop()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"{Fore.LIGHTRED_EX}\nGönderim durduruldu. Toplam: {send_sms.adet} SMS{Style.RESET_ALL}")
        sleep(2)

def main():
    while True:
        choice = display_menu()
        if choice == 1:
            normal_sms()
        elif choice == 2:
            turbo_sms()
        elif choice == 3:
            print_banner()
            print(f"{Fore.LIGHTRED_EX}Program kapatılıyor...{Style.RESET_ALL}")
            sleep(2)
            break
        else:
            print(f"{Fore.LIGHTRED_EX}Geçersiz seçim! 1, 2 veya 3 girin.{Style.RESET_ALL}")
            sleep(2)

if __name__ == "__main__":
    main()
