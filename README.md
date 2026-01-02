# 豆瓣电影 Top 250 爬虫

> 📚 本项目为 Python 课程大作业
基于 Flask + Pandas + Matplotlib 的全栈数据分析项目，集成了爬虫、数据清洗、可视化分析及 Web 展示功能。

---

## 📋 项目简介

这是一个完整的 Python 数据分析实战项目。它首先通过爬虫获取豆瓣电影 Top 250 的完整榜单数据，进行清洗和格式化存储（CSV/Excel/JSON）；随后使用 Matplotlib 和 WordCloud 生成专业的分析图表和词云；最后通过 Flask 搭建 Web 界面，直观展示分析结果。

---

## ✨ 功能特性

- 🎬 爬取豆瓣电影 Top 250 完整榜单(提取电影详细信息——标题、评分、导演、主演)
- 🧹 数据清洗, 规范数据的格式
- 💾 支持多种数据导出格式（CSV、JSON、Excel）
- 📊 数据可视化, 使用 matplotlib 生成分析图表
- ☁️ 词云分析：集成 `jieba` 分词，针对电影“标题”和“短评”生成高频词云图。
- 🌐 Web 应用界面，使用 Flask 提供交互式数据浏览和可视化
- 🛡️ 友好的请求频率控制，避免对服务器造成压力
- 📝 完整的日志记录
- 🔄 断点续爬功能

---

## 🚀 快速开始

### 1. 环境准备

- Python 3.8+

```bash
# 克隆项目
git clone https://github.com/gushi4421/douban-top250-spider.git
cd douban-top250-spider
# 安装依赖包
pip install -r requirements.txt
```


### 2. 运行爬虫与分析

运行主程序，它将依次执行：爬取 -> 清洗 -> 保存 -> 绘图 -> 生成词云。

``` bash
# 进入 Project 目录
cd Project

# 基础使用
python main.py
```

#### 3. 启动 Web 应用

数据爬取完成后，可以启动 Flask Web 应用查看可视化结果：

```bash
# 确保在 Project 目录下
cd Project

# 启动 Flask 应用
python app.py
```

然后在浏览器中访问 `http://127.0.0.1:5000` 查看可视化结果。

#### 常用命令参数
你可以通过命令行参数自定义保存路径或控制功能开关
``` bash
# 查看所有可用参数
python main.py --help

# 示例：仅爬取数据保存为Excel，不进行可视化
python main.py --if_data_visualization False --if_save_to_csv False --if_save_to_json False

# 示例：自定义保存路径并显示图表窗口
python main.py --csv_save_path "./my_data/movies.csv" --show_charts True
```
| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| **爬虫控制** | | | |
| `--if_print` | bool | `True` | 是否在终端实时打印爬取到的电影详细信息 |
| `--if_reset_log` | bool | `False` | 程序启动时是否清空旧的日志文件 |
| **数据保存** | | | |
| `--if_save_to_csv` | bool | `True` | 是否将爬取结果保存为 CSV 文件 |
| `--csv_save_path` | str | `data/douban_top250_movies.csv` | CSV 文件的保存路径 |
| `--if_save_to_excel` | bool | `True` | 是否将爬取结果保存为 Excel 文件 |
| `--excel_save_path` | str | `data/douban_top250_movies.xlsx` | Excel 文件的保存路径 |
| `--if_save_to_json` | bool | `True` | 是否将爬取结果保存为 JSON 文件 |
| `--json_save_path` | str | `data/douban_top250_movies.json` | JSON 文件的保存路径 |
| **数据可视化** | | | |
| `--if_data_visualization`| bool | `True` | 是否执行 Matplotlib 常规图表分析 |
| `--image_save_dir` | str | `static/images`| 可视化图表和词云图片的保存目录 |
| `--show_charts` | bool | `False` | 生成图表时是否弹出窗口显示（Web部署建议关闭） |
| **词云生成** | | | |
| `--if_generate_wordcloud`| bool | `True` | 是否基于文本生成词云图 |
| `--wordcloud_mask` | str | `static/masks/tree.jpg` | 词云生成所需的遮罩图片路径 |
| `--wordcloud_columns` | list | `['title', 'comment']` | 指定对哪些列（标题/短评）生成词云 |

---

## 📁 项目结构

```
douban-top250-spider/
├── Project/
│   ├── app.py                  # Flask Web 应用入口
│   ├── main.py                 # 爬虫与分析程序主入口
│   ├── config.py               # 项目配置文件 (路径、URL、参数)
│   ├── spiders/
│   │   └── spider.py           # 爬虫核心逻辑 (MovieSpider)
│   ├── utils/
│   │   ├── data_clean.py       # 数据清洗 (DataCleaner)
│   │   ├── data_save.py        # 数据持久化 (DataSaver)
│   │   ├── data_visualization.py # Matplotlib 绘图 (DataVisualizer)
│   │   ├── wordcloud_generator.py # 词云生成 (WordCloudGenerator)
│   │   └── log.py              # 日志配置
│   └── templates/              # Flask HTML 模板
│       ├── index.html
│       ├── movie.html
│       ├── ...
├── static/
│   ├── assets/                 # 网页静态资源 (CSS/JS/Vendor)
│   ├── images/                 # [生成] 可视化图表与词云
│   └── masks/                  # 词云遮罩底图
├── data/                       # [生成] 爬取的数据文件 (csv/xlsx/json)
├── logs/                       # [生成] 运行日志
└── requirements.txt            # 项目依赖
```

---

## 📝 示例输出

**JSON 格式：**
```json
{
  "rank": 1,
  "title": "肖申克的救赎",
  "title_en": "The Shawshank Redemption",
  "rating": 9.7,
  "rating_count": 2800000,
  "director": "弗兰克·德拉邦特",
  "actors": "蒂姆·罗宾斯 / 摩根·弗里曼",
  "year": 1994,
  "genre": "剧情 / 犯罪"
}
```

---

## 🌐 Web 应用功能

项目集成了 Flask Web 应用，提供友好的可视化界面：

### 页面功能
- **首页 (`/index`)**: 欢迎页面，提供导航入口
- **电影列表 (`/movie`)**: 表格展示所有 250 部电影的详细信息
- **数据分析 (`/score`)**: 展示数据可视化图
- **词云图 (`/word`)**: 展示评论和标题的词云可视化
- **关于 (`/aboutMe`)**: 作者信息

---

## 📈 生成的分析图表

运行结束后，`static/visualization/images/` 目录下将自动生成以下高清图表：

1.  **`rating_distribution.png`**: 电影评分的正态分布情况。
2.  **`year_distribution.png`**: 上映年份的柱状统计，分析电影黄金年代。
3.  **`country_distribution.png`**: 制片国家/地区的饼图与柱状图（支持多国家拆分统计）。
4.  **`genre_distribution.png`**: 电影类型的词频统计。
5.  **`top_directors.png`**: 上榜作品最多的导演排名。
6.  **`wordcloud_comment.png`**: 电影一句话短评的词云。
7.  **`wordcloud_title.png`**: 电影标题的词云。

---

## ⚠️ 注意事项

1. **学习目的**：本项目为课程学习作业，仅供学习交流使用
2. **遵守 robots.txt**：请遵守豆瓣网站的 robots.txt 规则
3. **合理使用**：请设置合理的请求间隔，避免对服务器造成过大压力
4. **数据使用**：爬取的数据仅供个人学习研究使用，请勿用于商业目的
5. **法律责任**：使用本项目产生的任何法律问题由使用者自行承担



## 👤 作者

**gushi4421**

- GitHub: [@gushi4421](https://github.com/gushi4421)
- 身份：在读本科生（2024届的大二小登）

## 🙏 致谢

- 感谢 Python 课程老师的悉心指导
- 感谢豆瓣提供的优质电影数据
- 感谢所有开源贡献者的无私分享
- 特别鸣谢[long1546](https://github.com/long1546)提供一些支持

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [Issue](https://github.com/gushi4421/douban-movie-top250/issues)
- 发送邮件至：gushi4421@qq.com

---

⭐ 如果这个项目对你有帮助，欢迎 Star 支持！

**声明**：本项目仅用于学习交流，不得用于任何商业用途。