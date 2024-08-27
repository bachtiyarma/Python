import os
import numpy
import pandas
import requests
from urllib.parse import quote

default_path = 'https://raw.githubusercontent.com/bachtiyarma/Python/main/Streamlit/Pizza%20Project/'

def extract_data(name_file: str) -> pandas.DataFrame:
    """
    Proses untuk melakukan ekstraksi data yang diperlukan 
    
    Args:
        name_file (str): Nama File excel
    
    Return:
        raw_data (pandas.DataFrame): Data mentah hasil ekstraksi (transaksi pizza)
    """
    
    name_file = default_path + 'Data/' + quote(name_file)
    
    raw_data = pandas.read_excel(
        name_file,
        engine = 'openpyxl', 
        parse_dates = ['date'],
        dtype = {
            'order_id' : 'object',
            'order_details_id' : 'object'
        }
    )
    
    return(raw_data)

def transform_data(raw_data: pandas.DataFrame) -> pandas.DataFrame :
    """
    Proses mentransformasi data 
    
    Args:
        None
    
    Return:
        transformed_data: Data hasil transformasi
    """
    
    transformed_data = raw_data
    
    # Ubah kolom time bertipe object menjadi timestamp
    transformed_data['time'] = pandas.to_datetime(
        transformed_data['time'],
        format = '%H:%M:%S'
    )
    
    # Ekstrak beberapa elemen waktu
    hours = transformed_data['time'].dt.hour
    day_name = transformed_data['date'].dt.day_name()
    month_name = transformed_data['date'].dt.month_name()
    
    # Transformasikan kolom month menjadi tipe kategorikal
    months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    month_name = pandas.Categorical(
        month_name,
        categories = months,
        ordered = True
    )
    
    # Transformasikan kolom days menjadi tipe kategorikal
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]
    
    day_name = pandas.Categorical(
        day_name,
        categories = days,
        ordered = True
    )
    
    # Insert beberapa data tambahan
    transformed_data.insert(4, 'month_trx', month_name)
    transformed_data.insert(5, 'day_trx', day_name)
    transformed_data.insert(6, 'hour_trx', hours)
    
    transformed_data.loc[:, 'total_price'] = transformed_data['quantity'] * transformed_data['price']
    
    return(transformed_data)

def extract_text(file_name):
    """
    Proses untuk melakukan ekstraksi data teks
    
    Args:
        file_name (str): Nama File yang akan diekstrak
    
    Return:
        text (str): Teks hasil ekstraksi
    """
    
    encoded_url = default_path + 'Teks/' + quote(file_name)
    response = requests.get(encoded_url)
    text = '<p align="justify">' + response.text + '</p>'
    return(text)

class Aggregation():
    
    def __init__(self, data):
        self.data = data
    
    def calc_summary_performance(self) -> dict:
        summary_performance = dict(
            total_revenue_per_year = int(self.data['total_price'].sum().round(0)),
            total_order_per_year = int(self.data['order_id'].nunique()),
            total_pizza_per_year = int(self.data['quantity'].sum().round(0))
        )
        
        return(summary_performance)
    
    def calc_trx_and_revenue_per_month(self) -> pandas.DataFrame:
        total_trx_per_month = self.data\
            .groupby(['month_trx'], as_index = False)\
            .agg(total_trx = ('order_id', 'nunique'),
                 total_revenue = ('total_price', 'sum'))
        
        total_trx_per_month['rank_total_trx'] = total_trx_per_month['total_trx'].rank(method = 'max', ascending = False).astype(int)
        total_trx_per_month['rank_revenue'] = total_trx_per_month['total_revenue'].rank(method = 'max', ascending = False).astype(int)
        return(total_trx_per_month)
    
    def calc_qty_per_pizzacategory(self) -> pandas.DataFrame:
        total_qty_per_pizzacat_per_month = self.data\
            .groupby(['month_trx', 'pizza_category'], as_index = False)\
            .agg(total_quantity = ('quantity', 'sum'))

        # Memberi rank urutan untuk penjualan best seller pizza
        total_qty_per_pizzacat_per_month['ranking'] = total_qty_per_pizzacat_per_month.groupby(['pizza_category'])['total_quantity'].transform(sum)\
                                                            .rank(ascending = False, method='dense')\
                                                            .astype(int)
        
        total_qty_per_pizzacat_per_month = total_qty_per_pizzacat_per_month.sort_values(
            by = ['ranking', 'month_trx'],
            ascending = True,
            ignore_index = False
        )
        
        return(total_qty_per_pizzacat_per_month)
    
    def calc_qty_per_pizzaname(self) -> pandas.DataFrame:
        total_qty_per_pizzaname = self.data\
            .groupby(['pizza_category', 'pizza_name'], as_index = False)\
            .agg(total_quantity = ('quantity', 'sum'))
            
        total_qty_per_pizzaname['pizza_name'] = '<b>' + total_qty_per_pizzaname['pizza_category'] + '</b> | ' + total_qty_per_pizzaname['pizza_name']
        total_qty_per_pizzaname = total_qty_per_pizzaname.sort_values(
            by = ['total_quantity'],
            ascending = True,
            ignore_index = True
        )
        
        total_qty_per_pizzaname = total_qty_per_pizzaname.tail(10)
        return(total_qty_per_pizzaname)
    
    def calc_total_pizza_sold_per_day(self) -> pandas.DataFrame:
        total_pizza_sold_per_day = self.data\
            .groupby(['day_trx'], as_index = False).agg(
                total_quantity = ('quantity', 'sum'),
                total_revenue = ('total_price', 'sum'),
                total_day = ('date', 'nunique'),
            )
        
        total_pizza_sold_per_day['avg_sold_per_day'] = (total_pizza_sold_per_day['total_quantity'] / total_pizza_sold_per_day['total_day']).round(0).astype(int)
        total_pizza_sold_per_day['avg_revenue_per_day'] = (total_pizza_sold_per_day['total_revenue'] / total_pizza_sold_per_day['total_day']).round(0).astype(int)
        total_pizza_sold_per_day['Color'] = total_pizza_sold_per_day['avg_sold_per_day'].apply(lambda x: '#D6AE86' if x == total_pizza_sold_per_day['avg_sold_per_day'].max() else '#F3DDBD')
        return(total_pizza_sold_per_day)
    
    def calc_avg_qty_pizza_per_hour(self):
        
        num_order_per_hour = self.data[['order_id', 'month_trx', 'day_trx', 'hour_trx', 'quantity']]
        num_order_per_hour = num_order_per_hour.groupby(['month_trx', 'day_trx', 'hour_trx']).agg(total_order_per_month = ('order_id', 'nunique'))
        num_order_per_hour = num_order_per_hour.groupby(['day_trx', 'hour_trx']).agg(avg_order_per_month = ('total_order_per_month', 'mean')).reset_index()
        num_order_per_hour['avg_order_per_month'] = num_order_per_hour['avg_order_per_month'].round().fillna(0)
        
        
        avg_order_per_hour = num_order_per_hour.groupby(['hour_trx'], as_index = False).agg(avg_order_per_hour = ('avg_order_per_month', 'mean'))
        
        num_order_per_hour_pivot = num_order_per_hour.pivot(
            index = 'day_trx',
            columns = 'hour_trx',
            values = 'avg_order_per_month'
        ).sort_values(by = 'day_trx', ascending = False)
        
        num_order_per_hour_pivot

        return(avg_order_per_hour, num_order_per_hour_pivot)
    
    def calc_total_order_per_hour(self):
        total_order_per_date_and_hour = self.data.groupby(['date', 'hour_trx', 'order_id'], as_index = False).agg(total_pizza = ('quantity', 'sum'))
        total_order_per_date_and_hour['table'] = (total_order_per_date_and_hour['total_pizza']/4).apply(numpy.ceil)
        total_order_per_date_and_hour = total_order_per_date_and_hour.groupby(['date', 'hour_trx'], as_index = False).agg(total_table = ('table', 'sum'))
        return(total_order_per_date_and_hour)
    
    def calc_quantity_per_order(self):
        quantity_per_order = self.data.groupby(['order_id'], as_index = False).agg(total = ('quantity', 'sum'))
        quantity_per_order['type_order'] = quantity_per_order['total'].apply(lambda x : '1-2 Order' if x <= 2 else '> 2 Order')
        quantity_per_order = quantity_per_order.groupby('type_order', as_index = False).agg(total = ('order_id', 'count'))
        return(quantity_per_order)