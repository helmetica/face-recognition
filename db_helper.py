import psycopg2

# подключение к БД
conn = psycopg2.connect(dbname='FRDB', user='postgres', password='qwerty', host='localhost')
cursor = conn.cursor()

# получение списка событий
def get_events():
    cursor.execute('''SELECT ev.event_id, ev.datetime, cam.camera_name, f.name, f.lastname, f.fathername, f.photo_path 
                        FROM events ev
                        JOIN faces f ON ev.face_id=f.face_id
                        JOIN cameras cam ON ev.camera_id=cam.camera_id''')
    events = cursor.fetchall()
    events_full = []
    
    for (event_id, datetime, camera, name, lastname, fathername, photo_path) in events:
        event = {}
        event['event_id'] = event_id
        event['datetime'] = datetime
        event['camera'] = camera
        event['name'] = name
        event['lastname'] = lastname
        event['fathername'] = fathername
        event['photo_path'] = photo_path
        events_full.append(event)

    return events_full

# получение данных из таблицы faces
# мб передан id
def get_faces(id):
    query = 'SELECT face_id, name, lastname, fathername, group_id, photo_path FROM faces'
    if id is not None:
        query += 'WHERE face_id={0}'.format(id)
        
    cursor.execute(query)
    faces = cursor.fetchall()
    faces_full = []

    for (face_id, name, lastname, fathername, group_id, photo_path) in faces:
        face = {}
        face['face_id'] = face_id
        face['name'] = name
        face['lastname'] = lastname
        face['fathername'] = fathername
        face['group_id'] = group_id
        face['photo_path'] = photo_path
        faces_full.append(face)

    return faces_full