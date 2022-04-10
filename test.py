from dbcm import *

config = {'host': '127.0.0.1',
          'user': 'avilio',
          'password': '******',
          'database': 'linux'}
USER = 'admi'

try:
    with UseDatabase(config) as cursor:
        print('here')
        QUERY = """select password
                    from temp
                    where email = %s"""
        cursor.execute(QUERY, (USER,))
        data = cursor.fetchone()
    print('here')
    if data:

    else:
        print('empty')
except ConnectionError as err:
    print('Is your Database on? Error:', err)
except CredentialError as err:
    print('User-id/Password issue. Error:', err)
except SQLError as err:
    print('Check your query. Error:', err)
