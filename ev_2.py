#Registro del detalle de ventas un negocio de ferretería
#Requerimientos funcionales:
#Se debe ofrecer un menú navegable con las siguientes opciones: Registrar una venta Consultar una venta Salir
import os
import datetime
import pandas as pd
LimpiarPantalla = lambda: os.system('cls')
SEPARADOR = ("*" * 20) + "\n"
totales={}
productos={}
fechas={}
reportes={}

#Elaborado por Javier Alejandro Álvarez Rios
def cargar():
    cuenta=[]
    total=[]
    fecha=[]
    monto_total = 0
    print (SEPARADOR)
    print("Registro de ventas")
    print (SEPARADOR)
    print("**Para finalizar la cuenta basta con dejar en blanco la descripcion del artículo**")

    while True:
        if productos:
            clave = max(productos) + 1
        else:
            clave = 1
        descripcion=input("Ingrese la descripcion:")
        if descripcion == "":
            break
        else:
            unidades_venta=int(input("Unidades vendidas:"))
            precio=float(input("Ingrese el precio de venta:"))
            diav= datetime.date.today()
            dia = str(diav)
            cuenta.append((descripcion,unidades_venta,precio,dia))
            suma = (precio*unidades_venta)
            monto_total = suma + monto_total
    print("El total a pagar es de $",monto_total," y la clave de cuenta es: ",clave)
    total.append(monto_total)
    totales[clave]=total
    productos[clave]=cuenta
    reportes[clave]=(cuenta,dia)
    return productos

#Elaborado por Andrés Torres Montemayor
def consulta(productos):
    print (SEPARADOR)
    print("Consulta de ventas")
    print (SEPARADOR)

    if productos:
        buscar=int(input("Ingrese la clave de venta a consultar:"))
        if buscar in productos.keys():
            for articulo,unidades,precio,fecha in productos[buscar]:
                print("Articulo: ",articulo,"\nUnidades vendidas: ",unidades,"\nPrecio por unidad: ",precio,"\nFecha de venta: ",fecha)
            for total in totales[buscar]:
                print("El total de la cuenta fue de: $",total)
        else:
            print("No se encontro la venta deseada.")
    else:
        print("No existen ventas registradas")

#Elaborado por Andrés Torres Montemayor
def reporte(reportes,productos):
    lista=[]
    print (SEPARADOR)
    print("Consulta de ventas")
    print (SEPARADOR)

    print(reportes)
    if productos:
        buscar=input("Ingrese la fecha deseada para el reporte(aaa-mm-dd):")
        for x in reportes:
            if buscar in reportes[x]:
                lista.append(productos[x])
        archivo = pd.DataFrame(lista)
        archivo.to_csv (r'reporte.csv',index=False, header=True)
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
                    consulta(productos)

                if opcion==3:
                    reporte(reportes,productos)

                if opcion==4:
                    print("Gracias por utilizar el programa.")
                    break

                input("Pulsa enter para continuar...")
            else:
                print("Esa respuesta no es válida.")
                input("Pulsa enter para continuar...")


menu()


