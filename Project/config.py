import os
import logging


# 豆瓣网址
BASE_URL = "https://movie.douban.com/top250"
# 日志文件路径
LOG_PATH = "logs/spider.log"  # 日志文件路径

# 数据保存文件路径
BASE_DATA_DIR = "data"
CSV_PATH = os.path.join(BASE_DATA_DIR, "douban_top250_movies.csv")  # 用于保存CSV文件
JSON_PATH = os.path.join(BASE_DATA_DIR, "douban_top250_movies.json")  # 用于保存JSON文件
EXCEL_PATH = os.path.join(
    BASE_DATA_DIR, "douban_top250_movies.xlsx"
)  # 用于保存Excel文件
STOPWORDS_PATH = os.path.join(BASE_DATA_DIR, "stopwords.txt")  # 停用词文件路径

# 图片保存目录
BASE_STATIC_DIR = "static/visualization"
IMAGE_SAVE_DIR = os.path.join(BASE_STATIC_DIR, "images")

# 词云遮罩路径
BASE_MASK_DIR = os.path.join(BASE_STATIC_DIR, "masks")
MASK = os.path.join(BASE_MASK_DIR, "example.png")
GENERATE_WORDCLOUD_DIR = []

# 检查有无遮罩图片
if not MASK:
    logging.warning("警告信息：无遮罩图片")

# 爬取电影信息
MOVIE_INFO = {
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

# 确保目录存在
os.makedirs("logs", exist_ok=True)
os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)
os.makedirs(BASE_DATA_DIR, exist_ok=True)
