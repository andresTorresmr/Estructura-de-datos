#Registro del detalle de ventas un negocio de ferretería
#Requerimientos funcionales:
#Se debe ofrecer un menú navegable con las siguientes opciones: Registrar una venta Consultar una venta Salir
import os
import datetime
import sqlite3
from sqlite3 import Error
import pandas as pd
LimpiarPantalla = lambda: os.system('cls')
SEPARADOR = ("*" * 20) + "\n"

try:
    with sqlite3.connect("Venta_cosmeticos.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS totales (clave INTEGER PRIMARY KEY, total TEXT NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS venta (clave INTEGER PRIMARY KEY, descripcion TEXT NOT NULL, piezas INTEGER NOT NULL, precio TEXT NOT NULL, fecha_venta DATE,idcuenta INTEGER NOT NULL);")

        #Elaborado por Javier Alejandro Álvarez Rios
        def cargar():
            monto_total = 0
            print (SEPARADOR)
            print("Registro de ventas")
            print (SEPARADOR)
            print("**Para finalizar la cuenta basta con dejar en blanco la descripcion del artículo**")

            while True:
            #cuenta los registros que existen en la tabla venta para no asignar un id existente
                cuenta = ("select count(clave) from venta")
                c.execute(cuenta)
                rtotales = c.fetchone()
            #cuenta los registros que existen en la tabla totales para no asignar un id existente
                total_cuenta = ("select count(clave) from totales")
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
                print(clave)
                print(clave_total)
                descripcion=str(input("Ingrese la descripcion:"))
                if descripcion == "":
                    break
                else:
                    unidades_venta=int(input("Unidades vendidas:"))
                    precio=str(input("Ingrese el precio de venta:"))
                    tot = float(precio)
                    fecha_vta = datetime.date.today()
                    suma = (tot*unidades_venta)
                    monto_total = suma + monto_total
                    valores = {"clave": clave, "nombre":descripcion, "unidades": unidades_venta, "precio": precio, "fecha": fecha_vta, "idcuenta": clave_total}
                    c.execute("INSERT INTO venta VALUES(:clave, :nombre, :unidades, :precio, :fecha, :idcuenta)", valores)
            totales ={"clave_total": clave_total, "total": monto_total}
            c.execute("INSERT INTO totales VALUES(:clave_total, :total)",totales)
        #Saca el total de la cuenta para mostrarlo al cierre de cuenta
            c.execute("SELECT clave, total FROM totales WHERE clave = :clave_total",totales)
            cuenta_final = c.fetchall()
            for Id, total in cuenta_final:
                print(f"El total de la cuenta es de: ${total}")

        #Elaborado por Andrés Torres Montemayor
        def consulta():
            print (SEPARADOR)
            print("Consulta de ventas")
            print (SEPARADOR)

            cuenta = ("select count(clave) from venta")
            c.execute(cuenta)
            rtotales = c.fetchone()
            if rtotales:
                buscar=int(input("Ingrese la clave de venta a consultar:"))
                clave_buscar = {"clave_b":buscar}
                c.execute("SELECT clave, descripcion, piezas, precio, fecha_venta FROM venta WHERE idcuenta = :clave_b",clave_buscar)
                resultado = c.fetchall()
                for Id, nombre, cantidad, precio, fecha in resultado:
                    print(f"Se compraron {cantidad} piezas de {nombre} a un precio de ${precio} el día {fecha}")
            else:
                print("No existen ventas registradas")

        #Elaborado por Andrés Torres Montemayor
        def reporte():
            print (SEPARADOR)
            print("Consulta de ventas")
            print (SEPARADOR)

            cuenta = ("select count(clave) from venta")
            c.execute(cuenta)
            rtotales = c.fetchone()
            if rtotales:
                fecha_consultar = input("Dime una fecha (aaa-mm-dd): ")
                fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%Y-%m-%d").date()
                fecha_buscar = {"fecha_b":fecha_consultar}
                c.execute("SELECT clave, descripcion, piezas, precio, fecha_venta FROM venta WHERE DATE(fecha_venta) = :fecha_b",fecha_buscar)
                resultado = c.fetchall()
                print("Descripción | Piezas vendidas | Precio | Fecha")
                print("*" * 60)
                for Id, nombre, cantidad, precio, fecha in resultado:
                    print(f"{nombre}\t\t {cantidad}\t\t {precio}\t {fecha} ")
            else:
                print("No existen ventas registradas")

        #Elaborado por Javier Alejandro Álvarez Rios
        def menu():
            while (True):
                    LimpiarPantalla()
                    print (SEPARADOR)
                    print("COSMETICOS\n")
                    print (SEPARADOR)
                    print("[1] Registrar una venta.")
                    print("[2] Consultar una venta.")
                    print("[3] Generar reporte de venta.")
                    print("[4] Salir.")
                    opcion = int(input("Selecciona una opción  > "))
                    if opcion <= 4:
                        if opcion==1:
                            productos=cargar()

                        if opcion==2:
                            consulta()

                        if opcion==3:
                            reporte()

                        if opcion==4:
                            print("Gracias por utilizar el programa.")
                            break

                        input("Pulsa enter para continuar...")
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