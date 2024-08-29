import streamlit
import warnings
import css_style as css
import ts_forecasting as ts
import data_manipulation as dm
import plot_graph as pg

# Konfigurasi awal streamlit
streamlit.set_page_config(
    page_title = 'Pizza Sales Analysis - Bachtiyar', 
    page_icon = '🍕', 
    layout = 'wide'
)

def markdown_html(rows, text):
    rows.markdown(
        text,
        unsafe_allow_html = True
    )
    
def display_plotly(row, fig, container_width = False): 
    row.plotly_chart(
        figure_or_data = fig, 
        use_container_width = container_width
    )

def format_number(value):
    text = f"{value:,}".replace(',', '.')
    return(text)

@streamlit.cache_resource
def teks_pemisah_halaman():
    _, row, _ = streamlit.columns([0.1, 7.2, 0.1])
    teks_pemisah = '<p align="center" style="font-size: 25px;">──── 🍅🧀🍕🍄🌶️🥓 ────<br><br></p>'
    markdown_html(row, text = teks_pemisah)

@streamlit.cache_data
def get_data():
    raw_data = dm.extract_data('Pizza Sales.xlsx')
    transformed_data = dm.transform_data(raw_data)
    return(raw_data, transformed_data)

# LAYOUT 1
@streamlit.cache_resource
def display_header():
    _, row, _ = streamlit.columns([0.1, 7.2, 0.1])
    
    # Atur judul
    title_component = css.rectangular_shape(
        text_color = 'white',
        font_size = 300,
        border_radius = 15,
        background_color = '#ffac0e',
        text = '🍕 Operational Improvement Review 2015 🍅<br>Plato\'s Pizzeria'
    )
    markdown_html(row, text = title_component)
    
    markdown_html(row, text = css.name_header())
    markdown_html(row, text = css.subtitle(text = 'Latar Belakang'))
    markdown_html(row, text = dm.extract_text('1. Latar Belakang.txt'))

# LAYOUT 2
@streamlit.cache_data
def display_data(raw_data):
    _, row, _ = streamlit.columns([0.1, 7.2, 0.1])

    markdown_html(row, text = css.subtitle(text = 'Data'))
    markdown_html(row, text = dm.extract_text('2. Data.txt'))
    
    row.dataframe(
        data = raw_data, 
        use_container_width = False, 
        hide_index = True, 
    )
    
    teks_pemisah_halaman()

# LAYOUT 3
@streamlit.cache_resource
def display_report_summary(_agg):
    _, row0, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _, row3, _ = streamlit.columns([0.1, 3, 0.1, 3, 0.1, 3, 0.1])
    _, row4, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row5, _, row6, _ = streamlit.columns([0.1, 5, 0.1, 3, 0.1])
    _, row7, _ = streamlit.columns([0.1, 7.2, 0.1])
    
    summary_performance = agg.calc_summary_performance()
    markdown_html(row0, text = css.subtitle(text = '<i>Performance Summary</i>'))
    
    markdown_html(row0, text = css.score_card())
    row1.write(
        css.summary_rectangle('Total Revenue', '$' + format_number(summary_performance.get("total_revenue_per_year"))),
        unsafe_allow_html = True
    )
    
    row2.write(
        css.summary_rectangle('Total Order', format_number(summary_performance.get("total_order_per_year"))),
        unsafe_allow_html = True
    )
    
    row3.write(
        css.summary_rectangle('Total Pizza Sold', format_number(summary_performance.get("total_pizza_per_year"))),
        unsafe_allow_html = True
    )
    
    markdown_html(row4, text = "<br>" + dm.extract_text('3. Performance Summary 1.txt'))
    
    trx_and_revenue_per_month = agg.calc_trx_and_revenue_per_month()
    fig_trx_vs_revenue = pg.plot_trx_vs_revenue(trx_and_revenue_per_month)
    display_plotly(row4, fig_trx_vs_revenue)
    
    markdown_html(row4, text = dm.extract_text('3. Performance Summary 2.txt') + '<br>')
    
    total_qty_per_pizzacategory = agg.calc_qty_per_pizzacategory()
    fig_qty_per_pizzacategory = pg.plot_total_qty_per_pizzacategory(total_qty_per_pizzacategory)
    display_plotly(row5, fig_qty_per_pizzacategory)
    
    
    total_qty_per_pizzaname = agg.calc_qty_per_pizzaname()
    fig_qty_per_pizzaname = pg.plot_total_qty_per_pizzaname(total_qty_per_pizzaname)
    display_plotly(row6, fig_qty_per_pizzaname)
    
    markdown_html(row7, text = dm.extract_text('3. Performance Summary 3.txt'))
    
    cta_performance_summary_text = dm.extract_text('3. Rekomendasi.txt')
    markdown_html(row7, text = css.note_rectangle())
    row7.write(
        css.recommendation_rectangle(cta_performance_summary_text),
        unsafe_allow_html = True
    )
    
    teks_pemisah_halaman()

# LAYOUT 4
@streamlit.cache_resource
def display_peak_time(_agg):
    _, row0, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _ = streamlit.columns([0.1, 5, 0.1, 5, 0.1])
    _, row3, _ = streamlit.columns([0.1, 7.2, 0.1])
    
    markdown_html(row0, text = css.subtitle(text = '<i>Peak Time</i> : Optimalkan Persiapan Staff Saat Jam Makan Siang'))
    markdown_html(row0, text = dm.extract_text('4. Peak Time A.txt'))
    
    total_pizza_sold_per_day = agg.calc_total_pizza_sold_per_day()
    fig_pizza_sold_per_day = pg.plot_pizza_sold_per_day(total_pizza_sold_per_day)
    display_plotly(row0, fig_pizza_sold_per_day, container_width = True)
    markdown_html(row0, text = dm.extract_text('4. Peak Time B.txt'))
    
    avg_order_per_hour, num_order_per_hour = agg.calc_avg_qty_pizza_per_hour()
    fig_plot_avg_order_per_hour = pg.plot_avg_order_per_hour(avg_order_per_hour, num_order_per_hour)
    display_plotly(row1, fig_plot_avg_order_per_hour, container_width = True)
    markdown_html(row2, text = dm.extract_text('4. Peak Time C.txt'))
    
    cta_peak_time_text = dm.extract_text('4. Rekomendasi.txt')
    markdown_html(row3, text = css.note_rectangle())
    row3.write(
        css.recommendation_rectangle(cta_peak_time_text),
        unsafe_allow_html = True
    )
    
    teks_pemisah_halaman()

# LAYOUT 5
@streamlit.cache_resource
def display_seating_capacity(_agg):
    _, row0, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _ = streamlit.columns([0.1, 5, 0.1, 5, 0.1])
    _, row3, _, row4, _ = streamlit.columns([0.1, 5, 0.1, 5, 0.1])
    _, row5, _ = streamlit.columns([0.1, 7.2, 0.1])
    
    markdown_html(row0, text = css.subtitle(text = '<i>Kapasitas Pelanggan</i> : Pertimbangkan Meja Berkapasitas Kecil'))
    markdown_html(row1, text = dm.extract_text('5. Seating Capacity A.txt'))
    
    total_order_per_hour = agg.calc_total_order_per_hour()
    fig_total_order_per_hour = pg.plot_total_order_per_hour(total_order_per_hour)
    display_plotly(row2, fig_total_order_per_hour, container_width = True)
    
    quantity_per_order = agg.calc_quantity_per_order()
    fig_quantity_per_order = pg.plot_quantity_per_order(quantity_per_order)
    display_plotly(row3, fig_quantity_per_order, container_width = True)
    
    markdown_html(row4, text = dm.extract_text('5. Seating Capacity B.txt'))
    
    cta_seating_capacity_text = dm.extract_text('5. Rekomendasi.txt')
    markdown_html(row5, text = css.note_rectangle())
    row5.write(
        css.recommendation_rectangle(cta_seating_capacity_text),
        unsafe_allow_html = True
    )
    
    teks_pemisah_halaman()

# LAYOUT 6
@streamlit.cache_resource
def display_prediction(_agg):
    _, row0, _ = streamlit.columns([0.1, 7.2, 0.1])
    _, row1, _, row2, _ = streamlit.columns([0.1, 5, 0.1, 5, 0.1])
    
    markdown_html(row0, text = css.subtitle(text = '<i>Proyeksi Kedepan</i> : Perencanaan yang Lebih Matang'))
    total_qty_pizza_per_day = agg.calc_total_qty_pizza_per_day()
    
    forecast = ts.predict_qty_pizza(total_qty_pizza_per_day, pizza_name = 'The Barbecue Chicken Pizza', period = 90)
    fig_prediction = pg.plot_prediction(
        data = forecast.set_index('ds'),
        value = 'y',
        tipe = 'category',
        judul = f"<b><span style='color:#FFAF00'>Prediksi Penjualan</span><span style='color:#BA0001'> {pizza_name} </span></b><br><sup><sup>di Plato's Pizzarea untuk {period} hari Kedepan</sup></sup>",
        showtrend = True
    )

    fig_total_order_per_hour = pg.plot_total_order_per_hour(total_order_per_hour)
    display_plotly(row1, fig_total_order_per_hour, container_width = True)

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    
    display_header()
    
    raw_data, transformed_data = get_data()
    display_data(raw_data)
    
    agg = dm.Aggregation(transformed_data)
    display_report_summary(agg)
    
    display_peak_time(agg)
    display_seating_capacity(agg)
    display_prediction(agg)
