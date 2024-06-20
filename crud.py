# name: str = input("Enter your name: ")
# print(f'WITAJ{name}')

data_of_users: list = [
    {'name': 'Julia', 'surname': 'Szklarzewska', 'posts': 5, 'location': 'Hajnówka'},
    {'name': 'Norbert', 'surname': 'Szeliga', 'posts': 15, 'location': 'Rzeszów'},
    {'name': 'Kacper', 'surname': 'Wójcik', 'posts': 8, 'location': 'Legnica'},
    {'name': 'Sebastian', 'surname': 'Wątroba', 'posts': 12, 'location': 'Siedlce'},
]
print(f'Witaj {data_of_users[0]['name']}')

import requests
from bs4 import BeautifulSoup
import psycopg2

db_params=psycopg2.connect(
    user="postgres",database="postgres",host="localhost",port="5432",password="geoinformatyka"
)

def get_coordinates(nazwa_miejscowosci)->list:

    url:str=f'https://pl.wikipedia.org/wiki/{nazwa_miejscowosci}'
    response=requests.get(url)
    # print(response.text)
    response_html=BeautifulSoup(response.text,'html.parser')
    # print(response_html)
    response_html_lat:list=response_html.select('.latitude')[1].text.replace(',','.')
    response_html_lng:list=response_html.select('.longitude')[1].text.replace(',','.')
    print (response_html_lat)
    print (response_html_lng)
    return [response_html_lat,response_html_lng]

# get_coordinates()

def create_user(db_params)-> None:

    name: str = input("Enter your name: ")
    surname: str = input("Enter your surname: ")
    posts: int = int(input("Enter your number of posts: "))
    location: str = input("Enter your location: ")
    new_user: dict = {'name': name, 'surname': surname, 'posts': posts, 'location': location}
    longitude,latitude=get_coordinates(location)
    cursor=db_params.cursor()
    sql=f"INSERT INTO public.users(name, surname, posts, location, cords) VALUES('{name}', '{surname}',{posts}, '{location}', 'SRID=4326;POINT({latitude} {longitude})');"
    cursor.execute(sql)
    db_params.commit()
    cursor.close()

def read_db(db_params)-> None:
    cursor=db_params.cursor()
    sql=f"SELECT * FROM public.users"
    cursor.execute(sql)
    users=cursor.fetchall()
    cursor.close()
    for user in users:
        print(user)

def remove_user_db(db_params)-> None:
    cursor=db_params.cursor()
    sql=f"DELETE FROM public.users WHERE name='{input('kogo usunąć?: ')}';"
    cursor.execute(sql)
    db_params.commit()
    cursor.close()

def read(users: list) -> None:
    """
    show users from an list
    :param users: a list of users
    :return: None
    """
    for user in users[1:]:
        print(f'twój znajomy: {user['name']}, opublikował: {user['posts']}')


# read(data_of_users)

def add_user(users: list) -> None:
    """
    add user to a list
    :param users: user list
    :return: None
    """
    name: str = input("Enter your name: ")
    surname: str = input("Enter your surname: ")
    posts: int = int(input("Enter your number of posts: "))
    location: str = input("Enter your location: ")
    new_user: dict = {'name': name, 'surname': surname, 'posts': posts, 'location': location}
    users.append(new_user)

# add_user(data_of_users)
# read(data_of_users)
def delete_user(users:list)-> None:
    name:str=input('enter a name of user to remove: ')
    for user in users:
        if user['name']==name:
            users.remove(user)



# delete_user(data_of_users)
# read(data_of_users)

def update(users:list)->None:

    name:str=input("Enter name of user to be modified: ")
    for user in users:
        if user['name']==name:
            new_name:str=input('Enter new name: ')
            new_surname:str=input('Enter new surname: ')
            new_posts:int=int(input('Enter new number of posts: '))
            new_location:str=input('Enter new location: ')
            user['name']=new_name
            user['surname']=new_surname
            user['posts']=new_posts
            user['location']=new_location

# update (data_of_users)
def update_db(db_params) -> None:
    new_name: str = input("New name: ")
    new_surname: str = input("New surname: ")
    new_posts: int = int(input("Enter new number of posts: "))
    new_location: str = input("Enter your new location: ")
    longitude, latitude = get_coordinates(new_location)
    cursor = db_params.cursor()
    sql=f"UPDATE public.users SET  name='{new_name}', surname='{new_surname}', posts='{new_posts}', location='{new_location}', cords='SRID=4326;POINT({latitude} {longitude})' WHERE name='{input('kogo zaktualizować ?: ')}';"
    cursor.execute(sql)
    db_params.commit()
    cursor.close()
# read(data_of_users)


