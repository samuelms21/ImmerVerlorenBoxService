from locker.ui import LockerUI
from locker.dto import *
import argparse
from kink import di

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dbinit')
    args = parser.parse_args()
    dbinit = args.dbinit

    di.clear_cache()

    di["db_name"] = r"locker/immer_verloren.db"
    di["_dbinit"] = dbinit[7:]

    ui = LockerUI()
    ui.run()



