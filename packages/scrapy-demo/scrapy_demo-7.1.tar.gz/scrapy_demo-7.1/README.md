### scrapy通用模板

导入待爬取json文件

模板如下

```json
{
    "name": "qidian",
    "start_url": ["https://www.qidian.com/all/","https://www.qidian.com/all/page2/"],
    "allowed_domains": [
        "www.qidian.com", 
		"book.qidian.com"
    ],
    "datas": {
		"classify":"//div[@class='work-filter type-filter']/h3/text()",
		"//ul[@class='all-img-list cf']/li":{
        "name": ".//div[@class='book-mid-info']/h2/a/text()",
        "img_url": ".//a[@data-eid='qd_B57']/img/@src",
        "detail_url": ".//a[@data-eid='qd_B57']/@href"
    }},
    "start_page": 1,
    "end_page": 5,
    "save_pipeline": {
        "type": "csv",
		"file_path": "C://Users//17580//Desktop//scrapy-redis分享//test.csv"
    },
	"RETRY_TIMES":3,
    "DOWNLOAD_DELAY": 1,
	"DEFAULT_REQUEST_HEADERS":{
	  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	  "Accept-Language": "en"
	}
}
```

