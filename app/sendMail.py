import smtplib, ssl
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailClient:
    def __init__(self, smtp_server, port, sender_email, sender_name, password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email  # Default sender email
        self.sender_name = sender_name  # Display name for the sender
        self.password = password
        self.context = ssl.create_default_context()

    def send_email(self, receiver_email, subject, body, image_path=None):
        # Create a multipart message for text + image
        msg = MIMEMultipart()
        msg['From'] = formataddr((self.sender_name, self.sender_email))
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the body text as HTML
        html_body = MIMEText(body, 'html')
        msg.attach(html_body)

        # Attach the image if provided
        if image_path:
            try:
                with open(image_path, 'rb') as img_file:
                    img = MIMEImage(img_file.read())
                    img.add_header('Content-Disposition', 'attachment', filename="welcome_image.jpg")
                    msg.attach(img)
            except Exception as e:
                print(f"Failed to attach image: {e}")

        try:
            # Connect to the server
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=self.context)  # Secure the connection
                server.ehlo()  # Can be omitted
                server.login(self.sender_email, self.password)

                # Send the email
                server.sendmail(self.sender_email, receiver_email, msg.as_string())
                print('Email sent successfully')
        except Exception as e:
            print(f"Failed to send email: {e}")

# Create an instance of the EmailClient class
email_client = EmailClient(
    smtp_server="smtp.gmail.com", 
    port=587, 
    sender_email="jimlestonosoi42@gmail.com", 
    sender_name="DAIRYFARMERS",  # Display name
    password="cxvs sdvg ayek jxbk"
)
