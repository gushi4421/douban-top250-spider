# 豆瓣电影 Top 250 爬虫

> 📚 本项目为大二期末 Python 课程大作业
一个用于爬取豆瓣电影 Top 250 榜单的 Python 爬虫项目。

---

## 📋 项目简介

本项目是我在大学二年级 Python 程序设计课程的期末大作业，是一个简单易用的 Python 爬虫工具，用于获取豆瓣电影 Top 250 榜单的电影信息，包括电影名称、评分、导演、主演、年份、类型等详细数据。

**课程信息：**
- 📖 课程名称：Python 程序设计
- 🎓 学期：大二上学期/下学期
- 🎯 作业类型：期末大作业

---

## ✨ 功能特性

- 🎬 爬取豆瓣电影 Top 250 完整榜单(提取电影详细信息——标题、评分、导演、主演)
- 🧹 数据清洗, 规范数据的格式
- 💾 支持多种数据导出格式（CSV、JSON、Excel）
- 📊 数据可视化, 使用 matplotlib 生成分析图表
- 🛡️ 友好的请求频率控制，避免对服务器造成压力
- 📝 完整的日志记录
- 🔄 断点续爬功能

---

## 🚀 快速开始

### 环境要求

- Python 3.7+
- pip 包管理器

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/gushi4421/douban-top250-spider.git
cd douban-top250-spider

# 安装依赖包
pip install -r requirements.txt
```


### 使用方法

``` bash
# 基础使用
python main.py
```
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
| 参数 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `--if_save_to_csv` | 是否保存为 CSV | `True` |
| `--csv_save_path` | CSV 保存路径 | `data/douban_top250_movies.csv` |
| `--if_save_to_excel` | 是否保存为 Excel | `True` |
| `--excel_save_path` | Excel 保存路径 | `data/douban_top250_movies.xlsx` |
| `--if_save_to_json` | 是否保存为 JSON | `True` |
| `--json_save_path` | JSON 保存路径 | `data/douban_top250_movies.json` |
| `--if_data_visualization` | 是否进行可视化分析 | `True` |
| `--image_save_dir` | 图片保存目录 | `images` |
| `--show_charts` | 是否弹窗显示图表 | `False` |

---

## 📁 项目结构

```
Project/
├── data/                   # 存放爬取到的数据文件 (运行后生成)
├── images/                 # 存放生成的可视化图表 (运行后生成)
├── logs/                   # 存放运行日志 (spider.log)
├── spiders/
│   └── spider.py           # 爬虫核心逻辑 (MovieSpider 类)
├── utils/
│   ├── data_clean.py       # 数据清洗模块 (DataCleaner 类)
│   ├── data_save.py        # 数据保存模块 (DataSaver 类)
│   └── data_visualization.py # 数据可视化模块 (DataVisualizer 类)
├── main.py                 # 程序主入口
└── requirements.txt        # 依赖列表
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

## 📈 可视化展示

运行结束后，`images/` 目录下将生成以下图表：

*   `rating_distribution.png`: 评分分布
*   `country_distribution.png`: 制片国家分布（Top10）
*   `genre_distribution.png`: 电影类型分布
*   `year_distribution.png`: 年份分布
*   `top_directors.png`: 导演作品数量排名
*   ...更多
  
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
- 特别鸣谢long1546(https://github.com/long1546)提供一些支持

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [Issue](https://github.com/gushi4421/douban-movie-top250/issues)
- 发送邮件至：gushi4421@qq.com

---

⭐ 如果这个项目对你有帮助，欢迎 Star 支持！

**声明**：本项目仅用于学习交流，不得用于任何商业用途。