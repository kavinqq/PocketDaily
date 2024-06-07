import logging

# 設置日誌配置
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# 創建一個專用的 logger
logger = logging.getLogger('my_app_logger')
