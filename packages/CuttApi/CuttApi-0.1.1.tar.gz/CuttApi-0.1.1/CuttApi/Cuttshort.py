import requests
import urllib.parse as urlparse
from urllib.parse import urlencode
import urllib
import pyperclip


#ak = stdiomask.getpass("Enter your Cuttly api key: ")

class Cuttshort:
    def __init__(self, ak):
        while True:
            try:
                api_key = ak
                api_url = 'http://cutt.ly/api/api.php?key={}'.format(api_key)
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
                                    name = input("Would you like to give a name? : ")
                                    if name.upper()=="YES":
                                        while True:
                                            name1 = input("Enter name: ")
                                            api_url1 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(api_key, url, name1)
                                            data1 = requests.get(api_url1).json()["url"]
                                            if data1["status"] == 7:
                                                shortened_url1 = data1["shortLink"]
                                                print("Shortened URL:", shortened_url1)
                                                pyperclip.copy(shortened_url1)
                                                break
                                            elif data1["status"] == 5:
                                                print("Please re-enter the name as the name contains invalid characters!")
                                            else:
                                                print("Please re-enter the name as the entered name already exists!")
                                                continue
                                    elif name.upper()=="NO":
                                        api_url2 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(api_key, url)
                                        data2 = requests.get(api_url2).json()["url"]
                                        if data2["status"] == 7:
                                            # OK, get shortened URL
                                            shortened_url2 = data2["shortLink"]
                                            print("Shortened URL:", shortened_url2)
                                            pyperclip.copy(shortened_url2)
                                    else:
                                        print("Please enter either Yes/No!")
                                elif status==301:
                                    secpro, urllink = link.split("://")
                                    if secpro=="http":
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
                                            name4 = input("Would you like to give a name? : ")
                                            if name4.upper()=="YES":
                                                while True:
                                                    name5 = input("Enter name: ")
                                                    api_url5 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(api_key, url5, name5)
                                                    data5 = requests.get(api_url5).json()["url"]
                                                    if data5["status"] == 7:
                                                        shortened_url5 = data5["shortLink"]
                                                        print("Shortened URL:", shortened_url5)
                                                        pyperclip.copy(shortened_url5)
                                                        break
                                                    elif data5["status"] == 5:
                                                        print("Please re-enter the name as the name contains invalid characters!")
                                                    else:
                                                        print("Please re-enter the name as name already exists!")
                                                        continue
                                            elif name4.upper()=="NO":
                                                api_url6 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(api_key, url5)
                                                data6 = requests.get(api_url6).json()["url"]
                                                if data6["status"] == 7:
                                                    # OK, get shortened URL
                                                    shortened_url6 = data6["shortLink"]
                                                    print("Shortened URL:", shortened_url6)
                                                    pyperclip.copy(shortened_url6)
                                            else:
                                                print("Please enter either Yes/No!")
                                        else:
                                            print("The entered URL is already shortened")
                                    else:
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
                                            name6 = input("Would you like to give a name? : ")
                                            if name6.upper()=="YES":
                                                while True:
                                                    name7 = input("Enter name: ")
                                                    api_url7 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(api_key, url7, name7)
                                                    data7 = requests.get(api_url7).json()["url"]
                                                    if data7["status"] == 7:
                                                        shortened_url7 = data7["shortLink"]
                                                        print("Shortened URL:", shortened_url7)
                                                        pyperclip.copy(shortened_url7)
                                                        break
                                                    elif data7["status"] == 5:
                                                        print("Please re-enter the name as the name contains invalid characters!")
                                                    else:
                                                        print("Please re-enter the name as name already exists!")
                                                        continue
                                            elif name6.upper()=="NO":
                                                api_url8 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(api_key, url7)
                                                data8 = requests.get(api_url8).json()["url"]
                                                if data8["status"] == 7:
                                                    # OK, get shortened URL
                                                    shortened_url8 = data8["shortLink"]
                                                    print("Shortened URL:", shortened_url8)
                                                    pyperclip.copy(shortened_url8)
                                            else:
                                                print("Please enter either Yes/No!")
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
                                    name3 = input("Would you like to give a name? : ")
                                    if name3.upper()=="YES":
                                        while True:
                                            name2 = input("Enter name: ")
                                            api_url3 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(api_key, url3, name2)
                                            data3 = requests.get(api_url3).json()["url"]
                                            if data3["status"] == 7:
                                                shortened_url3 = data3["shortLink"]
                                                print("Shortened URL:", shortened_url3)
                                                pyperclip.copy(shortened_url3)
                                                break
                                            elif data3["status"] == 5:
                                                print("Please re-enter the name as the name contains invalid characters!")
                                            else:
                                                print("Please re-enter the name as name already exists!")
                                                continue
                                    elif name3.upper()=="NO":
                                        api_url4 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(api_key, url3)
                                        data4 = requests.get(api_url4).json()["url"]
                                        if data4["status"] == 7:
                                            # OK, get shortened URL
                                            shortened_url4 = data4["shortLink"]
                                            print("Shortened URL:", shortened_url4)
                                            pyperclip.copy(shortened_url4)
                                    else:
                                        print("Please enter either Yes/No!")
                                elif status1==301:
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
                                        name8 = input("Would you like to give a name? : ")
                                        if name8.upper()=="YES":
                                            while True:
                                                name9 = input("Enter name: ")
                                                api_url9 = 'http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(api_key, url9, name9)
                                                data9 = requests.get(api_url9).json()["url"]
                                                if data9["status"] == 7:
                                                    shortened_url9  = data9["shortLink"]
                                                    print("Shortened URL:", shortened_url9)
                                                    pyperclip.copy(shortened_url9)
                                                    break
                                                elif data9["status"] == 5:
                                                    print("Please re-enter the name as the name contains invalid characters!")
                                                else:
                                                    print("Please re-enter the name as name already exists!")
                                                    continue
                                        elif name8.upper()=="NO":
                                            api_url10 = 'http://cutt.ly/api/api.php?key={}&short={}'.format(api_key, url9)
                                            data10 = requests.get(api_url10).json()["url"]
                                            if data10["status"] == 7:
                                                # OK, get shortened URL
                                                shortened_url10 = data10["shortLink"]
                                                print("Shortened URL:", shortened_url10)
                                                pyperclip.copy(shortened_url10)
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
    api_key200 = stdiomask.getpass("Enter your Cuttly api key: ")
    short1 = Cuttshort(api_key200)