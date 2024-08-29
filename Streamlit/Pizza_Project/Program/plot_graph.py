import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_trx_vs_revenue(summary_trx_per_month):
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        row_heights = [0.50, 0.75],
        vertical_spacing = 0.01
    )
    
    # Line chart pada subplot 1
    fig.add_trace(
        px.line(
          summary_trx_per_month,
          x = 'month_trx',
          y = 'total_trx',
          markers = True,
          color_discrete_sequence=['#03c03c'],
          labels = dict(
              x = 'month_trx',
              y = 'total_trx'
          ),
          line_shape='linear'
        ).data[0],
        row = 1,
        col = 1
    )
    
    for i in [0, 11]:
        last_month_trx = summary_trx_per_month.loc[i, 'month_trx']
        last_value_trx = summary_trx_per_month.loc[i, 'total_trx']
        if(i == 11):
            add_y = -100
        else:
            add_y = 100
        fig.add_annotation(
            x = last_month_trx,
            y = last_value_trx + add_y,
            text = f'<b>{last_month_trx} ❄️</b><br>Total Transaction : {last_value_trx}',
            showarrow = False,
            font = dict(
                color='#03c03c',
                family = "sans serif",
                size = 15,
            )
        )
    
    fig.update_layout(
        yaxis = dict(
            showline = False,
            showgrid = False,
            showticklabels = False,
        )
    )
    
    # Add annotation for the maximum value with distance
    max_month_trx = summary_trx_per_month.loc[summary_trx_per_month['total_trx'].idxmax(), 'month_trx']
    max_value_trx = summary_trx_per_month['total_trx'].max()
    
    fig.add_annotation(
        x = max_month_trx,
        y = max_value_trx + 100,
        text = f'<b>{max_month_trx} ☀️ </b><br>Best Transaction : {max_value_trx}',
        showarrow = False,
        font = dict(
            color='#02862a',
            family = "sans serif",
            size = 15,
        )
    )
    
    # Add line chart to the second row
    fig.add_trace(
        px.bar(
          summary_trx_per_month,
          x = 'month_trx',
          y = 'total_revenue',
          labels = dict(
              x = 'month_trx',
              y = 'total_revenue'
          ),
          text = ['$' + str(round(value / 1000, 1)) + 'k' for value in summary_trx_per_month['total_revenue']]
        ).data[0],
        row = 2,
        col = 1
    )
    
    # Update layout
    fig.update_layout(
        height = 600,
        width = 1200,
        bargap = 0.05,
        showlegend = False,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
    )
    
    fig.update_traces(
        marker = dict(
            color= ['#02862a' if val == 1 else '#03c03c' for val in summary_trx_per_month['rank_revenue']]
        )
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        showgrid  = False,
        visible = False,
        tickfont_color = "white"
    )
    
    return(fig)

def plot_total_qty_per_pizzacategory(total_qty_per_pizzacat_per_month):
    
    end_of_data = total_qty_per_pizzacat_per_month[total_qty_per_pizzacat_per_month['month_trx'] == 'December']
    end_of_data['avg_total_order'] = total_qty_per_pizzacat_per_month.groupby(['pizza_category'])['total_quantity'].transform('mean')\
                                                .round(0).astype(int)
                                                
    # Definisikan warna garis
    pick_color = ['#D19C4B', '#FAE8C5', '#FAE8C5', '#FAE8C5']
    
    # Buat grafik line dasar
    fig = px.line(
        total_qty_per_pizzacat_per_month,
        x = 'month_trx',
        y = 'total_quantity',
        color = 'pizza_category',
        color_discrete_sequence = pick_color,
        hover_data = ['pizza_category']
    )
    # Edit Hover Template
    fig.update_traces(
        hovertemplate = 'Pizza %{customdata[0]}<br>%{x} 2015<br><sup>Total Order = %{y}</sup>',
        hoverlabel = dict(
            bgcolor = 'white',
            font = dict(
                size = 14,
                color = '#D19C4B'
            )
        )
    )
    
    # Definisikan tebal garis
    tebal_garis = [8, 5, 5, 5]
    
    # Penebalan Garis yang ingin di highlight
    for trace, width in zip(fig.data, tebal_garis):
        if isinstance(trace, go.Scatter):
            trace.line.width = width
            
    # Menambahkan titik diujung grafik
    fig.add_trace(
        go.Scatter(
            x = end_of_data['month_trx'],
            y = end_of_data['total_quantity'],
            mode = 'markers',
            marker = dict(
                size = [22, 15, 15, 15],
                color = pick_color,
                opacity = 1,
            ),
            text = end_of_data['pizza_category'],
            hovertemplate = "Pizza %{text}<br>%{x} 2015<br><sup>Total Order = %{y}</sup>"
        )
    )
    
    # Tambahkan annotation
    for i in end_of_data['ranking']:
        if(i == end_of_data['ranking'].min()):
            teks = f"<b>Pizza {end_of_data[end_of_data['ranking'] == i]['pizza_category'].values[0]}</b><br><sup>Avg. Order = {end_of_data[end_of_data['ranking'] == i]['avg_total_order'].values[0]}</sup>"
        else:
            teks = f"<b>Pizza {end_of_data[end_of_data['ranking'] == i]['pizza_category'].values[0]}</b><br>"
        fig.add_annotation(
            x = end_of_data[end_of_data['ranking'] == i]['month_trx'].values[0],
            y = end_of_data[end_of_data['ranking'] == i]['total_quantity'].values[0],
            text = teks,
            showarrow = False,
            font = dict(
                size = 17,
                color = pick_color[i-1],
                family = "sans serif"
            ),
            align = "left",
            xshift = 80,
            yshift = -1,
            opacity = 0.8
        )
        
    fig.update_layout(
        height = 450,
        width = 780,
        showlegend = False,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        title = dict(
            text = '<b>Total Pizza Terjual Berdasarkan Kategori</b><br><sup><sup>Pizza Classic konsisten menjadi primadona pada tahun 2015</sup></sup>',
            font = dict(
                color = '#D19C4B'
            )
        ),
        yaxis = dict(
            title = 'Total Order',
            showline = True,
            linewidth = 1,
            color = '#E58651',
            linecolor = '#E58651',
            showgrid = False
        ),
        xaxis = dict(
            title = '',
            showline = True,
            linewidth = 1,
            color = '#E58651',
            linecolor = '#E58651',
            showgrid = False
        )
    )
    
    return(fig)

def plot_total_qty_per_pizzaname(total_qty_per_pizzaname):
    
    total_qty_per_pizzaname['Color'] = total_qty_per_pizzaname['total_quantity'].apply(lambda x: 'Top' if x == total_qty_per_pizzaname['total_quantity'].max() else 'Other')

    fig = px.bar(
        total_qty_per_pizzaname,
        x = 'total_quantity',
        y = 'pizza_name',
        orientation = 'h',
        color = 'Color',
        color_discrete_map = {
            'Other': '#85ff7a',
            'Top': '#2db83d'
        },
        text_auto = True
    )
    
    fig.update_layout(
        width = 450,
        height = 470,
        xaxis_title = '',
        yaxis_title = '',
        showlegend = False,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        title = dict(
            text = '<b><i>Best Seller</i> Pizza Berdasarkan Nama</b><br><sup><sup>Periode 2015</sup></sup>',
            font = dict(
                color = '#D19C4B'
            )
        )
    )
    
    fig.update_xaxes(showticklabels=False)
    
    fig.update_traces(
        textposition = 'inside',
        hovertemplate = '<b>Pizza %{label}</b><br>Total Quantity = %{value}'
    )
    
    return(fig)

def plot_pizza_sold_per_day(total_pizza_sold_per_day):

    fig = px.bar(
        total_pizza_sold_per_day,
        x = 'day_trx',
        y = 'avg_sold_per_day',
        orientation = 'v',
        text_auto = True,
        hover_data = ['avg_revenue_per_day']
    )
    
    fig.update_layout(
        width = 500,
        height = 500,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        xaxis_title = '',
        yaxis_title = '',
        showlegend = False,
    )
    
    fig.update_yaxes(
        showticklabels = False, 
        showgrid = False
    )
    
    fig.update_traces(
        textposition = 'inside',
        hovertemplate = '<b>%{label}</b><br>Avg Pizza Sold = %{value}<br>Avg Revenue = $ %{customdata[0]}',
        marker_color = total_pizza_sold_per_day['Color'].tolist()
    )
    
    return(fig)

def plot_avg_order_per_hour(avg_order_per_hour, num_order_per_hour):

    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        row_heights = [0.25, 0.75],
        vertical_spacing = 0.01
    )
    
    fig.add_trace(
        px.bar(
          avg_order_per_hour,
          x = 'hour_trx',
          y = 'avg_order_per_hour',
          labels = dict(
              x = 'month_trx',
              y = 'total_revenue'
          ),
          color = 'avg_order_per_hour',
        ).data[0],
        row = 1,
        col = 1
    )
    
    fig.update_layout(
        yaxis = dict(
            showline = False,
            showgrid = False,
            showticklabels = False,
        )
    )
    
    fig.add_trace(
        px.imshow(
            num_order_per_hour
        ).data[0],
        row = 2,
        col = 1
    )
    
    fig.update(
        layout_coloraxis_showscale = False
    )
    
    fig.update_xaxes(
        automargin=True
    )
    
    fig.update_layout(
        height = 600,
        width = 700,
        bargap = 0.05,
        coloraxis_colorscale = 'oranges',
        xaxis_tickangle = 0,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        title = dict(
            text = '<b>Rata - Rata Pizza Dipesan Tiap Jam Setiap Harinya</b><br><sup><sup>Periode 2015</sup></sup>',
            font = dict(
                color = '#B54B1F'
            )
        )
    )
    
    return(fig)

def plot_total_order_per_hour(total_order_per_date_and_hour):
    
    total_order_per_date_and_hour.loc[:, 'flag'] = total_order_per_date_and_hour['total_table'].apply(lambda x : 'Red' if x > 15 else 'Grey')
        
    fig = px.scatter(
        total_order_per_date_and_hour,
        x = 'date',
        y = 'total_table',
        color = 'flag',
        color_discrete_map = {
            'Grey' : '#B8B2B6',
            'Red' : '#DA1D1D'
        },
        text = 'hour_trx'
    )
        
    # Update layout
    fig.update_layout(
        height = 400,
        width = 400,
        bargap = 0.05,
        showlegend = False,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        #paper_bgcolor = 'rgba(0, 0, 0, 0)',
        yaxis = dict(
            title = '<b>Total Meja</b>'
        ),
        margin = dict(t=0)
    )
    
    fig.update_xaxes(showgrid=False)
    
    fig.update_yaxes(
        showgrid=False,
        #visible=False,
        #tickfont_color="white"
    )
        
    return(fig)

def plot_quantity_per_order(quantity_per_order):
    total_data = quantity_per_order['total'].sum()
    
    # Warna
    hijau_pucat = '#E0ECE4'
    merah = '#FF4B5C'
    
    # Buat pie chart
    fig = px.pie(
        values = quantity_per_order['total'],
        names = quantity_per_order['type_order'],
        color_discrete_sequence = [merah, hijau_pucat],
        hole = 0.65
    )
    
    # Atur posisi label
    fig.update_traces(
        textposition = 'outside',
        textinfo = 'percent+label',
        hovertemplate='<b>%{label}</b><br>%{value} Customers'
    )
    
    # Atur luas grafik, hapus legend dan beri judul
    fig.update_layout(
        width = 400,
        height = 400,
        showlegend = False,
        margin = dict(t=0, l=50, r=50, b=50)
    )
    
    # Berikan informasi total pelanggan di tengah donut chart
    fig.add_annotation(
        text = f'Total Order<br><b><span style="font-size: 28px;">{total_data}</b></span>',
        x = 0.5,
        y = 0.5,
        showarrow = False,
        font = dict(size = 20)
    )
    
    # Tampilkan grafik
    return(fig)

def plot_prediction(
    data : pandas.DataFrame,
    value : str,
    judul : str,
    tipe : str,
    warna : str = 'black',
    showtrend : bool = False,
):
    fig = px.line(
        data_frame = data,
        x = data.index,
        y = value,
        color = tipe,
        color_discrete_map = {
            'original_data' : '#BA0001',
            'prediction' : '#FFAF00'
        } 
    )

    if(showtrend):
        # Hitung koefisien regresi linier
        coefficients = np.polyfit(range(len(data)), data[value], 1)
        slope = coefficients[0]
        intercept = coefficients[1]

        # Tambahkan garis regresi ke plot
        fig.add_scatter(
            x = data.index,
            y = range(len(data)) * slope + intercept,
            mode = 'lines',
            line = dict(
                color = '#F7B4BB',
                dash = 'dash'
            )
        )

    fig.update_layout(
        width = 1200,
        height = 500,
        showlegend = False,
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        title = dict(
            text = judul,
            font = dict(
                size = 28,
                color = '#B0A7A7'
            ),
            y = 0.92,
            x = 0.5
        ),
        yaxis = dict(
            title = '',
            showgrid = False,
            showline = False,
            showticklabels = False,
            zeroline = False,
        ),
        margin = dict(
            t = 80,
            b = 10,
            r = 20
        )
    )

    return(fig)
