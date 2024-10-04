import urllib.request
import urllib.parse
from lxml import etree


# 封装爬虫
class Translator:
    # 翻译接口
    url = "http://wap.youdao.com/translate"

    # 配置用户代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    # 有道翻译
    def translate(self, inputtext):
        # 需要翻译的数据
        data = {
            'inputtext': inputtext,
            'type': 'AUTO'
        }

        # post 请求的参数需要编码
        data = urllib.parse.urlencode(data).encode('utf-8')

        # 定制 Request 对象，指定接口、数据和用户代理
        request = urllib.request.Request(url=Translator.url, data=data, headers=Translator.headers)
        response = urllib.request.urlopen(request)

        content = response.read().decode('utf-8')
        tree = etree.HTML(content)

        result = tree.xpath('//div[@class="generate"]//li/text()')[0]
        return result