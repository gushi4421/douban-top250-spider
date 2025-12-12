"""
爬虫的核心模块，用于爬取网页数据

下面是对各个函数的简单介绍：
    __init__()  类的初始化函数
    setup_logging() 日志记录函数，用于记录爬取过程中的信息，将信息保存在logs/spider.log文件当中
    fetch_page()  爬取一整个网页的信息，返回一整个网页的信息
    parse_single_movie()  解析单个电影的信息，返回解析到的电影信息
    parse_single_page() 解析一整个页面的电影信息，通过调用parse_single_movie()来实现对电影的解析
    parse_all_pages()   解析所有页面的信息，过程：通过fetch_page()抓取一整个页面的信息，然后调用parse_single_page()解析页面中的电影信息
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
import logging
from typing import List, Dict, Optional
import os
from sympy import true


class MovieSpider:
    def __init__(
        self,
        url: str = "https://movie.douban.com/top250",
    ):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",  # 反爬虫标识
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",  # 告诉服务器可以接受的内容类型
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",  # 语言偏好
            "Connection": "keep-alive",  # 连接方式
        }
        self.movies: List[Dict[str, Optional[str]]] = []  # 存储电影信息的列表
        self.setup_logging()

    def setup_logging(self):
        """
        设置日志记录
        """
        # 创建目录日志
        if not os.path.exists("logs"):
            os.makedirs("logs")

        logging.basicConfig(
            level=logging.INFO,  # 日志级别
            format="%(asctime)s - %(name)s -  %(levelname)s - %(message)s",  # 日志格式
            handlers=[
                logging.FileHandler("logs/spider.log", encoding="utf-8"),  # 日志文件
                logging.StreamHandler(),  # 控制台输出
            ],
        )
        self.logger = logging.getLogger(__name__)  # 获取日志记录器

    def fetch_page(self, url: str, retries: int = 3) -> Optional[str]:
        """
        获取网页内容（带重试机制）

        Args:
            retries (int): 重试次数

        Returns:
        页面HTML内容，如果失败则返回NOne
        """

        for attempt in range(retries):
            try:
                self.logger.info(f"正在请求页面：{url},第{attempt+1}次尝试")

                time.sleep(random.uniform(1, 3))  # 随机延时，模拟人类行为
                response = requests.get(
                    url=url,
                    headers=self.headers,
                    timeout=10,
                )
                print("当前状态码:", response.status_code)
                if response.status_code == 200:
                    response.encoding = "utf-8"
                    return response.text
                else:
                    self.logger.error(f"请求失败，状态码：{response.status_code}")
                    continue

            except requests.exceptions.Timeout as e:
                self.logger.error(f"第{attempt+1}次请求失败：{url}，错误信息：{e}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"第{attempt+1}次请求失败：{url},错误信息：{e}")
            except Exception as e:
                self.logger.error(f"第{attempt+1}次请求失败：{url},错误信息：{e}")
        return None

    def parse_single_movie(self, movie) -> Optional[Dict]:
        """
        解析单个电影信息
        Args:
            movie: 包含单个电影的div标签

        Returns:
                电影信息字典

        导演，演员部分的说明：
            第一行: 导演: XXX    主演: YYY /...
            第二行: 年份 / 国家 / 类型

            解析策略:
            1. 使用列表推导式清洗数据
            - 按换行符分割文本
            - 去除每行首尾空白 (strip)
            - 过滤掉空行
            示例:  lines = [line.strip() for line in text.split("\n") if line.strip()]

            2. 导演信息提取 (需要两次分割)
            原因: 导演在字符串开头，后面紧跟"主演:"信息
            步骤:
            - 第一次分割: 按"导演: "分割，取后半部分
                结果: "XXX    主演: YYY /..."
            - 第二次分割: 按"主演: "分割，取前半部分
                结果:  "XXX"
            - 边界处理: 如果没有"主演:"，直接使用第一次分割结果

            3. 演员信息提取 (只需一次分割)
            原因: 主演在字符串末尾，后面没有其他关键字段
            步骤:
            - 按"主演:"分割，取后半部分
            - 去除末尾的"..."符号
            结果: "YYY /"

            4. 年份/国家/类型提取
            格式: "1994 / 美国 / 犯罪 剧情"
            方法:  按"/"分割，依次取出三个部分

            关键点:
            - 导演处理复杂:  位于开头，需要"夹心提取"(去掉前后无关内容)
            - 演员处理简单: 位于末尾，只需"尾部截取"(去掉前面的关键字)
            - 使用strip()去除空白字符，使用rstrip()去除右侧特定字符
        """
        # 电影信息相关映射
        movie_info = {
            "rank": None,  # 排名
            "title": None,  # 电影名
            "director": None,  # 导演
            "actors": None,  # 演员
            "year": None,  # 上映时间
            "country": None,  # 制片国家/地区
            "classification": None,  # 影片类型
            "star-rating": None,  # 电影星级评分
            "nums-rating": None,  # 数字评分
            "comment_nums": None,  # 评论数
            "comment": None,  # 短评
        }

        # 爬取电影排名
        div_pic_tag = movie.find("div", class_="pic")
        movie_rank = div_pic_tag.find("em")
        if movie_rank:
            movie_info["rank"] = movie_rank.text.strip()
        else:
            movie_info["rank"] = None
            self.logger.warning("电影排名未找到")
            return None

        # 爬取电影标题
        movie_title = movie.find(
            "span", class_="title"
        )  # 在html中可以发现一个电影含有多个名称，只取第一个1
        if movie_title:
            movie_info["title"] = movie_title.text.strip()
        else:
            movie_info["title"] = None
            self.logger.warning("电影标题未找到")
            return None

        # <div class="bd"> 中包含了很多信息：导演，演员，年份，国家，类型，星级，评分，评论人数，短评
        bd_div_tag = movie.find("div", class_="bd")

        if bd_div_tag:
            # 爬取导演，演员，年份，国家和类型，这几个信息都存在一个p标签当中
            p_tag = bd_div_tag.find("p")
            if p_tag:
                # 按行进行分割
                p_text = p_tag.get_text(separator="\n", strip=True)
                p_lines = [line.strip() for line in p_text.split("\n") if line.strip()]
                if len(p_lines) >= 2:
                    first_line = p_lines[0]  # &nbsp已被BeautifulSoup自动处理为普通空格

                    # 解析导演
                    if "导演:" in first_line:
                        director = first_line.split("导演:")[1]
                        if "主演:" in director:
                            director = director.split("主演:")[0].strip()
                            movie_info["director"] = director.strip()
                    else:
                        movie_info["director"] = None
                        print("导演信息未找到")
                        return None
                    # 解析演员
                    if "主演:" in first_line:
                        actors = first_line.split("主演:")[1].strip()
                        movie_info["actors"] = actors.rstrip("...").strip()
                    else:
                        movie_info["actors"] = "unshown"
                        # self.logger.warning("演员信息未找到，已设置为'unshown'")
                        # 不返回 None，继续执行

                    # 解析年份，国家和类型
                    second_line = p_lines[1]
                    parts = [
                        part.strip() for part in second_line.split("/") if part.strip()
                    ]
                    if len(parts) >= 3:
                        movie_info["year"] = parts[0]
                        movie_info["country"] = parts[1]
                        movie_info["classification"] = parts[2]
                    else:
                        self.logger.warning(f"年份/国家/类型信息不完整: {second_line}")
                        return None
                else:
                    self.logger.warning("导演，演员等信息行格式不正确")
                    return None

            else:
                self.logger.warning("未找到包含导演，演员等信息的<p>标签")
                return None

            # 爬取评论星级
            for star in [
                "5",
                "45",
                "4",
            ]:  # 分析电影html可知，只有5和45这两种(5表示5星，45表示4.5星, 4表示4星)
                star_tag = bd_div_tag.find("span", class_=f"rating{star}-t")
                if star_tag:
                    movie_info["star-rating"] = star.replace("45", "4.5")
                    break
            if not movie_info["star-rating"]:
                movie_info["star-rating"] = None
                self.logger.warning("星级评分未找到")
                return None

            # 爬取评分
            num_rating_tag = bd_div_tag.find("span", class_="rating_num")
            if num_rating_tag:
                movie_info["nums-rating"] = num_rating_tag.text.strip()
            else:
                movie_info["nums-rating"] = None
                self.logger.warning("数字评分未找到")
                return None

            # 爬取评论人数
            spans = bd_div_tag.find_all("span")
            if spans:
                for span in spans:
                    if "人评价" in span.text:
                        movie_info["comment_nums"] = span.text.replace(
                            "人评价", ""
                        ).strip()
                        break
                if not movie_info["comment_nums"]:
                    movie_info["comment_nums"] = None
                    self.logger.warning("评论人数未找到")
                    return None
            # 爬取短评
            quote_tag = movie.find("p", class_="quote")
            if quote_tag:
                movie_info["comment"] = quote_tag.text.strip()
            else:
                movie_info["comment"] = None  # 短评可以为空，不强制要求
        else:
            self.logger.warning("未找到包含电影信息的<div class='bd'>标签")
        print(movie_info, "\n")
        return movie_info

    def parse_single_page(
        self, page_content: str, page_number: int
    ) -> Optional[List[Dict]]:
        """
        解析单个页面的所有电影信息
        Args:
            page_content(str):页面的内容信息
            page_number(int):当前页面的编号
        Returns:
            返回当前页面所有的电影的信息列表
        """
        results = []  # 存储当前页面的所有电影信息

        if not page_content:
            self.logger.warning(f"第{page_number}页的内容缺失")
            return None
        else:
            soup = BeautifulSoup(page_content, "lxml")
            movies = soup.find_all("div", class_="item")
            if not movies:
                self.logger.warning(f"第{page_number}页未找到任何电影项")
                return None
            for i, movie in enumerate(movies, 1):
                movie_info = self.parse_single_movie(movie)
                if movie_info:
                    results.append(movie_info)
                else:
                    self.logger.warning(f"第{page_number}页的第{i}个电影信息解析失败")
            return results

    def parse_all_pages(self, page_nums: int = 10) -> Optional[List[Dict]]:
        """
        爬取所有页面的电影信息

        Args:
            page_nums(int):需要爬取页面的数

        Returns:
            返回所有页面的电影信息列表
        """
        results = []  # 所有电影的信息

        # 构造页面的url
        for i in range(page_nums):
            other_url = "?start=" + str(i * 25) + "&filter="
            true_url = self.url + other_url
            page_content = self.fetch_page(true_url)
            page_movies = self.parse_single_page(page_content, i + 1)
            if page_movies:
                results.extend(page_movies)
            else:
                self.logger.warning(f"第{i+1}页的电影信息解析失败")
        return results
