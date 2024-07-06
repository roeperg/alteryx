import sqlite3
conn = sqlite3.connect(r'c:\Greg\dev\dev_certification_practice.db')
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


ups = [
[347,45,'A'],[334,40,'ABC'],[309,38,'A'],[312,13,'C'],[340,30,'BC'],[344,42,'B'],
[299,27,'B'],[319,14,'BC'],[348,51,'D'],[317,1,'A'],[296,46,'A'],[349,4,'A'],[304,17,'A'],
[338,8,'AD'],[310,28,'D'],[345,43,'D'],[301,19,'D'],[332,6,'A'],[333,33,'C'],[300,39,'B'],
[307,21,'ACE'],[295,37,'C'],[313,22,'AB'],[311,9,'B'],[316,24,'C'],[303,3,'B'],[331,47,'ABC'],
[302,34,'C'],[318,25,'B'],[346,26,'ABD'],[306,29,'C'],[308,36,'A'],[315,23,'B'],[314,10,'AB'],
[337,41,'ABC'],[297,5,'ACE'],[329,16,'ABD'],[335,31,'AC'],[330,32,'A'],[343,20,'D'],[336,11,'ABC'],
[339,15,'ABC'],[298,49,'AD'],[305,2,'BC'],[328,12,'BCE'],[342,50,'B'],[350,7,'AC'],
]

for foo in ups:
	cmd = f"update questions set question_nbr = {foo[1]}, my_answer = '{foo[2]}' where qid = {foo[0]}"
	print(cmd)
	c.execute(cmd)
  

conn.commit();
conn.close()


