#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#CLIENT
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import sys
from enlace import *
import time
from dicionario import printador_dic, header_maker, eap_maker

print("SERVER")
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1463101"  # Mac    (variacao de)
serialName = "COM10"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com.enable()
    
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!


    

        print("Aguardando Pacote")
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        
    
            
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #com.sendData(txBuffer)

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #txSize = com.tx.getStatus()
       
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
        rodando=True
        ESTADO = "INCIO"
        foto=bytes(0)
        pacote_passado=0

        #acesso aos bytes recebidos
        while rodando:
            print("mensagem do tipo: ", ESTADO)
            rxBuffer, nRx = com.getData(10)
                
            inicio_header = rxBuffer[0]
            tipo_header = rxBuffer[1]
            print("INICIO HEADER: {}".format(inicio_header))
            if inicio_header == 255:
                ESTADO = "HEADER"
            else:
                ESTADO = "ERRO"
                header=header_maker(2,0,0,0)
                eop=eap_maker()
                pacote=header+eop
                com.sendData(pacote)

            if ESTADO == "HEADER":
                if tipo_header == 1:
                    ESTADO = "HANDSHAKE"
                elif tipo_header == 0:
                    ESTADO = "DADOS"
            if ESTADO == "HANDSHAKE":
                eop, sz = com.getData(4)


                header = header_maker(3,0,0,0)
                eop = eap_maker()
                pacote = header + eop
                com.sendData(pacote)

            elif ESTADO == "DADOS":
                total_pacotes=rxBuffer[2]
                pacote_atual=rxBuffer[3]
                tamanho_pacote=rxBuffer[4]
                dif_pacotes=pacote_atual-pacote_passado
                print("PACOTE PASSADO: {}".format(pacote_passado))
                pacote_passado+=1
                rxBuffer,nRx=com.getData(tamanho_pacote) 
                print("TAMANHO PACOTE:{}".format(tamanho_pacote))
                foto_parte=rxBuffer
                
                eop, eop2 = com.getData(4)
                print(eop)
                print("PACOTE ATUAL: {}".format(pacote_atual))
                
                if int.from_bytes(eop, byteorder='big')!=0 or dif_pacotes!=1:
                    if dif_pacotes!=1:
                        print("PACOTE NAO ERA UM MAIOR QUE O PASSADO")
                        header=header_maker(5,0,0,0)
                    else:
                        print("PAYLOAD COM TAMANHO DIFERENTE DO HEADER, PEDINDO PRA MANDAR PACOTE DE NOVO.")
                        header=header_maker(2,0,0,0)
                    ESTADO = "ERRO"
                    #MANDAR MENSAGEM FALANDO PRA MANDAR DE NOVO
                    
                    eop=eap_maker()
                    pacote=header+eop
                    com.sendData(pacote)
                    pacote_passado-=1
                
                elif pacote_atual>=total_pacotes:
                    print("Recebido último pacote")
                    foto+=foto_parte
                    
                    header=header_maker(4,0,0,0)
                    eop=eap_maker()
                    pacote=header+eop
                    com.sendData(pacote)

                    f=open("./imagem_gerada.png", 'wb')
                    print("imagem recebida pelo server")
                    f.write(foto)
                    f.close()
                    print("imagem escrita pelo server")

                    rodando=False
                    ESTADO="FIM"
                    
                    
                else:
                    foto+=foto_parte
                    print("Pacote recebido!")
                    header=header_maker(4,0,0,0)
                    eop=eap_maker()
                    pacote=header+eop
                    com.sendData(pacote)
                    




        










        
    
        
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno

        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
    
        com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
