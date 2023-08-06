from mypyliex.classes.something import Something


def main():
    print('Hello')

    jacket = Something('Jacket')
    print(f'\nIt is a Jacket, right? Yes it is a {jacket.get_thing()}')
    input()

    jacket.rename_thing('hammer')
    print(f'\nNow it is a hammer, right? No it is {jacket.get_thing()}')
    input()

    something_else = Something(12)
    print(f'\n\nOh yes so... now it is 12, right? Yes it is {something_else.get_thing()}')
    input()

    something_else.rename_thing(12)
    print(f'\nSo... now it is 1212, right? No it is {something_else.get_thing()}')


if __name__ == '__main__':
    main()
