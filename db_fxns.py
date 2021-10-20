import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table_compra():
	#c.execute('DROP TABLE compra')
	c.execute('CREATE TABLE IF NOT EXISTS compra(Artículo TEXT, Descripción TEXT, Inscripción_Fecha TEXT, Inscripción_User TEXT, Inscripción_ID_Actualizada TEXT, Activo NUMBER)')   
	
def add_data_compra(Artículo,Descripción,now,user):
	c.execute('INSERT INTO compra(Artículo,Descripción,Inscripción_Fecha,Inscripción_User,Inscripción_ID_Actualizada,Activo) VALUES (?,?,?,?,?,?)',(Artículo,Descripción,now,user,-1,1))
	conn.commit()

def view_active_data_compra():
	c.execute('SELECT * FROM compra WHERE Activo = 1')
	data = c.fetchall()
	return data

def view_all_data_compra():
	c.execute('SELECT * FROM compra')
	data = c.fetchall()
	return data

def view_all_task_names_compra():
	c.execute('SELECT DISTINCT Artículo,Descripción FROM compra WHERE Activo = 1')
	data = c.fetchall()
	return data
	
def deactivate_data_compra(Artículo,Descripción):
	c.execute('UPDATE compra SET Activo =0 WHERE Artículo ="{}" and Descripción = "{}" and Activo = 1'.format(Artículo,Descripción))
	conn.commit()

def view_all_deleted_task_names_compra():
	c.execute('SELECT DISTINCT Artículo,Descripción FROM compra WHERE Activo = 0')
	data = c.fetchall()
	return data
	
def reactivate_data_compra(Artículo,Descripción):
	c.execute('UPDATE compra SET Activo =1 WHERE Artículo ="{}" and Descripción = "{}" and Activo = 0'.format(Artículo,Descripción))
	conn.commit()

	#c.execute('DELETE FROM compra WHERE articulo ="{}"'.format(Artículo))


def create_table_calendar():
	c.execute('CREATE TABLE IF NOT EXISTS calendar(evento TEXT, Comentarios TEXT, fecha TEXT, Inscripción_Fecha TEXT, Inscripción_User TEXT, Inscripción_ID_Actualizada TEXT, Activo NUMBER)')

def add_data_calendar(Evento,Comentarios,Fecha,now,user):
	c.execute('INSERT INTO calendar(evento,Comentarios,fecha,Inscripción_Fecha,Inscripción_User,Inscripción_ID_Actualizada,Activo) VALUES (?,?,?,?,?,?,?)',(Evento,Comentarios,Fecha,now,user,-1,1))
	conn.commit()

def view_active_data_calendar():
	c.execute('SELECT * FROM calendar WHERE Activo = 1')
	data = c.fetchall()
	return data

def view_all_data_calendar():
	c.execute('SELECT * FROM calendar')
	data = c.fetchall()
	return data

def view_all_task_names_calendar():
	c.execute('SELECT DISTINCT evento,Comentarios,fecha FROM calendar WHERE Activo = 1')
	data = c.fetchall()
	return data
	
def deactivate_data_calendar(evento,Comentarios,fecha):
	c.execute('UPDATE calendar SET Activo =0 WHERE evento ="{}" and Comentarios ="{}" and fecha ="{}" and Activo = 1'.format(evento,Comentarios,fecha))
	conn.commit()

def view_all_deleted_task_names_calendar():
	c.execute('SELECT DISTINCT evento,Comentarios,fecha FROM calendar WHERE Activo = 0')
	data = c.fetchall()
	return data
	
def reactivate_data_calendar(evento,Comentarios,fecha):
	c.execute('UPDATE calendar SET Activo =1 WHERE evento ="{}" and Comentarios ="{}" and fecha ="{}" and Activo = 0'.format(evento,Comentarios,fecha))
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