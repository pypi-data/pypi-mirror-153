import os
from datetime import datetime, timedelta


class DbAction:
    def __init__(self, query_path, db_cursor) -> None:
        self.query_path = query_path
        self.db_cursor = db_cursor

    def product_checking(self):
        query = open(os.path.join(self.query_path, "product_checking.sql"), "r").read()
        self.db_cursor.execute(query)
        return self.db_cursor.fetchall()

    def insert_transaction(self):
        query = open(os.path.join(self.query_path, "insert_transaction.sql"), "r").read()
        self.db_cursor.execute(query)
        self.db_cursor.commit()

    def insert_stock_in(self):
        query = open(os.path.join(self.query_path, "insert_stock_in.sql"), "r").read()
        self.db_cursor.execute(query)
        self.db_cursor.commit()

    def insert_stock(self):
        # get min data
        query = "select min(date) from sales_value where (quantity_sellout > 0) and (date(created_at) = current_date)"
        self.db_cursor.execute(query)

        # delete product stock start from specific date until current date
        min_date = self.db_cursor.fetchone()
        query = f"delete from product_stock where date >= '{min_date}'"
        self.db_cursor.execute(query)
        self.db_cursor.commit()

        min_date = datetime.strptime(min_date, '%Y-%m-%d')

        base = datetime.now()
        diff_days = (base - min_date).days
        date_list = [base - timedelta(days=x + 1) for x in range(diff_days)]
        for d in date_list:
            query = open(os.path.join(self.query_path, "insert_stock.sql"))
            self.db_cursor.execute(query.replace("[date]", d.strftime("%Y-%m-%d ")))
            self.db_cursor.commit()

    def insert_product(self):
        query = open(os.path.join(self.query_path, "insert_product.sql"), "r").read()
        self.db_cursor.execute(query)
        self.db_cursor.commit()

    def insert_traffic(self):
        query = open(os.path.join(self.query_path, "insert_traffic.sql"), "r").read()
        self.db_cursor.execute(query)
        self.db_cursor.commit()
