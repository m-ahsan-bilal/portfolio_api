# Email Notification System for Contact Form
# This will send you an email whenever someone submits the contact form

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

class EmailNotifier:
    def __init__(self):
        # Email configuration - you'll need to set these up
        self.sender_email = os.getenv("SENDER_EMAIL", "ahsan123.bilal@gmail.com")
        self.sender_password = os.getenv("SENDER_PASSWORD", "ajwb qijf gibx lhif")
        self.admin_email = os.getenv("ADMIN_EMAIL", "ahsan123.bilal@gmail.com")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
    def send_contact_notification(self, contact_data):
        """
        Send email notification when contact form is submitted
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.admin_email
            msg['Subject'] = f"New Contact Form Submission - {contact_data['topic']}"
            
            # Create email body
            body = f"""
            📧 New Contact Form Submission
            
            From: {contact_data['email']}
            Topic: {contact_data['topic']}
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Message:
            {contact_data['message']}
            
            ---
            This is an automated notification from your portfolio contact form.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.admin_email, text)
            server.quit()
            
            print(f"✅ Email notification sent to {self.admin_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def send_daily_summary(self, submissions):
        """
        Send daily summary of all submissions
        """
        if not submissions:
            return True
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.admin_email
            msg['Subject'] = f"Daily Contact Form Summary - {datetime.now().strftime('%Y-%m-%d')}"
            
            body = f"""
            📊 Daily Contact Form Summary
            
            Date: {datetime.now().strftime('%Y-%m-%d')}
            Total Submissions: {len(submissions)}
            
            Recent Submissions:
            """
            
            for submission in submissions[-5:]:  # Last 5 submissions
                body += f"""
                ---
                ID: {submission.get('id')}
                From: {submission.get('email')}
                Topic: {submission.get('topic')}
                Date: {submission.get('timestamp')}
                Message: {submission.get('message')[:100]}...
                """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, self.admin_email, text)
            server.quit()
            
            print(f"✅ Daily summary sent to {self.admin_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending daily summary: {e}")
            return False

