import smtplib
from email.mime.text import MIMEText
from core.config import config


class EmailActions:
    async def send_demo(self, to_email: str, context: dict):
        if not to_email:
            return "❌ No email provided"

        try:
            msg = MIMEText("This is a demo email from AAROH AI Assistant.")
            msg["Subject"] = "AAROH Demo Email"
            msg["From"] = config.EMAIL_USER
            msg["To"] = to_email

            # NOTE: This is demo-safe (won’t crash if no credentials)
            if not config.EMAIL_USER or not config.EMAIL_PASS:
                return f"📧 (Demo Mode) Email simulated to {to_email}"

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(config.EMAIL_USER, config.EMAIL_PASS)
            server.sendmail(config.EMAIL_USER, to_email, msg.as_string())
            server.quit()

            return f"✅ Email sent to {to_email}"

        except Exception as e:
            return f"❌ Email failed: {str(e)}"