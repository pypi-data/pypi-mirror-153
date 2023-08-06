import requests
import urllib.parse as urlparse
from urllib.parse import urlencode
import urllib
import pyperclip


class Cuttshort:
    def __init__(self, api_key):
        while True:
            try:
                ak = api_key
                api_url = 'http://cutt.ly/api/api.php?key={}'.format(ak)
                data = requests.get(api_url).json()
                if data["auth"]==True:
                    while True:
                        try:
                            link = input("Enter the link to be shortened: ")
                            params = {'utm_source':'apidevthe'}
                    

                            if link.startswith("http"):
                                response = requests.head(link)
                                status = response.status_code
                                url_parts = list(urlparse.urlparse(link))
                                query = dict(urlparse.parse_qsl(url_parts[4]))
                                query.update(params)
     
                                url_parts[4] = urlencode(query)
                                url1 = urlparse.urlunparse(url_parts)
                                url = urllib.parse.quote(url1)

                                if status==200:
                                    while True:
                                        name = input("Would you like to give a name? : ")
                                        if name.upper()=="YES":
                                            while True:
                                                name1 = input("Enter name: ")
                                                api_url1 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url, name1)
                                                data1 = requests.get(api_url1).json()["url"]
                                                if data1["status"] == 7:
                                                    shortened_url1 = data1["shortLink"]
                                                    print("Shortened URL: ", shortened_url1)
                                                    pyperclip.copy(shortened_url1)
                                                    break
                                                elif data1["status"] == 5:
                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                else:
                                                    print("Please re-enter the name as the entered name already exists!")
                                                    continue
                                            break
                                        elif name.upper()=="NO":
                                            api_url2 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url)
                                            data2 = requests.get(api_url2).json()["url"]
                                            if data2["status"] == 7:
                                                shortened_url2 = data2["shortLink"]
                                                print("Shortened URL: ", shortened_url2)
                                                pyperclip.copy(shortened_url2)
                                                break
                                        else:
                                            print("Please enter either Yes/No!")
                                elif status==301:
                                    secpro, urllink = link.split("://")
                                    if not link.endswith("/"):
                                                link8 = link + "/"
                                                response6 = requests.head(link8)
                                                status6 = response6.status_code
                                                url_parts6 = list(urlparse.urlparse(link8))
                                                query6 = dict(urlparse.parse_qsl(url_parts6[4]))
                                                query6.update(params)
     
                                                url_parts6[4] = urlencode(query6)
                                                url12= urlparse.urlunparse(url_parts6)
                                                url13 = urllib.parse.quote(url12)

                                                if status6==200:
                                                    while True:
                                                        name12 = input("Would you like to give a name? : ")
                                                        if name12.upper()=="YES":
                                                            while True:
                                                                name13 = input("Enter name: ")
                                                                api_url13 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url13, name13)
                                                                data13 = requests.get(api_url13).json()["url"]
                                                                if data13["status"] == 7:
                                                                    shortened_url13 = data13["shortLink"]
                                                                    print("Shortened URL: ", shortened_url13)
                                                                    pyperclip.copy(shortened_url13)
                                                                    break
                                                                elif data11["status"] == 5:
                                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                                else:
                                                                    print("Please re-enter the name as name already exists!")
                                                                    continue
                                                            break
                                                        elif name12.upper()=="NO":
                                                            api_url14 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url13)
                                                            data14 = requests.get(api_url14).json()["url"]
                                                            if data14["status"] == 7:
                                                                shortened_url14 = data14["shortLink"]
                                                                print("Shortened URL: ", shortened_url14)
                                                                pyperclip.copy(shortened_url14)
                                                                break
                                                        else:
                                                            print("Please enter either Yes/No!")
                                                elif status6==301:
                                                    if secpro=="http":
                                                        link41 = "https://" + urllink + "/"
                                                        response21 = requests.head(link41)
                                                        status21 = response21.status_code
                                                        url_parts21 = list(urlparse.urlparse(link41))
                                                        query21 = dict(urlparse.parse_qsl(url_parts21[4]))
                                                        query21.update(params)
     
                                                        url_parts21[4] = urlencode(query21)
                                                        url41 = urlparse.urlunparse(url_parts21)
                                                        url51 = urllib.parse.quote(url41)

                                                        if status21==200:
                                                            while True:
                                                                name41 = input("Would you like to give a name? : ")
                                                                if name41.upper()=="YES":
                                                                    while True:
                                                                        name51 = input("Enter name: ")
                                                                        api_url51 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url51, name51)
                                                                        data51 = requests.get(api_url51).json()["url"]
                                                                        if data51["status"] == 7:
                                                                            shortened_url51 = data51["shortLink"]
                                                                            print("Shortened URL: ", shortened_url51)
                                                                            pyperclip.copy(shortened_url51)
                                                                            break
                                                                        elif data51["status"] == 5:
                                                                            print("Please re-enter the name as the name contains invalid characters!")
                                                                        else:
                                                                            print("Please re-enter the name as name already exists!")
                                                                            continue
                                                                    break
                                                                elif name41.upper()=="NO":
                                                                    api_url61 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url51)
                                                                    data61 = requests.get(api_url61).json()["url"]
                                                                    if data61["status"] == 7:
                                                                        shortened_url61 = data61["shortLink"]
                                                                        print("Shortened URL: ", shortened_url61)
                                                                        pyperclip.copy(shortened_url61)
                                                                        break
                                                                else:
                                                                    print("Please enter either Yes/No!")
                                                        else:
                                                            print("The entered URL is already shortened")
                                                    elif secpro=="https":
                                                        link42 = "http://" + urllink + "/"
                                                        response22 = requests.head(link42)
                                                        status22 = response22.status_code
                                                        url_parts22 = list(urlparse.urlparse(link42))
                                                        query22 = dict(urlparse.parse_qsl(url_parts22[4]))
                                                        query22.update(params)
     
                                                        url_parts22[4] = urlencode(query22)
                                                        url42 = urlparse.urlunparse(url_parts22)
                                                        url52 = urllib.parse.quote(url42)

                                                        if status22==200:
                                                            while True:
                                                                name42 = input("Would you like to give a name? : ")
                                                                if name42.upper()=="YES":
                                                                    while True:
                                                                        name52 = input("Enter name: ")
                                                                        api_url52 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url52, name52)
                                                                        data52 = requests.get(api_url52).json()["url"]
                                                                        if data52["status"] == 7:
                                                                            shortened_url52 = data52["shortLink"]
                                                                            print("Shortened URL: ", shortened_url52)
                                                                            pyperclip.copy(shortened_url52)
                                                                            break
                                                                        elif data52["status"] == 5:
                                                                             print("Please re-enter the name as the name contains invalid characters!")
                                                                        else:
                                                                            print("Please re-enter the name as name already exists!")
                                                                            continue
                                                                    break
                                                                elif name42.upper()=="NO":
                                                                    api_url62 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url52)
                                                                    data62 = requests.get(api_url62).json()["url"]
                                                                    if data62["status"] == 7:
                                                                        shortened_url62 = data62["shortLink"]
                                                                        print("Shortened URL: ", shortened_url62)
                                                                        pyperclip.copy(shortened_url62)
                                                                        break
                                                                else:
                                                                    print("Please enter either Yes/No!")
                                                                    continue
                                                        else:
                                                            print("The entered URL is already shortened")
                                    elif secpro=="http":
                                        link4 = "https://" + urllink
                                        response2 = requests.head(link4)
                                        status2 = response2.status_code
                                        url_parts2 = list(urlparse.urlparse(link4))
                                        query2 = dict(urlparse.parse_qsl(url_parts2[4]))
                                        query2.update(params)
     
                                        url_parts2[4] = urlencode(query2)
                                        url4 = urlparse.urlunparse(url_parts2)
                                        url5 = urllib.parse.quote(url4)

                                        if status2==200:
                                            while True:
                                                name4 = input("Would you like to give a name? : ")
                                                if name4.upper()=="YES":
                                                    while True:
                                                        name5 = input("Enter name: ")
                                                        api_url5 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url5, name5)
                                                        data5 = requests.get(api_url5).json()["url"]
                                                        if data5["status"] == 7:
                                                            shortened_url5 = data5["shortLink"]
                                                            print("Shortened URL: ", shortened_url5)
                                                            pyperclip.copy(shortened_url5)
                                                            break
                                                        elif data5["status"] == 5:
                                                            print("Please re-enter the name as the name contains invalid characters!")
                                                        else:
                                                            print("Please re-enter the name as name already exists!")
                                                            continue
                                                    break
                                                elif name4.upper()=="NO":
                                                    api_url6 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url5)
                                                    data6 = requests.get(api_url6).json()["url"]
                                                    if data6["status"] == 7:
                                                        shortened_url6 = data6["shortLink"]
                                                        print("Shortened URL: ", shortened_url6)
                                                        pyperclip.copy(shortened_url6)
                                                        break
                                                else:
                                                    print("Please enter either Yes/No!")
                                        elif status2==301:
                                            if not link.endswith("/"):
                                                link7 = "https://" + urllink + "/"
                                                response5 = requests.head(link7)
                                                status5 = response5.status_code
                                                url_parts5 = list(urlparse.urlparse(link7))
                                                query5 = dict(urlparse.parse_qsl(url_parts5[4]))
                                                query5.update(params)
     
                                                url_parts5[4] = urlencode(query5)
                                                url10 = urlparse.urlunparse(url_parts5)
                                                url11 = urllib.parse.quote(url10)

                                                if status5==200:
                                                    while True:
                                                        name10 = input("Would you like to give a name? : ")
                                                        if name10.upper()=="YES":
                                                            while True:
                                                                name11 = input("Enter name: ")
                                                                api_url11 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url11, name11)
                                                                data11 = requests.get(api_url11).json()["url"]
                                                                if data11["status"] == 7:
                                                                    shortened_url11 = data11["shortLink"]
                                                                    print("Shortened URL: ", shortened_url11)
                                                                    pyperclip.copy(shortened_url11)
                                                                    break
                                                                elif data11["status"] == 5:
                                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                                else:
                                                                    print("Please re-enter the name as name already exists!")
                                                                    continue
                                                            break
                                                        elif name4.upper()=="NO":
                                                            api_url12 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url11)
                                                            data12 = requests.get(api_url12).json()["url"]
                                                            if data12["status"] == 7:
                                                                shortened_url12 = data12["shortLink"]
                                                                print("Shortened URL: ", shortened_url12)
                                                                pyperclip.copy(shortened_url12)
                                                                break
                                                        else:
                                                            print("Please enter either Yes/No!")
                                                else:
                                                    print("The entered URL is already shortened")
                                            else:
                                                print("The entered URL is already shortened")
                                    elif secpro=="https":
                                        link5 = "http://" + urllink
                                        response3 = requests.head(link5)
                                        status3 = response3.status_code
                                        url_parts3 = list(urlparse.urlparse(link5))
                                        query3 = dict(urlparse.parse_qsl(url_parts3[4]))
                                        query3.update(params)
     
                                        url_parts3[4] = urlencode(query3)
                                        url6 = urlparse.urlunparse(url_parts3)
                                        url7 = urllib.parse.quote(url6)

                                        if status3==200:
                                            while True:
                                                name6 = input("Would you like to give a name? : ")
                                                if name6.upper()=="YES":
                                                    while True:
                                                        name7 = input("Enter name: ")
                                                        api_url7 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url7, name7)
                                                        data7 = requests.get(api_url7).json()["url"]
                                                        if data7["status"] == 7:
                                                            shortened_url7 = data7["shortLink"]
                                                            print("Shortened URL: ", shortened_url7)
                                                            pyperclip.copy(shortened_url7)
                                                            break
                                                        elif data7["status"] == 5:
                                                            print("Please re-enter the name as the name contains invalid characters!")
                                                        else:
                                                            print("Please re-enter the name as name already exists!")
                                                            continue
                                                    break
                                                elif name6.upper()=="NO":
                                                    api_url8 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url7)
                                                    data8 = requests.get(api_url8).json()["url"]
                                                    if data8["status"] == 7:
                                                        shortened_url8 = data8["shortLink"]
                                                        print("Shortened URL: ", shortened_url8)
                                                        pyperclip.copy(shortened_url8)
                                                        break
                                                else:
                                                    print("Please enter either Yes/No!")
                                        else:
                                            print("The entered URL is already shortened")
                                    else:
                                            print("The entered URL is already shortened")
                                else:
                                    print("URL does not exist on the Internet")
                            else:
                                link1 = "http://" + link
                                response1 = requests.head(link1)
                                status1 = response1.status_code
                                url_parts1 = list(urlparse.urlparse(link1))
                                query1 = dict(urlparse.parse_qsl(url_parts1[4]))
                                query1.update(params)
     
                                url_parts1[4] = urlencode(query1)
                                url2 = urlparse.urlunparse(url_parts1)
                                url3 = urllib.parse.quote(url2)
                                if status1 == 200:
                                    while True:
                                        name3 = input("Would you like to give a name? : ")
                                        if name3.upper()=="YES":
                                            while True:
                                                name2 = input("Enter name: ")
                                                api_url3 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url3, name2)
                                                data3 = requests.get(api_url3).json()["url"]
                                                if data3["status"] == 7:
                                                    shortened_url3 = data3["shortLink"]
                                                    print("Shortened URL: ", shortened_url3)
                                                    pyperclip.copy(shortened_url3)
                                                    break
                                                elif data3["status"] == 5:
                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                else:
                                                    print("Please re-enter the name as name already exists!")
                                                    continue
                                            break
                                        elif name3.upper()=="NO":
                                            api_url4 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url3)
                                            data4 = requests.get(api_url4).json()["url"]
                                            if data4["status"] == 7:
                                                shortened_url4 = data4["shortLink"]
                                                print("Shortened URL: ", shortened_url4)
                                                pyperclip.copy(shortened_url4)
                                                break
                                        else:
                                            print("Please enter either Yes/No!")
                                elif status1 == 301:
                                    secpro1, urllink1 = link1.split("://")
                                    link6 = "https://" + urllink1
                                    response4 = requests.head(link6)
                                    status4 = response4.status_code
                                    url_parts4 = list(urlparse.urlparse(link6))
                                    query4 = dict(urlparse.parse_qsl(url_parts4[4]))
                                    query4.update(params)
     
                                    url_parts4[4] = urlencode(query4)
                                    url8 = urlparse.urlunparse(url_parts4)
                                    url9 = urllib.parse.quote(url8)

                                    if status4==200:
                                        while True:
                                            name8 = input("Would you like to give a name? : ")
                                            if name8.upper()=="YES":
                                                while True:
                                                    name9 = input("Enter name: ")
                                                    api_url9 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url9, name9)
                                                    data9 = requests.get(api_url9).json()["url"]
                                                    if data9["status"] == 7:
                                                        shortened_url9  = data9["shortLink"]
                                                        print("Shortened URL: ", shortened_url9)
                                                        pyperclip.copy(shortened_url9)
                                                        break
                                                    elif data9["status"] == 5:
                                                        print("Please re-enter the name as the name contains invalid characters!")
                                                    else:
                                                        print("Please re-enter the name as name already exists!")
                                                        continue
                                                break
                                            elif name8.upper()=="NO":
                                                api_url10 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url9)
                                                data10 = requests.get(api_url10).json()["url"]
                                                if data10["status"] == 7:
                                                    shortened_url10 = data10["shortLink"]
                                                    print("Shortened URL: ", shortened_url10)
                                                    pyperclip.copy(shortened_url10)
                                                    break
                                            else:
                                                print("Please enter either Yes/No!")
                                                continue
                                    elif status4==301:
                                        if not link.endswith("/"):
                                            link9 = link6 + "/"
                                            response7 = requests.head(link9)
                                            status7 = response7.status_code
                                            url_parts7 = list(urlparse.urlparse(link9))
                                            query7 = dict(urlparse.parse_qsl(url_parts7[4]))
                                            query7.update(params)
     
                                            url_parts7[4] = urlencode(query7)
                                            url14 = urlparse.urlunparse(url_parts7)
                                            url15 = urllib.parse.quote(url14)

                                            if status7==200:
                                                while True:
                                                    name14 = input("Would you like to give a name? : ")
                                                    if name14.upper()=="YES":
                                                        while True:
                                                            name15 = input("Enter name: ")
                                                            api_url15 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(ak, url15, name15)
                                                            data15 = requests.get(api_url15).json()["url"]
                                                            if data15["status"] == 7:
                                                                shortened_url15 = data15["shortLink"]
                                                                print("Shortened URL: ", shortened_url15)
                                                                pyperclip.copy(shortened_url15)
                                                                break
                                                            elif data15["status"] == 5:
                                                                print("Please re-enter the name as the name contains invalid characters!")
                                                            else:
                                                                print("Please re-enter the name as name already exists!")
                                                                continue
                                                        break
                                                    elif name14.upper()=="NO":
                                                        api_url16 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(ak, url15)
                                                        data16 = requests.get(api_url16).json()["url"]
                                                        if data16["status"] == 7:
                                                            shortened_url16 = data16["shortLink"]
                                                            print("Shortened URL: ", shortened_url16)
                                                            pyperclip.copy(shortened_url16)
                                                            break
                                                    else:
                                                        print("Please enter either Yes/No!")
                                            else:
                                                print("The entered URL is already shortened")
                                else:
                                    print("URL does not exist on the Internet")

                        except requests.ConnectionError as exception:
                            
                            print("URL does not exist on the Internet")
                            break
                else:
                    print("The entered API key does not exist. Please retry!")
                    break
            except requests.JSONDecodeError as exception:
                print("There is an issue with the API. Please try after a few seconds")
                break

if __name__ == "__main__":
    import stdiomask
    api_key = stdiomask.getpass("Enter your Cuttly api key: ")
    short = Cuttshort(api_key)