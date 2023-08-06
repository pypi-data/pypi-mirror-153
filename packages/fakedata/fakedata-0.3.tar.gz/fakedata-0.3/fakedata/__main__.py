import logging
from fakedata.fakedata import FakeData

logging.basicConfig(level=logging.DEBUG)


def main(data):
    nombreRandom = data.RandomName()
    sex = data.CheckSex(nombreRandom)
    nombreOne = data.RandomOneName()
    sexOne = data.CheckSex(nombreOne)
    nombreTwo = data.RandomTwoName()
    sexTwo = data.CheckSex(nombreTwo)
    email = data.RandomEmail(nombreRandom)
    emailPersonalizado = data.PersonalizedEmail(nombreRandom, 'outlook.com')
    sexRandom = data.RandomSex()
    tel = data.RandomTel()
    
    print(f'Nombre ramdom: {nombreRandom}')
    print(f'Email random: {email}')
    print(f'Sexo : {sex}')
    print(f'Email personalizado: {emailPersonalizado}')
    print(f'Un solo nombre: {nombreOne}')
    print(f'Sexo One: {sexOne}')
    print(f'Dos nombre: {nombreTwo}')
    print(f'Sexo Two: {sexTwo}')
    print(f'Sexo Random: {sexRandom}')
    print(f'Telefono: {tel}')

if __name__ == '__main__':
    data = FakeData
    x = 0
    while x != 1:
        logging.debug("Ejecutando pruebas FakeData".center(50, '-'))
        main(data)
        logging.debug("Finalizando pruebas FakeData".center(50, '-'))
        x += 1
        