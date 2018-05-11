### 爬取[http://hzp.onlylady.com/brand.html](http://hzp.onlylady.com/brand.html)上的各个品牌的商品
- 使用`python3.6`
- 需要安装`pip install scrapy`
- 图片我爬取下来总共`25535`张
- 写入`txt`文件的信息有：
  - 商品名
  - 商品类型
  - 商品所属的品牌
  - 商品价格
  - 商品图片对应的图片名
> 各个参数直接用`@`分割开，每个商品之间用`####`分隔开，便于对文件的处理
### 爬取[http://cosmetic.lady.163.com/search/product/](http://cosmetic.lady.163.com/search/product/)上的各个品牌的商品
- 同上，只是图片有所减少，因为排除了一些默认图片的商品
