import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import aiohttp
from requests_html import HTMLSession
from fake_useragent import UserAgent


def get_location(city_name):
    url = "https://ru.wikipedia.org/w/api.php?action=query&prop=coordinates&format=json&titles={}"
    data = requests.get(url.format(city_name)).json()
    resp = data["query"]['pages']
    key = next(iter(resp))
    lat, lon = resp[key]['coordinates'][0]['lat'], resp[key]['coordinates'][0]['lon']

    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.reverse(f"{lat},{lon}")

    return location.raw['address']['state']


# cookies = {
#             'spravka': 'dD0xNzAxNDIxNDQ1O2k9OTUuMzIuNzMuMTMwO0Q9MUMyOUNDMzU2RjQwMjI4QTQ1NjhBQzQ2RTc0MTVEQ0IyOUJDMTZGMTM3N0FFRENCQTAwNTFFMjhCRjFENUY3REU2QzI1MzVGMUYyQjUzREQ5NTQ0RjQyNEIxQzdBQUE5NjFBOUJGMjMxMkIzNUY1Njc2MEVGMUY3Q0FGMkYzNDhEM0U4MUQ4MTYwNzVBNDM0O3U9MTcwMTQyMTQ0NTI3ODY4Njk5MDtoPWMxNGJhMTI3Yzk0YjUzYjM2MmFhYmNiZjMzOWRkMTdk',
#             '_yasc': 'Z8ito11h5tGI5jm0NtCLX91IeaTFO7V/DawtMmY2RILBrY4r+LxPoXMZ6tvpUMhqSsvKOOgoBqE=',
#             'gdpr': '0',
#             '_ym_visorc': 'b',
#             'suid': '1fcc5294ad3df71178d0da0a8a412119.188e4f223b937631fab3e2f6573b83cb',
#             '_csrf_token': '1aed5afef4e512162132d613fe6e0fddf9112a4247b84622',
#             'autoru_sid': 'a^%^3Ag6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c^%^7C1701421445487.604800.STEgpmoYnjmdyrYH85l5hw.ATkLP66QoTuhm3Zq5XyF2Ie1PLZGqdOio7wYM-jhwx0',
#             'autoruuid': 'g6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c',
#             'from_lifetime': '1701422479248',
#             'from': 'direct',
#             'autoru_sso_blocked': '1',
#             'Session_id': 'noauth:1701421445',
#             'sessar': '1.1184.CiA95iTx5Q98Ew3VgO38HNc3S9KfDkP4yTvTAuRYBYawfg.9fCnR83NZZ7Cg5-KdL838qcpw_aZ5t_MMI6RbOJQo3A',
#             'yandex_login': '',
#             'ys': 'c_chck.3192317861',
#             'i': 'XteuW9UhfJ6HFrsugRX3jGL3Bjr57t9zIHP07IhF0o5kcpYQ8ADX89Vk4zSSMvuxiBOiRmJ0nsnMMdu8tXQvpSrDSLs=',
#             'yandexuid': '1765520041701333029',
#             'mda2_beacon': '1701421445786',
#             'sso_status': 'sso.passport.yandex.ru:synchronized_no_beacon',
#             'layout-config': '{screen_height:960,screen_width:1708,win_width:1686.25,win_height:273.75}',
#             '_arsus': 'true',
#             'count-visits': '3',
#             '_ym_uid': '1701421443933204740',
#             '_ym_d': '1701421641',
#             '_ym_isad': '2',
#             'yaPassportTryAutologin': '1',
#             'popups-dr-shown-count': '1',
#             'fp': 'b8b930ff929cc40b202f0caaeb2af241^%^7C1701421456264',
#             'cycada': 'P7mdXXLuSRcHx26DoWg4gyoGuewZ52Ht1fvNM5rDEfo=',
#             'autoru-visits-count': '1',
#             'autoru-visits-session-unexpired': '1',
#         }
#
# ua = UserAgent()
# user_agent = ua.random
# headers = {
#             'User-Agent': user_agent,
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#             'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#             # 'Accept-Encoding': 'gzip, deflate, br',
#             'Connection': 'keep-alive',
#             # 'Cookie': 'spravka=dD0xNzAxNDIxNDQ1O2k9OTUuMzIuNzMuMTMwO0Q9MUMyOUNDMzU2RjQwMjI4QTQ1NjhBQzQ2RTc0MTVEQ0IyOUJDMTZGMTM3N0FFRENCQTAwNTFFMjhCRjFENUY3REU2QzI1MzVGMUYyQjUzREQ5NTQ0RjQyNEIxQzdBQUE5NjFBOUJGMjMxMkIzNUY1Njc2MEVGMUY3Q0FGMkYzNDhEM0U4MUQ4MTYwNzVBNDM0O3U9MTcwMTQyMTQ0NTI3ODY4Njk5MDtoPWMxNGJhMTI3Yzk0YjUzYjM2MmFhYmNiZjMzOWRkMTdk; _yasc=Z8ito11h5tGI5jm0NtCLX91IeaTFO7V/DawtMmY2RILBrY4r+LxPoXMZ6tvpUMhqSsvKOOgoBqE=; gdpr=0; _ym_visorc=b; suid=1fcc5294ad3df71178d0da0a8a412119.188e4f223b937631fab3e2f6573b83cb; _csrf_token=1aed5afef4e512162132d613fe6e0fddf9112a4247b84622; autoru_sid=a^%^3Ag6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c^%^7C1701421445487.604800.STEgpmoYnjmdyrYH85l5hw.ATkLP66QoTuhm3Zq5XyF2Ie1PLZGqdOio7wYM-jhwx0; autoruuid=g6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c; from_lifetime=1701422479248; from=direct; autoru_sso_blocked=1; Session_id=noauth:1701421445; sessar=1.1184.CiA95iTx5Q98Ew3VgO38HNc3S9KfDkP4yTvTAuRYBYawfg.9fCnR83NZZ7Cg5-KdL838qcpw_aZ5t_MMI6RbOJQo3A; yandex_login=; ys=c_chck.3192317861; i=XteuW9UhfJ6HFrsugRX3jGL3Bjr57t9zIHP07IhF0o5kcpYQ8ADX89Vk4zSSMvuxiBOiRmJ0nsnMMdu8tXQvpSrDSLs=; yandexuid=1765520041701333029; mda2_beacon=1701421445786; sso_status=sso.passport.yandex.ru:synchronized_no_beacon; layout-config={screen_height:960,screen_width:1708,win_width:1686.25,win_height:273.75}; _arsus=true; count-visits=3; _ym_uid=1701421443933204740; _ym_d=1701421641; _ym_isad=2; yaPassportTryAutologin=1; popups-dr-shown-count=1; fp=b8b930ff929cc40b202f0caaeb2af241^%^7C1701421456264; cycada=P7mdXXLuSRcHx26DoWg4gyoGuewZ52Ht1fvNM5rDEfo=; autoru-visits-count=1; autoru-visits-session-unexpired=1',
#             'Upgrade-Insecure-Requests': '1',
#             'Sec-Fetch-Dest': 'document',
#             'Sec-Fetch-Mode': 'navigate',
#             'Sec-Fetch-Site': 'none',
#             'Sec-Fetch-User': '?1',
#             # Requests doesn't support trailers
#             # 'TE': 'trailers',
#         }
#
# session = HTMLSession()
# r = session.get('https://auto.ru/trailer/new/sale/krone/sd/1120649739-60456017/', cookies=cookies, headers=headers)
# soup = BeautifulSoup(r.text, "lxml")
# html_year = soup.find('li', class_='CardInfoRow CardInfoRow_year')
# year = html_year.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_year else 0
# city = soup.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').get_text(strip=True).replace(',', '')

# def useragent_soup(url_):
#     ua = UserAgent()
#     user_agent = ua.random
#     headers = {'User-Agent': user_agent}
#     response = requests.get(url_, headers=headers)
#     soup = BeautifulSoup(response.text, 'lxml')
#
#     return soup
#
# useragent_soup('https://auto.ru/trailer/new/sale/krone/sd/1120649739-60456017/')