import sqlite3
import hashlib
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()


def create_table_users():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,userhash TEXT)')

def add_data_users(username, password):
    c.execute('INSERT INTO usertable(username,userhash) VALUES (?,?)',(username, hashlib.sha256(str.encode(password)).hexdigest()))
    conn.commit()

def view_active_username(username, userhash):
	c.execute('SELECT Count(username) FROM usertable WHERE username = "{}" and userhash = "{}" '.format(username,userhash))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT username FROM usertable')
	data = c.fetchall()
	return data

def delete_users(username):
	c.execute('DELETE FROM usertable WHERE username = "{}"'.format(username))
	conn.commit()


def create_table_compra():
	#c.execute('DROP TABLE compra')
	c.execute('CREATE TABLE IF NOT EXISTS compra(Artículo TEXT, Descripción TEXT, Número NUMBER, Inscripción_Fecha TEXT, Inscripción_User TEXT, Modificación_Fecha TEXT, Modificación_User Text, Activo NUMBER)')   
	
def add_data_compra(Artículo,Descripción,Número,now,user):
	c.execute('INSERT INTO compra(Artículo,Descripción,Número,Inscripción_Fecha,Inscripción_User,Modificación_Fecha,Modificación_User,Activo) VALUES (?,?,?,?,?,?,?,?)',(Artículo,Descripción,Número,now,user,now,user,1))
	conn.commit()

def view_active_data_compra():
	c.execute('SELECT Distinct Artículo,Descripción,Número FROM compra WHERE Activo = 1')
	data = c.fetchall()
	return data

def view_all_data_compra():
	c.execute('SELECT * FROM compra')
	data = c.fetchall()
	return data

#def view_all_task_names_compra():
#	c.execute('SELECT DISTINCT Artículo,Descripción,Número FROM compra WHERE Activo = 1')
#	data = c.fetchall()
#	return data
	
def deactivate_data_compra(Artículo,Descripción,Número,now,user):
	c.execute('UPDATE compra SET Activo =0 , Modificación_Fecha = "{}" , Modificación_User= "{}" WHERE Artículo ="{}" and Descripción = "{}" and Número = "{}" and Activo = 1'.format(now,user,Artículo,Descripción,Número))
	conn.commit()

def view_all_deleted_task_names_compra():
	c.execute('SELECT DISTINCT Artículo,Descripción,Número FROM compra WHERE Activo = 0 Order by Inscripción_Fecha desc')
	data = c.fetchall()
	return data
	
def reactivate_data_compra(Artículo,Descripción,Número,now,user):
	c.execute('UPDATE compra SET Activo =-1 WHERE Artículo ="{}" and Descripción = "{}" and Número = "{}" and Activo = 0'.format(Artículo,Descripción,Número))
	c.execute('INSERT INTO compra(Artículo,Descripción,Número,Inscripción_Fecha,Inscripción_User,Modificación_Fecha,Modificación_User,Activo) VALUES (?,?,?,?,?,?,?,?)',(Artículo,Descripción,Número,now,user,now,user,1))
	conn.commit()

	#c.execute('DELETE FROM compra WHERE articulo ="{}"'.format(Artículo))


def create_table_calendar():
	c.execute('CREATE TABLE IF NOT EXISTS calendar(evento TEXT, Comentarios TEXT, fecha TEXT, Inscripción_Fecha TEXT, Inscripción_User TEXT, Inscripción_ID_Actualizada TEXT, Activo NUMBER)')

def add_data_calendar(Evento,Comentarios,Fecha,now,user):
	c.execute('INSERT INTO calendar(evento,Comentarios,fecha,Inscripción_Fecha,Inscripción_User,Inscripción_ID_Actualizada,Activo) VALUES (?,?,?,?,?,?,?)',(Evento,Comentarios,Fecha,now,user,-1,1))
	conn.commit()

def view_active_data_calendar():
	c.execute('SELECT * FROM calendar WHERE Activo = 1  Order by fecha asc')
	data = c.fetchall()
	return data

def view_all_data_calendar():
	c.execute('SELECT * FROM calendar')
	data = c.fetchall()
	return data

def view_all_task_names_calendar():
	c.execute('SELECT DISTINCT evento,Comentarios,fecha FROM calendar WHERE Activo = 1 Order by fecha desc')
	data = c.fetchall()
	return data
	
def deactivate_data_calendar(evento,Comentarios,fecha):
	c.execute('UPDATE calendar SET Activo =0 WHERE evento ="{}" and Comentarios ="{}" and fecha ="{}" and Activo = 1'.format(evento,Comentarios,fecha))
	conn.commit()

def view_all_deleted_task_names_calendar():
	c.execute('SELECT DISTINCT evento,Comentarios,fecha FROM calendar WHERE Activo = 0 Order by fecha desc')
	data = c.fetchall()
	return data
	
def reactivate_data_calendar(evento,Comentarios,fecha):
	c.execute('UPDATE calendar SET Activo =1 WHERE evento ="{}" and Comentarios ="{}" and fecha ="{}" and Activo = 0'.format(evento,Comentarios,fecha))
	conn.commit()



def create_table(table,fields_type):
	c.execute('DROP TABLE compra')
	c.execute('CREATE TABLE IF NOT EXISTS "{}"("{}")'.format(table,fields_type))   
	
def add_data(table,fields_add,values_add):
	c.execute('INSERT INTO {} ({}) VALUES ({})'.format(table,fields_add,values_add))
	conn.commit()

def view_active_data(table,fields):
	c.execute('SELECT Distinct * FROM "{}" '.format(table))#WHERE Activo = 1          "{}" FROM "{}" '.format(fields,table))
	data = c.fetchall()
	return data

#def deactivate_data(Artículo,Descripción,Número,now,user):
#	c.execute('UPDATE compra SET Activo =0 , Modificación_Fecha = "{}" , Modificación_User= "{}" WHERE Artículo ="{}" and Descripción = "{}" and Número = "{}" and Activo = 1'.format(now,user,Artículo,Descripción,Número))
#	conn.commit()

#def view_deactive_data():
#	c.execute('SELECT Distinct Artículo,Descripción,Número FROM compra WHERE Activo = 1')
#	data = c.fetchall()
#	return data
#
#def reactivate_data(Artículo,Descripción,Número,now,user):
#	c.execute('UPDATE compra SET Activo =-1 WHERE Artículo ="{}" and Descripción = "{}" and Número = "{}" and Activo = 0'.format(Artículo,Descripción,Número))
#	c.execute('INSERT INTO compra(Artículo,Descripción,Número,Inscripción_Fecha,Inscripción_User,Modificación_Fecha,Modificación_User,Activo) VALUES (?,?,?,?,?,?,?,?)',(Artículo,Descripción,Número,now,user,now,user,1))
#	conn.commit()
#
#def view_all_data():
#	c.execute('SELECT * FROM compra')
#	data = c.fetchall()
#	return data
	

	
