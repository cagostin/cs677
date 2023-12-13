# CONSTANTS

PROJECT_DIR = __file__.replace('/config/__init__.py', '')
S3 = 's3://agsc-cs677-final-project/'
ITEMS_CSV_PATH = f'{S3}items.csv'
ITEMS_CSV_COLS = [
    'Line Item Date',       # date
    'Item Name',            # unique name for an item
    'Modifiers',            # text block of additional items with id and price
    'Item Revenue',         # base cost for order based on item
    'Modifiers Revenue',    # total cost of modifiers
    'Order Discount Proportion',  # monetary value of discount
    'Tax Amount'             # total tax
]
ITEMS_CSV_COLS_DROP = [
    'Order ID',             # unique identifier for all items in the same order
    'Item ID',              # unique identifier for an item
    'Item Product Code',    # empty
    'Item SKU',             # empty
    'Currency',             # USD
    'Per Unit Quantity',    # empty
    'Item Unit',            # empty
    'Total Revenue',        # base cost + modifier cost
    'Discounts',            # empty
    'Total Discount',       # always 0
    'Order Discounts',      # text display of discount type
    'Item Total',           # total revenue less discount
    'Item Tax Rate',        # fractional tax on item as decimal
    'Item Fee',             # always 0
    'Item Total with Tax/Fee Amount',  # item total plus tax
    'Refunded',             # assume all sales final
    'Exchanged',            # assume all sales final
    'Order Payment State'   # assume all sales paid
]
ITEMS_COLS = [
    'Year',
    'Month',
    'MonthDay',
    'WeekDay',
    'Hour',
    'Name',
    'Item',
    'Cost'
]
ITEMS_FINAL_PICKLE_PATH = f'{PROJECT_DIR}/items/items.pickle'
ITEMS_FINAL_CSV_PATH = f'{PROJECT_DIR}/items/items.csv'

# GLOBAL VARS

items_csv = None
items_csv_dt_col_i = None
items_csv_in_col_i = None
items_csv_mod_col_i = None
items_csv_ic_col_i = None
items_csv_mc_col_i = None

items = None
items_y_col_i = ITEMS_COLS.index('Year')
items_m_col_i = ITEMS_COLS.index('Month')
items_md_col_i = ITEMS_COLS.index('MonthDay')
items_wd_col_i = ITEMS_COLS.index('WeekDay')
items_h_col_i = ITEMS_COLS.index('Hour')
items_i_col_i = ITEMS_COLS.index('Item')
items_c_col_i = ITEMS_COLS.index('Cost')

item_re_texas_meet_plate = r'^Texas \d Meat Plate$'
item_re_mod_name = r'(\A[a-zA-Z]+[^(]+\b).*'
item_re_mod_price = r'.*[$](\d+\.\d{2}$)'
item_re_texas_plate = r'\ATexas\s(Big-|Mini-|\s)Plate\s(\d)$'
item_re_pot_bomb = r'\APotato Bomb Bowl$'
item_re_meet = r'Rib|Pulled|Sausage|Brisket|Chicken|Beef|Burnt|Moist'
item_re_mac_pot_bomb = r'^Build a Bowl, Mac Bowl or Potato Bomb Bowl$'

items_pickle = None
