import asyncio, aiohttp, ssl, logging, os, re
from bs4 import BeautifulSoup
from django.conf import settings


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='logs/blacktyres_parser.log',
    filemode='w',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

BLACKTYRES_PARSER_API_HOST = os.getenv('BLACKTYRES_PARSER_API_HOST', 'localhost')
BLACKTYRES_PARSER_API_PORT = os.getenv('BLACKTYRES_PARSER_API_PORT', '8000')

SEASON_URLS = {
    'zimnie': 'https://blacktyres.ru/catalog-tyres/zimnie-shiny/',
    'letnie': 'https://blacktyres.ru/catalog-tyres/letnie-shiny/',
    'vsesezonnye': 'https://blacktyres.ru/catalog-tyres/vsesezonnye-shiny/'
}

semaphore = asyncio.Semaphore(5)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def clean_numeric_value(value, is_int=False):
    if value is None or value == 'Not found':
        return None
    cleaned_value = re.sub(r'[^\d.]', '', str(value).strip())
    if not cleaned_value:
        return None
    try:
        if is_int:
            return int(float(cleaned_value))
        return float(cleaned_value)
    except (ValueError, TypeError):
        logger.warning(f"Не удалось преобразовать значение: {value}")
        return None

async def fetch(session, url, retries=3, delay=5, timeout=60):
    for attempt in range(retries):
        try:
            async with session.get(url, headers=headers, timeout=timeout) as response:
                if response.status == 404:
                    logger.info(f"Конец пагинации достигнут для {url}")
                    return None
                logger.info(f"Успешный запрос: {url}")
                return await response.text()
        except asyncio.TimeoutError:
            if attempt == retries - 1:
                logger.error(f"Таймаут при запросе {url} после {retries} попыток")
                return None
            else:
                logger.warning(f"Таймаут при запросе {url}, попытка {attempt + 1}")
                await asyncio.sleep(delay)
        except aiohttp.ClientError as e:
            if attempt == retries - 1:
                logger.error(f"Ошибка при запросе {url} после {retries} попыток: {e}")
                return None
            else:
                logger.warning(f"Ошибка при запросе {url}, попытка {attempt + 1}: {e}")
                await asyncio.sleep(delay)

async def get_price(soup):
    price_tag = soup.select_one('.product-price span[id^="cart-price-"]')
    return price_tag.get_text(strip=True) if price_tag else 'Not found'

async def get_all_brands(session, base_url):
    content = await fetch(session, base_url)
    if content is None:
        logger.warning(f"Не удалось получить бренды с {base_url}")
        return {}
    soup = BeautifulSoup(content, 'html.parser')
    brands = {}
    
    brand_list = soup.find('div', class_="item filter-brand")
    if brand_list:
        for brand in brand_list.find_all('a', class_="filter-name"):
            brand_name = brand.get_text(strip=True).replace(' ', '_')
            brand_url = 'https://blacktyres.ru' + brand.get('href')
            brands[brand_name] = brand_url
            logger.info(f"Добавлен бренд: {brand_name}")
    return brands

async def process_pagination(session, base_url):
    page = 0
    products_data_list = []

    while True:
        if page == 0:
            url = base_url
        else:
            url = f"{base_url}{page * 25}/"

        content = await fetch(session, url)
        if content is None:
            logger.info(f"Конец пагинации достигнут для {url}")
            break

        soup = BeautifulSoup(content, 'html.parser')
        products = soup.find_all('div', class_="catalog-product-wrap")

        if not products:
            logger.info(f"Нет продуктов на странице {url}")
            break

        for product in products:
            product_url_tag = product.find('a')
            if product_url_tag:
                full_url = 'https://blacktyres.ru' + product_url_tag.get('href')
                if full_url and not full_url.endswith('#'):
                    products_data_list.append(full_url)
                    logger.info(f"Добавлен продукт: {full_url}")
        page += 1
    return products_data_list

async def get_products_from_brand(session, brand_url):
    return await process_pagination(session, brand_url)

async def get_detail_info(session, url):
    async with semaphore:
        await asyncio.sleep(0.5)
        content = await fetch(session, url)
        if content is None:
            logger.warning(f"Не удалось получить данные с {url}")
            return None
        soup = BeautifulSoup(content, "html.parser")
        data = {}
        
        for meta in soup.find_all("meta", itemprop=True):
            data[meta["itemprop"]] = meta.get("content", "")
        
        for li in soup.select(".product-properties li, ul.properties li, li.property-code"):
            name_tag = li.select_one(".name span")
            value_tag = li.select_one(".value")
            
            if name_tag and value_tag:
                key = name_tag.get_text(strip=True)
                value = value_tag.get_text(strip=True)
                data[key] = value
        
        availability = 'В наличии' if soup.select_one('.product-status.yes') else 'Нет в наличии'
        images = [f'https://blacktyres.ru{soup.select_one(".product-image.block img").get("data-src", "")}'] if soup.select_one(".product-image.block img") else ['Not found']
        
        product_info = {
            'product_name': data.get('Модель', 'Not found'),
            'price': await get_price(soup),
            'manufacturer': data.get('Бренд', 'Not found'),
            'speed_index': data.get('Индекс скорости', 'Not found'),
            'load_index': data.get('Индекс нагрузки', 'Not found'),
            'season': data.get('Сезон', 'Not found'),
            'width': data.get('Ширина профиля', 'Not found'),
            'height': data.get('Высота профиля', 'Not found'),
            'diameter': data.get('Диаметр', 'Not found'),
            'availability': availability,
            'images': images,
            'url': url
        }
        return product_info

async def save_product_info(product_info):
    if product_info:
        data = {
            "season": product_info.get("season", "unknown"),
            "brand": product_info["manufacturer"].replace(" ", "_"),
            "product_name": product_info.get("product_name", "Not found"),
            "price": clean_numeric_value(product_info.get("price", "Not found")),
            "speed_index": product_info.get("speed_index", "Not found"),
            "load_index": product_info.get("load_index", "Not found"),
            "width": clean_numeric_value(product_info.get("width", "Not found"), is_int=True),
            "height": clean_numeric_value(product_info.get("height", "Not found"), is_int=True),
            "diameter": clean_numeric_value(product_info.get("diameter", "Not found")),
            "availability": product_info.get("availability", "Not found"),
            "images": product_info.get("images", []),
            "url": product_info.get("url", "Not found"),
        }
        logger.info(f"Отправляемые данные: {data}")
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://localhost:8000/api/v1/tyres/', json=data) as response:
                if response.status == 201:
                    logger.info(f'Данные успешно отправлены в API для {product_info["manufacturer"]} - {product_info["season"]}')
                else:
                    logger.error(f'Ошибка при отправке данных в API: {response.status}, ответ сервера: {await response.text()}')

async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        for season, base_url in SEASON_URLS.items():
            logger.info(f'Парсинг сезонов: {season}')
            brands = await get_all_brands(session, base_url)
            
            for brand_name, brand_url in brands.items():
                logger.info(f'Получени бренда: {brand_name} ({season})')
                product_urls = await get_products_from_brand(session, brand_url)
                
                for product_url in product_urls:
                    product_info = await get_detail_info(session, product_url)
                    if product_info:
                        await save_product_info(product_info)
                    else:
                        logger.warning(f"Не удалось получить информацию о продукте с {product_url}. Попытка повторного получения.")
                        product_info_retry = await get_detail_info(session, product_url)
                        if product_info_retry:
                            await save_product_info(product_info_retry)
                        else:
                            logger.error(f"Окончательно не удалось получить информацию о продукте с {product_url}")

if __name__ == "__main__":
    asyncio.run(main())
