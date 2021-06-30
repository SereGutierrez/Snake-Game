from random import randint
from terminal import clear_terminal
from terminal import timed_input
import csv

MOV_VALIDOS = {"w" : (0,-1),"a" : (-1,0), "s" : (0,1), "d" : (1,0)}
def procesar_nivel(nivel):
	"""Procesa los datos de un archivo que contiene las cracteristicas de un nivel y devuelve cada dato en variables"""
	with open(nivel) as f:
		largo_max = f.readline()
		tiempo = f.readline()
		DIM = f.readline()
		I,J = DIM.split("x")
		obs = f.readline()
		obstac = obs.rstrip("\n").split(";")
		obstaculos= []
		for e in obstac:
			coord = []
			s = e.split(",")
			coord.append(int(s[0]))
			coord.append(int(s[1]))
			obstaculos.append(coord)
		espe = f.readline()
		especiales=espe.split(",")
		return int(largo_max), float(tiempo), int(I), int(J), obstaculos, especiales

def armar_tabla(archivo, mochila):
	"""Lee un archivo y arma una tabla con los especiales, su descripción y tecla para activalos, devuelve la tabla y una mochila (diccionario) que contiene los simbolos de los especiales y su cantidad"""
	tabla={}
	with open(archivo) as arch:
		arch_csv = csv.DictReader(arch)
		for linea in arch_csv:
			mochila[linea["simbolo"]] = 0
			tabla[linea["tecla"]]=[linea["aspecto"],linea["simbolo"],linea["alteracion"], linea["descripcion"]]
	return tabla, mochila

def activar_especial(ulttecla, snake, tabla, SEG, pos_snake, mochila):
	"""Cambia aspectos de la serpiente segun la tecla especial que ingresa el usuario, si no esta el especial en la mochila, no lo activa. Devuelve la serpiente y los segundos que tarda en moverse la misma"""
	alteracion = tabla[ulttecla][2]
	aspecto = tabla[ulttecla][0]
	if mochila[tabla[ulttecla][1]] > 0:
		if aspecto == "VELOCIDAD":
			if (SEG + float(alteracion)) > 0.01:
				SEG += float(alteracion)
				mochila[tabla[ulttecla][1]] -= 1
		if aspecto == "LARGO":
			if alteracion[0] == "-" and len(snake) > int(alteracion):
				for i in range(0-int(alteracion)):
					snake.pop()
				mochila[tabla[ulttecla][1]] -= 1
			if alteracion.isdigit():
				for pos in pos_snake[-1: -int(alteracion)-1: -1]:
					snake.append(pos)
				mochila[tabla[ulttecla][1]] -= 1
	return snake, SEG, mochila

def mover(snake,comio_fruta,ultmov,pos_snake):
	"""Define a que lado debe moverse la serpiente y devuelve su nueva posición. Guarda las tres ultimas posiciones por las que pasó la serpiente, para usar en el especial que aumenta su largo"""
	direccion = MOV_VALIDOS[ultmov]
	snake.insert(0,[snake[0][0]+direccion[0],snake[0][1]+direccion[1]])
	if (not comio_fruta):
		if (len(pos_snake) > 10):
			pos_snake.pop(0)
		pos_snake.append(snake.pop())
	return snake

def pedir_mov(ultmov, SEG, tabla):
	"""Pide al usuario el movimiento o una tecla especial, si este no ingresa nada, o ingresa muchos movimientos, devuelve el ultimo ingresado en un tiempo determinado y la tecla especial"""
	m=timed_input(SEG)
	if m=="":
		ulttecla=""
		return ultmov, ulttecla
	if m[-1] in MOV_VALIDOS:
		ultmov = m[-1]
	if (m[-1] in tabla):
		ulttecla = m[-1]
		return ultmov, ulttecla
	else:
		ulttecla = ""
	return ultmov,ulttecla
	
def armar_tablero(J, I):
	"""Al comenzar el juego arma un tablero de IxJ, dimensiones que recibe"""
	matriz=[]
	for i in range (I+1):
		matriz.append([])
		for j in range (J+1):
			matriz[i].append(" ")
	return matriz

def imprimir_tablero_mochila(tablero,mochila,J,I, cont_nivel, tabla):
	"""Imprime en pantalla el tablero y la mochila"""
	clear_terminal()
	print("NIVEL: " + str(cont_nivel))
	for i in range(I):
		print("\n")
		for j in range(J + 1):
			print(tablero[i][j],end= ". ")
	print("\nUsá w,a,s,d para cambiar de dirección")
	print("MOCHILA")
	print("simbolo  cantidad  tecla  descripcion")
	for letra in tabla:
		print(tabla[letra][1] + "        " + str(mochila[tabla[letra][1]]) + "         " + letra + "      " + tabla[letra][3])

def actualizar_tablero(fruta,snake,obstaculos,pos_especial,esp,J,I):
	"""Actualiza el tablero agregando la fruta, la serpiente, los obstaculos y los especiales, en las posiones que recibe"""
	tablero = armar_tablero(J, I)
	for i in range(I+1):
		for j in range(J+1):
			if [j,i] in snake:
				tablero[i].pop(j)
				tablero[i].insert(j,"o")
			if [j,i]==fruta:
				tablero[i].pop(j)
				tablero[i].insert(j,"*")
			if [j,i] in obstaculos:
					tablero[i].pop(j)
					tablero[i].insert(j,"@")
			if [j,i] == pos_especial:
				tablero[i].pop(j)
				tablero[i].insert(j,esp)
	return tablero

def perder(snake, obstaculos,J,I):
	"""Decide si el usuario perdió el juego o no"""
	return (snake[0] in snake[1:]) or snake[0][0]<1 or snake[0][0]>J or snake[0][1]<0 or snake[0][1]>I-1 or (snake[0] in obstaculos)
		

def generar_fruta(snake,obstaculos,pos_especial,J,I):
	"""Devuelve una nueva posición para la fruta"""
	fruta=[randint(1,J-1),randint(0,I-1)]
	while (fruta in snake) or (fruta in obstaculos) or (fruta==pos_especial):
		fruta=[randint(1,J-1),randint(0,I-1)]
	return fruta

def comer_fruta(fruta,snake,pos_especial,obstaculos,J,I):
	"""Si la serpiente come la fruta, devuelve una nueva posicion para esta ultima y asigna True a la variable "comio_fruta", sino, devuelve la posición de la fruta que recibió, y asigna False a la variable "comio_fruta" """
	if fruta==snake[0]:
		fruta = generar_fruta(snake,obstaculos,pos_especial,J,I)
		comio_fruta= True
		return (fruta,comio_fruta)
	else:
		comio_fruta= False
	return (fruta,comio_fruta)

def generar_especiales(snake, obstaculos,fruta, especiales,J,I):
	"""Devuelve un nuevo simbolo de especial y una nueva posición para el mismo"""
	esp = especiales[randint(0,len(especiales)-1)]
	pos_especial=[randint(1,J),randint(0,I-1)]
	while pos_especial in snake or pos_especial in obstaculos or pos_especial==fruta:
		pos_especial=[randint(1,J),randint(0,I-1)]
	return pos_especial, esp

def comer_especial(pos_especial, snake, mochila, esp, fruta, obstaculos, especiales,J,I):
	"""Si la serpiente come el especial, devuelve la mochila modificada y un nuevo especial, sino, devuelve la misma mochila y especial que recibió"""
	if pos_especial==snake[0]:
		mochila[esp] += 1
		pos_especial, esp = generar_especiales(snake,obstaculos,fruta,especiales,J, I)
	return mochila, pos_especial, esp

def es_especialMov (mov, tabla):
	"""Decide si la tecla ingresada es valida para activar un especial"""
	return mov in tabla

def cambiar_nivel(cont_nivel, snake, pos_especial):
	"""Cambia de nivel cuando se llega a un largo determinado"""
	nivel = "nivel_" + str(cont_nivel) + ".txt"
	largo_max, SEG, I, J, obstaculos, especiales = procesar_nivel(nivel)
	snake = [[3,3]]
	ultmov = "d"
	fruta = generar_fruta(snake,obstaculos,pos_especial,J,I)
	pos_especial, esp = generar_especiales(snake, obstaculos, fruta, especiales,J,I)
	return largo_max, SEG, I, J, obstaculos, especiales, snake, ultmov, fruta, pos_especial,esp