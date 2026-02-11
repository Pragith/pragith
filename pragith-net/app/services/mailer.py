import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class MailerService:
    def verify_recaptcha(self, token: str) -> bool:
        """
        Verifies reCAPTCHA v2 token with Google.
        """
        if not settings.RECAPTCHA_SECRET_KEY:
             # In strict prod, fail. Logic same as before.
            print("WARNING: RECAPTCHA_SECRET_KEY is missing.")
            return False

        payload = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token
        }
        
        try:
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
            resp.raise_for_status()
            result = resp.json()
            return result.get('success', False)
        except Exception as e:
            print(f"reCAPTCHA verification failed: {e}")
            return False

    def send_contact_email(self, name: str, email: str, company: str, message: str) -> bool:
        """
        Sends contact form submission via SMTP.
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.MAIL_FROM
            msg['To'] = settings.MAIL_TO
            msg['Subject'] = f"New Contact from {name} ({company})"
            
            body = f"""
            New Contact Request
            -------------------
            Name: {name}
            Email: {email}
            Company: {company}
            
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
