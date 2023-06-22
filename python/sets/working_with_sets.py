

def appending_a_list_to_a_set():
    my_pets = ['Caopolican', 'Oso', 'Manchita', 'Nanook', 'Petite']

    pets_set = set()

    pets_set.update(my_pets)

    pets_set.update(['Oso', 'Obi', 'Thor'])

    print(pets_set)


if __name__ == '__main__':
    appending_a_list_to_a_set()