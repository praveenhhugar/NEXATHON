import smtplib
from email.mime.text import MIMEText
import threading

# ==========================================
# ⚠️ EDIT THESE THREE LINES BEFORE RUNNING ⚠️
# ==========================================
# 1. Your new dummy Gmail address
SENDER_EMAIL = "deceptoralerts@gmail.com"

# 2. The 16-letter App Password from Google (REMOVE ALL SPACES)
SENDER_PASSWORD = "frugsusrtekczvis"
# 3. Where to send the alert (Use the same dummy email for testing)
RECEIVER_EMAIL = "deceptoralerts@gmail.com"
# ==========================================


def send_alert(ip_address):
    """Sends an email in a background thread so it doesn't freeze the server."""
    def _send():
        try:
            # Create the email content
            msg = MIMEText(f"""
            🚨 DECEPTOR AI SECURITY ALERT 🚨

            VERIFIED ENGAGEMENT DETECTED
            An unknown user has triggered a Honeytoken in the decoy environment.

            Attacker IP: {ip_address}
            Inferred Intent: Credential Harvesting / Reconnaissance
            
            ACTION TAKEN: 
            The IP has been automatically moved to the Firewall Blocklist.
            They are now locked out of the system.

            Evidence: The attacker attempted to use the planted fake credential.
            """)
            
            msg['Subject'] = f"🚨 URGENT: Honeytoken Triggered by {ip_address}"
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL

            
            # Connect to Gmail's server and send (Using SSL Port 465)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            server.quit()
            
            print(f"[*] EMAIL SENT TO COMPANY: Alert for {ip_address}")
            
        except Exception as e:
            print(f"[!] Failed to send email: {e}")
            print("[!] Check if you are using a 16-letter App Password (no spaces).")

    # Run in a background thread
    threading.Thread(target=_send).start()