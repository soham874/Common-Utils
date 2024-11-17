import mysql.connector
from softeam_common_config.config_reader import ConfigReader

from softeam_common_config.log_config import get_logger

log = get_logger(__name__)

__configReader = ConfigReader()

connection = mysql.connector.connect(
    host="softeam-sql-db",
    port=3306,
    user=__configReader.get_config_from_env_or_file('MYSQL_USER'),
    password=__configReader.get_config_from_env_or_file('MYSQL_PASSWORD'),
    database=__configReader.get_config_from_env_or_file('MYSQL_DATABASE')
)

cursor = connection.cursor()
log.info("DB Conection acquired successfully")

def close_connections():
    connection.close()
    cursor.close()
    log.info("DB Conection closed successfully")