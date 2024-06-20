from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup
import psycopg2

db_params = psycopg2.connect(
    user="postgres", database="postgres", host="localhost", port="5432", password="geoinformatyka"
)
users: list = []


class User:
    def __init__(self, name, surname, posts, location, coords):
        self.name = name
        self.surname = surname
        self.posts = posts
        self.location = location
        self.coords = coords
        self.marker = map_widget.set_marker(float(self.coords.split(' ')[1][0:-1]),
                                            float(self.coords.split(' ')[0][6:]))


def get_coordinates(location: str) -> list:
    """
    Komentarz
    :param location:
    :return:
    """
    url: str = f'https://pl.wikipedia.org/wiki/{location}'
    response = requests.get(url)

    response_html = BeautifulSoup(response.text, 'html.parser')

    response_html_lat = float(response_html.select('.latitude')[1].text.replace(',', '.'))
    response_html_lng = float(response_html.select('.longitude')[1].text.replace(',', '.'))
    print([response_html_lat, response_html_lng])
    return [response_html_lat, response_html_lng]


def add_user():
    name: str = entry_name.get()
    surname: str = entry_surname.get()
    posts: str = entry_posts.get()
    location: str = entry_location.get()
    # new_user: dict = {'name': name, 'surname': surname, 'posts': posts, 'location': location}
    # new_user = User(name, surname, posts, location)

    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_posts.delete(0, END)
    entry_location.delete(0, END)

    entry_name.focus()

    longitude, latitude = get_coordinates(location)
    cursor = db_params.cursor()
    sql = f"INSERT INTO public.users(name, surname, posts, location, cords) VALUES('{name}', '{surname}',{posts}, '{location}', 'SRID=4326;POINT({latitude} {longitude})');"
    cursor.execute(sql)
    db_params.commit()
    cursor.close()
    show_users()


def user_details():
    i = listbox_lista_obiektow.index(ACTIVE)

    label_name_szczegoly_obiektu_wartosc.config(text=users[i].name)
    label_surname_szczegoly_obiektu_wartosc.config(text=users[i].surname)
    label_posts_szczegoly_obiektu_wartosc.config(text=users[i].posts)
    label_location_szczegoly_obiektu_wartosc.config(text=users[i].location)
    map_widget.set_position(users[i].coords[0], users[i].coords[1])
    map_widget.set_zoom(12)


def remove_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    cursor = db_params.cursor()
    sql = f"DELETE FROM public.users WHERE name='{users[i].name}';"
    cursor.execute(sql)
    db_params.commit()
    cursor.close()
    users[i].marker.delete()
    users.pop(i)
    show_users()


def show_users():
    listbox_lista_obiektow.delete(0, END)
    for user in users:
        user.marker.delete()
    cursor = db_params.cursor()
    sql = f"SELECT id,name,surname,posts,location,st_astext(cords) FROM public.users"
    cursor.execute(sql)
    users_db = cursor.fetchall()
    cursor.close()
    for idx, user in enumerate(users_db):
        listbox_lista_obiektow.insert(idx, f'{user}')
        new_user = User(user[1], user[2], user[3], user[4], user[5])
        users.append(new_user)


def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    print(users[i])
    entry_name.insert(0, users[i].name)
    entry_surname.insert(0, users[i].surname)
    entry_posts.insert(0, users[i].posts)
    entry_location.insert(0, users[i].location)
    button_dodaj_obiekt.config(text='Zapisz zmiany', command=lambda: update_user(i))


def update_user(i):
    users[i].name = entry_name.get()
    users[i].surname = entry_surname.get()
    users[i].posts = entry_posts.get()
    users[i].location = entry_location.get()

    button_dodaj_obiekt.config(text='Dodaj', command=add_user)

    users[i].marker.delete()
    users[i].coords = get_coordinates(users[i].location)
    users[i].marker = map_widget.set_marker(users[i].coords[0], users[i].coords[1])
    cursor = db_params.cursor()
    sql = f"UPDATE public.users SET  name='{users[i].name}', surname='{users[i].surname}', posts='{users[i].posts}', location='{users[i].location}', cords='SRID=4326;POINT({users[i].coords[1]} {users[i].coords[0]})' WHERE name='{users[i].name}';"
    cursor.execute(sql)
    db_params.commit()
    cursor.close()
    show_users()
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_posts.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()


root = Tk()
root.title('mapapp')
root.geometry('1025x760')

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, padx=50)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2, padx=50, pady=20)
ramka_mapa.grid(row=2, column=0, columnspan=8)

# ramka_lista_obiektow
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista obiektów: ")
listbox_lista_obiektow = Listbox(ramka_lista_obiektow)
button_pokaz_szczegoly = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=user_details)
button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_user)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_user)

label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz
label_formularz = Label(ramka_formularz, text='Formularz')
label_name = Label(ramka_formularz, text='Imię: ')
label_surname = Label(ramka_formularz, text='Nazwisko: ')
label_posts = Label(ramka_formularz, text='Liczba postów: ')
label_location = Label(ramka_formularz, text='Miejscowosć: ')

entry_name = Entry(ramka_formularz)
entry_surname = Entry(ramka_formularz)
entry_posts = Entry(ramka_formularz)
entry_location = Entry(ramka_formularz)

button_dodaj_obiekt = Button(ramka_formularz, text='Dodaj: ', command=add_user)

label_formularz.grid(row=0, column=0, columnspan=2)
label_name.grid(row=1, column=0, sticky=W)
label_surname.grid(row=2, column=0, sticky=W)
label_posts.grid(row=3, column=0, sticky=W)
label_location.grid(row=4, column=0, sticky=W)

entry_name.grid(row=1, column=1)
entry_surname.grid(row=2, column=1)
entry_posts.grid(row=3, column=1)
entry_location.grid(row=4, column=1)

button_dodaj_obiekt.grid(row=5, column=1, columnspan=2)

# ramka_szczegoly_obiektu
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text='Szczegóły użytkownika: ')

label_name_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text='Imię: ')
label_name_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text='...', width=10)
label_surname_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text='Nazwisko: ')
label_surname_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text='...', width=10)
label_posts_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text='Posty: ')
label_posts_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text='...', width=10)
label_location_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text='Miejscowosć')
label_location_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text='...', width=10)

label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)
label_name_szczegoly_obiektu.grid(row=1, column=0)
label_name_szczegoly_obiektu_wartosc.grid(row=1, column=1)
label_surname_szczegoly_obiektu.grid(row=1, column=2)
label_surname_szczegoly_obiektu_wartosc.grid(row=1, column=3)
label_posts_szczegoly_obiektu.grid(row=1, column=4)
label_posts_szczegoly_obiektu_wartosc.grid(row=1, column=5)
label_location_szczegoly_obiektu.grid(row=1, column=6)
label_location_szczegoly_obiektu_wartosc.grid(row=1, column=7)

# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1050, height=400, corner_radius=0)
map_widget.set_position(52.23, 21)  # Warsaw, Poland
map_widget.set_zoom(5)
map_widget.grid(row=0, column=0, columnspan=8)

root.mainloop()
