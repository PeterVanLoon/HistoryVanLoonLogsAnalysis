#!/usr/bin/env python
# Logs Analysis program.  Building it off my old tournament program
#

import psycopg2

# def connect():
"""Connect to the PostgreSQL database.  Returns a database connection."""
conn = psycopg2.connect("dbname = news")
c = conn.cursor()
c.execute("SELECT title, name FROM articles join authors \
on articles.author = authors.id order by authors.id")
authorCount = c.fetchall()
print
# print ("This is a list of articles ordered by the author's name")
# print ("I print this every time because I know I am \
# connected to the database")
# print ("this still works, but I commented out the print statement")
print('First Query - What are the top three articles by number of views?')
print
c.execute(
    "select title, count(*) as query1 from articles inner join \
    log on concat('/article/', articles.slug) = log.path group by \
    log.path, articles.title order by query1 desc limit 3"
    )
pathone = c.fetchall()
# print pathone
print "1.", pathone[0], ""
print "2.", pathone[1], ""
print "3.", pathone[2], ""
print
print('Second Query - Who are the most popular article authors?')
print
print
c.execute("select authors.name, count(*) as query2 \
from articles inner join authors on \
articles.author = authors.id inner join log \
on concat('/article/', articles.slug) = log.path \
group by authors.name order by query2 desc limit 4")
pathtwo = c.fetchall()
print "1.", pathtwo[0], ""
print "2.", pathtwo[1], ""
print "3.", pathtwo[2], ""
print "4.", pathtwo[3], ""
print
print('Third Query - 1) What are  the days in the database log \
where the ERROR RATE is greater than 1%?')
month = input("What is the Month to start the analysis - Use its number?")
year = input("What year?")
days = input("How many days should the report run?")

c.execute("select date(time) as day from log group by day")
paththree = c.fetchall()
# print paththree
# print ('Third Query - How many views per day?')
# print
c.execute("select date(time) as day, count (*) \
as views from log group by day order by day asc")
pathfour = c.fetchall()
# print "Pathfour"
# rint pathfour
# rint ('Third Query - How many errors per day?')
# print
c.execute("select date(time) as day, count (*) \
as views from log where status = '404 NOT FOUND' \
group by day order by day asc")
pathfive = c.fetchall()
# print "Pathfive"
# print pathfive

# This takes each day's count of views and puts it into a list
views_per_day = []
report_days = 0
while report_days < days:
    pathsix = pathfour[report_days]
    views_per_day.append(float(pathsix[1]))
    report_days += 1
print
# print('This is the list of views_per_day')
# print(views_per_day)
# This takes each days errors and puts it into a list
errors_per_day = []
report_days = 0
while report_days < days:
    pathseven = pathfive[report_days]
    errors_per_day.append(float(pathseven[1]))
# print pathsix
    report_days += 1

print
# print('This is the list of errors_per_day')
# print type(errors_per_day)
# print(errors_per_day)

error_percent_per_day = []
report_days = 0
while report_days < days:
    error_rate_per_day = (100*float(((
     (errors_per_day[report_days])/(views_per_day[report_days])))))
# print type(error_rate_per_day)
    if error_rate_per_day >= 1:
        print
        print "For : ", month, "/", \
            report_days+1, "/", year, "the error rate is",\
            round(error_rate_per_day, 3), "%, and is GREATER THAN ONE PERCENT"
        print
    else:
        print "For : ", month, "/", report_days+1, "/", year, \
            "the error rate is", round(error_rate_per_day, 3), \
            "%, and is unremarkable"
    # print errors_per_day[july_day]
    # print type(errors_per_day[july_day])
    # print views_per_day[july_day]
    # print type(views_per_day[july_day])
    # ratio =(float((((errors_per_day[july_day])/(views_per_day[july_day])))))
    error_percent_per_day.append(error_rate_per_day)
    report_days += 1

# print (error_percent_per_day)
# print type(error_percent_per_day)

conn.close()
