from sqlalchemy import (BIGINT, Column, Float, String, Table, and_, asc, desc,
                        func, or_, select)

from .base import BaseTable, engine, meta


class KlineData(BaseTable):
    def __init__(self, table_name="kline_data_1min", *args, **kwargs):
        super(KlineData, self).__init__(table_name=table_name, *args, **kwargs)
        self.table = Table(self.table_name, meta,
                           Column('symbol', String(30), comment='symbol', primary_key=True),
                           Column('timestamp', BIGINT, comment='timestamp', primary_key=True),
                           Column('open', Float, comment='open', default=0),
                           Column('close', Float, comment='close', default=0),
                           Column('low', Float, comment='low', default=0),
                           Column('high', Float, comment='high', default=0),
                           Column('vol', Float, comment='vol', default=0))

    def select_symbol_maxmin(self, symbol):
        meta.create_all(engine)
        s = select(self.table.columns.symbol,
                   func.max(self.table.columns.timestamp).label('max_time'),
                   func.min(self.table.columns.timestamp).label('min_time')
                   ).where(self.table.columns.symbol == symbol).group_by(self.table.columns.symbol)
        data = [line for line in engine.execute(s)]
        if len(data) == 1:
            return data[0][1], data[0][2]
        else:
            return 0, 0
