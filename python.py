cat > python.py << 'EOF'
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

# ===================== AYARLAR =====================
YAPIMCI = "soytariomer.17"
INSTAGRAM = "soytariomer.17"

servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith('__')]

def clear_screen():
    system("cls" if os.name == "nt" else "clear")

def print_banner():
    clear_screen()
    banner = f"""
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTMAGENTA_EX}🎯 SMS Gönderim Paneli v2.3 🎯{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
{Fore.LIGHTYELLOW_EX}Yapımcı: {YAPIMCI} | Instagram: @{INSTAGRAM}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}Toplam Servis: {len(servisler_sms)}{Style.RESET_ALL}
{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}
"""
    print(banner)

def validate_phone(phone):
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Telefon numarası 10 haneli ve sadece rakam olmalıdır!")
    return phone

def validate_email(email):
    if not email: return ""
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise ValueError("Geçersiz e-posta adresi!")
    return email

def validate_number_input(prompt, allow_empty=False, max_value=None):
    while True:
        print(f"{Fore.LIGHTYELLOW_EX}{prompt}{Style.RESET_ALL}", end="")
        value = input().strip()
        if allow_empty and not value:
            return None
        try:
            num = int(value)
            if max_value and num > max_value:
                print(f"{Fore.LIGHTRED_EX}Hatalı! 1-{max_value} arası girin.{Style.RESET_ALL}")
                sleep(1.5)
                continue
            return num
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Sadece sayı giriniz.{Style.RESET_ALL}")
            sleep(1.5)

def display_menu():
    print_banner()
    print(f"{Fore.LIGHTBLUE_EX}[1] Normal Mod")
    print(f"[2] Turbo Mod")
    print(f"[3] HyperSonic Mod")
    print(f"[4] Çıkış")
    print(f"{Fore.LIGHTCYAN_EX}{'═' * 60}{Style.RESET_ALL}")
    return validate_number_input("Seçiminiz (1-4): ", max_value=4)

def get_phone_numbers():
    print_banner()
    print(f"{Fore.LIGHTGREEN_EX}Telefon numarası (10 haneli) veya dosya yolu:{Style.RESET_ALL}")
    inp = input(f"{Fore.LIGHTGREEN_EX}> ").strip()
    
    if not inp:
        path = input(f"{Fore.LIGHTYELLOW_EX}Numara listesi dosyası: {Style.RESET_ALL}").strip()
        try:
            with open(path, "r", encoding="utf-8") as f:
                numbers = [validate_phone(line.strip()) for line in f if line.strip()]
            return numbers, True
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Dosya okunamadı: {e}{Style.RESET_ALL}")
            sleep(3)
            return None, False
    else:
        try:
            return [validate_phone(inp)], False
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            sleep(3)
            return None, False

def get_email():
    print_banner()
    print(f"{Fore.LIGHTGREEN_EX}E-posta (isteğe bağlı):{Style.RESET_ALL}")
    while True:
        try:
            return validate_email(input(f"{Fore.LIGHTGREEN_EX}> "))
        except ValueError as e:
            print(f"{Fore.LIGHTRED_EX}{e}{Style.RESET_ALL}")
            sleep(2)

def log_failed_services(failed, tel_no):
    filename = f"failed_services_{tel_no}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Telefon: {tel_no}\n")
        f.write(f"Başarısız servis sayısı: {len(failed)}\n\n")
        for s in failed:
            f.write(f"- {s}\n")
    print(f"{Fore.LIGHTYELLOW_EX}Başarısız servisler '{filename}' dosyasına kaydedildi.{Style.RESET_ALL}")

# ==================== NORMAL MOD ====================
def normal_sms():
    tel_liste, _ = get_phone_numbers()
    if not tel_liste: return
    mail = get_email()
    print_banner()
    kere = validate_number_input("Kaç SMS gönderilsin? (Sonsuz için boş): ", allow_empty=True)
    aralik = validate_number_input("Gönderim aralığı (saniye): ") or 0

    for tel_no in tel_liste:
        sms = SendSms(tel_no, mail)
        failed_services = []
        total_sent = 0

        with tqdm(desc=f"{tel_no}", unit=" SMS") as pbar:
            target = kere if kere is not None else float('inf')
            sent = 0
            while sent < target:
                for serv in servisler_sms:
                    if sent >= target: break
                    try:
                        if getattr(sms, serv)():
                            sent += 1
                            total_sent += 1
                            pbar.update(1)
                            print(f"{Fore.LIGHTGREEN_EX}✓ {serv}{Style.RESET_ALL}")
                        else:
                            failed_services.append(serv)
                            print(f"{Fore.LIGHTRED_EX}✗ {serv} → Tekrar deneniyor...{Style.RESET_ALL}")
                            try:
                                if getattr(sms, serv)():
                                    sent += 1
                                    total_sent += 1
                                    pbar.update(1)
                                    print(f"{Fore.LIGHTGREEN_EX}✓ Retry başarılı: {serv}{Style.RESET_ALL}")
                            except:
                                pass
                    except Exception:
                        failed_services.append(serv)
                        print(f"{Fore.LIGHTRED_EX}✗ {serv} hatası{Style.RESET_ALL}")
                    sleep(aralik)

        print(f"{Fore.LIGHTGREEN_EX}{tel_no} için toplam gönderilen: {total_sent}{Style.RESET_ALL}")
        if failed_services:
            log_failed_services(failed_services, tel_no)

    input(f"\n{Fore.LIGHTYELLOW_EX}Menüye dönmek için Enter...{Style.RESET_ALL}")

def main():
    while True:
        choice = display_menu()
        if choice == 1:
            normal_sms()
        elif choice in (2, 3):
            print(f"{Fore.LIGHTRED_EX}Bu mod henüz güncellenmedi. Normal Mod önerilir.{Style.RESET_ALL}")
            sleep(2)
        elif choice == 4:
            print_banner()
            print(f"{Fore.LIGHTRED_EX}Program kapatılıyor...{Style.RESET_ALL}")
            sleep(1.5)
            break

if __name__ == "__main__":
    main()
EOF
