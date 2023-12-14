"""
takes about 2 min to complete running
"""
import sys
import re
import logging
from pandas import DataFrame, isna, notna, to_datetime, concat
import config as cfg
from items import s3csv

re_mod_name = re.compile(cfg.item_re_mod_name)
re_mod_price = re.compile(cfg.item_re_mod_price)


def texas_meet_plate(item='UNKNOWN', price='UNKNOWN', mod_line=''):
    # item_null_mod_price
    # item price is null
    # modifier_price is rollup across all modifiers
    # e.g.
    # Texas 1 Meat Plate
    #       Chicken Quarter (J3R80YK9MN6SJ) $10.00
    #       Loaded Mashed Potatoes (3S29ND8N2EPE0) $0.00
    #       Bobs Country Beans (P35411P5NFMJP) $0.00
    #           0
    #               10
    if mod_line == '':
        raise 'Modifiers is an empy string'
    if re_mod_name.match(mod_line) is not None:
        item = f'{re_mod_name.match(mod_line).groups()[0]}__combo'
    if re_mod_price.match(mod_line) is not None:
        price = re_mod_price.match(mod_line).groups()[0]
    return item, float(price)


def texas_plate(item='UNKNOWN', price='UNKNOWN', mod_line=''):
    # item_price_mod_null
    # item has price
    # individual modifiers and rollup price is null
    # e.g.
    # Texas Plate 3
    #   Brisket (F72E3W1JRJF5W) $0.00
    #   Ribs (NGEY1X1B9VS5W) $0.00
    #   Pulled Pork (NEHASBGT206K0) $0.00
    #   Creamy Smoked Mac-N-Cheese (8WPJ7YZ85K8SG) $0.00
    #   Bob’s Country Beans (EX1071770XJBE) $0.00
    #       29.24
    #           0
    if mod_line == '':
        raise 'Modifiers is an empy string'
    if re_mod_name.match(mod_line) is not None:
        item = f'{re_mod_name.match(mod_line).groups()[0]}__combo'
    return item, float(price)


def pot_bomb(item='UNKNOWN', price='UNKNOWN', mod_line=''):
    # item_price_mod_null
    # item has price
    # individual modifiers and rollup price is null
    # !! Assumes 1 meet
    # e.g.
    # Potato Bomb Bowl
    #   Angus Prime Brisket (XPBEWN7WAG41M) $0.00
    #        13.51
    #            0
    if mod_line == '':
        raise 'Modifiers is an empy string'
    if re_mod_name.match(mod_line) is not None:
        item = f'{re_mod_name.match(mod_line).groups()[0]}__p_bomb'
    return item, float(price)


def item_main(item='UNKNOWN', price='UNKNOWN'):
    # item_price_mod_null
    # item has price
    # individual modifiers and rollup price is null
    # !! Assumes no meet in modifier
    # e.g.
    # Reg Chopped Prime Angus Beef Brisket Sandwich 1/3 Lb
    #   Deli sweet pickles (KPRJEDEWQGCBW) $0.00
    #   A little sauce (J0GT697DQBGX2) $0.00
    #       14.13
    #       0
    return item, float(price)


def modifier_general(item='UNKNOWN', price='UNKNOWN', mod_line=''):
    if mod_line == '':
        raise 'Modifiers is an empy string'
    if re_mod_name.match(mod_line) is not None:
        item = f'{re_mod_name.match(mod_line).groups()[0]}'
    if re_mod_price.match(mod_line) is not None:
        price = re_mod_price.match(mod_line).groups()[0]
    return item, float(price)


def mp_bomb(item='UNKNOWN', price='UNKNOWN', mod_line=''):
    if mod_line == '':
        raise 'Modifiers is an empy string'
    if re_mod_name.match(mod_line) is not None:
        item = f'{re_mod_name.match(mod_line).groups()[0]}__mp_bomb'
    if re_mod_price.match(mod_line) is not None:
        price = re_mod_price.match(mod_line).groups()[0]
    return item, float(price)


def item_case(item_name, item_price, modifier_lines, modifier_price):
    items_prices = []
    if notna(modifier_lines):

        # case 1
        if item_price == 0.0 and modifier_price > 0.0:

            # case 1 a
            if re.match(cfg.item_re_texas_meet_plate, item_name) is not None:
                for mod_line in modifier_lines.split('\n'):
                    item, price = texas_meet_plate(mod_line=mod_line)
                    items_prices.append((item, price))
                return items_prices
            else:
                raise 'Case 1 A UNKNOWN'

        # case 2
        elif item_price > 0.0 and modifier_price == 0.0:

            # case 2 a
            if re.match(cfg.item_re_texas_plate, item_name) is not None:
                item_match = re.match(cfg.item_re_texas_plate, item_name)
                meet_count = int(item_match.groups()[1])
                if type(meet_count) != int and meet_count <= 0:
                    raise 'Meet count is not an int or is not gt than 0'
                else:
                    meet_price = item_price / meet_count  # estimated price
                for mod_line in modifier_lines.split('\n'):
                    if re.match(cfg.item_re_meet, mod_line) is not None:
                        item_price = meet_price
                    else:
                        item_price = 0
                    item, price = texas_plate(price=item_price,
                                              mod_line=mod_line)
                    items_prices.append((item, price))
                return items_prices

            # case 2 b
            elif re.match(cfg.item_re_pot_bomb, item_name) is not None:
                for mod_line in modifier_lines.split('\n'):
                    if re.match(cfg.item_re_meet, mod_line) is None:
                        item_price = 0
                    item, price = pot_bomb(price=item_price, mod_line=mod_line)
                    items_prices.append((item, price))
                return items_prices

            # case 2 c
            elif notna(item_name):  # dummy elif
                item, price = item_main(item=item_name, price=item_price)
                items_prices.append((item, price))
                return  items_prices

            else:
                raise 'Case 2 A, B or C UNKNOWN'

        # case 3
        elif item_price > 0.0 and modifier_price > 0.0:

            # case 3 a
            if re.match(cfg.item_re_texas_plate, item_name) is not None:
                item_match = re.match(cfg.item_re_texas_plate, item_name)
                meet_count = int(item_match.groups()[1])
                if type(meet_count) != int and meet_count <= 0:
                    raise 'Meet count is not an int or is not gt than 0'
                else:
                    meet_price = item_price / meet_count  # estimated price
                for mod_line in modifier_lines.split('\n'):
                    if re.match('Additional', mod_line):
                        item, price = modifier_general(mod_line=mod_line)
                        items_prices.append((item, price))
                    else:
                        if re.match(cfg.item_re_meet, mod_line) is not None:
                            item_price = meet_price
                        else:
                            item_price = 0
                        item, price = texas_plate(price=item_price,
                                                  mod_line=mod_line)
                        items_prices.append((item, price))
                return items_prices

            # case 3 b
            elif re.match(cfg.item_re_mac_pot_bomb, item_name) is not None:
                items_prices.append((item_name, item_price))
                for mod_line in modifier_lines.split('\n'):
                    item, price = mp_bomb(mod_line=mod_line)
                    items_prices.append((item, price))
                return items_prices

            # case 3 c
            elif notna(item_name):  # dummy elif
                items_prices.append((item_name, item_price))
                for mod_line in modifier_lines.split('\n'):
                    item, price = modifier_general(mod_line=mod_line)
                    items_prices.append((item, price))
                return items_prices

            else:
                raise 'Case 3 A, B or C UNKNOWN'

    # case 4
    elif isna(modifier_lines):
        items_prices.append((item_name, item_price))
        return items_prices

    else:
        raise 'Case 1, 2, 3 or 4 UNKNOWN'


def date_day_time(dt: str):
    logging.info(f'converting datetime: {dt}')
    dt_ts = to_datetime(dt[:-4], format='%d-%b-%Y %I:%M %p')
    logging.info(f'converted to: {dt_ts}')
    return dt_ts, dt_ts.year, dt_ts.month, int(dt_ts.strftime('%d')), \
        int(dt_ts.strftime('%w')), int(dt_ts.strftime('%H'))


def main():

    logging.basicConfig(level=logging.INFO)

    s3csv.main()
    logging.info(f'items_csv summary: {cfg.items_csv.info()}')

    cfg.items = DataFrame()
    for row_i in range(len(cfg.items_csv)):

        dt_str = cfg.items_csv.iloc[row_i, cfg.items_csv_dt_col_i]
        dt, year, month, mday, wday, hr = date_day_time(dt=dt_str)

        items_costs = item_case(
            item_name=cfg.items_csv.iloc[row_i, cfg.items_csv_in_col_i],
            item_price=cfg.items_csv.iloc[row_i, cfg.items_csv_ic_col_i],
            modifier_lines=cfg.items_csv.iloc[row_i, cfg.items_csv_mod_col_i],
            modifier_price=cfg.items_csv.iloc[row_i, cfg.items_csv_mc_col_i]
        )

        for ic in items_costs:
            item_data = [year, month, mday, wday, hr, ic[0], ic[1]]
            logging.info(f'adding item data with date: {dt} | {item_data}')
            item_dict = dict(zip(cfg.ITEMS_COLS, item_data))
            cfg.items = concat([cfg.items, DataFrame(item_dict, index=[dt])])

    cfg.items.to_pickle(cfg.ITEMS_FINAL_PICKLE_PATH)
    cfg.items.to_csv(cfg.ITEMS_FINAL_CSV_PATH)

    return 0


if __name__ == '__main__':
    sys.exit(main())


