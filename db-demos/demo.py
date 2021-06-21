import psycopg2

connection = psycopg2.connect('dbname=temp')

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS table2;")

cursor.execute('''
  CREATE TABLE table2 (
  id SERIAL PRIMARY KEY,
  type VARCHAR NOT NULL,
  completed BOOLEAN NOT NULL DEFAULT False,
  description VARCHAR
  );
''')

cursor.execute("INSERT INTO table2 (type, completed, description) VALUES ('important', true, 'Very important task');")

cursor.execute('INSERT INTO table2 (type, completed, description) VALUES (%s, %s, %s);', ('someday', 'False', 'To do someday in life...'))

cursor.execute('INSERT INTO table2 (type, completed) VALUES (%(type)s, %(done)s);', {
    'type': 'anything',
    'done': 'False',
})

new_data = {
  'type': 'important',
  'done': False,
  'description': 'Another important task'
}

SQL = 'INSERT INTO table2 (type, completed, description) VALUES (%(type)s, %(done)s, %(description)s);'

cursor.execute(SQL, new_data)

connection.commit()

cursor.execute('select * from table2;')

result1 = cursor.fetchall()
print('result1', result1)

# result2 returns None because all results were already fetch
result2 = cursor.fetchall()
print('result2', result2)

cursor.execute('select * from table2;')
# results are filled again as a ne query is made
result3 = cursor.fetchall()

for i, val in enumerate(result3):
    print('result3', i, val)

connection.close()
cursor.close()
