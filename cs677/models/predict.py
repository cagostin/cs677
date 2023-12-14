import sys
import logging
import config as cfg
from models import regression


def main():

    logging.basicConfig(level=logging.INFO)
    regression.main()

    cfg.predict = cfg.model.predict(cfg.x_test)
    logging.info(f'Multi-task Lasso Regression coefficients: {cfg.predict}')

    return 0


if __name__ == '__main__':
    sys.exit(main())

