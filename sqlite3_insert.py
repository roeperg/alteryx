import sqlite3
conn = sqlite3.connect(r'c:\Greg\SQLite\greg_roeper.db')
c = conn.cursor()

print('Lavastorm Desktop','Programming','QuickBase')

queries = [
"""insert into experiences ('EXP_ID','LINE_NO','DESCRIPTION') values
(16,6,'Created and maintained numerous QuickBase databases for agent attendence and performance tracking.'),
(17,5,'Built a fully functional Python package to interact directly with the QuickBase API via REST.'),
(18,7,'Developed solutions to ensure that external QuickBooks Solution Providers (QSP) are correctly paid using Alteryx workflows, Python API scripts, and customer facing production QuickBase databases.  Also automated hourly data cleanup of the QSP QuickBase.'),
(18,8,'Built and maintained ETL processes to populate Spark Hive data lake from production QuickBase databases.')
""",
"""insert into skills ('LABEL','YEARS','SQL','ETL','ANALYST','ENGINEER','BI','SNOWFLAKE','METHOD','DEVELOPER','CLOUD','ORACLE','QUICKBASE','SCHEDULING','GIT','LEADERSHIP'
                     ,'IMAGING_3D')  values
  ('QuickBase/QuickBase API',15,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0)""",                                                                                                                                  
]

print(queries[1])

for row in c.execute(queries[1]):
    print(row)


conn.commit();
conn.close()


