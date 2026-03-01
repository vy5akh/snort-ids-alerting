# Snort IDS Alerting System

A Network-Based Intrusion Detection System (NIDS) built using Snort 2.9 with custom detection rules and real-time mobile alerting via ntfy and ZeroTier.

This project demonstrates practical implementation of signature-based intrusion detection, automated alert parsing, and secure remote notification delivery in a virtual lab environment.

---

## 🔎 Project Overview

This system detects:

- ICMP Flood Attacks
- TCP SYN Flood Attacks (hping3)
- TCP Port Scanning (Nmap)

When an attack is detected:

1. Snort generates an alert
2. Alerts are written to `alert.fast`
3. A Python script parses the log in real-time
4. A formatted notification is sent to a self-hosted ntfy server
5. Alerts are delivered securely to a mobile device via ZeroTier

---

## 🏗️ Architecture

```text
Kali Linux (Attacker)
        ↓
Ubuntu 20.04 (Snort IDS)
        ↓
alert.fast log
        ↓
Python Monitoring Script
        ↓
ntfy Server
        ↓
ZeroTier Private Network
        ↓
Mobile Notification
```
---

## 🛡️ Features

- Custom Snort detection rules
- Threshold-based `detection_filter` logic
- Real-time log monitoring
- Fingerprint-based cooldown mechanism
- Mobile notification support
- ZeroTier secure overlay networking
- Fully isolated virtual lab environment

---

## 📂 Repository Structure

## 📂 Repository Structure

```text
snort-ids-alerting/
├── local.rules
├── snort_ntfy.py
├── README.md
└── SETUP.md
```
---

## 🚀 Quick Start

For full installation and configuration steps, see:

👉 **[SETUP.md](SETUP.md)**

---

## 🧪 Attack Testing

Example testing commands:

ICMP Flood: ping -f <TARGET_IP>

TCP SYN Flood: sudo hping3 -S --flood -p 80 <TARGET_IP>

Port Scan: nmap -sT -p 1-1000 <TARGET_IP>

---

## ⚠️ Limitations

- Signature-based detection only
- Detection mode (not IPS)
- Lab-scale testing environment
- Requires rule tuning for production deployment

---

## 🚀 Future Improvements

- Brute-force attack detection
- SIEM integration (ELK/Splunk)
- IPS inline mode
- Anomaly-based detection
- Production deployment testing

---

## 👨‍💻 Author

Vysakh B  
Bachelor of Computer Applications (Cybersecurity)
