# name: str = input("Enter your name: ")
# print(f'WITAJ{name}')

data_of_users: list = [
    {'name': 'Julia', 'surname': 'Szklarzewska', 'posts': 5, 'location': 'Hajnówka'},
    {'name': 'Norbert', 'surname': 'Szeliga', 'posts': 15, 'location': 'Rzeszów'},
    {'name': 'Kacper', 'surname': 'Wójcik', 'posts': 8, 'location': 'Legnica'},
    {'name': 'Sebastian', 'surname': 'Wątroba', 'posts': 12, 'location': 'Siedlce'},
]
print(f'Witaj {data_of_users[0]['name']}')


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

update (data_of_users)
read(data_of_users)
