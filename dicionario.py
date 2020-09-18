#####################################################
# Camada Física da Computação        
# DICIONARIO
imageW = "imageB.png"
txBuffer = open(imageW, 'rb').read()
tamanho_arquivo = len(txBuffer)
razao = round(tamanho_arquivo/114)

def printador_dic():
        
    print("########################################")
    print("DICIONARIO INICIO")
    print()
    print("########################################")
    print()
    print( "HEADER" )
    print("########################################")
    print()
    print("BYTE 0 - Inicio de um Header")
    print()
    print((255).to_bytes(2, byteorder='big'), "Inicio de HEADER")
    print("########################################")
    print()
    print("BYTE 1 - Tipo de Mensagem")
    print((0).to_bytes(1, byteorder='big'), "Dados")
    print((1).to_bytes(1, byteorder='big'), "HandShake")
    print((2).to_bytes(1, byteorder='big'), "Erro")
    print((3).to_bytes(1, byteorder='big'), "Estou Vivo!")
    print((4).to_bytes(1, byteorder='big'), "Pacote recebido, pode mandar o próximo!")
    print((5).to_bytes(1, byteorder='big'), "Mandou o pacote errado!")
    print("########################################")
    print()
    print("BYTE 2 - Número de Pacotes a ser enviados para a mensagem")
    print("########################################")
    print()
    print("BYTE 3 - Pacote correspondente dessa mensagem")
    print("########################################")
    print()
    print("BYTE 4 - Tamanho do Payload")
    print("########################################")
    print("DICIONARIO FIM")
    print()
    print("########################################")
    print()

'''def header_maker1(arg1,arg3,arg4):
    un0 = (255).to_bytes(1,byteorder="big") #Anuciar Header (FF)
    un1 = (arg1).to_bytes(1,byteorder="big") # Tipo de mensagem
    un2 = (razao).to_bytes(1,byteorder="big") # Razao
    un3 = (arg3).to_bytes(1,byteorder="big") # pacote correspondente do pacote
    un4 = (arg4).to_bytes(1,byteorder="big") # tamanho do pacote
    un5 = (0).to_bytes(1,byteorder="big")
    un6 = (0).to_bytes(1,byteorder="big")
    un7 = (0).to_bytes(1,byteorder="big")
    un8 = (0).to_bytes(1,byteorder="big")
    un9 = (0).to_bytes(1,byteorder="big")
    un10 = (0).to_bytes(1,byteorder="big")

    header= un0 + un1 + un2  + un3 + un4 + un5 + un6 + un7 + un8 + un10
    return header
    '''
def header_maker(arg1,arg2,arg3,arg4):
    un0 = (255).to_bytes(1,byteorder="big") #Anuciar Header (FF)
    un1 = (arg1).to_bytes(1,byteorder="big") # Tipo de mensagem
    un2 = (arg2).to_bytes(1,byteorder="big") # Razao (numero total de pacotes)
    un3 = (arg3).to_bytes(1,byteorder="big") # pacote correspondente do pacote
    un4 = (arg4).to_bytes(1,byteorder="big") # tamanho do pacote
    un5 = (0).to_bytes(1,byteorder="big")
    un6 = (0).to_bytes(1,byteorder="big")
    un7 = (0).to_bytes(1,byteorder="big")
    un8 = (0).to_bytes(1,byteorder="big")
    un9 = (0).to_bytes(1,byteorder="big")
    

    header = un0 + un1 + un2  + un3 + un4 + un5 + un6 + un7 + un8 + un9
    return header
def eap_maker():
    return (0).to_bytes(4,byteorder="big")

