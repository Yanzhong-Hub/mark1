"""
The module for all sql query
"""
import pandas as pd
from sqlalchemy import create_engine


class MySQL:
    def __init__(self):
        # create engine
        self.engine = create_engine('mysql+pymysql://root:Hyz.js180518@localhost:3306/tushare',
                                    echo=False)

    def save_data(self, df, df_name, method):
        df.to_sql(name=df_name, con=self.engine, if_exists=method, index=False)

    def get_data(self, sql):
        return pd.read_sql(sql=sql, con=self.engine)


if __name__ == '__main__':
    pass
