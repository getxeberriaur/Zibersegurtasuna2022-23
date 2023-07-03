#*******************************************************************
#Curso "Python para hacking ético" Tknika 2022/2023
#Conocidas unas credenciales, tomamos el control de un servidor ssh. 
#*******************************************************************
import paramiko
#Importamos la clase ssh del módulo Er1_UD3_SSH_Bat_Soluzioa
from Er1_UD3_SSH_Bat_Soluzioa import ssh
   
if __name__ == '__main__':
    try:
        #Creamos un objeto de la clase ssh
        objeto_ssh=ssh()
        conexion_establecida=False
        #Mientras la conexión no se haya establezca correctamente, solicitamos los datos al usuario. 
        while not conexion_establecida: 
            #Solicitamos los datos al usuario
            objeto_ssh.solicitar_datos_usuario()
            #Pedimos al usuario que introduzca la contraseña
            objeto_ssh.password=input ("Introduzca la contraseña del usuario " + objeto_ssh.usuario + ":")
            conexion_establecida=objeto_ssh.conectar_ssh()
        #Realizamos la conexión al servidor SSH
        try:
            ejecuta_exit=False  
            #Bucle mediante el cual permitiremos al usuario enviar comandos al servidor ssh
            while not ejecuta_exit:
                #Con esta línea solicitamos al usuario que escriba un comando, y lo guardamos en la variable "comando"
                comando = input("$ ")
                #Si el comando  es exit, actualizamos la variable booleana para que la ejecución no vuelva a entrar en el bucle
                if comando.strip().lower() == 'exit':
                    ejecuta_exit=True
                #Si es otro comando
                else:
                    #Ejecutamos el comando ingresado, guardando su salida en la variable "stdout"
                    _, stdout, _ = objeto_ssh.cliente.exec_command(comando)
                    #Leemos la salida que se ha generado, y se decodifica a utf-8 para que sea legible
                    salida = stdout.read().decode('utf-8')
                    #Imprimimos la salida del comando en la consola, sin salto de línea adicional
                    print(salida, end="")
        except ValueError:
            print('Error inesperado con el shell')
            exit()
        #Llegados a este punto, cerramos la conexión ssh. 
        print ("Se ha cerrado la conexión con el servidor")
        objeto_ssh.cliente.close()
    except ValueError:
        print("Ha ocurrido un error inesperado")
    exit()
