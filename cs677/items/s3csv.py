import sys
from pandas import read_csv
from cs677 import config as cfg


def main():

    cfg.items_csv = read_csv(cfg.ITEMS_CSV_PATH, low_memory=False)
    cfg.items_csv.drop(cfg.ITEMS_CSV_COLS_DROP, axis=1, inplace=True)
    cfg.items_csv['Item Revenue'] = cfg.items_csv['Item Revenue'].fillna(0.0)
    cfg.items_csv['Modifiers Revenue'] = cfg.items_csv['Modifiers Revenue'].\
        fillna(0.0)

    cfg.items_csv_dt_col_i = cfg.items_csv.columns.get_loc('Line Item Date')
    cfg.items_csv_in_col_i = cfg.items_csv.columns.get_loc('Item Name')
    cfg.items_csv_mod_col_i = cfg.items_csv.columns.get_loc('Modifiers')
    cfg.items_csv_ic_col_i = cfg.items_csv.columns.get_loc('Item Revenue')
    cfg.items_csv_mc_col_i = cfg.items_csv.columns.get_loc('Modifiers Revenue')

    return 0


if __name__ == '__main__':
    sys.exit(main())

