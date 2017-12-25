
#coding: gb18030
import requests
from bs4 import BeautifulSoup
from wenzhi import Wenzhi
import time
import sys, os


def get_html(url):
    html_content = requests.get(url)
    return html_content.content

def post_html(url, unit, user):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    data = 'dayy=730%23%C1%BD%C4%EA&search_type=fu&keyword={}&keyword_user={}&searchb1=%CB%D1%CB%F7'.format(unit, user)
    print (data)
    html_content = requests.post(url, data=data, headers=headers)
    print(html_content)
    return html_content.content

'''
html_parser use html5lib for it can parser the url easier
maybe can use lxml to replace it
'''
def post_recent(url):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    data = 'dayy=30%23%D2%BB%B8%F6%D4%C2&search_type=fu&keyword=%D0%A3%CD%C5%CE%AF&keyword_user=&searchb1=%CB%D1%CB%F7'
    html_content = requests.post(url,data=data,headers=headers)
    return html_content.content

def html_parser(html_content):
    soup = BeautifulSoup(html_content, 'html5lib')
    return soup


'''
we need get all tr from the html
'''
def get_info(soup):
    all_tr = soup.table.find_all('tr')[8].find_all('tr')[2].find_all('tr')[4].find_all('tr')
    info_list = []
    for i in range(2,len(all_tr)):
        each_dict = {}
        each_dict['info_type'] = all_tr[i].td.next_sibling.next_sibling.a.string
        each_dict['info_unit'] = all_tr[i].td.next_sibling.next_sibling.next_sibling.next_sibling.a.string
        temp = all_tr[i].td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
        if ('置顶' in temp):
            each_dict['info_top'] = True
            each_dict['info_title'] = temp.strip()[8:]
        else:
            each_dict['info_top'] = False
            each_dict['info_title'] = temp.strip()[1:]
        each_dict['info_data'] = all_tr[i].td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
        each_dict['info_url'] = 'http://www1.szu.edu.cn/board/' + all_tr[i].td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.a.get('href')
        temp = all_tr[i].td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        if('img' in temp.__str__()):
            each_dict['info_file'] = True
        else:
            each_dict['info_file'] = False
        info_list.append(each_dict)
    return info_list

def get_content(soup):
    content_dict = {}
    try:
        title = soup.find_all('td', attrs={'align': 'center','valign': 'top'})[2].find_all('tr')[1].tr.td.text.strip()
    except:
        title = "error"
    try:
        content = soup.find_all('td', attrs={'align': 'center','valign': 'top'})[2].find_all('tr')[1].find_all('tr')[2].text.strip().replace('\n','')
    except:
        content = soup
    content_dict['title'] = title
    content_dict['content'] = content
    return content_dict


def update_info():
    html = post_recent('http://www1.szu.edu.cn/board/')
    par = html_parser(html)
    info = get_info(par)

    # for i in info:
    #     url = i['info_url']
    #     print (url)
    #     html = get_html(url)
    #     soup = html_parser(html)
    #     content = get_content(soup)
    #     if(not Item.objects.filter(title=i['info_title'])):
    #         try:
    #             Item(type=i['info_type'].strip(), unit=i['info_unit'].strip(), title=i['info_title'], date=i['info_data'],
    #             content=content, UID=int(i['info_url'].split('id=')[1])).save()
    #
    #         except:
    #             print "too long"

def getTick(action):
    action_param = action
    sys.path.append("..")
    from board.config import wenzhi_info
    param = {
        'Region': 'sz',
        'SecretId': wenzhi_info['SecretId'],
        'SecretKey': wenzhi_info['SecretKey'],
        'Action': 'TextClassify',
        'action-param': action_param
    }
    w = Wenzhi(param)
    res = w.send()
    #print (res)
    #time.sleep(10)
    return res.json()

def tickChoice(tick):
    # return the useful tick ...
    classes = tick['classes']
    for c in classes:
        if c['class'] == '未分类':
            continue
        else:
            return c['class']

def saveItem(info, content, tick, eu):
    t = tickChoice(tick)
    # import django
    # django.setup()
    from api.models import Announce, SType
    # judge that the t is saved or not
    st = SType.objects.filter(name=t)
    if len(st) == 0:
        # doesn't exist
        st = SType(name=t).save()
    else:
        st = st[0]
    Announce(s_type = st, ori_type=info['info_type'], unit=eu, title = info['info_title'], content = content['content'], time ="13:14").save()
    return True

def getUnitInfo():
    import requests
    from bs4 import BeautifulSoup as bs
    from api.models import Unit
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    url = 'http://www1.szu.edu.cn/board/userlist.asp'
    a = requests.get(url)
    b = bs(a.content, 'lxml')
    c = b.find_all("option")
    Unit.objects.all().delete()
    for i in c[1:]:
        d = i.attrs['value'].split('#')
        Unit(name=d[0], user=d[1], perm=0).save()


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.path.append("../board")
    sys.path.append("..")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    import django
    django.setup()
    from api.models import Unit
    u = Unit.objects.all()
    for eu in u[96:]:
        unit = eu.name
        user = eu.user
        from urllib.parse import quote
        unit = unit.encode('gb2312')
        unit = quote(unit)
        html = post_html('http://www1.szu.edu.cn/board/', unit, user)
        par = html_parser(html)
        info = get_info(par)
        for i in info:
            url = i['info_url']
            print(url)
            html = get_html(url)
            soup = html_parser(html)
            content = get_content(soup)
            try:
                tick = getTick(content)
            except:
                print("cause some error , sleep 60s to continue")
                time.sleep(60)
                continue
            if(tick['codeDesc'] != "Success"):
                continue
            #  save the thing you want
            #print (tick)
            try:
                saveItem(i, content, tick, eu)
            except:
                continue
        # try:
        #     Item(type=i['info_type'].strip(), unit=i['info_unit'].strip(), title=i['info_title'], date=i['info_data'],
        #         content=content, UID=int(i['info_url'].split('id=')[1]), isTop=i['info_top'],
        #         hasFile=i['info_file']).save()
        # except:
        #     print "too long"
    #do some work to make it inside into sql