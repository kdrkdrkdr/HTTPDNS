#-*- coding:utf-8 -*-

from os import system, popen, getcwd
from psutil import net_if_addrs
from ctypes import windll
from sys import executable
from bs4 import BeautifulSoup
from requests import get, exceptions
from time import sleep
from random import choice


ProxyList = []


AuthorInfo = '''
제작자: 김경민
최종수정: 2019년 7월 17일'''

SelectList = '''
1) Proxy 사용하기
2) DNS 변경하기
3) 프로그램 종료하기
\n>> '''


Banner = '''
.-. .-. .---.  .---. .----. .----. .-. .-. .----.
| {_} |{_   _}{_   _}| {}  }| {}  \|  `| |{ {__  
| { } |  | |    | |  | .--' |     /| |\  |.-._} }
`-' `-'  `-'    `-'  `-'    `----' `-' `-'`----'
'''


def PrintBanner():
    print(Banner)
    return



def CheckAdmin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False



def ClearWindow():
    system('cls')



def ChangeDNS():
    AdapterList = [adpt for adpt in net_if_addrs().keys()]

    randDns = ['1.1.1.1', '8.8.8.8']

    for adpt in AdapterList:
        popen("netsh interface ip set dns {} static {}".format(adpt, choice(randDns)))
    print('\nDNS가 ({}) 로 변경되었습니다.\n'.format(randDns))
    return



def CheckInternetConnection():
    try:
        get("https://www.google.com")
        return True
    except ( exceptions.ConnectionError ):
        return False
    

    
def EchoOff():
    system('echo off')
    return



def ApplyProxy(ip_port="", reset=False):
    if ip_port.replace(' ', '') != "":
        popen('netsh winhttp set proxy {}'.format(ip_port))
        print('Proxy가 [{}] 로 설정되었습니다.\n'.format(ip_port))

    if reset == True:
        popen('netsh winhttp reset proxy')
        print('Proxy가 초기화 되었습니다.\n')

    return



def GetProxy(Store=False):
    url = "https://free-proxy-list.net/"
    html = get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    proxyAddr = soup.find("tbody").find_all('tr')
    contents = ""

    for i in proxyAddr:
        j = i.find_all('td')

        ip = j[0].text
        port = j[1].text
        ProxyList.append("{}:{}".format(ip, port))

        for k in j:
            content = k.text + ","
            contents += content

        contents += "\n"
    
    if Store == False:
        return

    else:
        with open('{}\\proxylist.csv'.format(getcwd()), 'w') as f:
            f.write('IP Address,Port,Code,Country,Anonymity,Google,Https,Last Checked\n\n')
            f.write(contents)

        print("[{}\\proxylist.csv] 에 저장되었습니다.".format(getcwd()))
    
    return



def Apply():
    EchoOff()
    GetProxy(Store=False)
    proxy = choice(ProxyList)
    ApplyProxy(ip_port=proxy)
    return



def ServiceProxy():
    count = 0
    while True:
        try:
            ClearWindow()
            count += 1
            print("{}번 바뀌었습니다.".format(count))
            print("Ctrl-C 를 입력하면 종료됩니다.\n")
            Apply()
            sleep(60)
        except ( KeyboardInterrupt ):
            ApplyProxy(reset=True)
            break
    return



def main():
    print(AuthorInfo)
    print('\n[!] 인터넷 브라우저는 크롬을 권장합니다.\n')
    PrintBanner()

    if CheckInternetConnection() == False:
        print('\n[!] 인터넷 연결을 확인하세요.\n\n')
        system('pause')
        return

    while True:

        try:
            select = int(input(SelectList))

            if select == 1:
                ClearWindow()
                ServiceProxy()

            elif select == 2:
                ClearWindow()
                ChangeDNS()

            elif select == 3:
                break

            else:
                print("\n다시 입력해주세요.\n")

        except ( ValueError, EOFError, KeyboardInterrupt ):
            print("\n다시 입력해주세요.\n")

    return





if __name__ == "__main__":
    if CheckAdmin():
        main()
    else:
        windll.shell32.ShellExecuteW(None, 'runas', executable, __file__, None, 1)