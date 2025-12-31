"""
词云生成模块，用于对文本数据进行分词并生成词云图片

下面是对WordCloudGenerator类中各个方法的介绍：
    __init__(): 初始化生成器，设置日志记录器和默认字体
    _load_stopwords(): 私有方法，加载停用词（可扩展）
    _processing_text(): 私有方法，对文本列表进行分词和清洗
    generate_wordcloud(): 核心方法，生成并保存词云图片
"""

import logging
import jieba
import numpy as np
import pandas as pd
from PIL import Image
from sympy import false
from wordcloud import WordCloud
from typing import List, Optional, Union
import os
from matplotlib import pyplot as plt
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMAGE_SAVE_DIR, MASK


class WordCloudGenerator:
    """
    词云生成工具类
    """

    def __init__(
        self,
        data: pd.DataFrame,
        logger: logging.Logger = None,
        save_dir: str = IMAGE_SAVE_DIR,
        font_path: str = "msyh.ttc",  # 默认字体路径
    ):
        """
        初始化词云生成器

        Args:
            logger: 日志记录器
            save_dir: 图片保存目录
            font_path: 字体路径，防止中文乱码
        """
        self.logger = logger
        self.save_dir = save_dir
        self.font_path = font_path
        self.data = data

    def _processing_text(self, text_series: pd.Series) -> str:
        """
        对Pandas Series中的文本进行清洗和分词
        """
        # 1. 拼接所有文本
        text = " ".join(text_series.dropna().astype(str).tolist())

        # 2. jieba分词
        cut = jieba.cut(text)
        string = " ".join(cut)
        return string

    def generate_wordcloud(
        self,
        mask_path: Optional[str] = MASK,
        columns: List[str] = ["comment"],
    ) -> bool:
        """
        生成词云图

        Args:
            data: 数据源 (DataFrame)
            column_name: 需要分析的列名 (如 'comment', 'classification')
            file_name: 保存的文件名
            mask_path: 遮罩图片路径 (可选)
        """
        if not mask_path:
            self.logger.warning("未提供遮罩图片，无法生成词云")
            return False

        img = mask_path
        img_array = np.array(Image.open(img))

        success = False
        for column in columns:
            if self.data[column].empty:
                self.logger.warning(f"列 {column} 中没有数据，跳过该列的词云生成")
                continue
            file_name = f"wordcloud_{column}.png"
            string = self._processing_text(self.data[column])
            wc = WordCloud(
                background_color="white",
                mask=img_array,
                font_path=self.font_path,
            )
            wc.generate_from_text(string)

            # 绘制图片
            success = True
            plt.imshow(wc)
            plt.axis("off")
            plt.savefig(os.path.join(self.save_dir, file_name))
            plt.close()
        if success:
            self.logger.info(
                f"词云图片已保存至 {os.path.join(self.save_dir, file_name)}"
            )

        else:
            print("生成过程出现错误！未生成任何词云图片")
            self.logger.error("未生成任何词云图片")
        return success
