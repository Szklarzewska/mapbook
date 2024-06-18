from crud import add_user, data_of_users, read_db, remove_user_db, update_db, create_user, db_params



while True:
    print('menu:')
    print('0 - zakończ pracę')
    print('1 - dodaj użytkownika')
    print('2 - usuń użytkownika')
    print('3 - wyswietl użytkowników')
    print('4 - aktualizuj')


    menu_option: str = input('podaj opcję do uruchomienia: ')
    if menu_option == '0': break
    if menu_option == '1': create_user(db_params)
    if menu_option == '2': remove_user_db(db_params)
    if menu_option == '3': read_db(db_params)
    if menu_option == '4': update_db(db_params)
