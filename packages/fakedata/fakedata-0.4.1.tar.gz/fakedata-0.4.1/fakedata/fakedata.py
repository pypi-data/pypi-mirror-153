import random
import fakedata.lista as lista

class FakeData:

    def RandomOneName():
        """Devuelve un nombre aleatoreamente en el siguiente formato:
        nombre apellido apellido
        
        Returns
        -------
        name : str
            Cadena que contiene el nombre generado
        """
        sex = random.choice(['male', 'female'])
        if sex == 'male':
            name = random.choice(lista.name_m) + " " + random.choice(lista.last_names) + " " + random.choice(lista.last_names)
            return name.title()
        elif sex == 'female':
            name = random.choice(lista.name_f) + " " + random.choice(lista.last_names) + " " + random.choice(lista.last_names)
            return name.title()
        
    def RandomTwoName():
        """Devuelve un nombre aleatoreamente en el siguiente formato:
        nombre nombre apellido apellido
        
        Returns
        -------
        name : str
            Cadena que contiene el nombre generado
        """
        sex = random.choice(['male', 'female'])
        if sex == 'male':
            name = random.choice(lista.name_m) + " " + random.choice(lista.name_m) + " " +random.choice(lista.last_names) + " " + random.choice(lista.last_names)
            return name.title()
        elif sex == 'female':
            name = random.choice(lista.name_f) + " " + random.choice(lista.name_f) + " " +random.choice(lista.last_names) + " " + random.choice(lista.last_names)
            return name.title()
        
    def RandomUSAName():
        sex = random.choice(['male', 'female'])
        if sex == 'male':
            name = random.choice(lista.name_m) + " " + random.choice(lista.name_m) + " " +random.choice(lista.last_names)
            return name.title()
        elif sex == 'female':
            name = random.choice(lista.name_f) + " " + random.choice(lista.name_f) + " " +random.choice(lista.last_names)
            return name.title()
        
    def RandomName():
        """Devuelve un nombre aleatoreamente de los siguientes formatos:
        nombre nombre apellido apellido
        nombre apellido apellido
        
        Returns
        -------
        name : str
            Cadena que contiene el nombre generado
        """
        name_length = random.choice([1, 2])
        if name_length == 1:
            name = FakeData.RandomOneName()
            return name
        elif name_length == 2:
            name = FakeData.RandomTwoName()
            return name
    
    def CheckSex(name):
        """Devuelve el genero del nombre proporcionado. Esta funcion solo funciona
        con los nombres generados por las funciones:
        RandomOneName()
        RandomTwoName()
        RandomName()
        
        Returns
        -------
        sex : str
            Cadena que contiene el sexo del nombre proporcionado puede ser:
            male
            female
        """
        name_list = name.split(' ')
        if name_list[0].upper() in lista.name_m:
            return 'male'
        elif name_list[0].upper() in lista.name_f:
            return 'female'
        else:
            return 'El nombre no esta en la lista, si quieres un sexo random utiliza: RandomSex'
        
    def RandomSex():
        return random.choice(['male', 'female'])
        
    def RandomEmail(nombre):
        """Devuelve un email al pasarle un nombre
        Parameters
        ----------
        nombre : str
            Cadena que contendra el nombre del cual se generara un email
        Returns
        -------
        email : str
            Cadena que contiene el email generado
        """
        servers = [
            'gmail',
            'outlook',
            'yahoo',
            'yopmail'
        ]
        dot = [
            '.com',
            '.net',
            '.es',
            '.mx',
        ]
        list_name = nombre.split(' ')
        num_name = len(list_name)
        if num_name >= 5:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[3]
            last_name_fa = list_name[4]
            first_letter_last_fa = last_name_fa[0]
            user = (first_letter_name + last_name_ma +
                    first_letter_last_fa).lower()
            email = user + '@' + random.choice(servers) + random.choice(dot)
            return email
        if num_name == 4:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[2]
            last_name_fa = list_name[3]
            first_letter_last_fa = last_name_fa[0]
            user = (first_letter_name + last_name_ma +
                    first_letter_last_fa).lower()
            email = user + '@' + random.choice(servers) + random.choice(dot)
            return email
        elif num_name == 3:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[1]
            last_name_fa = list_name[2]
            first_letter_last_fa = last_name_fa[0]
            user = (first_letter_name + last_name_ma +
                    first_letter_last_fa).lower()
            email = user + '@' + random.choice(servers) + random.choice(dot)
            return email
        elif num_name == 2:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[1]
            user = (first_letter_name + last_name_ma).lower()
            email = user + '@' + random.choice(servers) + random.choice(dot)
            return email
        elif num_name == 1:
            first_name = list_name[0]
            user = (first_name).lower()
            email = user + '@' + random.choice(servers) + random.choice(dot)
            return email

    def PersonalizedEmail(nombre, servidor_web):
        """Devuelve un email al pasarle un nombre
        Parameters
        ----------
        nombre : str
            Cadena que contendra el nombre del cual se generara un email.
            Ejemplo: Jose Angel Colin Najera
        servidor_web : str
            Cadena que contendra el servidor con el que cuente el email.
            Ejemplo: gmail.com
        Returns
        -------
        email : str
            Cadena que contiene el email generado
        """
        list_name = nombre.split(' ')
        num_name = len(list_name)
        if num_name >= 5:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[3]
            last_name_fa = list_name[4]
            first_letter_last_fa = last_name_fa[0]
            user = (first_letter_name + last_name_ma +
                    first_letter_last_fa).lower()
            email = user + '@' + servidor_web
            return email
        if num_name == 4:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[2]
            last_name_fa = list_name[3]
            first_letter_last_fa = last_name_fa[0]
            user = (first_letter_name + last_name_ma +
                    first_letter_last_fa).lower()
            email = user + '@' + servidor_web
            return email
        elif num_name == 3:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[1]
            last_name_fa = list_name[2]
            first_letter_last_fa = last_name_fa[0]
            user = (first_letter_name + last_name_ma +
                    first_letter_last_fa).lower()
            email = user + '@' + servidor_web
            return email
        elif num_name == 2:
            first_name = list_name[0]
            first_letter_name = first_name[0]
            last_name_ma = list_name[1]
            user = (first_letter_name + last_name_ma).lower()
            email = user + '@' + servidor_web
            return email
        elif num_name == 1:
            first_name = list_name[0]
            user = (first_name).lower()
            email = user + '@' + servidor_web
            return email
        
    def RandomTel():
        tel = []
        new_tel = ''
        x = 0
        while x!= 10:
            new_tel += str(random.choice(range(0,10)))
            x += 1
        return new_tel

if __name__ == '__main__':
    data = FakeData
    x = 0
    while x != 100:
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
        print("".center(50, '-'))
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
        print("".center(50, '-'))
        x += 1
        

