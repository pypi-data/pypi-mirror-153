from glob import glob
import pandas as pd
import numpy as np
import os
import re


class CleaningData:
    def __init__(self, date, company, warehouse_ids, folder) -> None:
        """
        NOTES:
        - Shopee supermarket
            - Raw data dibuat 1 bulan 1 file.
            - SKU tambahin (field: Product ID)
            - Summary jangan ditambahin
        - JDID b2b
            - header sku: sku
            - header qty: sales_quantity
            - header sales: sales_value
            - Summary jangan ditambahin
        - Blibli b2b
            - header sku: sku
            - header qty: sales_quantity
            - header sales: sales_value
        - Shopee b2b formatter
            ex: shopee_b2b_20220301.xlsx
        """

        self.date = date
        self.company = company
        self.col = [
            "date",
            "company",
            "channel",
            "channel_id",
            "transaction_number",
            "sku",
            "sales_value",
            "sales_quantity",
            "status",
            "warehouse_id"
        ]
        self.warehouse_ids = warehouse_ids
        self.df_output = pd.DataFrame(columns=self.col)
        self.folder = os.path.join(folder, self.date)
        self.files = list(map(lambda x: x.lower(), os.listdir(self.folder)))

    def exec(self):
        self.shopee_b2b()
        self.shopee_b2c()
        self.shopee_supermarket()
        self.tokopedia_b2b()
        self.tokopedia_b2c()
        self.blibli_b2b_nmv()
        self.blibli_b2b_gmv()
        self.blibli_b2c()
        self.lazada_b2b()
        self.lazada_b2c()
        self.orami_b2b()
        self.orami_b2c()
        self.bukalapak_b2b()
        self.bukalapak_b2c()
        self.jdid_b2b()
        self.jdid_b2c()
        self.tiktokshop_b2c()
        self.grabmart_b2b()
        self.stock_out_b2b()

        df = self.df_output
        df['company'] = self.company
        df['warehouse_id'] = df.warehouse_id.fillna(1)
        df['sku'] = df.sku.fillna("null_sku")
        df['sku'] = df.sku.apply(lambda x: str(x).replace(".0", ""))
        for s in ['sales_value', 'sales_quantity']:
            try:
                df[s] = np.floor(pd.to_numeric(df[s], errors='coerce')).astype('Int64')
            except:
                df[s] = df[s].astype(int)
        df['date'] = pd.to_datetime(df.date).dt.date
        df['status'] = df.status.str.lower()
        df['transaction_number'] = df.transaction_number.astype(str)
        return df

    def shopee_b2b(self):
        files = glob(os.path.join(self.folder, 'shopee_b2b*'))
        if not files:
            return

        for file in files:
            df = pd.read_excel(file, sheet_name="Product Performance Item Level")
            df['sku'] = df['Product ID']
            df['date'] = pd.to_datetime(file.split('_')[-1].split('.')[0])
            df['channel_id'] = 7

            # gmv
            gmv = df.copy()
            gmv['status'] = 'GMV'
            gmv.rename(columns={
                "Gross Sales(Rp)": "sales_value",
                "Gross Units Sold": "sales_quantity"
            }, inplace=True)

            # nmv
            nmv = df.copy()
            nmv['status'] = 'NMV'
            nmv.rename(columns={
                "Net Sales(Rp)": "sales_value",
                "Net Units Sold": "sales_quantity"
            }, inplace=True)

            df = gmv.append(nmv, ignore_index=True)
            col = list(set(df.columns) & set(self.col))
            self.df_output = self.df_output.append(df[col], ignore_index=True)

    def shopee_b2c(self):
        file = os.path.join(self.folder, 'shopee_b2c.xlsx')
        if 'shopee_b2c.xlsx' not in self.files:
            return
        df = pd.read_excel(file, converters={'Total Harga Produk': str})
        df.rename(columns={
            "Waktu Pesanan Dibuat": "date",
            "No. Pesanan": "transaction_number",
            "SKU Induk": "sku",
            "Total Harga Produk": "sales_value",
            "Jumlah Produk di Pesan": "sales_quantity",
            "Status Pesanan": "status"
        }, inplace=True)
        df['date'] = pd.to_datetime(df.date).dt.date
        df['channel_id'] = 11
        df['sales_value'] = df.sales_value.apply(lambda x: int(re.sub("[\D]", "", x)))
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def shopee_supermarket(self):
        files = glob(os.path.join(self.folder, 'shopee_supermarket*'))
        if not files:
            return
        file = files[0]
        df = pd.read_excel(file)
        df['date'] = pd.to_datetime(file.split('_')[-1].split('.')[0])
        df['channel_id'] = 7
        df['status'] = "GMV"
        df.rename(columns={
            "Product ID": "sku",
            "Gross Sales(Rp)": "sales_value"
        }, inplace=True)
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def tokopedia_b2b(self):
        pass

    def tokopedia_b2c(self):
        file = os.path.join(self.folder, 'tokopedia_b2c.xlsx')
        if 'tokopedia_b2c.xlsx' not in self.files:
            return
        df = pd.read_excel(file, skiprows=4, sheet_name='Laporan Penjualan')
        df.rename(columns={
            "Tanggal Pembayaran": "date",
            "Nomor Invoice": "transaction_number",
            "Nomor SKU": "sku",
            "Status Terakhir": "status",
            "Jumlah Produk Dibeli": "sales_quantity"
        }, inplace=True)
        df = df[df['sku'].isna() == False]
        df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y %H:%M:%S").dt.date
        df['channel_id'] = 5
        df['sales_value'] = df['sales_quantity'] * df['Harga Jual (IDR)']
        try:
            df['Gudang Pengiriman'].fillna(method='ffill', inplace=True)
            df['warehouse_id'] = df['Gudang Pengiriman'].apply(lambda x: self.warehouse_ids[x.lower()])
        except:
            pass
        col = list(set(df.columns) & set(self.col))
        df.fillna(method='ffill', inplace=True)
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def blibli_b2b_nmv(self):
        file = os.path.join(self.folder, 'blibli_b2b_nmv.xlsx')
        if 'blibli_b2b_nmv.xlsx' not in self.files:
            return
        df = pd.read_excel(file, skiprows=3)
        df = df.iloc[:(df[df.Date == 'Total'].index[0])]
        df.rename(columns={
            "Date": "date",
            "Sales": "sales_value",
            "Sold Product": "sales_quantity"
        }, inplace=True)
        df['date'] = pd.to_datetime(df.date)
        # df = df[df['date'].dt.date == (self.date - timedelta(days=1)).date()]
        df['status'] = 'NMV'
        df['channel_id'] = 1
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def blibli_b2b_gmv(self):
        files = glob(os.path.join(self.folder, 'blibli_b2b_gmv*'))
        if not files:
            return
        file = files[0]
        df = pd.read_excel(file)
        df['date'] = pd.to_datetime(file.split('_')[-1].split('.')[0])

        df['channel_id'] = 1
        df['status'] = 'GMV'
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def blibli_b2c(self):
        pass

    def lazada_b2b(self):
        pass

    def lazada_b2c(self):
        files = glob(os.path.join(self.folder, 'lazada*b2c*'))
        if not files:
            return
        for file in files:
            df = pd.read_excel(file)
            df.rename(columns={
                "createTime": "date",
                "orderNumber": "transaction_number",
                "sellerSku": "sku",
                "paidPrice": "sales_value",
                "status": "status"
            }, inplace=True)
            df['date'] = pd.to_datetime(df.date).dt.date
            df['channel_id'] = 3
            df['sales_quantity'] = 1
            col = list(set(df.columns) & set(self.col))
            # pivot
            df = pd.pivot_table(df,
                                index=['channel_id', 'date', 'transaction_number', 'sku', 'status'],
                                values=['sales_value', 'sales_quantity'],
                                aggfunc=np.sum).reset_index()
            self.df_output = self.df_output.append(df[col], ignore_index=True)

    def orami_b2b(self):
        pass

    def orami_b2c(self):
        file = os.path.join(self.folder, 'orami_b2c.xls')
        if 'orami_b2c.xls' not in self.files:
            return
        df = pd.read_excel(file)
        df.rename(columns={
            "Tanggal pesanan": "date",
            "Nomor pesanan": "transaction_number",
            "SKU": "sku",
            "Total harga produk": "sales_value",
            "Kuantitas": "sales_quantity",
            "Status pesanan": "status"
        }, inplace=True)
        df['date'] = pd.to_datetime(df.date).dt.date
        df['channel_id'] = 6
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def bukalapak_b2b(self):
        pass

    def bukalapak_b2c(self):
        file = os.path.join(self.folder, 'bukalapak_b2c.xlsx')
        if 'bukalapak_b2c.xlsx' not in self.files:
            return
        df = pd.read_excel(file)
        df.rename(columns={
            "Tanggal": "date",
            "ID Transaksi": "transaction_number",
            "SKU": "sku",
            "Total Terbayar": "sales_value",
            "Jumlah Produk": "sales_quantity",
            "Status": "status"
        }, inplace=True)
        df['date'] = pd.to_datetime(df.date).dt.date
        df['channel_id'] = 2

        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def jdid_b2b(self):
        files = glob(os.path.join(self.folder, 'jdid_b2b*'))
        if not files:
            return
        file = files[0]
        df = pd.read_excel(file)
        df['date'] = pd.to_datetime(file.split('_')[-1].split('.')[0])
        df['channel_id'] = 4
        df['status'] = 'GMV'
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def jdid_b2c(self):
        pass

    def tiktokshop_b2c(self):
        file = os.path.join(self.folder, 'tiktokshop_b2c.xlsx')
        if 'tiktokshop_b2c.xlsx' not in self.files:
            return
        df = pd.read_excel(file)
        df.drop(0, inplace=True)
        df['channel_id'] = 12
        df.rename(columns={
            "Created Time": 'date',
            "Order ID": 'transaction_number',
            "Order Status": 'status',
            "Seller SKU": 'sku',
            "Order Amount": 'sales_value',
            "Quantity": 'sales_quantity'
        }, inplace=True)
        df['sales_value'] = df.sales_value.apply(lambda x: int(re.sub('[\D]', '', x)))
        df['date'] = pd.to_datetime(df.date)
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def grabmart_b2b(self):
        file = os.path.join(self.folder, 'grabmart_b2b.xlsx')
        if 'grabmart_b2b.xlsx' not in self.files:
            return
        df = pd.read_excel(file)
        df['channel_id'] = 13
        df1 = df.copy()
        df['status'] = 'GMV'
        df1['status'] = 'NMV'
        df = df.append(df1)
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def stock_in(self):
        file = os.path.join(self.folder, 'stock_in.xlsx')
        if 'stock_in.xlsx' not in self.files:
            return
        df = pd.read_excel(file)
        df['date'] = pd.to_datetime(df.date)
        df['warehouse_id'] = df.warehouse.apply(lambda x: self.warehouse_ids[x.lower()])
        df['company'] = self.company
        df['sku'] = df.sku.apply(lambda x: str(x).replace(".0", ""))
        col = ['date', 'warehouse_id', 'sku', 'stock_in_supplier', 'stock_in_retur', 'stock_in_other', 'transfer']
        return df[col]

    def stock_out_b2b(self):
        file = os.path.join(self.folder, 'stock_out_b2b.xlsx')
        if 'stock_out_b2b.xlsx' not in self.files:
            return
        df = pd.read_excel(file)
        df['date'] = pd.to_datetime(df.date)
        df['status'] = 'stock out'
        col = list(set(df.columns) & set(self.col))
        self.df_output = self.df_output.append(df[col], ignore_index=True)

    def product_insert(self):
        file = os.path.join(self.folder, 'product.xlsx')
        if 'product.xlsx' not in self.files:
            return
        df = pd.read_excel(file)
        for c in ['sku', 'regular_product_sku']:
            df[c] = df[c].apply(lambda x: str(x).replace('.0', ''))
        col = ['sku', 'product_name', 'is_bundling', 'regular_product_sku', 'regular_product_quantity', 'company']
        return df[col]

    def platform_traffic(self):
        file = os.path.join(self.folder, 'traffic.xlsx')
        if 'traffic.xlsx' not in self.files:
            return
        df = pd.read_excel(file)
        col = ['date', 'channel', 'total_invoice', 'total_follower', 'new_follower', 'total_viewer', 'company']
        df['company'] = self.company
        return df[col]
