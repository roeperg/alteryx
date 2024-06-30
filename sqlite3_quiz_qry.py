#!/python311/python

import sqlite3
import sys
import win32clipboard
import re

# get clipboard data
win32clipboard.OpenClipboard()
target = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()


conn = sqlite3.connect(r'c:\Greg\dev\dev_certification_practice.db')
c = conn.cursor()

qry = f"select qid, text from questions where family = 'Alteryx Advanced Desktop' and lower(text) like lower('%' || '{target}' || '%')"
#print(qry)

for row in c.execute(qry):
    print(row)


conn.commit();
conn.close()


