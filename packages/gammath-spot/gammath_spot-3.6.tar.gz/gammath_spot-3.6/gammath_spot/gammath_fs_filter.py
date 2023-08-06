# Author: Salyl Bhagwat, Gammath Works
# Copyright (c) 2021-2022, Salyl Bhagwat, Gammath Works
# All Rights Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__author__ = 'Salyl Bhagwat'
__copyright__ = 'Copyright (c) 2021-2022, Salyl Bhagwat, Gammath Works'

# THIS IS WIP: DO NOT USE
# Experimenting with backtesting framework and getting APIs to work; A lot will change later

import sys
from pathlib import Path
import pandas as pd
try:
    from gammath_spot import gammath_utils as gut
except:
    import gammath_utils as gut


#Quick experiment on basic filtering
def main():
    try:
        fs_file = sys.argv[1]
    except:
        print('ERROR: Need fundamental score file one argument to this Program.')
        raise ValueError('Missing filter file symbol')

    #Instantiate GUTILS class
    gutils = gut.GUTILS()

    path = Path('tickers')

    try:
        df = pd.read_csv(fs_file)
    except:
        print('Filter file not found')
        return

    #Aggregate all buy and sell scores
    gutils.aggregate_fs_filtered_scores(path, df)

if __name__ == '__main__':
    main()
