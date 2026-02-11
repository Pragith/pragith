import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class MailerService:
    def verify_recaptcha(self, token: str) -> bool:
        """
        Verifies reCAPTCHA v3 token with Google.
        Returns True if score >= 0.5 (likely human).
        """
        if not settings.RECAPTCHA_SECRET_KEY:
            print("WARNING: RECAPTCHA_SECRET_KEY is missing.")
            return True  # Allow form submission if CAPTCHA not configured

        payload = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token
        }
        
        try:
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
            resp.raise_for_status()
            result = resp.json()
            
            # v3 returns a score between 0.0 (bot) and 1.0 (human)
            success = result.get('success', False)
            score = result.get('score', 0.0)
            
            print(f"reCAPTCHA v3 score: {score}")
            
            # Threshold: 0.5 is recommended by Google
            return success and score >= 0.5
        except Exception as e:
            print(f"reCAPTCHA verification failed: {e}")
            return False

    def send_contact_email(self, name: str, email: str, inquiry_type: str, message: str) -> bool:
        """
        Sends contact form submission via SMTP.
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.MAIL_FROM
            msg['To'] = settings.MAIL_TO
            msg['Subject'] = f"[{inquiry_type}] New inquiry from {name}"
            
            body = f"""
            New Contact Request
            -------------------
            Name: {name}
            Email: {email}
            Inquiry Type: {inquiry_type}
            
            Message:
            {message}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                # Only login if credentials are provided (some local SMTPs don't need it)
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
                
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

mailer_service = MailerService()
