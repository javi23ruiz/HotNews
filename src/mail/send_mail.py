#set up an email account
#SMTP >> Simple Mail Transfer Protocol 

import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self):
        self.email_to = 'jrruiz1995@gmail.com'
        self.email_from = 'tracker.news.web@gmail.com'
        self.email_password = 'spyder.web727'

    def send_email_with_news():
        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = self.email_from
        message["To"] = self.email_to 

        # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        How are you?
        Real Python has many great tutorials:
        www.realpython.com"""

        html = """\
        <html>
        <body>
            <h1> NewsLetter Company X1</h1>
                <p>Hi,<br>
                    How are you?<br>
                    These are the most relevant articles that were found on the Internet. Hope you use the wisely!<br>
                </p>

                <p>
                    <h3> <a href="https://lifehacker.com/how-to-watch-apple-tvs-new-mtv-style-music-channel-1845429371">Titulo noticia</a></h3>
                    
                    <p>
                        Summary: This is a summary generated with AI <br>
                    </p>

                    <img src="https://i.kinja-img.com/gawker-media/image/upload/c_fill,f_auto,fl_progressive,g_center,h_675,pg_1,q_80,w_1200/djgs372gk8q9fskkytqq.png" alt="Girl in a jacket" width="250" height="200">
                </p>

                <p>
                    <h3> <a href="https://lifehacker.com/how-to-watch-apple-tvs-new-mtv-style-music-channel-1845429371">Titulo noticia</a></h3>
                    <br>
                    Summary: This is a summary generated with AI <br>
                    <img src="https://i.kinja-img.com/gawker-media/image/upload/c_fill,f_auto,fl_progressive,g_center,h_675,pg_1,q_80,w_1200/djgs372gk8q9fskkytqq.png" alt="Girl in a jacket" width="250" height="200">

                </p>
                
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        ###send email###
        port = 465  # For SSL
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: #Added Gmails SMTP Server
            server.login(email_from, email_password) #This command Login SMTP Library using your GMAIL
            server.sendmail(email_from, email_to, message.as_string()) #This Sends the message
            logging.info(f"Email sent")

        pass

if __name__ == '__mian__':
    pass