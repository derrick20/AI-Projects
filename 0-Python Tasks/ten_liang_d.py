import pickle
import os.path

def ten_a():
    file_a = 'mypickle_a.pk'
    if os.path.exists(file_a):
        with open(file_a, 'rb') as fi:
            prev = pickle.load(fi)
        print('The previous person\'s name was %s' % prev)

        name = input('What\'s your name?')
        with open(file_a, 'wb') as fi:
            pickle.dump(name, fi)
    else:
        print('You are the first person to run this script!')
        name = input('What\'s your name?')
        with open(file_a, 'wb') as fi:
            pickle.dump(name, fi)

def ten_b():
    file_b = 'mypickle_b.pk'
    if os.path.exists(file_b):
        with open(file_b, 'rb') as fi:
            list = pickle.load(fi)
        print('The previous people\'s names were %s' % list)

        list.append(input('What\'s your name?'))
        with open(file_b, 'wb') as fi:
            pickle.dump(list, fi)
    else:
        print('You are the first person to run this script!')
        list = []
        list.append(input('What\'s your name?'))
        with open(file_b, 'wb') as fi:
            pickle.dump(list, fi)

ten_a()
ten_b()
exit()

