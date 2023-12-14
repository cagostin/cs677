import sys
import logging
import re
import cs677.config as cfg
from pandas import read_pickle, DataFrame, concat, DateOffset
from numpy import datetime64, array, zeros, apply_along_axis


def weekdays(weekday):
    if weekday == 0:
        logging.info(f'weekday {weekday} is Sunday')
        return [1, 0, 0, 0, 0, 0, 0]
    elif weekday == 1:
        logging.info(f'weekday {weekday} is Monday')
        return [0, 1, 0, 0, 0, 0, 0]
    elif weekday == 2:
        logging.info(f'weekday {weekday} is Tuesday')
        return [0, 0, 1, 0, 0, 0, 0]
    elif weekday == 3:
        logging.info(f'weekday {weekday} is Wednesday')
        return [0, 0, 0, 1, 0, 0, 0]
    elif weekday == 4:
        logging.info(f'weekday {weekday} is Thursday')
        return [0, 0, 0, 0, 1, 0, 0]
    elif weekday == 5:
        logging.info(f'weekday {weekday} is Friday')
        return [0, 0, 0, 0, 0, 1, 0]
    elif weekday == 6:
        logging.info(f'weekday {weekday} is Saturday')
        return [0, 0, 0, 0, 0, 0, 1]
    else:
        raise 'Weekday unknown'


def row_items_costs(item, cost):

    if re.match(cfg.meat_re_m07, item) is not None:
        logging.info(f'item {item} match is an unknown meat')
        return array([0, 0, 0, 0, 0, 0, cost, 0])

    elif re.match(cfg.meat_re_m01, item) is not None:
        logging.info(f'item {item} match is Brisket')
        return array([cost, 0, 0, 0, 0, 0, 0, 0])

    elif re.match(cfg.meat_re_m02, item) is not None:
        logging.info(f'item {item} match is Pork')
        return array([0, cost, 0, 0, 0, 0, 0, 0])

    elif re.match(cfg.meat_re_m03, item) is not None:
        logging.info(f'item {item} match is Chicken')
        return array([0, 0, cost, 0, 0, 0, 0, 0])

    elif re.match(cfg.meat_re_m04, item) is not None:
        logging.info(f'item {item} match is Ribs')
        return array([0, 0, 0, cost, 0, 0, 0, 0])

    elif re.match(cfg.meat_re_m05, item) is not None:
        logging.info(f'item {item} match is Sausage')
        return array([0, 0, 0, 0, cost, 0, 0, 0])

    elif re.match(cfg.meat_re_m06, item) is not None:
        logging.info(f'item {item} match is Turkey')
        return array([0, 0, 0, 0, 0, cost, 0, 0])

    else:
        logging.info(f'item {item} match is NOT a meat')
        return array([0, 0, 0, 0, 0, 0, 0, cost])


def main():

    logging.basicConfig(level=logging.INFO)

    cfg.df_main = DataFrame(columns=cfg.MAIN_COLS)

    # modify items df

    with open(cfg.ITEMS_FINAL_PICKLE_PATH, 'rb') as f:
        items = read_pickle(f)
    items.rename_axis('Date', inplace=True)
    items.reset_index(inplace=True)
    items['Date'] = items['Date'].apply(lambda x: datetime64(x, 'D'))
    items.set_index('Date', inplace=True)

    # add rows to df_main from items rows - grouped by date - into one row
    #   D01 D02 D03 D04 D05 D06 D07
    #   S01 S02 S03 S04 S05
    #   M01 M02 M03 M04 M05 M06 M07 O01

    lag_init = [0, 0, 0, 0, 0]  # 5 elements for 5 lag features
    for by_value, group_df in items.groupby(by='Date'):
        row_values = []

        weekday = group_df['WeekDay'].values[0]
        weekday_binaries = weekdays(weekday)

        row_values.extend(weekday_binaries)
        row_values.extend(lag_init)

        rows_items_costs = zeros((len(group_df), 8))  # 8 is no. of predictors
        for row_i in range(len(group_df)):
            item = group_df.iloc[row_i, cfg.items_i_col_i]
            cost = group_df.iloc[row_i, cfg.items_c_col_i]
            rows_items_costs[row_i, :] = row_items_costs(item, cost)
        costs = apply_along_axis(sum, 0, rows_items_costs)
        row_values.extend(costs.tolist())

        cfg.df_main = concat([cfg.df_main, DataFrame(dict(zip(
            cfg.MAIN_COLS, row_values)), index=[by_value])])

    # complete main by updating lag values

    cfg.df_main.sort_index(ascending=False, inplace=True)
    ix_dates = cfg.df_main.index.values
    for row_i in range(len(cfg.df_main)):
        predict_date = cfg.df_main.index[row_i]

        s01_lag_date = predict_date - DateOffset(weeks=1)
        if s01_lag_date in ix_dates:
            s01_lag_sales = cfg.df_main.loc[s01_lag_date].iloc[-8:].sum()
            cfg.df_main.iloc[row_i, 7] = s01_lag_sales

        s02_lag_date = predict_date - DateOffset(weeks=2)
        if s02_lag_date in ix_dates:
            s02_lag_sales = cfg.df_main.loc[s02_lag_date].iloc[-8:].sum()
            cfg.df_main.iloc[row_i, 8] = s02_lag_sales

        s03_lag_date = predict_date - DateOffset(weeks=3)
        if s03_lag_date in ix_dates:
            s03_lag_sales = cfg.df_main.loc[s03_lag_date].iloc[-8:].sum()
            cfg.df_main.iloc[row_i, 9] = s03_lag_sales

        s04_lag_date = predict_date - DateOffset(weeks=4)
        if s04_lag_date in ix_dates:
            s04_lag_sales = cfg.df_main.loc[s04_lag_date].iloc[-8:].sum()
            cfg.df_main.iloc[row_i, 10] = s04_lag_sales

        s05_lag_date = predict_date - DateOffset(weeks=5)
        if s05_lag_date in ix_dates:
            s05_lag_sales = cfg.df_main.loc[s05_lag_date].iloc[-8:].sum()
            cfg.df_main.iloc[row_i, 11] = s05_lag_sales

    # drop the last five weeks due ot log offset

    cfg.df_main = cfg.df_main.loc[: cfg.df_main.index[-1] + DateOffset(weeks=5)]
    cfg.df_main.to_pickle(cfg.MAIN_PICKLE_PATH)
    cfg.df_main.to_csv(cfg.MAIN_CSV_PATH)

    return 0


if __name__ == '__main__':
    sys.exit(main())
