import subprocess
import sys
import os
import threading
import re
from time import sleep
from os import system
import logging
import uuid

# Gerekli modüller
required_modules = ["colorama", "tqdm"]
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        response = input(f"{module} modülü yüklü değil. Yüklemek ister misiniz? (e/h): ")
        if response.lower() == 'e':
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        else:
            print(f"{module} modülü gerekli, program kapanıyor.")
            sys.exit(1)

from colorama import init, Fore, Style
from tqdm import tqdm
from sms import SendSms  # sms.py aynı klasörde olmalı

# Logging yapılandırması
logging.basicConfig(filename='sms_panel.log', level=logging.INFO, format='%(asctime)s - %(message)s')

init()

YAPIMCI = "soytariomer.17"
INSTAGRAM = "omer.17___"

# Servisleri dinamik çek (yalnızca SMS gönderim metodları)
servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith("__")]

def clear_screen():
    try:
        system("cls" if os.name == "nt" else "clear")
    except OSError:
        print("\n" * 50)  # Yedek: ekranı temizlemek için yeni satırlar

def print_banner():
    clear_screen()
    banner = f"""
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTMAGENTA_EX} SMS Gönderim Paneli v2.1 {Style.RESET_ALL}
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
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")

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
        if not os.path.exists(dizin):
            print(f"{Fore.LIGHTRED_EX}Dosya bulunamadı veya geçersiz yol!{Style.RESET_ALL}")
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
            return None
        try:
            with open(dizin, "r", encoding="utf-8") as f:
                for line in f.read().splitlines():
                    if line.strip():
                        tel_liste.append(validate_phone(line))
            return tel_liste
        except UnicodeDecodeError:
            print(f"{Fore.LIGHTRED_EX}Dosya UTF-8 formatında değil!{Style.RESET_ALL}")
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
            return None
        except PermissionError:
            print(f"{Fore.LIGHTRED_EX}Dosyaya erişim izni yok!{Style.RESET_ALL}")
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
            return None
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}Dosya bulunamadı!{Style.RESET_ALL}")
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
            return None
    else:
        try:
            tel_liste.append(validate_phone(tel_input))
            return tel_liste
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")
            return None

def get_email():
    print_banner()
    print(f"{Fore.LIGHTGREEN_EX}E-posta adresini girin (boş bırakabilirsiniz):{Style.RESET_ALL}")
    while True:
        try:
            return validate_email(input(f"{Fore.LIGHTGREEN_EX}> "))
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")

def normal_sms():
    tel_liste = get_phone_numbers()
    if not tel_liste:
        return
    mail = get_email()
    print_banner()
    kere = validate_number_input("Kaç SMS gönderilsin? (Sonsuz için boş bırakın): ", allow_empty=True)
    aralik = validate_number_input("Gönderim aralığı (saniye): ")

    max_iterations = 10000  # Sonsuz döngü koruması
    print(f"{Fore.LIGHTCYAN_EX}Gönderim başlatılıyor...{Style.RESET_ALL}")
    for tel_no in tel_liste:
        sms = SendSms(tel_no, mail)
        sms.adet = 0
        iteration = 0
        try:
            if kere is None:
                with tqdm(desc=f"{tel_no} için SMS", unit=" SMS") as pbar:
                    while iteration < max_iterations:
                        for serv in servisler_sms:
                            try:
                                getattr(sms, serv)()
                                sms.adet += 1
                                pbar.update(1)
                                logging.info(f"SMS gönderildi: {tel_no} - {serv}")
                            except Exception as e:
                                print(f"{Fore.LIGHTRED_EX}Hata ({serv}): {e}{Style.RESET_ALL}")
                                logging.error(f"Hata ({tel_no}, {serv}): {e}")
                                continue
                            sleep(aralik)
                        iteration += 1
            else:
                with tqdm(total=kere, desc=f"{tel_no} için SMS", unit=" SMS") as pbar:
                    while sms.adet < kere:
                        for serv in servisler_sms:
                            if sms.adet >= kere:
                                break
                            try:
                                getattr(sms, serv)()
                                sms.adet += 1
                                pbar.update(1)
                                logging.info(f"SMS gönderildi: {tel_no} - {serv}")
                            except Exception as e:
                                print(f"{Fore.LIGHTRED_EX}Hata ({serv}): {e}{Style.RESET_ALL}")
                                logging.error(f"Hata ({tel_no}, {serv}): {e}")
                                continue
                            sleep(aralik)
        except KeyboardInterrupt:
            print(f"{Fore.LIGHTRED_EX}\nGönderim durduruldu. Toplam: {sms.adet} SMS ({tel_no}){Style.RESET_ALL}")
            logging.info(f"Gönderim durduruldu: {tel_no} - Toplam {sms.adet} SMS")
            input(f"{Fore.LIGHTYELLOW_EX}Menüye dönmek için Enter tuşuna basın...{Style.RESET_ALL}")
            return
        print(f"{Fore.LIGHTGREEN_EX}Gönderim tamamlandı! Toplam: {sms.adet} SMS ({tel_no}){Style.RESET_ALL}")
        logging.info(f"Gönderim tamamlandı: {tel_no} - Toplam {sms.adet} SMS")
    input(f"{Fore.LIGHTYELLOW_EX}Menüye dönmek için Enter tuşuna basın...{Style.RESET_ALL}")

def turbo_sms():
    tel_liste = get_phone_numbers()
    if not tel_liste:
        return
    mail = get_email()

    lock = threading.Lock()
    stop_event = threading.Event()

    def send_for_number(tel_no, mail, pbar):
        send_sms = SendSms(tel_no, mail)
        send_sms.adet = 0
        while not stop_event.is_set():
            threads = [
                threading.Thread(
                    target=lambda s=serv: [
                        getattr(send_sms, s)(),
                        lock.acquire(),
                        send_sms.adet += 1,
                        lock.release(),
                        pbar.update(1),
                        logging.info(f"SMS gönderildi: {tel_no} - {s}")
                    ] if not stop_event.is_set() else None,
                    daemon=True
                ) for serv in servisler_sms
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        return send_sms.adet

    print(f"{Fore.LIGHTCYAN_EX}Turbo gönderim başlatıldı. Durdurmak için CTRL+C tuşlayın.{Style.RESET_ALL}")
    try:
        with tqdm(desc="Turbo Gönderim", unit=" SMS") as pbar:
            threads = [threading.Thread(target=send_for_number, args=(tel_no, mail, pbar), daemon=True) for tel_no in tel_liste]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"{Fore.LIGHTRED_EX}\nGönderim durduruldu.{Style.RESET_ALL}")
        logging.info("Turbo gönderim durduruldu")
        input(f"{Fore.LIGHTYELLOW_EX}Menüye dönmek için Enter tuşuna basın...{Style.RESET_ALL}")

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
            logging.info("Program kapatıldı")
            sleep(2)
            break
        else:
            print(f"{Fore.LIGHTRED_EX}Geçersiz seçim! 1, 2 veya 3 girin.{Style.RESET_ALL}")
            input(f"{Fore.LIGHTYELLOW_EX}Devam etmek için Enter tuşuna basın...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
