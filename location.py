import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import aiohttp


def get_location(city_name):
    url = "https://ru.wikipedia.org/w/api.php?action=query&prop=coordinates&format=json&titles={}"
    data = requests.get(url.format(city_name)).json()
    resp = data["query"]['pages']
    key = next(iter(resp))
    lat, lon = resp[key]['coordinates'][0]['lat'], resp[key]['coordinates'][0]['lon']

    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.reverse(f"{lat},{lon}")

    return location.raw['address']['state']


# import requests
#
# cookies = {
#     'spravka': 'dD0xNzAxNDIxNDQ1O2k9OTUuMzIuNzMuMTMwO0Q9MUMyOUNDMzU2RjQwMjI4QTQ1NjhBQzQ2RTc0MTVEQ0IyOUJDMTZGMTM3N0FFRENCQTAwNTFFMjhCRjFENUY3REU2QzI1MzVGMUYyQjUzREQ5NTQ0RjQyNEIxQzdBQUE5NjFBOUJGMjMxMkIzNUY1Njc2MEVGMUY3Q0FGMkYzNDhEM0U4MUQ4MTYwNzVBNDM0O3U9MTcwMTQyMTQ0NTI3ODY4Njk5MDtoPWMxNGJhMTI3Yzk0YjUzYjM2MmFhYmNiZjMzOWRkMTdk',
#     '_yasc': 'rvurSqCV0dEuqcU0GAqFcuBZ2yeaTk6u7F3ESCmtQ5fVrplGk4dm7+EF2bZfxHELag5X1BvsBbU=',
#     'suid': '1fcc5294ad3df71178d0da0a8a412119.188e4f223b937631fab3e2f6573b83cb',
#     'autoru_sid': 'a^%^3Ag6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c^%^7C1701421445487.604800.STEgpmoYnjmdyrYH85l5hw.ATkLP66QoTuhm3Zq5XyF2Ie1PLZGqdOio7wYM-jhwx0',
#     'autoruuid': 'g6569a1852ijtl0p4lf31aavkcnhvvmd.3ee4ef13bed61551f74d5aa4cff1d29c',
#     'yandex_login': '',
#     'i': 'Ha19B7QYaEgnr1f1yJah2/ALH7Q/HcLfECpXtbr4k0gM3i67gKSE3zryYUGQAqMUz6UUBJSvE9NcAKtjcDl0DDOD+qw=',
#     'yandexuid': '5030237351701541850',
#     'mda2_beacon': '1701557616250',
#     'layout-config': '{screen_height:960,screen_width:1708,win_width:1707.5,win_height:306.25}',
#     '_ym_uid': '1701421443933204740',
#     '_ym_d': '1701559423',
#     'popups-dr-shown-count': '1',
#     'fp': 'b8b930ff929cc40b202f0caaeb2af241^%^7C1701421456264',
#     'cycada': 'VOPNeN8tXZpP+SloPp5LqCoGuewZ52Ht1fvNM5rDEfo=',
#     'autoru-visits-count': '4',
#     '_csrf_token': '5fccd8d506043cb52f4059266bd99ac1477899be94ef5dee',
#     'from_lifetime': '1701560507516',
#     'from': 'direct',
#     'ys': 'c_chck.158953186',
#     'yaPassportTryAutologin': '1',
#     'gdpr': '0',
#     '_ym_isad': '2',
#     'autoru_sso_blocked': '1',
#     'Session_id': 'noauth:1701557616',
#     'sessar': '1.1184.CiBJC8XWT7D_rSQjFlIDY8pXzmVOxv_xVNPiFnGz6Su_UA.nP6qOvtxCw5PlCe6rRZGvvyN08J4BI7DgT_Ht1Y0iAQ',
#     'sso_status': 'sso.passport.yandex.ru:synchronized_no_beacon',
#     'autoru-visits-session-unexpired': '1',
#     'count-visits': '3',
# }
#
# headers = {
#     'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
#     'Referer': 'https://www.wildberries.ru/catalog/164614093/detail.aspx',
#     'sec-ch-ua-mobile': '?0',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
#     'sec-ch-ua-platform': '"Windows"',
# }
#
# response = requests.get(
#     'https://auto.ru/trailer/new/sale/specpricep/tyajelovoz___m/1121488633-abf1b447/',
#     cookies=cookies,
#     headers={'Accept-Charset': 'utf-8'},
# )
# soup = BeautifulSoup(response.text, "lxml")
# price = soup.find('span', class_='OfferPriceCaption__price').get_text(strip=True)
# price = price.encode('utf-8').decode('unicode_escape')
# html_type = soup.find('li', class_='CardInfoRow CardInfoRow_trailerType')
# type_ = html_type.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_type else 0
# html_load = soup.find('li', class_='CardInfoRow CardInfoRow_loading')
# load = html_load.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_load else 0
# html_axis = soup.find('li', class_='CardInfoRow CardInfoRow_axis')
# axis = html_axis.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_axis else 0
# html_brake = soup.find('li', class_='CardInfoRow CardInfoRow_breakType')
# brake = html_brake.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_brake else 0
# html_suspension = soup.find('li', class_='CardInfoRow CardInfoRow_suspensionType')
# suspension = html_suspension.find_all('span', class_='CardInfoRow__cell')[1].get_text(strip=True) if html_suspension else 0