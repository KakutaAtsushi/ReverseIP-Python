from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup as bs4
import csv


def GetReverseDomain():
    format_domain_array = []
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    header = {'User-Agent': user_agent}
    input_domain_name = input("ドメイン・IPを入力してください\n")
    response_domain = requests.get("https://viewdns.info/reverseip/?host={}&t=1".format(input_domain_name),headers=header)
    soup = bs4(response_domain.text, "lxml")
    result_table = soup.find_all("table")[3]
    result_domain_array = result_table.find_all("td")
    if "Domain" not in result_domain_array[0]:
        print("指定されたドメイン・IPが存在しません")
        return sleep(3)

    for domain_context in result_domain_array:
        format_domain_array.append(domain_context.text)

    return format_domain_array, input_domain_name


def OutputCsv(reverse_func):
    if reverse_func is None:
        return
    domain_array = reverse_func[0]

    for domain in domain_array:
        print(domain)
    domain_name = reverse_func[1]
    f = open("ReverseIP-CSV/{0} {1}.csv".format(domain_name, datetime.today().strftime('%Y-%m-%d %H-%M')), 'w')
    data = domain_array
    writer = csv.writer(f)
    writer.writerow(data)
    f.close()
    sleep(5)
    return print("抽出に成功しました")


if __name__ == '__main__':
    OutputCsv(GetReverseDomain())
