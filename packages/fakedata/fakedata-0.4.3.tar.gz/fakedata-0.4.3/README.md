# FAKEDATA
# Modulo para la generacion de informacion falsa! 


Este modulo fue creado con la finalidad de crear **PRUEBAS**, esta idea me surgio ya que en un proyecto necesitaba rellenar mi base de datos con informacion tipo placeholder para realizar pruebas.


# Metodos

A continuacion se describiran los metodos que contiene el modulo.
Para utilizarlo solo importa la libreria.

    from  fakedata.fakedata  import  FakeData

## FakeData.RandomName()
Devuelve un nombre aleatoriamente de los siguientes formatos:

    Nombre Nombre Apellido Apellido
    Nombre Apellido Apellido


## FakeData.RandomOneName()

Devuelve un nombre aleatoriamente en el siguiente formato: 

    Nombre - Apellido - Apellido
    
## FakeData.RandomTwoName()

Devuelve un nombre aleatoreamente en el siguiente formato:

    Nombre Nombre Apellido Apellido

## FakeData.CheckSex(nombreRandom)

Devuelve el genero del nombre proporcionado. 
Esta funcion solo funciona con los nombres generados por las funciones:

    FakeData.RandomOneName()
    FakeData.RandomTwoName()
    FakeData.RandomName()

## FakeData.RandomEmail(nombreRandom)

Devuelve un email al pasarle un nombre, genera emails con los dominios:

    gmail, outlook, yahoo, yopmail
  Y con los las siguientes terminaciones

    .com ,.net ,.es ,.mx

## FakeData.PersonalizedEmail(nombre, servidor_web)

nombre : Cadena que contendra el nombre del cual se generara un email.
Ejemplo: Jose Angel Colin Najera

servidor_web : Cadena que contendrael servidor con el que cuente el email.
Ejemplo: gmail.com