from colorama import init, Fore, Style
from time import sleep
import os
from os import system
from sms import SendSms
import threading
import asyncio
import concurrent.futures
import re
from tqdm import tqdm  # İlerleme çubuğu için

# Colorama başlatma
init()

# Yapımcı bilgileri
YAPIMCI = "soytariomer.17"
INSTAGRAM = "omer.17___"

# SendSms sınıfındaki servisleri dinamik olarak çekme
servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith('__')]

def clear_screen():
    system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear_screen()
    banner = f"""
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTMAGENTA_EX}🎯 SMS Gönderim Paneli v2.1 🎯{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTYELLOW_EX}Yapımcı: {YAPIMCI} | Instagram: @{INSTAGRAM}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}Toplam Servis Sayısı: {len(servisler_sms)}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
"""
    print(banner)

def validate_phone(phone):
    """Telefon numarasını doğrula: 10 haneli ve sadece rakam."""
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Telefon numarası 10 haneli olmalı ve sadece rakamlardan oluşmalı!")
    return phone

def validate_email(email):
    """E-posta adresini doğrula: basit regex kontrolü."""
    if email == "":
        return email
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValueError("Geçersiz e-posta adresi!")
    return email

def validate_number_input(prompt, allow_empty=False):
    """Sayısal girişi doğrula."""
    while True:
        print(f"{Fore.LIGHTYELLOW_EX}{prompt}{Style.RESET_ALL}", end="")
        value = input()
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
    print(f"[3] SMS Gönder (HyperSonic Mod)")
    print(f"[4] Çıkış")
    print(f"{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}")
    return validate_number_input("Seçiminiz (1-4): ")

def get_phone_numbers():
    """Telefon numaralarını al: tek numara veya dosya."""
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
                for line in f.read().strip().split("\n"):
                    if line.strip():
                        tel_liste.append(validate_phone(line.strip()))
            return tel_liste, True  # True: sonsuz mod için
        except FileNotFoundError:
            print(f"{Fore.LIGHTRED_EX}Dosya bulunamadı! Lütfen geçerli bir dosya yolu girin.{Style.RESET_ALL}")
            sleep(3)
            return None, False
    else:
        try:
            tel_liste.append(validate_phone(tel_input))
            return tel_liste, False  # False: tek numara
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            sleep(3)
            return None, False

def get_email():
    """E-posta adresini al."""
    print_banner()
    print(f"{Fore.LIGHTGREEN_EX}E-posta adresini girin (boş bırakabilirsiniz):{Style.RESET_ALL}")
    while True:
        try:
            return validate_email(input(f"{Fore.LIGHTGREEN_EX}> "))
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            sleep(2)
            print_banner()
            print(f"{Fore.LIGHTGREEN_EX}E-posta adresini girin (boş bırakabilirsiniz):{Style.RESET_ALL}")

def normal_sms():
    """Normal mod: sırayla SMS gönderimi."""
    tel_liste, is_infinite = get_phone_numbers()
    if not tel_liste:
        return

    mail = get_email()
    print_banner()
    kere = validate_number_input("Kaç SMS gönderilsin? (Sonsuz için boş bırakın): ", allow_empty=True)
    aralik = validate_number_input("Gönderim aralığı (saniye): ")

    print(f"{Fore.LIGHTCYAN_EX}Gönderim başlatılıyor...{Style.RESET_ALL}")
    for tel_no in tel_liste:
        sms = SendSms(tel_no, mail)
        if kere is None:
            with tqdm(desc="Gönderilen SMS", unit=" SMS") as pbar:
                while True:
                    for serv in servisler_sms:
                        getattr(sms, serv)()
                        pbar.update(1)
                        sleep(aralik)
        else:
            with tqdm(total=kere, desc=f"{tel_no} için SMS", unit=" SMS") as pbar:
                while sms.adet < kere:
                    for serv in servisler_sms:
                        if sms.adet >= kere:
                            break
                        getattr(sms, serv)()
                        pbar.update(1)
                        sleep(aralik)
    print(f"{Fore.LIGHTGREEN_EX}Gönderim tamamlandı! Toplam: {sms.adet} SMS{Style.RESET_ALL}")
    input(f"{Fore.LIGHTYELLOW_EX}Menüye dönmek için Enter tuşuna basın...{Style.RESET_ALL}")

def turbo_sms():
    """Turbo mod: eşzamanlı SMS gönderimi."""
    tel_liste, _ = get_phone_numbers()
    if not tel_liste:
        return
    tel_no = tel_liste[0]  # Turbo modda sadece tek numara destekleniyor
    mail = get_email()

    send_sms = SendSms(tel_no, mail)
    stop_event = threading.Event()

    def turbo_loop():
        with tqdm(desc="Turbo Gönderim", unit=" SMS") as pbar:
            while not stop_event.is_set():
                threads = [threading.Thread(target=getattr(send_sms, serv), daemon=True) for serv in servisler_sms]
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                pbar.update(len(servisler_sms))

    print(f"{Fore.LIGHTCYAN_EX}Turbo gönderim başlatıldı. Durdurmak için CTRL+C tuşlayın.{Style.RESET_ALL}")
    try:
        turbo_loop()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"{Fore.LIGHTRED_EX}\nGönderim durduruldu. Toplam: {send_sms.adet} SMS{Style.RESET_ALL}")
        sleep(2)

async def hypersionic_sms_single(tel_no, mail, stop_event, pbar):
    """HyperSonic mod: Tek numara için asenkron SMS gönderimi."""
    send_sms = SendSms(tel_no, mail)
    while not stop_event.is_set():
        tasks = [asyncio.to_thread(getattr(send_sms, serv)) for serv in servisler_sms]
        await asyncio.gather(*tasks)
        pbar.update(len(servisler_sms))

async def hypersionic_sms():
    """HyperSonic mod: Çoklu numara için ultra hızlı SMS gönderimi."""
    tel_liste, _ = get_phone_numbers()
    if not tel_liste:
        return
    mail = get_email()
    stop_event = asyncio.Event()

    print(f"{Fore.LIGHTCYAN_EX}HyperSonic gönderim başlatıldı. Durdurmak için CTRL+C tuşlayın.{Style.RESET_ALL}")
    try:
        with tqdm(desc="HyperSonic Gönderim", unit=" SMS") as pbar:
            tasks = [hypersonic_sms_single(tel_no, mail, stop_event, pbar) for tel_no in tel_liste]
            await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        stop_event.set()
        print(f"{Fore.LIGHTRED_EX}\nHyperSonic gönderim durduruldu.{Style.RESET_ALL}")
        sleep(2)

def main():
    if platform.system() == "Emscripten":
        # Pyodide ortamı için asenkron çalıştırma
        asyncio.ensure_future(hypersonic_sms())
    else:
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
            else:
                print(f"{Fore.LIGHTRED_EX}Geçersiz seçim! 1, 2, 3 veya 4 girin.{Style.RESET_ALL}")
                sleep(2)

if __name__ == "__main__":
    main()
