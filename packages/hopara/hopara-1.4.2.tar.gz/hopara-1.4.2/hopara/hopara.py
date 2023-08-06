import json
import logging

from requests.compat import urljoin

from hopara.config import Config
from hopara.request import Request
from hopara.table import Table

BATCH_SIZE = 50000


class Hopara:
    """This class handles all data operations such as creating tables and inserting rows.
    """
    def __init__(self, organization: str = None):
        """Initialize with the organization you want to operate.
        Usually the organization is the domain of your work e-mail (e.g. mycompany.com).
        :param organization: Name of the organization.
        :type organization: str
        """
        self.config = Config()
        self.request = Request(self.config, {'tenant': organization} if organization else None)
        logging.info(f'ORGANIZATION: {organization}')
        logging.info(f'HOST: {self.config.get_dataset_url()}')
        logging.info(f'USER: {self.config.get_client_id() or self.config.get_email()}')

    def get_table_url(self, table_name: str) -> str:
        return urljoin(self.config.get_dataset_url(), f'/table/{table_name}/')

    def get_row_url(self, table_name: str) -> str:
        return urljoin(self.get_table_url(table_name), 'row')

    def delete_table(self, table: Table):
        """ Delete a table
        :param table: table name
        :type table: hopara.Table
        """
        url = self.get_table_url(table.name)
        response = self.request.delete(url, table.get_payload())
        logging.info(f'RESPONSE: {response} / {response.content}\n')

    def create_table(self, table: Table, recreate: bool = False):
        """ Create a table
        :param table: table name
        :type table: hopara.Table
        :param recreate: If set to ``True`` the table will be deleted and recreated. If set to ``False`` new columns will be added to the existing table.
        Default: False.
        **If True is set all data previously store in the table will be permanently removed.**
        :type recreate: bool
        """
        if recreate:
            self.delete_table(table)
        url = self.get_table_url(table.name)
        logging.info(f'URL: {url}')
        logging.info(f'TABLE: {json.dumps(table.get_payload())}')
        response = self.request.post(url, table.get_payload())
        logging.info(f'RESPONSE: {response} / {response.content}\n')

    def __insert_rows(self, url, rows: list):
        response = self.request.post(url, rows)
        logging.info(f'RESPONSE: {response} / {response.content}')

    def insert_rows(self, table: Table, rows: list):
        """ Insert rows in a table.
        :param table: table object
        :type table: hopara.Table
        :param rows: the data to be inserted in the following format: ``[{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]``
        """
        url = self.get_row_url(table.name)
        logging.info(f'URL: {url}')
        logging.info(f'SAMPLE: {json.dumps(rows[0])}')

        if BATCH_SIZE >= len(rows):
            return self.__insert_rows(url, rows)
        batches = range(0, len(rows), BATCH_SIZE)
        logging.info(f'Processing {len(rows):,} rows in {len(batches):,} batches of {BATCH_SIZE:,} rows each...')
        for i, start in enumerate(batches, 1):
            end = min(start + BATCH_SIZE, len(rows))
            self.__insert_rows(url, rows[start:end])

    def update_rows(self, table: Table, new_values: dict, filters: list):
        """Updated rows. The filters parameter can be used to restrict the affected rows.
        :param table: table name
        :type table: hopara.Table
        :param new_values: the new values for the columns in the following format:
        ``{'column_name1': new_value, 'column_name2': new_value2}``
        :type new_values: dict
        :param filters: a list of filter operations, you must use the hopara.Filter to generate it:
        ``[Filter('column_name1') > 10, Filter('column_name2') == 'name', Filter('column_name3') == False]``
        You can use as many Filters as you want to select the rows.
        :type filters: list
        """
        url = urljoin(self.get_table_url(table.name), 'update')
        response = self.request.post(url, {"values": new_values, "filters": filters})
        logging.info(f'RESPONSE: {response} / {response.content}\n')


if __name__ == "__main__":
    hopara = Hopara()
