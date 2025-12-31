"""
数据可视化模块，用于对爬取数据的可视化分析

下面是对类中各个模块的介绍：
    __init__(): 类的构造函数，用于类的初始化
    _ensure_dir(): 私有方法，确保文件路径存在，如不存在则创建
    _save_figure(): 私有方法，保存图片到指定目录
    load_data(): 加载数据
    plot_rating_distribution(): 绘制评分分布直方图
    plot_year_distribution(): 绘制电影年份分布图
    plot_country_distribution(): 绘制电影国家分布图
    plot_genre_distribution(): 绘制电影类型分布图
    plot_top_directors(): 绘制导演排名分布图
    plot_star_rating_distribution(): 绘制星级评分分布图
    generate_all_charts(): 封装绘制图像方法的方法
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging
import os

# 设置中文字体支持
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "STHeiti"]  # 中文字体
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题


class DataVisualizer:
    """
    数据可视化类，用于分析和展示电影数据
    """

    def __init__(self, logger: logging.Logger = None, save_dir: str = "images"):
        """
        初始化可视化器

        Args:
            logger:  日志记录器
            save_dir: 图片保存目录
        """
        self.logger = logger if logger else logging.getLogger(__name__)
        self.save_dir = save_dir
        self._ensure_dir()

    def _ensure_dir(self):
        """确保保存目录存在"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            self.logger.info(f"创建图片保存目录: {self.save_dir}")

    def _save_figure(self, fig, filename: str):
        """保存图片"""
        filepath = os.path.join(self.save_dir, filename)
        fig.savefig(filepath, dpi=300, bbox_inches="tight", facecolor="white")
        self.logger.info(f"图片已保存: {filepath}")
        plt.close(fig)

    def load_data(self, data_source) -> pd.DataFrame:
        """
        加载数据

        Args:
            data_source: 可以是 List[Dict] 或 CSV文件路径

        Returns:
            DataFrame
        """
        if isinstance(data_source, list):
            return pd.DataFrame(data_source)
        elif isinstance(data_source, str) and data_source.endswith(".csv"):
            return pd.read_csv(data_source)
        elif isinstance(data_source, pd.DataFrame):
            return data_source
        else:
            raise ValueError("数据源必须是 List[Dict]、CSV路径 或 DataFrame")

    def plot_rating_distribution(self, df: pd.DataFrame, show: bool = True) -> None:
        """
        绘制评分分布直方图

        Args:
            df: 电影数据DataFrame
            show: 是否显示图片
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # 转换评分为数值类型
        ratings = pd.to_numeric(df["nums-rating"], errors="coerce").dropna()

        # 绘制直方图
        counts, bins, patches = ax.hist(
            ratings, bins=20, edgecolor="black", alpha=0.7, color="steelblue"
        )

        # 添加均值线
        mean_rating = ratings.mean()
        ax.axvline(
            mean_rating,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"平均分:  {mean_rating:.2f}",
        )

        ax.set_xlabel("评分", fontsize=12)
        ax.set_ylabel("电影数量", fontsize=12)
        ax.set_title("豆瓣Top250电影评分分布", fontsize=14, fontweight="bold")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        self._save_figure(fig, "rating_distribution.png")
        if show:
            plt.show()

    def plot_year_distribution(self, df: pd.DataFrame, show: bool = True) -> None:
        """
        绘制电影年份分布图

        Args:
            df:  电影数据DataFrame
            show:  是否显示图片
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        # 提取年份并转换为数值
        years = df["year"].astype(str).str.extract(r"(\d{4})")[0]
        years = pd.to_numeric(years, errors="coerce").dropna().astype(int)

        # 统计每个年份的电影数量
        year_counts = years.value_counts().sort_index()

        # 绘制柱状图
        ax.bar(
            year_counts.index.astype(str),
            year_counts.values,
            color="coral",
            edgecolor="black",
            alpha=0.8,
        )

        ax.set_xlabel("年份", fontsize=12)
        ax.set_ylabel("电影数量", fontsize=12)
        ax.set_title("豆瓣Top250电影年份分布", fontsize=14, fontweight="bold")

        # 旋转x轴标签
        plt.xticks(rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)

        # 只显示部分年份标签，避免拥挤
        tick_positions = range(0, len(year_counts), max(1, len(year_counts) // 15))
        ax.set_xticks([list(year_counts.index.astype(str))[i] for i in tick_positions])

        plt.tight_layout()
        self._save_figure(fig, "year_distribution.png")
        if show:
            plt.show()

    def plot_country_distribution(
        self, df: pd.DataFrame, top_n: int = 10, show: bool = True
    ) -> None:
        """
        绘制制片国家/地区分布饼图（支持一个电影多个国家）
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # -------- 关键修改：先拆分，再统计 --------
        all_countries = []
        for country_str in df["country"].dropna():
            # 豆瓣常见格式: "美国 英国" / "中国大陆 中国香港"
            # 先把全角空格替换成半角，防止有奇怪空格
            s = str(country_str).replace("\u3000", " ").strip()
            # 按空格拆分，过滤掉空字符串
            parts = [p for p in s.split(" ") if p]
            all_countries.extend(parts)

        country_counts = pd.Series(all_countries).value_counts().head(top_n)
        # ----------------------------------------

        # 饼图
        colors = plt.cm.Set3(np.linspace(0, 1, len(country_counts)))
        wedges, texts, autotexts = ax1.pie(
            country_counts.values,
            labels=country_counts.index,
            autopct="%1.1f%%",
            colors=colors,
            explode=[0.05] * len(country_counts),
            shadow=True,
        )
        ax1.set_title(
            f"Top{top_n} 制片国家/地区分布 (饼图)", fontsize=12, fontweight="bold"
        )

        # 横向柱状图
        ax2.barh(
            country_counts.index[::-1],
            country_counts.values[::-1],
            color="teal",
            edgecolor="black",
            alpha=0.8,
        )
        ax2.set_xlabel("电影数量", fontsize=12)
        ax2.set_ylabel("国家/地区", fontsize=12)
        ax2.set_title(
            f"Top{top_n} 制片国家/地区分布 (柱状图)", fontsize=12, fontweight="bold"
        )

        # 在柱状图上显示数值
        for i, v in enumerate(country_counts.values[::-1]):
            ax2.text(v + 0.5, i, str(v), va="center", fontsize=10)

        plt.tight_layout()
        self._save_figure(fig, "country_distribution.png")
        if show:
            plt.show()

    def plot_genre_distribution(
        self, df: pd.DataFrame, top_n: int = 10, show: bool = True
    ) -> None:
        """
        绘制电影类型分布图

        Args:
            df: 电影数据DataFrame
            top_n:  显示前N个类型
            show: 是否显示图片
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        # 统计类型分布（一部电影可能有多个类型）
        all_genres = []
        for genres in df["classification"].dropna():
            # 按空格分割类型
            genre_list = str(genres).split()
            all_genres.extend(genre_list)

        genre_counts = pd.Series(all_genres).value_counts().head(top_n)

        # 绘制柱状图
        bars = ax.bar(
            genre_counts.index,
            genre_counts.values,
            color="mediumpurple",
            edgecolor="black",
            alpha=0.8,
        )

        # 在柱子上显示数值
        for bar, count in zip(bars, genre_counts.values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                str(count),
                ha="center",
                va="bottom",
                fontsize=10,
            )

        ax.set_xlabel("电影类型", fontsize=12)
        ax.set_ylabel("出现次数", fontsize=12)
        ax.set_title(
            f"豆瓣Top250电影类型分布 (Top{top_n})", fontsize=14, fontweight="bold"
        )
        plt.xticks(rotation=45, ha="right")
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        self._save_figure(fig, "genre_distribution.png")
        if show:
            plt.show()

    def plot_rating_vs_comments(self, df: pd.DataFrame, show: bool = True) -> None:
        """
        绘制评分与评论数的散点图

        Args:
            df: 电影数据DataFrame
            show: 是否显示图片
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # 转换数据类型
        ratings = pd.to_numeric(df["nums-rating"], errors="coerce")
        comments = pd.to_numeric(df["comment_nums"], errors="coerce")

        # 创建有效数据的mask
        valid_mask = ratings.notna() & comments.notna()
        ratings = ratings[valid_mask]
        comments = comments[valid_mask]
        titles = df.loc[valid_mask, "title"]

        # 绘制散点图
        scatter = ax.scatter(
            ratings,
            comments,
            c=ratings,
            cmap="RdYlGn",
            s=100,
            alpha=0.6,
            edgecolors="black",
            linewidth=0.5,
        )

        # 添加颜色条
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label("评分", fontsize=12)

        # 标注评论数最多的几部电影
        top_commented = comments.nlargest(5)
        for idx in top_commented.index:
            ax.annotate(
                titles[idx][:8] + "...",
                (ratings[idx], comments[idx]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
                alpha=0.8,
            )

        ax.set_xlabel("评分", fontsize=12)
        ax.set_ylabel("评论数", fontsize=12)
        ax.set_title("评分与评论数关系散点图", fontsize=14, fontweight="bold")
        ax.grid(alpha=0.3)

        # 格式化y轴（评论数可能很大）
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(
                lambda x, p: f"{x/10000:.1f}万" if x >= 10000 else f"{x:.0f}"
            )
        )

        self._save_figure(fig, "rating_vs_comments.png")
        if show:
            plt.show()

    def plot_top_directors(
        self, df: pd.DataFrame, top_n: int = 10, show: bool = True
    ) -> None:
        """
        绘制Top导演排行榜

        Args:
            df: 电影数据DataFrame
            top_n: 显示前N个导演
            show: 是否显示图片
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # 统计导演作品数量
        director_counts = df["director"].value_counts().head(top_n)

        # 绘制横向柱状图
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(director_counts)))
        bars = ax.barh(
            director_counts.index[::-1],
            director_counts.values[::-1],
            color=colors[::-1],
            edgecolor="black",
            alpha=0.8,
        )

        # 在柱子上显示数值
        for bar, count in zip(bars, director_counts.values[::-1]):
            ax.text(
                bar.get_width() + 0.1,
                bar.get_y() + bar.get_height() / 2,
                str(count),
                va="center",
                fontsize=11,
                fontweight="bold",
            )

        ax.set_xlabel("作品数量", fontsize=12)
        ax.set_ylabel("导演", fontsize=12)
        ax.set_title(
            f"豆瓣Top250电影导演排行榜 (Top{top_n})", fontsize=14, fontweight="bold"
        )
        ax.grid(axis="x", alpha=0.3)

        plt.tight_layout()
        self._save_figure(fig, "top_directors.png")
        if show:
            plt.show()

    def plot_star_rating_distribution(
        self, df: pd.DataFrame, show: bool = True
    ) -> None:
        """
        绘制星级评分分布

        Args:
            df: 电影数据DataFrame
            show: 是否显示图片
        """
        fig, ax = plt.subplots(figsize=(8, 6))

        # 统计星级分布
        star_counts = df["star-rating"].value_counts().sort_index()

        # 绘制柱状图
        colors = [
            "gold" if "5" in str(star) else "orange" for star in star_counts.index
        ]
        bars = ax.bar(
            star_counts.index.astype(str),
            star_counts.values,
            color=colors,
            edgecolor="black",
            alpha=0.8,
        )

        # 在柱子上显示数值
        for bar, count in zip(bars, star_counts.values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1,
                str(count),
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold",
            )

        ax.set_xlabel("星级", fontsize=12)
        ax.set_ylabel("电影数量", fontsize=12)
        ax.set_title("豆瓣Top250电影星级分布", fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        self._save_figure(fig, "star_rating_distribution.png")
        if show:
            plt.show()

    def generate_all_charts(self, data_source, show: bool = False) -> None:
        """
        生成所有图表

        Args:
            data_source: 数据源（List[Dict]、CSV路径或DataFrame）
            show: 是否显示图片
        """
        self.logger.info("开始生成所有可视化图表...")

        df = self.load_data(data_source)

        # 生成各类图表
        self.plot_rating_distribution(df, show)
        self.plot_year_distribution(df, show)
        self.plot_country_distribution(df, show=show)
        self.plot_genre_distribution(df, show=show)
        self.plot_top_directors(df, show=show)
        self.plot_star_rating_distribution(df, show=show)

        self.logger.info(f"所有图表已生成完成，保存在 {self.save_dir} 目录下")
