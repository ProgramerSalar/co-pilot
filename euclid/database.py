# database.py


import psycopg2
from psycopg2 import sql
from euclid.const import db




def create_connection():
    conn = psycopg2.connect(
        host=db.DB_HOST,
        database = db.DB_NAME,
        port = db.DB_PORT,
        user = db.DB_USER,
        password = db.DB_PASSWORD
    )


    return conn 


def create_tables():
    commands = (
        """ 
        DROP TABLE IF EXISTS progress_steps;
        DROP TABLE IF EXISTS apps;
        DROP TABLE IF EXISTS USERS;
        """,

        """ 
        CREATE TABLE users (
            id UUID PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """,

         """
        CREATE TABLE apps (
            id SERIAL PRIMARY KEY,
            user_id UUID NOT NULL,
            app_type VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE progress_steps (
            id SERIAL PRIMARY KEY,
            app_id INTEGER NOT NULL,
            step VARCHAR(255) NOT NULL,
            completed BOOLEAN NOT NULL,
            completed_at TIMESTAMP,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (app_id)
                REFERENCES apps (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )

    conn = None 
    try:
        conn = create_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


    finally:
        if conn is not None:
            conn.close()




def save_app(user_id, 
             app_type):
    
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT  * FROM users WHERE id = %s", (str(user_id)))

    if cursor.fetchone() is None:

        # if user doesn't exists create a new user 
        cursor.execute("INSERT INFO users (id, username, email, password) VALUES (%s, 'username', 'email', 'password')", (str(user_id), ))


    # Now save the app 
    cursor.execute("INSERT INTO apps (user_id, app_type, status) VALUES (%s, %s, 'started') RETURNING id", (str(user_id), app_type))
    app_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()
    return app_id




def save_progress(app_id, step, data):
    conn = create_connection()
    cursor = conn.cursor()

    insert = sql.SQL(
        "INSERT INTO progress_step (app_id, step, data, completed) VALUES (%s, %s, %s, false)"
    )

    cursor.execute(insert, (app_id, step, data))

    conn.commit()
    cursor.close()
    conn.close()



if __name__ == "__main__":
    create_tables()