import sys
import logging
import os
import config as cfg
from factors import postprocess
from pandas import read_pickle
from sklearn.model_selection import train_test_split


def main():

    logging.basicConfig(level=logging.INFO)

    if not os.path.isfile(cfg.MAIN_PICKLE_PATH):
        postprocess.main()
    with open(cfg.MAIN_PICKLE_PATH, 'rb') as f:
        main_df = read_pickle(f)

    cfg.x_train, cfg.x_test, cfg.y_train, cfg.y_test = train_test_split(
        main_df.iloc[:, :12], main_df.iloc[:, 12:], test_size=0.2,
        random_state=0)
    logging.info(f'x_train: {cfg.x_train}')
    logging.info(f'x_test: {cfg.x_test}')
    logging.info(f'y_train: {cfg.y_train}')
    logging.info(f'y_test: {cfg.y_test}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
