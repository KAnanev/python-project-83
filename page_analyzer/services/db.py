import psycopg
import logging
from typing import Optional, List, Tuple, Any

from psycopg.rows import dict_row


class PostgresDB:
    def __init__(self, dsn):

        self.logger = logging.getLogger(__name__)

        try:
            self.connection = psycopg.connect(dsn, row_factory=dict_row)
        except Exception as e:
            self.logger.error(f"Ошибка при подключении к базе данных: {str(e)}")

    def close(self) -> None:

        """Закрывает соединение с базой данных"""

        self.connection.close()
        self.logger.info("Соединение с базой данных закрыто")

    def execute_query(self,
                      query: str,
                      params: Optional[tuple] = None,
                      commit: bool = False) -> Optional[list[Any]]:
        """Запрос к бд"""

        result = None
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, params)

            if cursor.description:
                result = cursor.fetchall()

            if commit:
                self.connection.commit()

        except psycopg.Error as e:
            self.logger.error(f"Ошибка при выполнении запроса: {str(e)}")

        finally:
            if cursor:
                cursor.close()

        return result

    def is_closed(self):
        if self.connection:
            return self.connection.closed
