import email
import os
from urllib.parse import urlparse
import requests.adapters
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib import DELEGATE, Account, Credentials, Configuration, NTLM, Q, HTMLBody
import pandas as pd


class RootCAAdapter(requests.adapters.HTTPAdapter):
    """An HTTP adapter that uses a custom root CA certificate at a hard coded
    location.
    """

    def cert_verify(self, conn, url, verify, cert):
        cert_file = {
            'mail.slt.com.lk': 'D:\DevOps\Python\mailRead\mailcertificate.cer',
        }[urlparse(url).hostname]
        super().cert_verify(conn=conn, url=url, verify=cert_file, cert=cert)


# Use this adapter class instead of the default
# BaseProtocol.HTTP_ADAPTER_CLS = RootCAAdapter
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
creds = Credentials(
    username="012583@intranet.slt.com.lk",
    password="AAdp#19870120"
)

config = Configuration(server='mail.slt.com.lk', credentials=creds)

account = Account(
    primary_smtp_address="prabodha@slt.com.lk",
    autodiscover=False,
    config=config,
    access_type=DELEGATE,
)

for item in account.inbox.all().filter('subject:On net Test',is_read=False).order_by('-datetime_received')[:1]:
    # print(item.subject, item.sender, item.datetime_received, item.body)
    if os.path.exists("demofile2.html"):
        os.remove("demofile2.html")
        f = open("demofile2.html", "a")
        f.write(item.body)
        f.close()

    tables = pd.read_html('demofile2.html')
    print('Tables found:', len(tables))
    df1 = tables[0]  # Save first table in variable df1

    print('First Table')
    print(type(df1[7]))
    for i in df1[7]:
        print(i)
