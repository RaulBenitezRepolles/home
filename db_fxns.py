import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table_compra():
	#c.execute('DROP TABLE compra')
	c.execute('CREATE TABLE IF NOT EXISTS compra(articulo TEXT,fecha TEXT, activo NUMBER)')

def add_data_compra(Artículo,now):
	c.execute('INSERT INTO compra(articulo,fecha,activo) VALUES (?,?,?)',(Artículo,now,1))
	conn.commit()

def view_active_data_compra():
	c.execute('SELECT * FROM compra WHERE activo = 1')
	data = c.fetchall()
	return data

def view_all_data_compra():
	c.execute('SELECT * FROM compra')
	data = c.fetchall()
	return data

def view_all_task_names_compra():
	c.execute('SELECT DISTINCT articulo FROM compra WHERE activo = 1')
	data = c.fetchall()
	return data
	
def deactivate_data_compra(Artículo):
	c.execute('UPDATE compra SET activo =0 WHERE articulo ="{}" and activo = 1'.format(Artículo))
	conn.commit()

	#c.execute('DELETE FROM compra WHERE articulo ="{}"'.format(Artículo))


def create_table_calendar():
	c.execute('CREATE TABLE IF NOT EXISTS calendar(evento TEXT,fecha TEXT, activo NUMBER)')

def add_data_calendar(evento,fecha):
	c.execute('INSERT INTO calendar(evento,fecha,activo) VALUES (?,?,?)',(evento,fecha,1))
	conn.commit()

def view_active_data_calendar():
	c.execute('SELECT * FROM calendar WHERE activo = 1')
	data = c.fetchall()
	return data

def view_all_data_calendar():
	c.execute('SELECT * FROM calendar')
	data = c.fetchall()
	return data

def view_all_task_names_calendar():
	c.execute('SELECT DISTINCT evento,fecha FROM calendar WHERE activo = 1')
	data = c.fetchall()
	return data
	
def deactivate_data_calendar(Artículo):
	c.execute('UPDATE calendar SET activo =0 WHERE evento ="{}" and activo = 1'.format(Artículo))
	conn.commit()



def create_table_tickets():
	c.execute('CREATE TABLE IF NOT EXISTS tickets(supermercado TEXT,fecha TEXT,Articulo TEXT,total TEXT, precio TEXT, peso TEXT, activo TEXT)')

def add_data_tickets(Supermercado,Fecha,Articulo,Total,Precio,Peso,Activo):
	c.execute('INSERT INTO tickets(supermercado,fecha,Articulo,total,precio,peso,activo) VALUES (?,?,?,?,?,?,?)',(Supermercado,Fecha,Articulo,Total,Precio,Peso,Activo))
	conn.commit()

def view_active_data_tickets():
	c.execute('SELECT * FROM tickets WHERE activo = 1')
	data = c.fetchall()
	return data

def view_all_data_tickets():
	c.execute('SELECT * FROM tickets')
	data = c.fetchall()
	return data

#def view_index_tickets(INDEX):
#	c.execute('SELECT DISTINCT 	* FROM tickets WITH(INDEX("{}"))'.format(str(INDEX)))
#	data = c.fetchall()
#	return data
	
def deactivate_data_tickets(indice,Supermercado,Fecha,Articulo,Total,Precio,Peso,Activo):
	#c.execute('UPDATE tickets SET activo =0 WITH(INDEX("{}")) and activo = 1'.format(indice))
	c.execute('INSERT INTO tickets(supermercado,fecha,Articulo,total,precio,peso,activo) VALUES (?,?,?,?,?,?,?)',(Supermercado,Fecha,Articulo,Total,Precio,Peso,Activo))
	conn.commit()