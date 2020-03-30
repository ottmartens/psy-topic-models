import pymysql
import json

db_opts = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'pubmed'
}


def getAbstracts(count = None):
    db = pymysql.connect(**db_opts)

    cur = db.cursor()

    if count:
        sql = 'SELECT abstract, pmid from articles LIMIT {}'.format(count)
    else:
        sql = 'SELECT abstract, pmid from articles'

    try:
        cur.execute(sql)
        result = cur.fetchall()
    finally:
        db.close()

    abstracts = [entry[0] for entry in result]
    ids = [entry[1] for entry in result]

    return abstracts, ids
