import psycopg
import logging
from typing import Optional

from psycopg.rows import dict_row


class PostgresDB:
    def __init__(self, dsn):

        self.logger = logging.getLogger(__name__)

        try:
            self.connect = psycopg.connect(dsn,  row_factory=dict_row)
        except Exception as e:
            self.logger.error(f"Ошибка при подключении к базе данных: {str(e)}")

    def close(self) -> None:

        """Закрывает соединение с базой данных"""

        self.connect.close()
        self.logger.info("Соединение с базой данных закрыто")

    def execute_query(
            self, query: str,
            params: Optional[tuple] = None,
            commit: bool = False
    ) -> Optional[list]:
        """Выполняет SQL-запрос к базе данных"""

        connect = self.connect

        try:
            result = connect.execute(query, params).fetchall()
            if commit:
                connect.commit()
            return result
        except Exception as e:
            self.logger.error(f"Ошибка при выполнении запроса: {str(e)}")
            connect.rollback()
            return None

    def is_closed(self):
        if self.connect:
            return self.connect.closed
