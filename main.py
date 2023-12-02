import random
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import pickle
import openpyxl

from location import get_location


with open("proxy.txt") as file:
    PROXY_LIST = "".join(file.readlines()).split("\n")


def save_in_excel(year, type_, mark, model, suspension, brake, load, axis, up_axis, price, region, link, row):
    workbook = openpyxl.load_workbook('Таблица прицепы.xlsx')
    sheet = workbook.active
    sheet[f'A{row}'], sheet[f'B{row}'], sheet[f'C{row}'], sheet[f'D{row}'] = year, type_, mark, model
    sheet[f'E{row}'], sheet[f'F{row}'], sheet[f'G{row}'], sheet[f'H{row}'] = suspension, brake, load, axis
    sheet[f'I{row}'], sheet[f'J{row}'], sheet[f'K{row}'], sheet[f'L{row}'] = up_axis, price, region, link
    workbook.save('Таблица прицепы.xlsx')


async def settings(page_num, rand_proxy):
    async with aiohttp.ClientSession() as session:
        cookies = {
            'spravka': 'dD0xNzAxNDIxNDQ1O2k9OTUuMzIuNzMuMTMwO0Q9MUMyOUNDMzU2RjQwMjI4QTQ1NjhBQzQ2RTc0MTVEQ0IyOUJDMTZGMTM3N0FFRENCQTAwNTFFMjhCRjFENUY3REU2QzI1MzVGMUYyQjUzREQ5NTQ0RjQyNEIxQzdBQUE5NjFBOUJGMjMxMkIzNUY1Njc2MEVGMUY3Q0FGMkYzNDhEM0U4MUQ4MTYwNzVBNDM0O3U9MTcwMTQyMTQ0NTI3ODY4Njk5MDtoPWMxNGJhMTI3Yzk0YjUzYjM2MmFhYmNiZjMzOWRkMTdk',
            '_yasc': 'Z8ito11h5tGI5jm0NtCLX91IeaTFO7V/DawtMmY2RILBrY4r+LxPoXMZ6tvpUMhqSsvKOOgoBqE=',
            'gdpr': '0',
            '_ym_visorc': 'b',
            'suid': '1fcc5294ad3df71178d0da0a8a412119.188e4f223b937631fab3e2f6573b83cb',
            '_csrf_token': '1aed5afef4e512162132d613fe6e0fddf9112a4247b84622',
            'autoru_sid': 'a^%^3Ag6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c^%^7C1701421445487.604800.STEgpmoYnjmdyrYH85l5hw.ATkLP66QoTuhm3Zq5XyF2Ie1PLZGqdOio7wYM-jhwx0',
            'autoruuid': 'g6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c',
            'from_lifetime': '1701422479248',
            'from': 'direct',
            'autoru_sso_blocked': '1',
            'Session_id': 'noauth:1701421445',
            'sessar': '1.1184.CiA95iTx5Q98Ew3VgO38HNc3S9KfDkP4yTvTAuRYBYawfg.9fCnR83NZZ7Cg5-KdL838qcpw_aZ5t_MMI6RbOJQo3A',
            'yandex_login': '',
            'ys': 'c_chck.3192317861',
            'i': 'XteuW9UhfJ6HFrsugRX3jGL3Bjr57t9zIHP07IhF0o5kcpYQ8ADX89Vk4zSSMvuxiBOiRmJ0nsnMMdu8tXQvpSrDSLs=',
            'yandexuid': '1765520041701333029',
            'mda2_beacon': '1701421445786',
            'sso_status': 'sso.passport.yandex.ru:synchronized_no_beacon',
            'layout-config': '{screen_height:960,screen_width:1708,win_width:1686.25,win_height:273.75}',
            '_arsus': 'true',
            'count-visits': '3',
            '_ym_uid': '1701421443933204740',
            '_ym_d': '1701421641',
            '_ym_isad': '2',
            'yaPassportTryAutologin': '1',
            'popups-dr-shown-count': '1',
            'fp': 'b8b930ff929cc40b202f0caaeb2af241^%^7C1701421456264',
            'cycada': 'P7mdXXLuSRcHx26DoWg4gyoGuewZ52Ht1fvNM5rDEfo=',
            'autoru-visits-count': '1',
            'autoru-visits-session-unexpired': '1',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            # 'Cookie': 'spravka=dD0xNzAxNDIxNDQ1O2k9OTUuMzIuNzMuMTMwO0Q9MUMyOUNDMzU2RjQwMjI4QTQ1NjhBQzQ2RTc0MTVEQ0IyOUJDMTZGMTM3N0FFRENCQTAwNTFFMjhCRjFENUY3REU2QzI1MzVGMUYyQjUzREQ5NTQ0RjQyNEIxQzdBQUE5NjFBOUJGMjMxMkIzNUY1Njc2MEVGMUY3Q0FGMkYzNDhEM0U4MUQ4MTYwNzVBNDM0O3U9MTcwMTQyMTQ0NTI3ODY4Njk5MDtoPWMxNGJhMTI3Yzk0YjUzYjM2MmFhYmNiZjMzOWRkMTdk; _yasc=Z8ito11h5tGI5jm0NtCLX91IeaTFO7V/DawtMmY2RILBrY4r+LxPoXMZ6tvpUMhqSsvKOOgoBqE=; gdpr=0; _ym_visorc=b; suid=1fcc5294ad3df71178d0da0a8a412119.188e4f223b937631fab3e2f6573b83cb; _csrf_token=1aed5afef4e512162132d613fe6e0fddf9112a4247b84622; autoru_sid=a^%^3Ag6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c^%^7C1701421445487.604800.STEgpmoYnjmdyrYH85l5hw.ATkLP66QoTuhm3Zq5XyF2Ie1PLZGqdOio7wYM-jhwx0; autoruuid=g6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c; from_lifetime=1701422479248; from=direct; autoru_sso_blocked=1; Session_id=noauth:1701421445; sessar=1.1184.CiA95iTx5Q98Ew3VgO38HNc3S9KfDkP4yTvTAuRYBYawfg.9fCnR83NZZ7Cg5-KdL838qcpw_aZ5t_MMI6RbOJQo3A; yandex_login=; ys=c_chck.3192317861; i=XteuW9UhfJ6HFrsugRX3jGL3Bjr57t9zIHP07IhF0o5kcpYQ8ADX89Vk4zSSMvuxiBOiRmJ0nsnMMdu8tXQvpSrDSLs=; yandexuid=1765520041701333029; mda2_beacon=1701421445786; sso_status=sso.passport.yandex.ru:synchronized_no_beacon; layout-config={screen_height:960,screen_width:1708,win_width:1686.25,win_height:273.75}; _arsus=true; count-visits=3; _ym_uid=1701421443933204740; _ym_d=1701421641; _ym_isad=2; yaPassportTryAutologin=1; popups-dr-shown-count=1; fp=b8b930ff929cc40b202f0caaeb2af241^%^7C1701421456264; cycada=P7mdXXLuSRcHx26DoWg4gyoGuewZ52Ht1fvNM5rDEfo=; autoru-visits-count=1; autoru-visits-session-unexpired=1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        params = {
            'page': page_num,
        }
        async with session.get('https://auto.ru/rossiya/trailer/all/', params=params, cookies=cookies, headers=headers,
                               proxy=f"http://{rand_proxy}") as resp:
            return await resp.text(encoding="utf-8")


async def get_property_settings(url):#, rand_proxy):
    async with aiohttp.ClientSession() as session:
        cookies = {
            'spravka': 'dD0xNzAxNDIxNDQ1O2k9OTUuMzIuNzMuMTMwO0Q9MUMyOUNDMzU2RjQwMjI4QTQ1NjhBQzQ2RTc0MTVEQ0IyOUJDMTZGMTM3N0FFRENCQTAwNTFFMjhCRjFENUY3REU2QzI1MzVGMUYyQjUzREQ5NTQ0RjQyNEIxQzdBQUE5NjFBOUJGMjMxMkIzNUY1Njc2MEVGMUY3Q0FGMkYzNDhEM0U4MUQ4MTYwNzVBNDM0O3U9MTcwMTQyMTQ0NTI3ODY4Njk5MDtoPWMxNGJhMTI3Yzk0YjUzYjM2MmFhYmNiZjMzOWRkMTdk',
            '_yasc': '6/IEgn3KwqWyw/5ejNFt43ZMzO7KMbFtFO+OxGUCm/O9inF/nfJMRaeXkRaDG7lH6qkOT/cSvAE=',
            'suid': '1fcc5294ad3df71178d0da0a8a412119.188e4f223b937631fab3e2f6573b83cb',
            'autoru_sid': 'a^%^3Ag6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c^%^7C1701421445487.604800.STEgpmoYnjmdyrYH85l5hw.ATkLP66QoTuhm3Zq5XyF2Ie1PLZGqdOio7wYM-jhwx0',
            'autoruuid': 'g6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c',
            'yandex_login': '',
            'i': 'Ha19B7QYaEgnr1f1yJah2/ALH7Q/HcLfECpXtbr4k0gM3i67gKSE3zryYUGQAqMUz6UUBJSvE9NcAKtjcDl0DDOD+qw=',
            'yandexuid': '5030237351701541850',
            'mda2_beacon': '1701541850813',
            'layout-config': '{screen_height:960,screen_width:1708,win_width:1686.25,win_height:427.5}',
            '_ym_uid': '1701421443933204740',
            '_ym_d': '1701527792',
            'popups-dr-shown-count': '1',
            'fp': 'b8b930ff929cc40b202f0caaeb2af241^%^7C1701421456264',
            'cycada': 'iRAx/dArHO0cWwrcuFo/kqBkub9g5zWCcHiYTE11jGY=',
            'autoru-visits-count': '2',
            '_csrf_token': '5fccd8d506043cb52f4059266bd99ac1477899be94ef5dee',
            'from_lifetime': '1701541850256',
            'from': 'direct',
            'ys': 'c_chck.12635065',
            'count-visits': '4',
            'yaPassportTryAutologin': '1',
            'gdpr': '0',
            '_ym_isad': '2',
            'autoru_sso_blocked': '1',
            'Session_id': 'noauth:1701541850',
            'sessar': '1.1184.CiAJyjvKUTMLidVbA-Gkt67OUQB-s3YXEzWnlqEJ17a22Q.SN2EM2qDD8ARvkGIPkjFDftyT4hBXftEhf1dB9ATHag',
            'sso_status': 'sso.passport.yandex.ru:synchronized',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://sso.auto.ru/',
            'Connection': 'keep-alive',
            # 'Cookie': 'spravka=dD0xNzAxNDIxNDQ1O2k9OTUuMzIuNzMuMTMwO0Q9MUMyOUNDMzU2RjQwMjI4QTQ1NjhBQzQ2RTc0MTVEQ0IyOUJDMTZGMTM3N0FFRENCQTAwNTFFMjhCRjFENUY3REU2QzI1MzVGMUYyQjUzREQ5NTQ0RjQyNEIxQzdBQUE5NjFBOUJGMjMxMkIzNUY1Njc2MEVGMUY3Q0FGMkYzNDhEM0U4MUQ4MTYwNzVBNDM0O3U9MTcwMTQyMTQ0NTI3ODY4Njk5MDtoPWMxNGJhMTI3Yzk0YjUzYjM2MmFhYmNiZjMzOWRkMTdk; _yasc=6/IEgn3KwqWyw/5ejNFt43ZMzO7KMbFtFO+OxGUCm/O9inF/nfJMRaeXkRaDG7lH6qkOT/cSvAE=; suid=1fcc5294ad3df71178d0da0a8a412119.188e4f223b937631fab3e2f6573b83cb; autoru_sid=a^%^3Ag6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c^%^7C1701421445487.604800.STEgpmoYnjmdyrYH85l5hw.ATkLP66QoTuhm3Zq5XyF2Ie1PLZGqdOio7wYM-jhwx0; autoruuid=g6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c; yandex_login=; i=Ha19B7QYaEgnr1f1yJah2/ALH7Q/HcLfECpXtbr4k0gM3i67gKSE3zryYUGQAqMUz6UUBJSvE9NcAKtjcDl0DDOD+qw=; yandexuid=5030237351701541850; mda2_beacon=1701541850813; layout-config={screen_height:960,screen_width:1708,win_width:1686.25,win_height:427.5}; _ym_uid=1701421443933204740; _ym_d=1701527792; popups-dr-shown-count=1; fp=b8b930ff929cc40b202f0caaeb2af241^%^7C1701421456264; cycada=iRAx/dArHO0cWwrcuFo/kqBkub9g5zWCcHiYTE11jGY=; autoru-visits-count=2; _csrf_token=5fccd8d506043cb52f4059266bd99ac1477899be94ef5dee; from_lifetime=1701541850256; from=direct; ys=c_chck.12635065; count-visits=4; yaPassportTryAutologin=1; gdpr=0; _ym_isad=2; autoru_sso_blocked=1; Session_id=noauth:1701541850; sessar=1.1184.CiAJyjvKUTMLidVbA-Gkt67OUQB-s3YXEzWnlqEJ17a22Q.SN2EM2qDD8ARvkGIPkjFDftyT4hBXftEhf1dB9ATHag; sso_status=sso.passport.yandex.ru:synchronized',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }

        async with session.get(url, cookies=cookies, headers=headers)  as resp:#, proxy=f"http://{rand_proxy}") as resp:
            return await resp.text(encoding="utf-8")


async def get_ads_list(rand_proxy):
    link_list = []
    for page in range(1, 30):
        html_response = await settings(page_num=page, rand_proxy=rand_proxy)
        soup = BeautifulSoup(html_response, "lxml")

        html_blocks = soup.find_all('div', class_='ListingItem')

        for block in html_blocks:
            title = block.find('a', class_='Link ListingItemTitle__link').get_text(strip=True)
            link = block.find('a', class_='Link ListingItemTitle__link')['href']
            value = [title, link]
            link_list.append(value)

    with open('data_list.pickle', 'wb') as file_:
        pickle.dump(link_list, file_)


async def get_property():
    with open('data_list.pickle', 'rb') as file_:
        data_list = pickle.load(file_)
        data_list = data_list[170:]

    cnt = 171
    for link in data_list:
        # rand_proxy = random.choice(PROXY_LIST)
        mark = link[0].split(' ')[0]
        model = ' '.join(link[0].split(' ')[1:])
        response = await get_property_settings(link[1])#, rand_proxy)
        soup = BeautifulSoup(response, "lxml")
        html_year = soup.find('li', class_='CardInfoRow CardInfoRow_year')
        year = html_year.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_year else 0
        # if year != '2023':
        #     continue
        city = soup.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').get_text(strip=True).replace(',', '')
        try:
            region = get_location(city)
        except Exception:
            region = city
        price = soup.find('span', class_='OfferPriceCaption__price').get_text(strip=True).replace(' ', '').replace('₽', '')
        html_type = soup.find('li', class_='CardInfoRow CardInfoRow_trailerType')
        type_ = html_type.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_type else 0
        html_load = soup.find('li', class_='CardInfoRow CardInfoRow_loading')
        load = html_load.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_load else 0
        html_axis = soup.find('li', class_='CardInfoRow CardInfoRow_axis')
        axis = html_axis.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_axis else 0
        html_brake = soup.find('li', class_='CardInfoRow CardInfoRow_breakType')
        brake = html_brake.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_brake else 0
        html_suspension = soup.find('li', class_='CardInfoRow CardInfoRow_suspensionType')
        suspension = html_suspension.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_suspension else 0
        up_axis = 'нет'
        text_elements = soup.find_all(string=True)
        text = 'одъёмная ось'
        for element in text_elements:
            if text in element:
                up_axis = 'есть'
                break
        save_in_excel(year, type_, mark, model, suspension, brake, load, axis, up_axis, price, region, link[1], cnt)
        print(cnt)
        cnt += 1


if __name__ == "__main__":
    # rand_proxy = random.choice(PROXY_LIST)

    asyncio.run(get_property())
    # asyncio.run(get_ads_list(rand_proxy))
    # with open('data_list.pickle', 'rb') as file_:
    #     data_list = pickle.load(file_)
    # print(data_list)

