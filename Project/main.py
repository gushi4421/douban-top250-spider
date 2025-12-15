"""
主程序模块，用于协调整个豆瓣电影Top250爬虫项目的运行

下面是各个模块的功能介绍：
    main(args): 主函数，根据命令行参数执行爬取、清洗、保存和可视化流程
    命令行参数解析: 使用argparse解析命令行参数，控制程序行为
        1. if_save_to_csv: 是否保存为CSV文件
        2. csv_save_path: CSV文件保存路径
        3. if_save_to_excel: 是否保存为Excel文件
        4. excel_save_path: Excel文件保存路径
        5. if_save_to_json: 是否保存为JSON文件
        6. json_save_path: JSON文件保存路径
        7. if_data_visualization: 是否进行数据可视化
        8. image_save_dir: 可视化图片保存目录
        9. show_charts: 是否显示可视化图表
"""

import time
from spiders.spider import MovieSpider
import argparse
from utils.data_save import DataSaver
from utils.data_visualization import DataVisualizer
from utils.data_clean import DataCleaner  # 导入数据清洗模块

start_time = time.time()


def main(args):
    spider = MovieSpider()
    movies = spider.parse_all_pages()

    if not movies:
        print("未爬取到数据，程序结束。")
        return

    # 数据清洗
    data_cleaner = DataCleaner(logger=spider.logger)
    df_movies = data_cleaner.clean_data(movies)  # 获取清洗后的DataFrame

    # 数据保存 (使用清洗后的数据)
    data_saver = DataSaver(logger=spider.logger)

    if args.if_save_to_csv:
        data_saver.save_to_csv(save_path=args.csv_save_path, movies=df_movies)
    if args.if_save_to_excel:
        data_saver.save_to_excel(save_path=args.excel_save_path, movies=df_movies)
    if args.if_save_to_json:
        data_saver.save_to_json(save_path=args.json_save_path, movies=df_movies)

    # 数据可视化 (使用清洗后的数据)
    if args.if_data_visualization:
        visualizer = DataVisualizer(logger=spider.logger, save_dir=args.image_save_dir)
        visualizer.generate_all_charts(df_movies, show=args.show_charts)
        
    end_time = time.time()
    spider.logger.info(f"程序运行完毕，耗时 {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="豆瓣电影Top250爬虫")

    # csv保存相关参数
    parser.add_argument(
        "--if_save_to_csv", type=bool, default=True, help="是否保存到csv文件中"
    )
    parser.add_argument(
        "--csv_save_path",
        type=str,
        default="data/douban_top250_movies.csv",
        help="csv保存路径",
    )

    # excel保存相关参数
    parser.add_argument(
        "--if_save_to_excel", type=bool, default=True, help="是否保存到excel文件中"
    )
    parser.add_argument(
        "--excel_save_path",
        type=str,
        default="data/douban_top250_movies.xlsx",
        help="excel保存路径",
    )

    # json保存相关参数
    parser.add_argument(
        "--if_save_to_json", type=bool, default=True, help="是否保存到json文件中"
    )
    parser.add_argument(
        "--json_save_path",
        type=str,
        default="data/douban_top250_movies.json",
        help="json保存路径",
    )

    # 可视化相关参数
    parser.add_argument(
        "--if_data_visualization",
        type=bool,
        default=True,
        help="是否进行数据可视化分析",
    )
    parser.add_argument(
        "--image_save_dir", type=str, default="images", help="图片保存目录"
    )
    parser.add_argument(
        "--show_charts", type=bool, default=False, help="是否显示图表（交互模式）"
    )

    args = parser.parse_args()

    main(args)
    print("爬取完成！如果觉得这个项目对你有帮助的话，不妨点个Star支持一下吧！")
