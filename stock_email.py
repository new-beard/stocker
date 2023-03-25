import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def send_email():
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = "qlgfqeimqrjrbheb"
    msg['From'] = "515205935@qq.com"
    msg['To'] = "lianglx.alex@gmail.com"
    msg['Subject'] = "Stock Data"

    # add html email body
    html = """
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           Here is the <a href="http://www.python.org">link</a> you wanted.<br>
        </p>
      </body>
    </html>
    """
    body = MIMEText(html, 'html')
    msg.attach(body)

    # attach the image to the message
    with open("stocks.png", 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name="stocks_data.png")
    msg.attach(image)

    # attach the csv file to the message
    with open("stocks_data.csv", 'rb') as f:
        csv_data = f.read()
    csv = MIMEApplication(csv_data, name="stocks_data.csv")
    msg.attach(csv)

    result=True
    try:
        server=smtplib.SMTP_SSL("smtp.qq.com",465)  # smtp server & port
        server.ehlo() # open connection
        server.login(msg['From'],password) # login
        server.sendmail(msg['From'],msg['To'],msg.as_string()) # send email
        server.quit() # close connection
    except Exception as e:
        result=False
        print(e)
    return result

send_email()