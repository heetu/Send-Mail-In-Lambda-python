import smtplib
import os

def send_email(host, port, username, password, subject, body, mail_to, mail_from = None, reply_to = None):
    if mail_from is None: mail_from = username
    if reply_to is None: reply_to = mail_to
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (mail_from, mail_to, subject, body)
    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(mail_from, mail_to, message)
        server.close()
        return True
    except Exception as ex:
        print (ex)
        return False
        
def lambda_handler(event, context):
    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    host = os.environ['SMTPHOST']
    port = os.environ['SMTPPORT']
    mail_from = os.environ.get('MAIL_FROM')
    mail_to = os.environ['MAIL_TO']     # separate multiple recipient by comma. eg: "abc@gmail.com, xyz@gmail.com"
    subject = "Hello from DataVizz"
    body = "DataVizz is a technology consulting, analytics services and solutions company.Our capabilities range from Enterprise Cloud Migration, Data Visualization, Data Management to Advanced analytics, Big Data and Machine Learning."
    success = send_email(host, port, username, password, subject, body, mail_to, mail_from)
    response = {
        "isBase64Encoded": False,
    }
    if success:
        response["statusCode"] = 200
        response["body"] = '{"message":We have received your response,Thank You...!!}'
    else:
        response["statusCode"] = 400
        response["body"] = '{"status":false}'
    return response
