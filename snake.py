import funciones


def main():
	cont_nivel = 1
	nivel = "nivel_" + str(cont_nivel) + ".txt"
	largo_max, SEG, I, J, obstaculos, especiales = funciones.procesar_nivel(nivel)
	snake = [[1,1]]
	comio_fruta = False
	ultmov = "d"
	ulttecla = ""
	mochila = {}
	fruta = [6,5]
	pos_especial, esp = funciones.generar_especiales(snake, obstaculos, fruta, especiales,J,I)
	pos_snake=[]
	tabla, mochila= funciones.armar_tabla('especiales.csv', mochila)
	while True:
		tablero = funciones.actualizar_tablero(fruta, snake,obstaculos,pos_especial,esp,J,I)
		funciones.imprimir_tablero_mochila(tablero, mochila, J, I, cont_nivel, tabla)
		ultmov, ulttecla = funciones.pedir_mov(ultmov, SEG, tabla)
		isEspecial = funciones.es_especialMov(ulttecla, tabla)
		if (isEspecial):
			snake, SEG, mochila = funciones.activar_especial(ulttecla, snake, tabla, SEG, pos_snake, mochila)
		funciones.mover(snake,comio_fruta,ultmov, pos_snake)
		fruta,comio_fruta = funciones.comer_fruta(fruta,snake,pos_especial, obstaculos,J,I)
		mochila, pos_especial, esp = funciones.comer_especial(pos_especial, snake, mochila, esp, fruta, obstaculos, especiales,J,I)
		if len(snake) > largo_max:
			cont_nivel += 1
			try:
				largo_max, SEG, I, J, obstaculos, especiales, snake, ultmov, fruta, pos_especial,esp = funciones.cambiar_nivel(cont_nivel,snake, pos_especial)
			except FileNotFoundError:
				print("\n¡Felicitaciones! Has ganado el juego.")
				break
		if funciones.perder(snake,obstaculos,J,I):
			print("\nHas perdido el juego")
			break
main()
