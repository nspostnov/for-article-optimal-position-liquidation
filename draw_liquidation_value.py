import os 
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import config

from psycopg2 import connect as cnct
from datetime import datetime as dt


PATH_ABS = config.PATH_TO_SAVE_1
PATH_FROM_ABS = config.PATH_TO_SAVE_2
DBNAME = config.DB_NAME
USER = config.USER
PASSWORD = config.PASSWORD
HOST = config.HOST
PORT = config.PORT


def main():

    date_seccode_s = (
            [20190603, 'SBER'], 
            [20190624, 'SBER'])

    for key in date_seccode_s: 
        plot_save(*key)


def plot_save(date, seccode):
    data = generate_data(date, seccode)
    percent = round(sum(data['optimal'] > data['equal']) / len(data['optimal']) * 100,
            2)

    figure, ax = plt.subplots(1, 1, sharey=False)
    
    xformatter = mdates.DateFormatter('%H:%M')
    plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)

    ax.plot(data['datetime'], ((data['optimal'] - data['equal']) / 
        (data['volume_to_liquidate']) * 1000000), 
            color='#000000')
    ax.title.set_text(seccode + ' ' + str(date)[:4] + '-' + 
            str(date)[4:6] + '-' + str(date)[6:])

    ax.set_xlabel('Время')
    if percent >= 50:
        ax.legend(['Оптимальная стратегия\nлучше в ' + str(percent) + '%' + ' случаев'])
    else:
        ax.legend(['Наивная стратегия\nлучше в ' + str(100 - percent) + '%' + ' случаев'])

    plt.hlines(0, xmin=data['datetime'][0], 
            xmax=data['datetime'][len(data['datetime']) - 1], color='#DCDCDC')

    figure.autofmt_xdate()
    figure.set_size_inches(w=5, h=4)
    path_name = 'liq_value_comparison_' + seccode + '_' + str(date) + '.pgf'
    path = os.path.join(PATH_ABS, PATH_FROM_ABS, path_name)
    plt.savefig(path, bbox_inches='tight')
    plt.show()


def generate_data(date, seccode):
    connector = cnct(dbname=DBNAME, host=HOST, port=PORT, user=USER, password=PASSWORD)
    with connector as connect:
        cursor = connect.cursor()
        query = f'''
        SELECT date, time, seccode, volume_to_liquidate, optimal, equal
        FROM
            "liquidationvalue_{date}_{seccode}"
        WHERE
            date = {date} and seccode = '{seccode}'
        ORDER BY
            time
        '''
        query = ' '.join(query.split())
        cursor.execute(query)
        data = pd.DataFrame(cursor.fetchall(), columns=['date', 'time', 'seccode', 
            'volume_to_liquidate', 'optimal', 'equal'])
    data['datetime'] = list(map(lambda x: datetime_convert(x[0], x[1]), 
        zip(data['date'], data['time'])))

    data = data[['datetime', 'seccode', 'volume_to_liquidate', 'optimal', 'equal']]

    return data


def datetime_convert(date, time):
    date_str = str(date)
    time_str = str(time)

    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])

    hours = int(time_str[:2])
    minutes = int(time_str[2:4])
    seconds = int(time_str[4:6])
    microseconds = int(time_str[6:])

    datetime = dt(year=year, month=month, day=day, hour=hours, 
            minute=minutes, second=seconds, microsecond=microseconds)

    return datetime


if __name__ == '__main__':
    main()
