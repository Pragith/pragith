import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class MailerService:
    def _build_smtp(self):
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        return server

    def verify_recaptcha(self, token: str, expected_action: str = "submit_contact") -> bool:
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
            resp = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data=payload,
                timeout=5,
            )
            resp.raise_for_status()
            result = resp.json()
            
            # v3 returns a score between 0.0 (bot) and 1.0 (human)
            success = result.get('success', False)
            score = result.get('score', 0.0)
            action = result.get('action', '')
            
            print(f"reCAPTCHA v3 score: {score}")
            
            # Threshold: 0.5 is recommended by Google
            return success and score >= 0.5 and action == expected_action
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
            
            with self._build_smtp() as server:
                server.send_message(msg)
                
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def _demo_credentials_block(self) -> str:
        return (
            "Dashboard Demo Credentials\n"
            "--------------------------\n"
            f"URL: {settings.DASHBOARD_DEMO_URL}\n"
            f"Username: {settings.DASHBOARD_DEMO_USER or '[not configured]'}\n"
            f"Password: {settings.DASHBOARD_DEMO_PASSWORD or '[not configured]'}"
        )

    def send_dashboard_demo_access_email(
        self,
        name: str,
        email: str,
        company: str,
        role: str,
        notes: str,
        ref_page: str,
        cta_id: str,
        utm_source: str,
        utm_medium: str,
        utm_campaign: str,
        utm_content: str,
    ) -> bool:
        try:
            demo_block = self._demo_credentials_block()

            inbound = MIMEMultipart()
            inbound["From"] = settings.MAIL_FROM
            inbound["To"] = settings.MAIL_TO
            inbound["Subject"] = f"[Dashboard Demo Access] {name}"
            inbound_body = f"""
            Dashboard Demo Access Request
            -----------------------------
            Name: {name}
            Email: {email}
            Company: {company or '-'}
            Role: {role or '-'}
            Ref Page: {ref_page or '-'}
            CTA ID: {cta_id or '-'}
            UTM Source: {utm_source or '-'}
            UTM Medium: {utm_medium or '-'}
            UTM Campaign: {utm_campaign or '-'}
            UTM Content: {utm_content or '-'}

            Notes:
            {notes or '-'}

            {demo_block}
            """
            inbound.attach(MIMEText(inbound_body, "plain"))

            requester = MIMEMultipart()
            requester["From"] = settings.MAIL_FROM
            requester["To"] = email
            requester["Subject"] = "Your Pragith Dashboard Demo Access"
            requester_body = f"""
            Hi {name},

            Thanks for requesting dashboard demo access. You can use the credentials below:

            {demo_block}

            If access does not work, reply to this email and we will reset the demo account.
            """
            requester.attach(MIMEText(requester_body, "plain"))

            with self._build_smtp() as server:
                server.send_message(inbound)
                server.send_message(requester)

            return True
        except Exception as e:
            print(f"Failed to send dashboard demo access email: {e}")
            return False

mailer_service = MailerService()
