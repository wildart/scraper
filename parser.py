import sys
import json
import re
import pandas as pd
from typing import Dict

COLS = {1: 'name', 2: 'address_1', 3: 'address_2', 4: 'phone', 5: 'fax', 6: 'e-mail',
        7: 'web_site', 8: 'primary_contact', 9: 'primary_contact_url', 10: 'misc'}


def parse_record(rec: list):
    res = {'primary_contact_url': rec[-1]}  # type: Dict[str, str]
    rec = rec[:-1]
    tidx = 7
    while True:
        if tidx == 0:
            res[COLS[1]] = rec[-1]
            break
        col = COLS[tidx]
        if col.replace("_", " ") in rec[-1].lower():
            res[col] = rec[-1][len(col) + 2:]
            rec = rec[:-1]
        elif tidx in (2, 3) and len(rec) > 2:
            res[col] = rec[-1]
            rec = rec[:-1]
        elif tidx == 1:
            if len(rec) == 2:
                res[COLS[8]] = rec[-1]
            elif len(rec) == 3:
                misc = rec[1]
                if any(re.match('[A-Z]{3,4}', s) is None for s in misc.split(' ')):
                    res[COLS[2]] = rec[-1] + ' ' + res[COLS[2]]
                else:
                    res[COLS[10]] = misc
                    del rec[1]
                    continue
                tidx += 1
            rec = rec[:-1]
        tidx -= 1
    return res


# load from json
datafile = sys.argv[1] + '.json'
with open(datafile, 'r') as io:
    data = json.load(io)

# save in table
df = pd.DataFrame((parse_record(rec) for rec in data), columns=COLS.values())
df.to_csv(sys.argv[1] + '.tsv', sep='\t')
