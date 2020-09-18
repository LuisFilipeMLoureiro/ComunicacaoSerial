#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#SERVER
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import sys
from enlace import *
import time
from dicionario import printador_dic, header_maker, eap_maker



print("CLIENT")
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1463201"  # Mac    (variacao de)
serialName = "COM9"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com.enable()
        printador_dic()
    
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!


        



        contador = 0
        play = True
        ESTADO = "INICIO"
        

        while play:
            if  ESTADO == "INICIO":
                header = header_maker(1,0,0,0)
                eap = eap_maker()
                pacote = header + eap 
                com.rx.clearBuffer()
                com.sendData(pacote)
                print(pacote)
                print("Envio do Handshake")
                ESTADO = "HANDSHAKE"
                
            
            if ESTADO == "HANDSHAKE":
                
                start = time.time()
                controle = True
                while controle:
                    lenBuffer = com.rx.getBufferLen() # o problema é que nao temos certeza de que seria o tx que receberia o len de do bytes que tem no buffer
                    if lenBuffer == 14:
                        ESTADO = "VIVO"
                        controle = False
                        print("CLIENT RECONHECE SERVER COMO VIVO")
                        
                    end = time.time()
                    delta_t = end - start
                    print("delta_t: ", delta_t)
                    if delta_t > 5:
                        controle = False
                        continuidade = input("Servidor inativo. Tentar novamente? S/N ")
                        if continuidade == "S":
                            controle = True
                            header = header_maker(1,0,0,0)
                            eap = eap_maker()
                            pacote = header + eap 
                            com.sendData(pacote)
                            print(pacote)
                            print("Envio do Handshake")
                            ESTADO = "HANDSHAKE"               
                            start = time.time()
                        else:
                            print("Servidor Inativo. Encerrando")
                            break

            if ESTADO == "VIVO":
                rxBuffer, nRx = com.getData(10)
                eop, eop2 = com.getData(4)
                tipo_msg = rxBuffer[1]
                if tipo_msg == 3:
                    print("Aplicação respondeu")
                    imageW = "./imageB.png"
                    txBuffer = open(imageW, 'rb').read()
                    tamanho_arquivo = len(txBuffer)
                    lenBuffer = len(txBuffer)
                    razao = tamanho_arquivo//114 if tamanho_arquivo % 114 == 0 else tamanho_arquivo//114 + 1
                    contador = 0
                    pacote_correspondete = 1

                    print("tamanho arquivo: {}".format(tamanho_arquivo))

                    while tamanho_arquivo > 0:
                        if tamanho_arquivo >=114:
                            header = header_maker(0,razao,pacote_correspondete,114)
                            payload = txBuffer[contador:contador+114]
                            print("LEN PAYLOAD: {}".format(len(payload)))
                            eop = eap_maker()
                            pacote = header + payload + eop
                            com.sendData(pacote)

                            pacote_correspondete +=2
                            contador += 114
                            tamanho_arquivo -= 1106

                            time.sleep(0.01)
                            rxBuffer, nRx = com.getData(14)
                            if rxBuffer[1]==4:
                                print("Confirmação de pacote recebido foi lida. Próximo pacote será mandado.")
                            elif rxBuffer[1]==2:
                                pacote_correspondete -=1
                                contador -= 114
                                tamanho_arquivo += 114
                            elif rxBuffer[1]==5:
                                pacote_correspondete -=2
                                contador -= 114*2
                                tamanho_arquivo += 114*2
                            print("CONTADOR: {}".format(contador))
                            print("Tamanho restante do arquivo: {}".format(tamanho_arquivo))
                            print("PACOTE ATUAL: {}".format(pacote_correspondete))
                            print("RAZAO (NUMERO DE PACOTES): {}".format(razao))


                            
                        else:
                            
                            header = header_maker(0,razao,pacote_correspondete,tamanho_arquivo)
                            print("TAMANHO_ARQUIVO: {}".format(tamanho_arquivo))
                            payload = txBuffer[contador:lenBuffer]
                            print("LEN PAYLOAD: {}".format(len(payload)))
                            eop = eap_maker()
                            pacote = header + payload + eop
                            com.sendData(pacote)
                            print("ÚLTIMO PACOTE FOI MANDADO")
                            

                            pacote_correspondete +=1
                            contador += 114
                            tamanho_arquivo -= 114
                            play= False
                            

                        

                            
                            






                    

                

                
            #tamanho_arquivo_restante -= 114
            # Proximos passos: faxer o content do arquivo como o conteudo do arquivo e fazer o recebimento de arquivos
        
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        
    
         

        #prox passos: fazer um vetor de bytes de 10 e fazer os ifs, primeiro enviando o handshake e depois o de dado com o input
        #finalmente vamos transmitir os tados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #txSize = com.tx.getStatus()
       
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        #rxBuffer, nRx = com.getData(txLen)
    
    
        #print (rxBuffer)
    
        
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        print("ERRO: {}".format(e))
        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)
    
        com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
