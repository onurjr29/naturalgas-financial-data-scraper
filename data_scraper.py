from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
import requests
import pandas as pd

@dataclass
class Data:
    Date: str
    Open: float
    High: float
    Low: float
    Close: float
    Adj: float
    Volume: int

Data_List = []

headers = {
    "Accept": "*/*",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": "GUC=AQEBCAFnAlxnLkIiawTc&s=AQAAALbOXT6V&g=ZwEXOA; A1=d=AQABBF6KomQCEOx08YjqhDxudkcGyXZc_3cFEgEBCAFcAmcuZ8fJb2UB_eMBAAcIXoqiZHZc_3c&S=AQAAAoOj0DOek_R_Fb0sPVYrEqE; A3=d=AQABBF6KomQCEOx08YjqhDxudkcGyXZc_3cFEgEBCAFcAmcuZ8fJb2UB_eMBAAcIXoqiZHZc_3c&S=AQAAAoOj0DOek_R_Fb0sPVYrEqE; axids=gam=y-.iWAUqxE2uJKiYXRshnnD5wrOp.CNdIN~A&dv360=eS1yY2xjWGVkRTJ1R3ZNbXhaRmwwNUcxN2kuVk91Q1hPdn5B&ydsp=y-TWrk4MhE2uIFrD05nwvWec.WC1TUX9IF~A&tbla=y-Qo82fYVE2uJPavdUXaVGETcC3UopQD2E~A; tbla_id=51b21b5e-58cc-4f12-9765-424d9c9cc6bc-tuctb9c0fdf; trc_cookie_storage=taboola%2520global%253Auser-id%3D51b21b5e-58cc-4f12-9765-424d9c9cc6bc-tuctb9c0fdf; PRF=t%3DNG%253DF%252BSISE.IS%252BGMSTR.IS%252BZGOLD.IS%252BISGLK.IS%252BISKDN.IS%252BAPLIB.IS%252BGC%253DF%252BISBTR.IS%252BISCTR.IS; A1S=d=AQABBF6KomQCEOx08YjqhDxudkcGyXZc_3cFEgEBCAFcAmcuZ8fJb2UB_eMBAAcIXoqiZHZc_3c&S=AQAAAoOj0DOek_R_Fb0sPVYrEqE; cmp=t=1730968459&j=0&u=1---; gpp=DBAA; gpp_sid=-1",
    "Priority": "u=1, i",
    "Referer": "https://finance.yahoo.com/quote/NG%3DF/history/?period1=1043280000&period2=1729710047",
    "Sec-CH-UA": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

url = "https://finance.yahoo.com/quote/NG%3DF/history/?period1=1043280000&period2=1729710047"
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

tr_elements = soup.select('table tbody tr')

for element in tr_elements:
    td_elements = element.select('td')
    
    cleaned_data = Data(
        Date=td_elements[0].get_text(strip=True),
        Open=float(td_elements[1].get_text(strip=True).replace(',', '')),
        High=float(td_elements[2].get_text(strip=True).replace(',', '')),
        Low=float(td_elements[3].get_text(strip=True).replace(',', '')),
        Close=float(td_elements[4].get_text(strip=True).replace(',', '')),
        Adj=float(td_elements[5].get_text(strip=True).replace(',', '')),
        Volume=int(td_elements[6].get_text(strip=True).replace(',', '').replace('-', '0'))
    )
    Data_List.append(cleaned_data)

data_dicts = [asdict(data) for data in Data_List]

df = pd.DataFrame(data_dicts)

df.to_excel("financial_data.xlsx", index=False)