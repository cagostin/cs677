#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 18:00:00 2023

@author: Christopher Agostini
"""
import sys
import config as cfg
from results import analysis


def main():

    analysis.main()

    return 0


if __name__ == '__main__':
    sys.exit(main())

