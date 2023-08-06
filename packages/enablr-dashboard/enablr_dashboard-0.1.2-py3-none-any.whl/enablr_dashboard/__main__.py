from datetime import date, datetime, timedelta
from glob import glob
from .connect import Connect as db_connect
from .db_action import DbAction as db_action
from .cleaning_data import CleaningData as cleaning_data
from .read_gdrive import main as main_read_gdrive
from loguru import logger
import argparse
import pandas as pd
import os
import toml


def main(date_cutoff, warehouse_ids):
    data_trx = pd.DataFrame()
    data_sellin = pd.DataFrame()
    data_product = pd.DataFrame()
    data_traffic = pd.DataFrame()
    company_folder = os.listdir(os.path.join(os.getcwd(), 'tmp'))
    for company in company_folder:
        # check_folder
        data_company = os.path.join('tmp', company)
        data_company = os.path.join(os.getcwd(), data_company)
        try:
            os.listdir(os.path.join(data_company, date_cutoff))
        except Exception as err:
            continue
        obj = cleaning_data(
            date=date_cutoff,
            company=company,
            warehouse_ids=warehouse_ids,
            folder=data_company
        )
        data_trx = data_trx.append(obj.exec(), ignore_index=True)
        data_sellin = data_sellin.append(obj.stock_in(), ignore_index=True)
        data_product = data_product.append(obj.product_insert(), ignore_index=True)
        data_traffic = data_traffic.append(obj.platform_traffic(), ignore_index=True)

    db_prod = db_connect(conf_path, server='DB_PRODUCTION')
    db_action_prod = db_action(query_path, db_prod)

    if data_product.shape[0] == 0:
        db_prod.execute("delete from temp_product")
    else:
        data_product.to_sql('temp_product', db_prod.engine(), if_exists='replace', index=False, method='multi')
        db_action_prod.insert_product()

    if data_trx.shape[0] == 0:
        db_prod.execute("delete from temp_transaction")
    else:
        data_trx.to_sql('temp_transaction', db_prod.engine(), if_exists='replace', index=False, method='multi')
        product = db_action_prod.product_checking()
        # db_action_prod.insert_transaction()
        if not product:
            db_action_prod.insert_transaction()
        else:
            print(pd.DataFrame(product, columns=['sku', 'company']))

    if data_traffic.shape[0] == 0:
        db_prod.execute("delete from temp_traffic")
    else:
        data_traffic.to_sql("temp_traffic", db_prod.engine(), if_exists='replace', index=False, method='multi')
        db_action_prod.insert_traffic()
    return


if __name__ == '__main__':
    date_cutoff = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    ap = argparse.ArgumentParser()
    ap.add_argument('-cf', '--companies-folder-gdrive-id', help='Companies folder', required=True)
    ap.add_argument('-q', '--query-gdrive-id', help='Query path', required=True)
    ap.add_argument('-c', '--conf-gdrive-id', help='Conf path', required=True)
    ap.add_argument('-d', '--date-cutoff', help='Date cutoff')
    ap.add_argument('-t', '--test', help='Only for test, will not download new file from gdrive', action='store_true')
    args = ap.parse_args()
    companies_folder = args.companies_folder_gdrive_id
    conf_path = args.conf_gdrive_id
    query_path = args.query_gdrive_id
    date_cutoff_manual = args.date_cutoff
    if date_cutoff_manual:
        date_cutoff = date_cutoff_manual
    if not args.test:
        main_read_gdrive(conf_path)
    conf_path = 'tmp/ENABLR_CLIENT_DASHBOARD.toml'
    if not args.test:
        main_read_gdrive(query_path)
    query_path = 'tmp/customer_dashboard'
    if not args.test:
        main_read_gdrive(companies_folder, date_cutoff)
    warehouse_ids = toml.load(conf_path).get('warehouse_ids')
    if warehouse_ids:
        main(date_cutoff, warehouse_ids)
    else:
        logger.info("Tidak ada warehouse ids")
    logger.info("Finish....")

"""
old configuration for google collab
# companies_folder = glob("/content/drive/MyDrive/data_customer_dashboard/*")
# companies_folder_exc = glob("/content/drive/MyDrive/data_customer_dashboard/*.gsheet")
# companies_folder = list(set(companies_folder) - set(companies_folder_exc))
# conf_path = "/content/drive/MyDrive/Script/CONF/ENABLR_CLIENT_DASHBOARD.toml"
# query_path = "/content/drive/MyDrive/Script/QUERY/customer_dashboard"
"""