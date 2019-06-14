# -*- coding: utf-8 -*-
import url_manager, html_pareser, html_downloader, html_outputer
'''
time: 2017-03-18
'''


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownLoader()
        self.parser = html_pareser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('craw %d:%s' % (count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 1100:
                    break

                count = count + 1
            except:
                print('craw failed ：')
            #     想看错误日志时，可使用这个
            # except Exception as e:
            #     print('craw failed ：',e)

        self.outputer.output_html()


if __name__ == "__main__":
    url_list = [
        "https://baike.baidu.com/item/%E5%8E%86%E5%8F%B2%E4%BA%BA%E7%89%A9/60502#viewPageContent",
        "https://baike.baidu.com/item/%E6%94%BF%E6%B2%BB/169778?fr=aladdin",
        "https://baike.baidu.com/item/%E7%BB%8F%E6%B5%8E",
        "https://baike.baidu.com/item/%E7%A7%91%E5%AD%A6%E5%AE%B6/1210114?fr=aladdin",
        "https://baike.baidu.com/item/%E5%95%86%E4%BA%BA/1243610",
        "https://baike.baidu.com/item/%E7%94%B5%E5%BD%B1%E6%98%8E%E6%98%9F/1125388",
        "https://baike.baidu.com/item/%E6%AD%8C%E6%89%8B/20270239",
        "https://baike.baidu.com/item/%E9%A2%86%E5%AF%BC%E4%BA%BA",
        "https://baike.baidu.com/item/%E7%94%BB%E5%AE%B6/1215119",
        "https://baike.baidu.com/item/%E9%9F%B3%E4%B9%90%E5%AE%B6/68404#viewPageContent",
        "https://baike.baidu.com/item/%E5%8F%91%E6%98%8E%E5%AE%B6",
        "https://baike.baidu.com/item/%E5%BF%83%E7%90%86%E5%AD%A6%E5%AE%B6"
    ]
    for url in url_list:
    # root_url = "https://baike.baidu.com/item/%E5%8E%86%E5%8F%B2%E4%BA%BA%E7%89%A9/2973268"
        obj_spider = SpiderMain()
        obj_spider.craw(url)
