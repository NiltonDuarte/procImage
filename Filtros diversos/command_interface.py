# -*- coding: utf-8 -*-

from proc_img import *
import os, time

imgDir = sys.argv[1]
#outImgName = sys.argv[2]

live = True

myImg = MyImg(imgDir)
simpleFilter = SimpleFilters()
complexFilter = ComplexFilters()


def clean():
	if (sys.platform.startswith('win')):
		os.system('cls')
	else:
		os.system('clear')

def msgSucesso(msg):
	print msg
	raw_input("Pressione qualquer tecla para voltar ao menu.")

def filtroSimples():
	clean()

	print ">>> FILTROS SIMPLES <<<"
	print \
"""\n	1. Negativo
	2. Cúbico
	3. Quadrático
	9. Voltar
	0. Sair\n"""

	simpleInput = input("Escolha um filtro: ")
	simplesDict[simpleInput]()

def filtroComplexo():
	clean()

	condition = True
	print ">>> FILTROS COMPLEXOS <<<"
	print \
"""\n	1. Gradiente em 1 dimensão
	2. Gradiente em 4 dimensões
	3. Gaussiano
	4. Mediana
	5. Intensidade de radiação
	6. Energia Potencial Elétrica
	7. Sobel
	9. Voltar
	0. Sair\n"""

	while(condition):
		try:
			complexInput = input("Escolha um filtro: ")
			break
		except SyntaxError:
			print "Opção inválida"
		except NameError:
			print "Opção inválida"

	complexoDict[complexInput]()
		

def negativo():
	clean()

	print ">> FILTRO NEGATIVO <<\n"
	print "Aplicando efeito negativo...\n"
	myImg.applySimpleFilter(simpleFilter.negative, [])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()
	
def cubico():
	clean()

	print ">> FILTRO CÚBICO <<\n"
	condition = True

	print "Aplicando a*x^3 + b"

	while(condition):
		try:
			fator = input("Forneça o valor de a: ")
			offset = input("Forneça o valor de b: ")
			break
		except SyntaxError:
			print "Input inválido"
		except NameError:
			print "Input inválido"

	myImg.applySimpleFilter(simpleFilter.cubic, [fator, offset])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()


def quadratico():
	clean()

	print ">> FILTRO QUADRÁTICO <<\n"
	condition = True

	print "Aplicando a*x^2 + b"

	while(condition):
		try:
			fator = input("Forneça o valor de a: ")
			offset = input("Forneça o valor de b: ")
			break
		except SyntaxError:
			print "Input inválido"
		except NameError:
			print "Input inválido"

	myImg.applySimpleFilter(simpleFilter.quadratic, [fator, offset])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def gradiente1D():
	clean()

	print ">> FILTRO GRADIENTE EM 1 DIMENSÃO <<\n"
	print "Aplicando gradiente em uma dimensão...\n"
	myImg.applyComplexFilter(complexFilter.gradient1D, [])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def gradiente4D():
	clean()

	print ">> FILTRO GRADIENTE EM 4 DIMENSÕES <<\n"
	print "Aplicando gradiente em quatro dimensões...\n"
	myImg.applyComplexFilter(complexFilter.gradient4D, [])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def gaussiano():
	clean()

	print ">> FILTRO GAUSSIANO <<\n"

	condition = True
	print "Aplicando Gaussiana como peso em média"
	print "Default: 3x3, com desvio padrão 1.5"

	while(condition):
		try:
			window = input("Forneça o tamanho da janela de pixels: ")
			break
		except SyntaxError:
			print "Input inválido"
		except NameError:
			print "Input inválido"
	
	myImg.applyComplexFilter(complexFilter.gaussian, [1.5], window)
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def mediana():
	clean()

	print ">> FILTRO MEDIANA <<\n"
	print "Aplicando filtro mediana...\n"
	myImg.applyComplexFilter(complexFilter.median, [])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def radiacao():
	clean()
	
	print ">> FILTRO INTENSIDADE DE RADIAÇÃO <<\n"
	print "Aplicando intensidade de radiação de vizinhos...\n"
	myImg.applyComplexFilter(complexFilter.radiationIntensity, [])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def epeletrica():
	clean()
	
	print ">> FILTRO ENERGIA POTENCIAL ELÉTRICA <<\n"
	print "Aplicando média de energia potencial elétrica...\n"
	myImg.applyComplexFilter(complexFilter.eletricPotentialEnergy, [])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def sobel():
	clean()
	
	print ">> FILTRO SOBEL <<\n"
	print "Aplicando sobel...\n"
	myImg.applyComplexFilter(complexFilter.sobel, [])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def mudarRange():
	clean()
	
	print ">> MUDANÇA DE RANGE PARA TESTES <<\n"

	condition = True
	print "Aplicando filtro com máscara de Sobel...\n"
	print \
"""\n
	| i=2 | i=5 | i=4 |
	| i=1 | i=0 | i=3 |
	| i=6 | i=7 | i=8 |\n"""

	while(condition):
		try:
			indice = input("Forneça o índice do pixel a ser ignorado: ")
			break
		except SyntaxError:
			print "Input inválido"
		except NameError:
			print "Input inválido"

	myImg.applyComplexFilter(complexFilter.changeRange, [indice])
	msgSucesso("Filtro aplicado com sucesso")
	myImg.show()

def recarregaImg():
	clean()

	global myImg
	print ">> RECARREGAR IMAGEM ORIGINAL <<\n"
	print "Recarregando imagem original..."
	myImg = MyImg(imgDir)
	msgSucesso("Imagem carregada com sucesso.")
	myImg.show()
	

def voltar():
	return

def salvar():
	clean()
	aux = myImg.outImgName

	print ">> SALVAR IMAGEM <<\n"
	print "Default: ", aux
	outName = raw_input("Forneça o nome para o arquivo de saída (com extensão): ")
	
	if (outName):
		myImg.setOutName(outName)
	try:
    		myImg.save()
	except KeyError:
		print "Nome inválido. Usando default."
		print aux
    		myImg.setOutName(aux)
		myImg.save()
	msgSucesso("Salvo com sucesso.")

def sair():
	clean()
	global live
	live = False

simplesDict = { 1: negativo,
		2: cubico,
		3: quadratico,
		9: voltar,
		0: sair}

complexoDict = {1: gradiente1D,
		2: gradiente4D,
		3: gaussiano,
		4: mediana,
		5: radiacao,
		6: epeletrica,
		7: sobel,
		9: voltar,
		0: sair,
		2307: mudarRange}

inicialDict = { 1: filtroSimples,
		2: filtroComplexo,
		8: recarregaImg,
		9: salvar,
		0: sair}



while(live):
	clean()

	condition = True
	print "\n>>>> Processamento de Imagens 2014.1 <<<<"
	print \
"""\n	1. Filtros Simples
	2. Filtros Complexos
	8. Recarregar imagem original
	9. Salvar
	0. Sair\n"""

	while(condition):
		try:
			myInput = input("Escolha um tipo de filtro: ")
			break
		except SyntaxError:
			print "Opção inválida"
		except NameError:
			print "Opção inválida"

	inicialDict[myInput]()
