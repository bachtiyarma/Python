from prophet import Prophet

def predict_qty_pizza(total_qty_pizza_per_day, pizza_name, period):
    condition1 = total_qty_pizza_per_day['pizza_name'] == pizza_name
    trx_pizza_name = total_qty_pizza_per_day[condition1]
    data_trx_per_day = master_date.merge(trx_pizza_name, on = 'date', how = 'left')
    data_trx_per_day['pizza_name'] = pizza_name
    data_trx_per_day['total_qty'] = data_trx_per_day['total_qty'].fillna(0)    
    data_trx_per_day['category'] = 'original data'
    data_trx_per_day = data_trx_per_day.rename(columns = {
        'date' : 'ds',
        'total_qty' : 'y'
    })
    
    model = Prophet()
    model.fit(data_trx_per_day)

    future = model.make_future_dataframe(periods = period)
    forecast = model.predict(future)
    forecast['pizza_name'] = pizza_name
    forecast['category'] = 'prediction'

    forecast = forecast[forecast['ds'] >= '2015-12-31'][['ds', 'pizza_name', 'yhat', 'category']].reset_index(drop = True)
    forecast.loc[0, 'yhat'] = data_trx_per_day[data_trx_per_day['ds'] == '2015-12-31']['y'].values[0]
    forecast = forecast.rename(columns = {'yhat' : 'y'})
    forecast = pandas.concat([data_trx_per_day[['ds', 'pizza_name', 'y', 'category']], forecast])
    forecast['y'] = forecast['y'].round(0)
    return(forecast)
