import os
os.chdir('/home/project/stocker')

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import stock_config as sc
import datetime
import pandas as pd

email_config = sc.EMAIL_CONFIG

def send_email():
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
    password = email_config['password']
    msg['From'] = email_config['from']
    msg['To'] = ", ".join(email_config['to'])
    msg['Subject'] = email_config['subject']
    smtp_server = email_config['smtp_server']
    smtp_port = email_config['smtp_port']

    # attach the image to the message
    with open("stock_plots.png", 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name="stock_plots.png")
    image.add_header('Content-ID', '<image1>')
    msg.attach(image)

    # add html email body
    today = datetime.date.today().strftime("%Y-%m-%d")
    stock_values = pd.read_csv('stock_values.csv')
    html = """
    <html>
      <head>
        <style> 
            table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
            th, td {{ padding: 2px; }}
        </style>
      </head>
      <body>
        <p>Hi!</P>
        <p>Sent on: {}</p>
        <table>
            <tbody>
                {}
            </tbody>
        </table>
        <img src="cid:image1">
      </body>
    </html>

    """.format(today, stock_values.to_html(index=False))
    body = MIMEText(html, 'html')
    msg.attach(body)

    result=True
    try:
        server=smtplib.SMTP_SSL(smtp_server, smtp_port)  # connect to smtp server
        server.ehlo() # open connection
        server.login(msg['From'], password) # login to email account
        server.sendmail(msg['From'], msg['To'], msg.as_string()) # send email
        server.quit() # close connection
    except Exception as e:
        result=False
        print(e) # print error message if email sending fails
    return result # return True if email sent successfully, False otherwise

send_email() # call send_email function
