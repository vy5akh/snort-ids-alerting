import time
import requests

# ================= CONFIG =================
ALERT_FILE = "/var/log/snort/alert.fast"
# Replace <SERVER_IP> with your ntfy server address
NTFY_URL = "http://<SERVER_IP>:2586/snort-alerts"

COOLDOWN = 20  # seconds
last_sent = {}
# ==========================================

def send_notification(title, message):
    headers = {
        "Title": title,
        "Priority": "4"
    }
    r = requests.post(NTFY_URL, data=message, headers=headers)
    print("Sent to ntfy:", r.status_code)

def parse_alert(line):

    raw_ts = line.split()[0]
    date_part, time_part = raw_ts.split("-")

    date = date_part
    time_only = time_part.split(".")[0]

    parts = line.split()
    rule_id = parts[3].strip("[]")

    msg = line.split("] ", 2)[2].split(" [**]")[0]

    proto = line.split("{")[1].split("}")[0]

    src, dst = line.split("}")[-1].strip().split(" -> ")

    src_ip = src.split(":")[0]
    dst_ip = dst.split(":")[0]

    return {
        "date": date,
        "time": time_only,
        "rule": rule_id,
        "msg": msg,
        "proto": proto,
        "src_ip": src_ip,
        "dst_ip": dst_ip
    }

print("[*] Snort -> ntfy watcher started")
print("[*] Watching:", ALERT_FILE)

with open(ALERT_FILE, "r") as f:
    f.seek(0, 2)

    while True:
        line = f.readline()
        if not line:
            time.sleep(0.5)
            continue

        line = line.strip()
        if not line:
            continue

        try:
            alert = parse_alert(line)
        except Exception as e:
            print("Parse error:", e)
            continue

        fingerprint = f"{alert['rule']}_{alert['src_ip']}_{alert['dst_ip']}"
        now = time.time()

        if fingerprint in last_sent and now - last_sent[fingerprint] < COOLDOWN:
            continue

        last_sent[fingerprint] = now

        title = f"Snort Alert: {alert['proto']} Activity"

        body = (
            "ALERT DETECTED\n\n"
            f"Date       : {alert['date']}\n"
            f"Time       : {alert['time']}\n"
            f"Rule ID    : {alert['rule']}\n"
            f"Category   : {alert['msg']}\n\n"
            f"Source IP  : {alert['src_ip']}\n"
            f"Dest IP    : {alert['dst_ip']}\n"
            f"Protocol   : {alert['proto']}"
        )

        print("[ALERT]", alert["msg"])
        send_notification(title, body)
