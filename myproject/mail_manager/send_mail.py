#set up an email account
#SMTP >> Simple Mail Transfer Protocol 
import time
import logging
import smtplib, ssl
from smtplib import SMTPRecipientsRefused
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log_formatter = '%(asctime)s %(levelname)s %(filename)s(%(lineno)d) ::: %(message)s'
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=log_formatter, datefmt='%d-%m-%y %H:%M:%S')


class EmailSender:
    """ 
    Class to send an email with the news link. 
    """
    def __init__(self, keyword, email_to):
        """ 
        The constructor for Email SEnder class class. 
        Parameters: 
           keyword (str): Keyword of the search   
           email_to (str): email address of the reciptent 
        """
        self.email_to = email_to
        self.email_from = 'tracker.news.web@gmail.com'
        self.email_password = 'spyder.web727'
        self.keyword = keyword

    def generate_html_email(self, news_link_info):
        """ Method to generate the html body for the email
            Parameters:
                news_link_info (list): List of dicts with the info from the google news api
            Returns:
                html_body (str): string that contains the html generated. 
        """
        html_news = ""
        for link_info in news_link_info:
            html_news += ( """<p>
                                        <h2> <a href=%s> %s </a></h2>
                                            <p> 
                                                <h3> Source:  %s </h3> 
                                            </p>

                                            <p>
                                                <h3> Summary:  %s </h3> <br>
                                            </p>
                                        <img src=%s alt="Girl in a jacket" width="250" height="200">
                                </p>
                    """ % (link_info['url'], link_info['title'], link_info['source']['name'],link_info['description'], link_info['urlToImage']))

        html_body = ( """\
                            <html>
                                <body>
                                    <h1> NewsLetter Company %s </h1>
                                        <p>Hi,<br>
                                            How are you?<br>
                                            These are the most relevant articles that were found on the Internet. Hope you use the wisely!<br>
                                        </p>
                                        
                                        %s
                                    
                                </body>
                            </html>
                            """ % (self.keyword, html_news) ) 

        return html_body

    def send_email_with_news(self, news_link_info):
        """ Method to send the email using SMTP protocol
            Parameters:
                news_link_info (list): List of dicts with the info from the google news api
            Returns:
                bool: True if mail was sent successfully and False if it fails in the execution.
        """


        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "News Letter"
            message["From"] = self.email_from
            message["To"] = self.email_to 

            html_body = self.generate_html_email(news_link_info=news_link_info)
            part1 = MIMEText(html_body, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            message.attach(part1)

            port = 465  # For SSL
            # Create a secure SSL context
            context = ssl.create_default_context()

            start_time = time.time()
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: #Added Gmails SMTP Server
                server.login(self.email_from, self.email_password) #Login SMTP Library using your GMAIL
                server.sendmail(self.email_from, self.email_to, message.as_string())
                logger.info(f"Email sent to {self.email_to} in {round(time.time() - start_time, 4)} seconds")
                return True

        # manage mail exceptions
        except SMTPRecipientsRefused as e:
            logger.info(f"Error occured while sending email SMTPRecipientsRefused: {e}")
            return False




        
if __name__ == '__main__':
    mail = EmailSender(keyword='company_name', email_to='ffff')
    mail.send_email_with_news(news_link_info=[])
