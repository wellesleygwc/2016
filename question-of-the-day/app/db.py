import sqlite3

database_file = "static/example.db"

def create_db():
    # All your initialization code
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    
    # Create a table and add a record to it
    cursor.execute("create table if not exists users(username text primary key not null, password text not null, email text not null, total_answers int not null, right_answers int not null)")
    cursor.execute("insert or ignore into users values ('admin', 'admin', 'admin@gwc.com', 10, 5 )")

    # Save (commit) the changes
    connection.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    connection.close()

def check_password(username, password):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    
    # Try to retrieve a record from the users table that matches the username and password
    cursor.execute("select * from users where username='%s' and password='%s'" % (username, password))
    rows = cursor.fetchall()

    connection.close()
    
    return len(rows) > 0

def get_email(username):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Try to retrieve a record from the users table that matches the username and password
    cursor.execute("select email from users where username='%s'" % (username))
    row = cursor.fetchone()

    connection.close()

    return row[0]

def get_total_answers(username):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Try to retrieve a record from the users table that matches the username and password
    cursor.execute("select total_answers from users where username='%s'" % (username))
    row = cursor.fetchone()

    connection.close()

    return row[0]

def get_right_answers(username):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Try to retrieve a record from the users table that matches the username and password
    cursor.execute("select right_answers from users where username='%s'" % (username))
    row = cursor.fetchone()

    connection.close()

    return row[0]
