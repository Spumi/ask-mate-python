import connection


@connection.connection_handler
def test_connection(cursor):
    print('ok')


if __name__ == '__main__':
    test_connection()
