import sys
import logging
import cs677.config as cfg
from cs677.models import predict
from sklearn.metrics import mean_squared_error, r2_score


def main():

    logging.basicConfig(level=logging.INFO)

    if cfg.predict is None:
        predict.main()

    cfg.mse = mean_squared_error(cfg.y_test, cfg.predict, multioutput='raw_values')
    logging.info(f'Mean Squared Error: {cfg.mse}')

    cfg.r2 = r2_score(cfg.y_test, cfg.predict, multioutput='raw_values')
    logging.info(f'Coefficient of Determination: {cfg.r2}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
