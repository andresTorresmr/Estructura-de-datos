import os
import datetime
import sqlite3
import pandas as pd
from sqlite3 import Error
LimpiarPantalla = lambda: os.system('cls')
SEPARADOR = ("*" * 20) + "\n"

#se intenta conectar a la base de datos y verifica que las tablas existan, si no existen crea las tablas que se utilizarán
try:
    with sqlite3.connect("Venta_cosmeticos.db") as conn:
        c = conn.cursor()
        #creacion tabla totales
        c.execute("CREATE TABLE IF NOT EXISTS totales (clave_vta INTEGER PRIMARY KEY, total TEXT NOT NULL);")
        #creacion tabla venta
        c.execute("CREATE TABLE IF NOT EXISTS venta (clave INTEGER PRIMARY KEY, descripcion TEXT NOT NULL, piezas INTEGER NOT NULL, precio TEXT NOT NULL, fecha_venta DATE,idcuenta INTEGER NOT NULL);")
        #función registrar
        def registrar():
            #Suma todos los precios de los productos vendidos en la cuenta
            monto_total = 0
            print (SEPARADOR)
            print("Registro de ventas")
            print (SEPARADOR)
            print("**Para finalizar la cuenta basta con dejar en blanco la descripcion del artículo**")
            #Saca la fecha actual del sistema.
            fecha_vta = datetime.date.today()
            while True:
            #cuenta los registros que existen en la tabla venta para no asignar un id existente
                cuenta = ("select count(clave) from venta")
                c.execute(cuenta)
                rtotales = c.fetchone()
            #cuenta los registros que existen en la tabla totales para no asignar un id existente
                total_cuenta = ("select count(clave_vta) from totales")
                c.execute(total_cuenta)
                cuenta_total = c.fetchone()
            #extrae la cantidad de registros existente y le aumenta 1 para asignarle un id al producto vendido
                for registro in rtotales:
                    clave = registro
                if registro:
                    clave = clave + 1
                else:
                    clave = 1
            #extrae la cantidad de registros existentes en totales y le aumenta 1 para asignarle un id al producto vendido
                for claves in cuenta_total:
                    clave_total = claves
                if claves:
                    clave_total = clave_total + 1
                else:
                    clave_total = 1
            #Empieza a pedir los datos del producto
                #descripción
                descripcion=str(input("Ingrese la descripcion del producto: "))
                if descripcion == "" :
                    print("La cuenta se ha terminado")
                    break
                else:
                    if descripcion.isspace() == True:
                        print("No se pueden poner solo espacios en el nombre")
                        break
                    #unidades a vender
                    unidades_venta=int(input("Unidades vendidas:"))
                    #Si se pone 0 o un valor negativo se tomara como si la persona desea cerrar la cuenta asi que terminara el proceso de registro
                    if unidades_venta <= 0 or unidades_venta =="":
                        print("No se pueden vender 0 unidades o negativas")
                        break
                    #Precio por unidad
                    precio=float(input("Ingrese el precio unitario del producto:"))
                    #Si se pone 0 o un valor negativo se tomara como si la persona desea cerrar la cuenta asi que terminara el proceso de registro
                    if precio <= 0 or precio == "":
                        print("El precio no puede ser negativo o 0")
                        break
                    #Saca el  total de la cantidad vendida por el precio unitario
                    suma = (precio*unidades_venta)
                    #el resultado se almacena en monto_total para que se vaya agregando al total de la cuenta
                    monto_total = suma + monto_total
                    #Se crea un diccionario para agregar posteriormente los datos obtenidos a la base de datos
                    valores = {"clave": clave, "nombre":descripcion, "unidades": unidades_venta, "precio": precio, "fecha": fecha_vta, "idcuenta": clave_total}
                    #se intenta ejecutar la sentencia para registrar el producto, si esta falla reportará un error
                    try:
                        c.execute("INSERT INTO venta VALUES(:clave, :nombre, :unidades, :precio, :fecha, :idcuenta)", valores)
                    except Error as e:
                        print (e)
            #Esto se encuentra fuera del while por que se tomará como el final de la cuenta por lo tanto se crea un diccionario en donde se guardará el resultado de monto_total y se le asigna una clave de cuenta.
            totales ={"clave_total": clave_total, "total": monto_total}
            #se intenta ejecutar la sentencia para registrar la cuenta, si esta falla reportará un error
            try:
                c.execute("INSERT INTO totales VALUES(:clave_total, :total)",totales)
            except Error as e:
                print (e)
            #Saca el total de la cuenta para mostrarlo al cierre de cuenta
            try:
                c.execute("SELECT clave_vta, total FROM totales WHERE clave_vta = :clave_total",totales)
                cuenta_final = c.fetchall()
                #Se imprime el total de la cuenta
                for Id, total in cuenta_final:
                    print(f"El total de la cuenta es de: ${total}")
            except Error as e:
                print (e)

        #Función para consultar ventas de una fecha en específico.
        def consulta():
            print (SEPARADOR)
            print("Consulta de ventas")
            print (SEPARADOR)
            #Cuenta las claves que están registradas
            cuenta = ("select count(clave) from venta")
            c.execute(cuenta)
            #almacena el valor total de la cantidad de claves registradas
            rtotales = c.fetchone()
            if rtotales:
                #se pide la fecha a buscar
                fecha_consultar = input("Dime una fecha (aaa-mm-dd): ")
                #se covierte en
                try:
                    fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%Y-%m-%d").date()
                    fecha_consultar_str = str(fecha_consultar)
                    sentencia = (f"SELECT fecha_venta, totales.clave_vta AS ID_Venta , descripcion As Descripcion, piezas As Unidades_vendidas, precio As Precio, totales.total as Total FROM venta INNER JOIN totales ON venta.idcuenta = totales.clave_vta where fecha_venta = '{fecha_consultar_str}'")
                    df = pd.read_sql_query(sentencia, conn)
                    if df.empty == False:
                        print(df.head())
                        total_del_dia = (f"SELECT sum(total) AS Total_vendido from totales where clave_vta in (SELECT idcuenta FROM venta WHERE fecha_venta = '{fecha_consultar_str}')")
                        total_dia = pd.read_sql_query(total_del_dia, conn)
                        print(total_dia.head())
                    else:
                        print("No existen ventas registradas")

                except ValueError:
                    print ("El formato de la fecha no es el especificado.")

            else:
                print("No existen ventas registradas")

        #función menú
        def menu():
            while (True):
                    LimpiarPantalla()
                    print (SEPARADOR)
                    print("FERRETERIA\n")
                    print (SEPARADOR)
                    print("[1] Registrar una venta.")
                    print("[2] Consultar ventas de un día específico.")
                    print("[3] Salir.")
                    opcion = int(input("Selecciona una opción  > "))
                    if opcion <= 3:
                        if opcion==1:
                            #se manda a llamar la función para registrar venta
                            productos=registrar()
                        if opcion==2:
                            consulta()
                        if opcion==3:
                            print("Gracias por utilizar el programa.")
                            break

                        input("Pulsa enter para contunuar...")
                    else:
                        print("Esa respuesta no es válida.")
                        input("Pulsa enter para continuar...")

        menu()
except Error as e:
    print (e)
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")