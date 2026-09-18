import time
import pandas as pd
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def request_pro(url,limit,headers,timeout=10,original_resp=None):

    while limit:
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()

        except requests.exceptions.Timeout:
            print("请求超时")
            limit -= 1

        except requests.exceptions.ConnectionError:
            print("连接失败，比如 DNS、网络、连接被拒绝")
            limit -= 1

        except requests.exceptions.HTTPError as e:
            print("HTTP 错误：", e)
            limit -= 1

        except requests.exceptions.RequestException as e:
            print("其他请求异常：", e)
            limit -= 1

        else:
            print("成功")
            return resp

    return original_resp

"""def to_absolute_path(base_url,url):
    page = re.search(r"page=(\d+)",url)
    if not page:
        print('网址格式错误')
        return None
    page = page.group(1)
    new_url = re.sub(r"(page=)\d+", rf"\g<1>{page}", base_url)
    return new_url"""

def urljoin_plus(resp,url,soup):
    if not url:
        return None
    base = resp.url
    base_tag = soup.find("base", href=True)
    if base_tag:
        base = urljoin(resp.url, base_tag["href"])
    absolute = urljoin(base,url)
    return absolute

def collecter(data,cha,function):
    tag = data.select_one(cha)
    if tag is None:
        return None
    return function(tag)

def main():
    # 目标地址
    base_url = "http://127.0.0.1:8000/page1.html"
    url = base_url
    # 向服务器发出的请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
    }

    resp = request_pro(url,3,headers)

    if not resp:
        print('初始网址请求失败')
        return 0

    content_type = resp.headers.get("Content-Type", "")
    print(content_type)

    if "application/json" in content_type:
        data = resp.json()

    elif "text/html" in content_type:
        one_page = False
        fail = False
        df = {'product':[],'price':[],'category':[],'id':[],'rating':[],'url':[],'reviews':[]}
        url_set = []
        while 1:

            if url_set:
                url_set_copy = url_set.copy()
                for what_name in url_set_copy:
                    temp_resp = request_pro(url=what_name, limit=3, headers=headers)
                    url_set.pop(0)
                    if temp_resp:
                        resp = temp_resp
                        break
                    if not url_set:
                        fail = True
                        print('无法打开网页请检查网络')

            if fail:break

            soup = BeautifulSoup(resp.text, "lxml")
            product_set = soup.select_one('div.products')
            if not product_set:
                print('products未找到，或名称以改变')
                datas = []
            else:
                datas = product_set.select('div.product')

            if not datas:
                print('未找到class为product的标签,请确认class的值是否有变动')
            else:
                for data in datas:
                    df.get('product').append(collecter(data,'h2.title', lambda t: t.get_text()))
                    df.get('price').append(collecter(data,'span.price', lambda t: t.get_text()))
                    df.get('category').append(collecter(data,'span.category', lambda t: t.get_text()))
                    df.get('id').append(collecter(data,'span.category', lambda t: t.get('data-id')))
                    df.get('rating').append(collecter(data,'span.rating', lambda t: t.get_text()))
                    df.get('url').append(collecter(data,'a.detail-link', lambda t: t.get('href')))
                    df.get('reviews').append(collecter(data,'span.reviews', lambda t: t.get_text()))

            if url_set:continue

            next_btn = soup.select_one('.next')

            if not next_btn or one_page:
                print('所有分页数据均提取完成')
                break

            url = next_btn.get('href')

            if not url:
                print('错误,html未提供下一页网址\n')
                break

            url = urljoin_plus(resp,url,soup)

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
            }

            if not url:
                print('url转换失败')
                return

            temp_resp = request_pro(url=url,limit=3,headers=headers,original_resp=None)

            if not temp_resp:
                # 尝试寻找此页面的后续页面url
                url_set = soup.select('a.page')
                if not url_set:
                    print('next失效且此网页检索不到后续页面网址')
                    return 0
                url_set[:] = [
                    href for x in url_set
                    if (href := urljoin_plus(resp,x.get('href'),soup))
                ]
                url_set_copy = url_set.copy()
                for what_name in url_set_copy:
                    if what_name == resp.url:
                        url_set.pop(0)
                        break
                    url_set.pop(0)
                if not url_set:
                    print('next失效且此网页检索不到后续页面网址')
                    return 0
            else:
                resp = temp_resp

            time.sleep(1)

        df = pd.DataFrame(df)
        print(df)
    else:
        raw = resp.content

if __name__ == "__main__":
    print(main())