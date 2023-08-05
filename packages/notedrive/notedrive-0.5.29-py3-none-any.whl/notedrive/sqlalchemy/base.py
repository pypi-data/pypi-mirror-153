import warnings

from sqlalchemy import MetaData, Table, create_engine

meta = MetaData()


def create_engines(url, **kwargs):
    return create_engine(url, **kwargs)


class BaseTable:
    def __init__(self, table_name, engine, *args, **kwargs):
        self.table_name = table_name
        self.table: Table = None
        self.engine = engine

    def create(self):
        meta.create_all(self.engine)

    def insert(self, values, keys=None, *args, **kwargs):
        cols = [col.name for col in self.table.columns]
        if isinstance(values, dict):
            values = dict([(k, v) for k, v in values.items() if k in cols])
        elif isinstance(values, list):
            if isinstance(values[0], dict):
                values = [dict([(k, v) for k, v in item.items() if k in cols]) for item in values]
            elif isinstance(values[0], list):
                values = [dict(zip(keys, item)) for item in values]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # code here...
            if str(self.engine.url).startswith('sqlite'):
                ins = self.table.insert(values=values).prefix_with("OR IGNORE")
            else:
                ins = self.table.insert(values=values).prefix_with("IGNORE")
            self.engine.execute(ins)
