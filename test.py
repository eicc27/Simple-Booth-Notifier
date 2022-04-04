from urllib import request as req
from lxml import etree
import re

url = "https://amenochiyuki.booth.pm/"
opener = req.build_opener()
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")]
req.install_opener(opener)
reqStr: str = req.urlopen(url=url, timeout=10) \
    .read() \
    .decode("utf-8")
""" for m in re.finditer("data-product-id=\"[0-9]*\"", reqStr):
    print(m.group(0)) """
tree = etree.HTML(reqStr)
print(tree.xpath("//li/@data-product-id"))
