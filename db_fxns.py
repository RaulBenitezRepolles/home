import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()



def create_table_compra():
	c.execute('CREATE TABLE IF NOT EXISTS compra(articulo TEXT,fecha TEXT)')

def add_data_compra(Artículo,now):
	c.execute('INSERT INTO compra(articulo,fecha) VALUES (?,?)',(Artículo,now))
	conn.commit()

def view_all_data_compra():
	c.execute('SELECT * FROM compra')
	data = c.fetchall()
	return data

def view_all_task_names_compra():
	c.execute('SELECT DISTINCT articulo FROM compra')
	data = c.fetchall()
	return data
	
def delete_data_compra(Artículo):
	c.execute('DELETE FROM compra WHERE articulo ="{}"'.format(Artículo))
	conn.commit()


def create_table_calendar():
	c.execute('CREATE TABLE IF NOT EXISTS calendar(evento TEXT,fecha TEXT)')

def add_data_calendar(evento,fecha):
	c.execute('INSERT INTO calendar(evento,fecha) VALUES (?,?)',(evento,fecha))
	conn.commit()

def view_all_data_calendar():
	c.execute('SELECT * FROM calendar')
	data = c.fetchall()
	return data

def view_all_task_names_calendar():
	c.execute('SELECT DISTINCT evento,fecha FROM calendar')
	data = c.fetchall()
	return data
	
def delete_data_calendar(Artículo):
	c.execute('DELETE FROM calendar WHERE evento ="{}"'.format(Artículo))
	conn.commit()

