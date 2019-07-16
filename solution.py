#!/usr/bin/env python

import psycopg2

DBase = "news"


def queries():
    db = psycopg2.connect(database=DBase)
    cursor = db.cursor()

    # 1. What are the most popular three articles of all time?
    # Which articles have been accessed the most?
    # Present this information as a sorted list with
    # the most popular article at the top.

    # get paths with most visits
    cursor.execute('''
                create view most_visits_path as
                select path,
                count(path) as visits from log
                where path like '/article/%'
                group by path
                order by visits desc;
                    ''')
    # link the paths to slugs of table articles
    cursor.execute('''
                     create view most_visits_title as
                     select a.author,
                     a.title,
                     m.visits from articles as
                     a,most_visits_path as m
                     where a.slug = substr(m.path,10);
                    ''')
    # get the first 3 top viewed articles
    cursor.execute('''
                     select title,visits from most_visits_title limit 3;
                            ''')
    result = cursor.fetchall()

    print("\n \n")

    for i in range(len(result)):
        print(''' "%s" - %d views''' % (result[i][0], result[i][1]))

    print("\n \n")

    # 2. Who are the most popular article authors of all time?
    # That is, when you sum up all of the articles each author has written,
    # which authors get the most page views? Present this as a sorted list with
    # the most popular author at the top.

    # creating view to store author id and most views
    cursor.execute('''  create view authors_view as select author as id,
                        sum(visits) from most_visits_title
                        group by author;
                    ''')

    # linking author id with author name and most views
    cursor.execute('''  select au.name , av.sum from authors as au,
                        authors_view as av where au.id = av.id
                        order by sum desc;
                    ''')

    result = cursor.fetchall()
    for i in range(len(result)):
        print(''' %s - %d views''' % (result[i][0], result[i][1]))

    print("\n \n")

    # 3. On which days did more than 1% of requests lead to errors?
    # The log table includes a column status that indicates the HTTP
    # status code that the news site sent to the user's browser.

    # creating view to store date and total number of requests on that date
    cursor.execute('''  create view totalRequests as select date(time) as date,
                        count(*) as total_requests from log
                        group by date;
                    ''')

    # creating view to store date and no. of requests on that date
    cursor.execute('''  create view errorRequests as select date(time) as date,
                        count(*) as total_requests from log
                        where status not like '200%'
                        group by date;
                    ''')

    # creating view to store date and percentage of error requests on that date
    cursor.execute('''  create view errorPercentage as
                        select to_char(a.date :: DATE, 'Mon dd, yyyy') as date,
                        round((b.total_requests * 100)::numeric
                        /a.total_requests,3) as percentage
                        from totalRequests as a, errorRequests as b
                        where a.date = b.date;
                    ''')

    cursor.execute('''
                        select date,
                        percentage from errorPercentage
                        where percentage > 1;
                    ''')

    result = cursor.fetchall()
    for i in range(len(result)):
        print(''' %s - %f%% errors''' % (result[i][0], round(result[i][1], 3)))
    print("\n \n")

    db.close()


queries()
