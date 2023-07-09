import psycopg
import logging
from typing import Optional, List, Tuple, Any, Union, Dict

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
                      params: Tuple[Any, ...] = None,
                      commit: bool = False,
                      many: bool = False) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
        """Запрос к бд"""

        result = None

        with self.connection.cursor() as cursor:

            try:
                cursor.execute(query, params)

                if cursor.description:
                    if many:
                        result = cursor.fetchall()
                    else:
                        result = cursor.fetchone()

                if commit:
                    self.connection.commit()

            except Exception as e:
                self.logger.error(f"Ошибка при выполнении запроса: {str(e)}")

            return result

    def is_closed(self):
        if self.connection:
            return self.connection.closed
