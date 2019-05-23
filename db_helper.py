import psycopg2

# получение списка событий
def get_events():
    # подключение к БД
    conn = psycopg2.connect(dbname='FRDB', user='postgres', password='qwerty', host='localhost')
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

    return events_full

# очистка списка событий
def clear_events():
    conn = psycopg2.connect(dbname='FRDB', user='postgres', password='qwerty', host='localhost')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM events')  
    conn.commit()

    cursor.close()
    conn.close()

def get_cameras(id=None):
    # подключение к БД
    conn = psycopg2.connect(dbname='FRDB', user='postgres', password='qwerty', host='localhost')
    cursor = conn.cursor()

    query = '''SELECT camera_id, index, camera_name, camera_description 
                FROM cameras'''

    if id is not None:
        query += ' WHERE camera_id={0}'.format(id)

    cursor.execute(query)
    cameras = cursor.fetchall()
    cameras_full = []
    
    for (id, index, name, description) in cameras:
        cam = {}
        cam['id'] = id
        cam['index'] = index
        cam['name'] = name
        cam['description'] = description
        cameras_full.append(cam)

    cursor.close()
    conn.close()

    return cameras_full

# получение данных из таблицы faces
# мб передан id
def get_faces(id=None):
    # подключение к БД
    conn = psycopg2.connect(dbname='FRDB', user='postgres', password='qwerty', host='localhost')
    cursor = conn.cursor()

    query = 'SELECT face_id, name, lastname, fathername, group_id, photo_path, last_detection FROM faces'
    if id is not None:
        query += ' WHERE face_id={0}'.format(id)
        
    cursor.execute(query)
    faces = cursor.fetchall()
    faces_full = []

    for (face_id, name, lastname, fathername, group_id, photo_path, last_detection) in faces:
        face = {}
        face['face_id'] = face_id
        face['name'] = name
        face['lastname'] = lastname
        face['fathername'] = fathername
        face['group_id'] = group_id
        face['photo_path'] = photo_path
        face['last_detection'] = last_detection
        faces_full.append(face)

    cursor.close()
    conn.close()

    return faces_full

def insert_new_event(camera_id, face_id):
    conn = psycopg2.connect(dbname='FRDB', user='postgres', password='qwerty', host='localhost')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO events (camera_id, face_id) 
                      VALUES(%s, %s)''', (camera_id, face_id))

    conn.commit() 

    cursor.close()
    conn.close()

def update_last_detection(id, last_detection):
    # подключение к БД
    conn = psycopg2.connect(dbname='FRDB', user='postgres', password='qwerty', host='localhost')
    cursor = conn.cursor()

    query = """ UPDATE faces
                SET last_detection = %s
                WHERE face_id = %s"""
    updated_rows = 0
    try:
        cursor.execute(query, (last_detection, id))
        conn.commit()
        updated_rows = 1
    except:
        print('DB update err')

    cursor.close()
    conn.close()

    return updated_rows