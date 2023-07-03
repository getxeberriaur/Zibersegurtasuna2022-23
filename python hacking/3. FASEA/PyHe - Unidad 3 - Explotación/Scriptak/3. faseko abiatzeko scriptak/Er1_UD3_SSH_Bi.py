#*******************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#Conocidas unas credenciales, tomamos el control de un servidor ssh. 
#*******************************************************************
import paramiko
##(◕‿−)Importamos la clase ssh del módulo Er1_UD3_SSH_Bat_Soluzioa

   
# (◕‿−) A partir de aquí, introduce todo el código que falta

if __name__ == '__main__':
    try:
        #(◕‿−)Creamos un objeto de la clase ssh

        #(◕‿−)Mientras la conexión no se haya establezca correctamente, solicitamos los datos al usuario.
        
            #(◕‿−)Solicitamos los datos al usuario
        
            #(◕‿−)Pedimos al usuario que introduzca la contraseña
            
        #(◕‿−)Realizamos la conexión al servidor SSH
        try:
            #(◕‿−)Bucle mediante el cual permitiremos al usuario enviar comandos al servidor ssh
            
                #Con esta línea solicitamos al usuario que escriba un comando, y lo guardamos en la variable "comando"
                comando = input("$ ")
                #Si el comando  es exit, actualizamos la variable booleana para que la ejecución no vuelva a entrar en el bucle
                if comando.strip().lower() == 'exit':
                    #(◕‿−)
                #(◕‿−)Si es otro comando
            
                    #(◕‿−)Ejecutamos el comando ingresado, guardando su salida en la variable "stdout"
                    _, stdout, _ = objeto_ssh.cliente.exec_command(comando)
                    #Leemos la salida que se ha generado, y la decodificamos a utf-8 para que sea legible
                    salida = stdout.read().decode('utf-8')
            
                    #(◕‿−)Imprimimos la salida del comando en la consola, sin salto de línea adicional

        except ValueError:
            print('Error inesperado con el shell')
            exit(1)
        #Llegados a este punto, cerramos la conexión ssh. 
        print ("Se ha cerrado la conexión con el servidor")
        objeto_ssh.cliente.close()
    except ValueError:
        print("Ha ocurrido un error inesperado")
    exit()
