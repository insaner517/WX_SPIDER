if __name__ == '__main__':
    # Connect to a MySQL database on network.
    mysql_db = MySQLDatabase('my_app', user='app', password='db_password',
                             host='10.1.0.8', port=3316)