"""
数据保存模块，用于将电影数据保存为CSV、Excel和JSON格式

下面是对DataSaver类中各个方法的介绍：
    __init__(): 初始化数据保存器，设置日志记录器
    _ensure_dir(): 私有方法，确保保存路径的目录存在，如不存在则创建
    _convert_to_df(): 私有方法，将数据统一转换为DataFrame格式
    save_to_csv(): 将数据保存为CSV格式文件
    save_to_excel(): 将数据保存为Excel格式文件
    save_to_json(): 将数据保存为JSON格式文件
"""

import os
import pandas as pd
from typing import List, Dict, Optional, Union
import logging


class DataSaver:
    """
    数据保存工具类
    """

    def __init__(self, logger: logging.Logger = None):
        """
        初始化数据保存器

        Args:
            logger:  日志记录器（可选）
        """
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def _ensure_dir(self, save_path):
        """确保保存路径的目录存在"""
        # 添加类型检查
        if not isinstance(save_path, str):
            raise TypeError(
                f"save_path 必须是字符串，但收到了 {type(save_path)}:  {save_path}"
            )

        directory = os.path.dirname(save_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            if self.logger:
                self.logger.info(f"创建目录:  {directory}")

    def _convert_to_df(self, data: Union[List[Dict], pd.DataFrame]) -> pd.DataFrame:
        """辅助方法：统一转换为DataFrame"""
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, pd.DataFrame):
            return data
        else:
            raise ValueError("数据必须是 List[Dict] 或 pd.DataFrame")

    def save_to_csv(
        self, movies: Union[List[Dict], pd.DataFrame], save_path: str
    ) -> bool:
        """
        将电影数据保存到csv文件
        """
        try:
            if isinstance(movies, list) and not movies:
                self.logger.warning("没有任何电影数据可保存")
                return False

            self._ensure_dir(save_path)

            df = self._convert_to_df(movies)
            df.to_csv(save_path, index=False, encoding="utf-8-sig")
            self.logger.info(f"电影数据已保存至 {save_path}，共 {len(df)} 条记录")
            return True
        except Exception as e:
            self.logger.error(f"保存CSV失败: {e}")
            return False

    def save_to_excel(
        self, movies: Union[List[Dict], pd.DataFrame], save_path: str
    ) -> bool:
        """
        将电影数据保存到Excel文件
        """
        try:
            if isinstance(movies, list) and not movies:
                self.logger.warning("没有任何电影数据可保存")
                return False

            self._ensure_dir(save_path)

            df = self._convert_to_df(movies)
            df.to_excel(save_path, index=False, engine="openpyxl")
            self.logger.info(f"电影数据已保存至 {save_path}，共 {len(df)} 条记录")
            return True
        except Exception as e:
            self.logger.error(f"保存Excel失败: {e}")
            return False

    def save_to_json(
        self, movies: Union[List[Dict], pd.DataFrame], save_path: str
    ) -> bool:
        """
        将电影数据保存到JSON文件
        """
        try:
            if isinstance(movies, list) and not movies:
                self.logger.warning("没有任何电影数据可保存")
                return False

            self._ensure_dir(save_path)

            df = self._convert_to_df(movies)
            # 使用pandas的to_json方法
            df.to_json(save_path, orient="records", force_ascii=False, indent=2)

            self.logger.info(f"电影数据已保存至 {save_path}，共 {len(df)} 条记录")
            return True
        except Exception as e:
            self.logger.error(f"保存JSON失败: {e}")
            return False
