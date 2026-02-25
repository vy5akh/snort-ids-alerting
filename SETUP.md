# Snort IDS Alerting System – Setup Guide

This guide explains how to install, configure, and run the Snort IDS Alerting System in a virtual lab environment.

---

# 📋 Requirements

## Monitoring Machine
- Ubuntu 20.04
- Root or sudo access
- Internet connection

## Attacker Machine (for testing)
- Kali Linux

---

# 1️⃣ Install Snort

Update packages:

```bash
sudo apt update
```

Install Snort:

```bash
sudo apt install snort
```

Verify installation:

```bash
snort -V
```

---

# 2️⃣ Configure Snort

Edit configuration file:

```bash
sudo nano /etc/snort/snort.conf
```

Modify or confirm the following settings:

```bash
# Define internal network
ipvar HOME_NET 192.168.225.0/24

# Define external network
ipvar EXTERNAL_NET !$HOME_NET

# Include custom rules
include $RULE_PATH/local.rules

# Enable fast alert logging
output alert_fast: alert.fast
```

Save and exit.

---

# 3️⃣ Add Custom Detection Rules

Open local rules file:

```bash
sudo nano /etc/snort/rules/local.rules
```

Paste the contents of `local.rules` from this repository.

Validate configuration:

```bash
sudo snort -T -c /etc/snort/snort.conf
```

If successful, you should see:

```
Snort successfully validated the configuration!
```

---

# 4️⃣ Start Snort

## Option A – Run as Service (Recommended)

```bash
sudo systemctl start snort
sudo systemctl status snort
```

## Option B – Run Manually

```bash
sudo snort -i enp0s3 -c /etc/snort/snort.conf -A fast
```

Replace `enp0s3` with your correct network interface.

Monitor alerts:

```bash
sudo tail -f /var/log/snort/alert.fast
```

---

# 5️⃣ Install Python Dependencies

Install pip:

```bash
sudo apt install python3-pip
```

Install required module:

```bash
pip3 install requests
```

---

# 6️⃣ Install and Configure ntfy

Install ntfy:

```bash
sudo snap install ntfy
```

Start ntfy server:

```bash
ntfy serve
```

By default, it runs on:

```
http://localhost:2586
```

---

# 7️⃣ Update snort_ntfy.py

Edit the script:

```bash
nano snort_ntfy.py
```

Update the notification URL:

```python
NTFY_URL = "http://<SERVER_IP>:2586/snort-alerts"
```

Example:

```python
NTFY_URL = "http://10.52.214.165:2586/snort-alerts"
```

---

# 8️⃣ (Optional) Setup ZeroTier for Remote Notifications

Install ZeroTier:

```bash
curl -s https://install.zerotier.com | sudo bash
```

Join network:

```bash
sudo zerotier-cli join <NETWORK_ID>
```

Verify:

```bash
zerotier-cli listnetworks
```

Use the assigned ZeroTier IP inside `snort_ntfy.py`.

---

# 9️⃣ Run Alert Monitoring Script

Start the Python script:

```bash
sudo python3 snort_ntfy.py
```

The script will:

- Monitor `/var/log/snort/alert.fast`
- Parse new alerts
- Apply 20-second cooldown
- Send formatted notifications to ntfy

---

# 🔟 Clear Logs Before Testing

```bash
sudo truncate -s 0 /var/log/snort/alert.fast
```

---

# 🧪 Attack Simulation (Testing)

## ICMP Flood

```bash
ping -f <TARGET_IP>
```

## TCP SYN Flood

```bash
sudo hping3 -S --flood -p 80 <TARGET_IP>
```

## Port Scan

```bash
nmap -sT -p 1-1000 <TARGET_IP>
```

---

# 📱 Mobile Setup

1. Install ntfy mobile app
2. Subscribe to:

```
http://<SERVER_IP>:2586/snort-alerts
```

You will now receive real-time intrusion alerts.

---

# 🧹 Troubleshooting

## Snort Not Starting

```bash
sudo systemctl status snort
```

## No Alerts Triggered

- Verify HOME_NET is correct
- Confirm correct interface
- Validate config using `snort -T`
- Ensure rules are loaded

## Python Script Not Sending Alerts

- Ensure ntfy server is running
- Confirm correct NTFY_URL
- Check firewall settings for port 2586

---

# 🔐 Security Notice

This system is intended for educational and laboratory use only.

Do not perform attack simulations on networks without proper authorization.
