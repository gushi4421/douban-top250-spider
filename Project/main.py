"""
主程序模块，用于协调整个豆瓣电影Top250爬虫项目的运行

"""

import time
import argparse
import os
from spiders.spider import MovieSpider
from utils.data_save import DataSaver
from utils.data_visualization import DataVisualizer
from utils.data_clean import DataCleaner
from utils.wordcloud_generator import WordCloudGenerator
from utils.log import delete_log_file, setup_logging
from config import LOG_PATH, CSV_PATH, EXCEL_PATH, JSON_PATH, IMAGE_SAVE_DIR, MASK
import config  # 自动启动config，创建文件夹
from typing import List

start_time = time.time()


def main(args):
    """主函数，协调各个模块的运行"""

    # 是否删除先前的日志文件
    if args.if_reset_log:
        delete_log_file()

    # 设置日志
    logger = setup_logging()

    # 创建爬虫实例
    spider = MovieSpider(logger=logger)

    # 1. 爬取数据
    movies = spider.parse_all_pages()

    if not movies:  # 检测是否爬取到数据
        logger.warning("未爬取到数据，程序结束。")
        return

    # 2. 数据清洗
    data_cleaner = DataCleaner(logger=logger)
    df_movies = data_cleaner.clean_data(movies)

    # 3. 数据保存
    data_saver = DataSaver(logger=logger)
    if args.if_save_to_csv:
        data_saver.save_to_csv(save_path=args.csv_save_path, movies=df_movies)
    if args.if_save_to_excel:
        data_saver.save_to_excel(save_path=args.excel_save_path, movies=df_movies)
    if args.if_save_to_json:
        data_saver.save_to_json(save_path=args.json_save_path, movies=df_movies)

    # 4. 数据可视化
    if args.if_data_visualization:
        visualizer = DataVisualizer(logger=spider.logger, save_dir=args.image_save_dir)
        visualizer.generate_all_charts(df_movies, show=args.show_charts)

    # 5. 词云生成
    if args.if_generate_wordcloud:
        spider.logger.info("开始生成词云模块")
        wc_generator = WordCloudGenerator(
            data=df_movies,
            logger=spider.logger,
            save_dir=args.image_save_dir,
            font_path="msyh.ttc",
        )

        wc_generator.generate_wordcloud(
            mask_path=args.wordcloud_mask, columns=args.wordcloud_columns
        )
        
    end_time = time.time()
    spider.logger.info(f"程序运行完毕，耗时 {end_time - start_time:.2f} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="豆瓣电影Top250爬虫 & 可视化")

    # 爬虫相关参数
    parser.add_argument(
        "--if_print",
        type=bool,
        default=False,
        help="是否在终端当中打印爬取到的电影信息",
    )

    # CSV保存相关参数
    parser.add_argument(
        "--if_save_to_csv", type=bool, default=True, help="是否保存到csv"
    )
    parser.add_argument("--csv_save_path", type=str, default=CSV_PATH)

    # Excel保存相关参数
    parser.add_argument(
        "--if_save_to_excel", type=bool, default=True, help="是否保存到excel"
    )
    parser.add_argument("--excel_save_path", type=str, default=EXCEL_PATH)

    # JSON保存相关参数
    parser.add_argument(
        "--if_save_to_json", type=bool, default=True, help="是否保存到json"
    )
    parser.add_argument("--json_save_path", type=str, default=JSON_PATH)

    # 数据可视化相关参数
    parser.add_argument(
        "--if_data_visualization", type=bool, default=True, help="是否进行常规图表分析"
    )
    parser.add_argument(
        "--image_save_dir", type=str, default=IMAGE_SAVE_DIR, help="图片保存目录"
    )
    parser.add_argument(
        "--show_charts", type=bool, default=False, help="是否弹出显示图表"
    )

    # 词云相关参数
    parser.add_argument(
        "--if_generate_wordcloud", type=bool, default=True, help="是否生成词云图"
    )
    parser.add_argument(
        "--wordcloud_mask",
        type=str,
        default=MASK,
        help="词云遮罩图片路径",
    )
    parser.add_argument(
        "--wordcloud_columns",
        type=List[str],
        default=["title", "comment"],
        help="请参考config.py当中的MOVIE_INFO设置参数，代码将根据这部分的参数生成对应的词云",
    )

    # 是否重置日志
    parser.add_argument(
        "--if_reset_log", type=bool, default=False, help="是否删除旧日志文件"
    )

    args = parser.parse_args()
    print("开始执行爬虫")
    main(args)
    print("所有任务执行完毕！")
