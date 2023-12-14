# CONSTANTS

PROJECT_DIR = __file__.replace('/config/__init__.py', '')
ITEMS_FINAL_PICKLE_PATH = f'{PROJECT_DIR}/items/items.pickle'
ITEMS_FINAL_CSV_PATH = f'{PROJECT_DIR}/items/items.csv'
MAIN_PICKLE_PATH = f'{PROJECT_DIR}/factors/main.pickle'
MAIN_CSV_PATH = f'{PROJECT_DIR}/factors/main.csv'

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
    'Item',
    'Cost'
]
MAIN_COLS = [
    'D01',  # Sunday
    'D02',  # Monday
    'D03',  # ...
    'D04',
    'D05',
    'D06',
    'D07',   # Saturday
    'S01',  # Sales lagged by 1 week
    'S02',  # ... 2 weeks
    'S03',
    'S04',
    'S05',   # ... 5 weeks
    'M01',  # Sales of Brisket
    'M02',  # ... Pork
    'M03',  # ... Chicken
    'M04',  # ... Ribs
    'M05',  # ... Sausage
    'M06',  # ... Turkey
    'M07',  # ... Meat unknown
    'O01'   # Other not meat sales
]
PREDICT_COLS = [
    'Brisket',
    'Pork',
    'Chicken',
    'Ribs',
    'Sausage',
    'Turkey',
    'MeatOther',
    'Other'
]
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

df_main = None

meat_re_m01 = r'.*Brisket.*|.*Burnt Ends.*'
meat_re_m02 = r'.*Pork.*|.*Sloppy\sHog.*'
meat_re_m03 = r'.*Chicken.*'
meat_re_m04 = r'.*Ribs?.*'
meat_re_m05 = r'.*Sausage.*'
meat_re_m06 = r'.*Turkey.*'
meat_re_m07 = r'^Side Stacker$|^Side Stack$|^Brisork$|' \
              r'^Brisket trimmings and 2 who pork smoked shoulders$'

x_train = None
x_test = None
y_train = None
y_test = None

model = None
predict = None
mse = None
r2 = None
