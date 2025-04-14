# email_delivery.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
import os
from dotenv import load_dotenv

# Load environment variables from .env file (create this file with your email credentials)
load_dotenv()

class EmailDelivery:
    def __init__(self):
        # Email configuration - get from environment variables for security
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL", "your-email@gmail.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "your-app-password")
    
    def send_newsletter(self, recipient_email, newsletter_markdown, subject=None):
        """
        Send newsletter via email
        
        Args:
            recipient_email (str): Email address of recipient
            newsletter_markdown (str): Newsletter content in markdown format
            subject (str, optional): Email subject. Defaults to "Your Personalized Newsletter".
        
        Returns:
            bool: Success status
        """
        if not subject:
            subject = "Your Personalized Newsletter"
        
        try:
            # Convert markdown to HTML for email
            newsletter_html = markdown.markdown(newsletter_markdown)
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Attach plain and HTML versions
            text_part = MIMEText(newsletter_markdown, "plain")
            html_part = MIMEText(newsletter_html, "html")
            message.attach(text_part)
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            print(f"Newsletter sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    # This is a test function to demonstrate email sending
    delivery = EmailDelivery()
    
    # Sample newsletter content
    with open("sample_newsletter.md", "r") as f:
        newsletter_content = f.read()
    
    # Send to test email
    recipient = "test@example.com"
    delivery.send_newsletter(recipient, newsletter_content, "Your Weekly Tech Newsletter")