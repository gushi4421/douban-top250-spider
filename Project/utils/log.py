import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOG_PATH


def setup_logging():
    """创建日志记录器"""
    logging.basicConfig(
        level=logging.INFO,  # 日志级别
        format="%(asctime)s - %(name)s -  %(levelname)s - %(message)s",  # 日志格式
        handlers=[
            logging.FileHandler("logs/spider.log", encoding="utf-8"),  # 日志文件
            logging.StreamHandler(),  # 控制台输出
        ],
    )
    logger = logging.getLogger(__name__)  # 获取日志记录器
    return logger


def clear_log_file():
    """清除日志文件"""
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "w", encoding="utf-8") as f:
                pass  # 清空文件内容
            print(f"已清空日志文件: {LOG_PATH}")
            return True
        except Exception as e:
            print(f"清空日志文件失败: {e}")
            return False
    else:
        print(f"日志文件不存在，无法清空: {LOG_PATH}")
        return False


if __name__ == "__main__":
    clear_log_file()
