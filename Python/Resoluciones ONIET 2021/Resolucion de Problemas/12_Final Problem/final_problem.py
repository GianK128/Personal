# 
# GitHub: @GianK128
#

import os
import csv
import sqlite3 as sql

curr_dir = os.path.dirname(os.path.realpath(__file__))

BYTITLE, BYGENRE, BYACTOR, EXPORT, QUIT = range(1, 6)

MAIN_MENU_STR = """
===== MOVIES =====
  [1]. Buscar por Título.
  [2]. Buscar por Género.
  [3]. Buscar por Actores/Director.
  [4]. Exportar.
  [5]. Salir.
"""

EXPORT_STR = """
===== EXPORT =====
  [1]. Exportar por popularidad.
  [2]. Exportar por año.
  [3]. Exportar por duracion.
"""

EXPORT_ORD_STR = """
===== EXPORT =====
  [1]. Orden ascendente.
  [2]. Orden descendente.
"""

MOVIE_ENTRY_STR = """
{0} ({1}) - {2}/100 - {3} - {4}\n
""".strip()

conn = sql.connect(f'{curr_dir}/DB_FILMS')
cursor = conn.cursor()

def insert_film_data():
    try:
        cursor.execute("DROP TABLE IF EXISTS films")
        cursor.execute("""
            CREATE TABLE films (
                id INTEGER PRIMARY KEY,
                year UNSIGNED SMALLINT NOT NULL,
                length UNSIGNED SMALLINT,
                title VARCHAR(100) NOT NULL,
                subject VARCHAR(30) NOT NULL,
                actor VARCHAR(50),
                actress VARCHAR(50),
                director VARCHAR(50),
                popularity UNSIGNED TINYINT NOT NULL,
                awards BOOL NOT NULL,
                image VARCHAR(50)
            );
        """)
    except sql.OperationalError:
        print("La tabla ya existe.")
        # return
    
    with open(f"{curr_dir}/film.csv") as f:
        reader = csv.DictReader(f, delimiter=';')
        first_line = True
        insert_list = []

        for row in reader:
            if first_line:
                print("Saltando primera linea...")
                first_line = False
                continue
            
            has_awards = 1 if row['Awards'] == 'Yes' else 0

            insert_list.append(
                (row['Year'], row['Length'], row['Title'],
                row['Subject'], row['Actor'], row['Actress'],
                row['Director'], row['Popularity'], has_awards,
                row['*Image'])
            )
        
        cursor.executemany("""
            INSERT INTO films(year, length, title, subject, actor, actress, director, popularity, awards, image) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, insert_list)
        conn.commit()
        print("Cargado en la tabla.")

def search_title():
    title = input("Ingrese titulo a buscar:\n")
    s = f"%{title}%"
    cursor.execute("SELECT * FROM films WHERE title LIKE ? ORDER BY title ASC", (s,))
    text = f"\nPeliculas encontradas para {title}:\n\n"

    for entry in cursor.fetchall():
        text += "- " + MOVIE_ENTRY_STR.format(entry[3], entry[1], entry[8], entry[4], entry[2]) + "\n"
    
    print(text)
    return input("> Presione ENTER para continuar.")

def search_genre():
    genre = input("Ingrese género a buscar:\n")
    s = f"%{genre}%"
    cursor.execute("SELECT * FROM films WHERE subject LIKE ? ORDER BY title ASC", (s,))
    text = f"\nPeliculas encontradas para {genre}:\n\n"

    for entry in cursor.fetchall():
        text += "- " + MOVIE_ENTRY_STR.format(entry[3], entry[1], entry[8], entry[4], entry[2]) + "\n"
    
    print(text)
    return input("> Presione ENTER para continuar.")

def search_actor():
    actor = input("Ingrese actor/director a buscar:\n")
    s = f"%{actor}%"
    cursor.execute("SELECT * FROM films WHERE actor LIKE ? OR actress LIKE ? OR director LIKE ? ORDER BY title ASC", (s, s, s))
    text = f"\nPeliculas encontradas con {actor}:\n\n"

    for entry in cursor.fetchall():
        text += "- " + MOVIE_ENTRY_STR.format(entry[3], entry[1], entry[8], entry[4], entry[2]) + "\n"
    
    print(text)
    return input("> Presione ENTER para continuar.")
    
def export_file():
    i = int(input(EXPORT_STR + ">> "))
    o = int(input(EXPORT_ORD_STR + ">> "))

    s_val = "popularity" if i == 1 else "year" if i == 2 else "length" if i == 3 else 0
    o_val = "ASC" if o == 1 else "DESC" if o == 2 else 0

    if s_val == 0 or o_val == 0:
        print("Error ingresando las opciones. Intente nuevamente")
        return input("> Presione ENTER para continuar.")

    with open(f"{curr_dir}/exported-data-{s_val}-{o_val.lower()}.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, ['ID', 'YEAR', 'LENGTH', 'TITLE', 'SUBJECT', 'ACTOR', 'ACTRESS', 'DIRECTOR', 'POPULARITY', 'AWARDS', 'IMAGE'])
        cursor.execute(f"SELECT * FROM films ORDER BY {s_val} {o_val}")

        writer.writeheader()
        for entry in cursor.fetchall():
            writer.writerow({
                'ID' : entry[0], 
                'YEAR' : entry[1], 
                'LENGTH' : entry[2], 
                'TITLE' : entry[3],
                'SUBJECT' : entry[4], 
                'ACTOR' : entry[5], 
                'ACTRESS' : entry[6], 
                'DIRECTOR' : entry[7],
                'POPULARITY' : entry[8], 
                'AWARDS' : entry[9], 
                'IMAGE' : entry[10]
            })

    print("Exportacion completada.")
    return input("> Presione ENTER para continuar.")

def prompt_exit():
    while True:
        i = input("¿Quieres salir? [y/n] ")
        t = i.strip().lower()
        if t == 'y':
            conn.close()
            exit(1)
        elif t == 'n':
            break

choice_executer = {
    BYTITLE: search_title,
    BYGENRE: search_genre,
    BYACTOR: search_actor,
    EXPORT: export_file,
    QUIT : prompt_exit
}

if __name__ == "__main__":
    while True:
        i = int(input(MAIN_MENU_STR + ">> "))
        if (len(choice_executer) >= i) and (i > 0):
            choice_executer[i]()

conn.close()
