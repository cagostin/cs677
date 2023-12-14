import sys
import logging
import cs677.config as cfg
from cs677.models import split
from sklearn import linear_model


def main():

    logging.basicConfig(level=logging.INFO)
    split.main()

    cfg.model = linear_model.MultiTaskLasso(max_iter=10000)
    cfg.model.fit(cfg.x_train, cfg.y_train)
    logging.info(f'Multi-task Lasso Regression coefficients: {cfg.model.coef_}')

    return 0


if __name__ == '__main__':
    sys.exit(main())

