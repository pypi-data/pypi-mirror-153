import httpx

from ..database import Database, ServerError


class AioDatabase(Database):

    def __init__(
        self, db_name, db_url='http://localhost:18123/', username=None,
        password=None, readonly=False, autocreate=True, timeout=60,
        verify_ssl_cert=True, log_statements=False
    ):
        super().__init__(
            db_name, db_url, username, password, readonly,
            autocreate, timeout, verify_ssl_cert, log_statements
        )
        self.request_session.close()
        self.request_session = httpx.AsyncClient(verify=verify_ssl_cert)
        if username:
            self.request_session.auth = (username, password or '')
        self._send = self._aio_send

    async def aclose(self):
        await self.request_session.aclose()

    async def _aio_send(self, data, settings=None, stream=False):
        r = await super()._send(data, settings, stream)
        if r.status_code != 200:
            raise ServerError(r.text)
        return r

    async def count(
        self,
        model_class,
        conditions=None
    ) -> int:
        """
        Counts the number of records in the model's table.

        - `model_class`: the model to count.
        - `conditions`: optional SQL conditions (contents of the WHERE clause).
        """
        from clickhouse_orm.query import Q
        query = 'SELECT count() FROM $table'
        if conditions:
            if isinstance(conditions, Q):
                conditions = conditions.to_sql(model_class)
            query += ' WHERE ' + str(conditions)
        query = self._substitute(query, model_class)
        r = await self._send(query)
        return int(r.text) if r.text else 0

    async def aio_create_database(self):
        await self._send('CREATE DATABASE IF NOT EXISTS `%s`' % self.db_name)
        self.db_exists = True
