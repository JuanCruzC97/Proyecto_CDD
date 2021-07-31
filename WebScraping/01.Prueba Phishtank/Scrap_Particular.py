import requests
from scrapy import Selector

'''
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0" 
}
cookies = {'www.phishtank.com/':'a10','www.phishtank.com/cdn-cgi/challenge-platform/h/g/flow/ov1/0.9996953005258895:1627740307:670b6e3c96c9ab9e09578210b2962029aec620317713f6da506147a863270638/677792c92e5308c0':'f2f800fba3ce32a','.phishtank.com/':'49a74082e03544fc4f6d40a3ff6940e6010b1209-1627742459-0-250', 'www.phishtank.com/':'pgv2cmrndq7qf08868a6r5rqdppv8cuv'}
'''

# Probamos hacer request en un url particular id = 712354.
html2 = requests.get("https://www.phishtank.com/phish_detail.php?phish_id=7123354")
print(html2.cookies)
print(html2.url)

sel2 = Selector(text = html2.content)
sel2_list = sel2.xpath('/html')
print(sel2_list.extract())
print(len(sel2_list))