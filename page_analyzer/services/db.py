import logging
from typing import List, Tuple, Any, Union, Dict

import psycopg
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

    def cursor(self):
        """Запрос к бд"""

        return self.connection.cursor()

    def _execute(self, query, params):
        return self.cursor().execute(query, params)

    def execute_query(
            self,
            query: str,
            params: Tuple[Any, ...] = None,
            many=False,
            commit=False
    ) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:

        result = self._execute(query, params)

        if result.description:
            if many:
                result = result.fetchall()
            else:
                result = result.fetchone()

        if commit:
            self.connection.commit()

        return result

    def is_closed(self):
        if self.connection:
            return self.connection.closed
