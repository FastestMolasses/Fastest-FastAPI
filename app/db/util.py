from app.db.connection import mysqlEngine


def printTables():
    tables = mysqlEngine.table_names()
    print('Tables:')
    for table in tables:
        print('-', table)
