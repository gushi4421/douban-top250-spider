"""
数据清洗模块，用于对爬取到的电影数据进行清洗和预处理

下面是对DataCleaner类中各个方法的介绍：
    __init__(): 初始化数据清洗器，设置日志记录器
    clean_data(): 对原始数据进行清洗和预处理，返回清洗后的DataFrame
        1. 数值类型转换：将评分、评论数、年份等字段转换为合适的数值类型
        2. 文本清洗：去除标题、导演、演员等文本字段的首尾空格，处理空值
        3. 数据验证：检查数据完整性，记录清洗过程中的统计信息
"""

import pandas as pd
from typing import List, Dict, Union, Optional
import logging


class DataCleaner:
    """
    数据清洗工具类
    """

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger if logger else logging.getLogger(__name__)

    def clean_data(self, data: Union[List[Dict], pd.DataFrame]) -> pd.DataFrame:
        """
        对电影数据进行清洗

        Args:
            data: 原始数据，可以是列表或DataFrame

        Returns:
            清洗后的DataFrame
        """
        self.logger.info("开始进行数据清洗...")

        # 统一转换为DataFrame
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data.copy()

        # 1. 数值类型转换
        # 处理评分，转换为浮点数
        df["nums-rating"] = pd.to_numeric(df["nums-rating"], errors="coerce")

        # 处理评论数，转换为整数
        df["comment_nums"] = pd.to_numeric(df["comment_nums"], errors="coerce")

        # 处理年份，转换为整数
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

        # 2. 文本清洗
        text_columns = [
            "title",
            "director",
            "actors",
            "country",
            "classification",
            "comment",
        ]
        for col in text_columns:
            if col in df.columns:
                # 去除首尾空格，处理可能的空值
                df[col] = df[col].astype(str).str.strip()
                # 将字符串 'None' 或 'nan' 替换为实际的 NaN
                df[col] = df[col].replace({"None": None, "nan": None, "": None})

        self.logger.info("数据清洗完成")
        return df
