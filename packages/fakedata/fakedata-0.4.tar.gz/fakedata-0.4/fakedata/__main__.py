import logging
from fakedata.fakedata import FakeData

logging.basicConfig(level=logging.DEBUG)


def main():
    nombreRandom = FakeData.RandomName()
    sex = FakeData.CheckSex(nombreRandom)
    nombreOne = FakeData.RandomOneName()
    sexOne = FakeData.CheckSex(nombreOne)
    nombreTwo = FakeData.RandomTwoName()
    sexTwo = FakeData.CheckSex(nombreTwo)
    email = FakeData.RandomEmail(nombreRandom)
    emailPersonalizado = FakeData.PersonalizedEmail(nombreRandom, 'outlook.com')
    sexRandom = FakeData.RandomSex()
    tel = FakeData.RandomTel()
    
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
    x = 0
    while x != 1:
        logging.debug("Ejecutando pruebas FakeData".center(50, '-'))
        main()
        logging.debug("Finalizando pruebas FakeData".center(50, '-'))
        x += 1
        