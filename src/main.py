from .banco import Banco
from .database_manager import DatabaseManager

def mostrar_menu():
    print("\n--- Menú de Pruebas ---")
    print("1. Registrar cliente")
    print("2. Agregar cuenta")
    print("3. Realizar depósito")
    print("4. Realizar retiro")
    print("5. Realizar transferencia") 
    print("6. Mostrar tablas")
    print("7. Eliminar cuenta")
    print("8. Eliminar cliente")
    print("9. Ver historial de transacciones por cuenta")
    print("10. Ver historial de transacciones por cliente")
    print("11. Modificar cliente")
    print("12. Salir")
    print("-----------------------")

def main():
    db_manager = DatabaseManager("banco.db")  # Cambia a un archivo de base de datos persistente
    db_manager.crear_tablas()  # Crear las tablas necesarias
    banco = Banco(db_manager)  # Crear instancia de Banco

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1": # Opción de registro cliente
            nombre = input("Nombre del cliente: ")
            apellido = input("Apellido del cliente: ")
            email = input("Email del cliente: ")
            contrasena = input("Contraseña del cliente: ")
            cliente = banco.registrar_cliente(nombre, apellido, email, contrasena)
            print(f"Cliente registrado exitosamente con ID: {cliente.id_cliente}")  # Mensaje de depuració

        elif opcion == "2": # Opción de crear cuenta
            id_cliente = int(input("ID del cliente: "))
            tipo_cuenta = input("Tipo de cuenta (Ahorros/Corriente): ")
            saldo_inicial = float(input("Saldo inicial: "))
            nip = int(input("NIP de la cuenta: "))
            cliente = banco.obtener_cliente_por_id(id_cliente)  # aqui se obtiene el objeto cliente 

            if cliente:
                nueva_cuenta = banco.agregar_cuenta(cliente, tipo_cuenta, saldo_inicial, nip)#retornar objeto nuevacuenta
                print(f"Cuenta agregada: {nueva_cuenta}")
                # Muestra todas las cuentas del cliente
                todas_las_cuentas = cliente.obtener_cuentas()
                print("Cuentas del cliente después de agregar:")
                for cuenta in todas_las_cuentas:
                    print(cuenta)
            else:
                print("Cliente no encontrado.")

        elif opcion == "3": # Opción de depostio
            id_cuenta = int(input("ID de la cuenta: "))
            monto = float(input("Monto a depositar: "))
            cuenta = banco.obtener_cuenta_por_id(id_cuenta)  # Método que debes implementar en Banco
            if cuenta:
                banco.realizar_transaccion(cuenta, None, "Depósito", monto)
                print("Depósito realizado exitosamente.")
            else:
                print("Cuenta no encontrada.")

        elif opcion == "4": # Opción de retiro
            id_cuenta = int(input("ID de la cuenta: "))
            monto = float(input("Monto a retirar: "))
            cuenta = banco.obtener_cuenta_por_id(id_cuenta)  # Método que debes implementar en Banco
            if cuenta:
                try:
                    banco.realizar_transaccion(cuenta, None, "Retiro", monto)
                    print("Retiro realizado exitosamente.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Cuenta no encontrada.")

        elif opcion == "5":  # Opción de trasnferencia
            id_cuenta_origen = int(input("ID de la cuenta de origen: "))
            id_cuenta_destino = int(input("ID de la cuenta de destino: "))
            monto = float(input("Monto a transferir: "))

            cuenta_origen = banco.obtener_cuenta_por_id(id_cuenta_origen)  # Obtener la cuenta de origen
            cuenta_destino = banco.obtener_cuenta_por_id(id_cuenta_destino)  # Obtener la cuenta de destino

            if cuenta_origen and cuenta_destino:
                try:
                    # Realizar la transacción de tipo "Transferencia"
                    transaccion = banco.realizar_transaccion(cuenta_origen, cuenta_destino, "Transferencia", monto)
                    print(f"Transferencia realizada exitosamente. ID de la transacción: {transaccion.id_transaccion}")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Una de las cuentas no fue encontrada.")

        elif opcion == "6": # Opción de mostrar tablas
            print("Contenido de las tablas:")
            db_manager.mostrar_todas_las_tablas()  # Método para mostrar todas las tablas en la base de datos

        elif opcion == "7":  # Opción para eliminar cuenta
            id_cuenta = int(input("ID de la cuenta a eliminar: "))
            
            # Obtener la cuenta por su ID
            cuenta = banco.obtener_cuenta_por_id(id_cuenta)  
            if cuenta:
                # Acceder directamente al objeto cliente desde la cuenta
                cliente = cuenta.cliente  # Suponiendo que cuenta tiene un atributo cliente que es un objeto Cliente
                if cliente:
                    # Eliminar la cuenta pasando ambos, la cuenta y el cliente
                    banco.eliminar_cuenta(cuenta, cliente)
                    print(f"Cuenta con ID {cuenta.id_cuenta} eliminada exitosamente.")
                else:
                    print(f"No se encontró un cliente asociado para la cuenta con ID {cuenta.id_cuenta}.")
            else:
                print("Cuenta no encontrada.")

        elif opcion == "8":  # Opción para eliminar cliente
            id_cliente = int(input("ID del cliente a eliminar: "))
            cliente = banco.obtener_cliente_por_id(id_cliente)  # obtiene el objetco cliente con sus cuentas vinculadas solo con el id
            if cliente:
                print(f"Cliente encontrado: {cliente}")  # Muestra información del cliente
                cuentas = cliente.obtener_cuentas()  # Obtiene cuentas

                # Depuración para verificar que tienes objetos Cuenta y no IDs
                for cuenta in cuentas:
                    print(f"Cuenta: {cuenta}, Tipo: {type(cuenta)}")  # Verificar que sea un objeto Cuenta
                
                if cuentas:
                    print(f"El cliente tiene {len(cuentas)} cuentas.")
                else:
                    print("El cliente no tiene cuentas registradas.")
                
                # Confirmar eliminación
                confirmacion = input("¿Está seguro de que desea eliminar este cliente? (s/n): ")
                if confirmacion.lower() == 's':
                    banco.eliminar_cliente(cliente)  
                    print(f"Cliente con ID {cliente.id_cliente} eliminado exitosamente.")
                else:
                    print("Eliminación cancelada.")
            else:
                print("Cliente no encontrado.")

        elif opcion == "9":  # Ver historial de transacciones por cuenta
            id_cuenta = int(input("ID de la cuenta: "))
            cuenta = banco.obtener_cuenta_por_id(id_cuenta)
            if cuenta:
                transacciones = banco.obtener_historial_transacciones_por_cuenta(cuenta)
                if transacciones:
                    print(f"Historial de transacciones para la cuenta {id_cuenta}:")
                    db_manager.mostrar_tabla("Transacciones", transacciones)  # Muestra las transacciones en formato tabular
                    #for transaccion in transacciones:
                        #print(transaccion)  # Aquí puedes mostrar el detalle de cada transacción
                
                else:
                    print("No se encontraron transacciones para esta cuenta.")
            else:
                print("Cuenta no encontrada.")
        
        elif opcion == "10":  # Ver historial de transacciones por cliente
            id_cliente = int(input("ID del cliente: "))
            cliente = banco.obtener_cliente_por_id(id_cliente)
            if cliente:
                print(f"Historial de transacciones para el cliente {cliente.id_cliente}:")
                cuentas_cliente = cliente.obtener_cuentas()
            
                if cuentas_cliente:
                    print(f"Cuentas actuales del cliente: {[cuenta.id_cuenta for cuenta in cuentas_cliente]}")
                    for cuenta in cuentas_cliente:
                        transacciones = banco.obtener_historial_transacciones_por_cuenta(cuenta)
                        if transacciones:
                            print(f"Historial de transacciones para la cuenta {cuenta.id_cuenta}:")
                            db_manager.mostrar_tabla("Transacciones", transacciones)  # Muestra las transacciones en formato tabular              
                else:
                        print("No se encontraron transacciones para esta cuenta.")
            else:
                print("Cuenta no encontrada.")
        
        elif opcion == "11":  # Modificar cliente
            id_cliente = int(input("ID del cliente a modificar: "))
            cliente = banco.obtener_cliente_por_id(id_cliente)
            
            if cliente:
                print(f"Cliente encontrado: {cliente}")

                # Preguntar qué campo desea modificar
                print("¿Qué campo deseas modificar?")
                print("1. Nombre")
                print("2. Apellido")
                print("3. email")
                print("4. Contraseña")
                print("5. Todos los campos")
                campo_opcion = input("Selecciona una opción (1-5): ")

                # Inicializar variables para los nuevos datos
                nuevo_nombre = cliente.nombre
                nuevo_apellido = cliente.apellido
                nuevo_correo = cliente.email
                nueva_contrasena = cliente.contrasena
                
                if campo_opcion == "1":
                    nuevo_nombre = input(f"Nombre actual: {cliente.nombre}. Nuevo nombre: ")
                elif campo_opcion == "2":
                    nuevo_apellido = input(f"Apellido actual: {cliente.apellido}. Nuevo apellido: ")
                elif campo_opcion == "3":
                    nuevo_correo = input(f"email actual: {cliente.email}. Nuevo email: ")
                elif campo_opcion == "4":
                    nueva_contrasena = input(f"Contraseña actual: {cliente.contrasena}. Nueva contraseña: ")
                elif campo_opcion == "5":
                    nuevo_nombre = input(f"Nombre actual: {cliente.nombre}. Nuevo nombre: ")
                    nuevo_apellido = input(f"Apellido actual: {cliente.apellido}. Nuevo apellido: ")
                    nuevo_correo = input(f"email actual: {cliente.email}. Nuevo email: ")
                    nueva_contrasena = input(f"Contraseña actual: {cliente.contrasena}. Nueva contraseña: ")
                else:
                    print("Opción no válida. No se realizarán cambios.")
                    return

                # Llamar al método de modificar cliente, pasando los nuevos datos
                banco.modificar_cliente(
                    cliente,
                    nombre=nuevo_nombre if nuevo_nombre else None,
                    apellido=nuevo_apellido if nuevo_apellido else None,
                    email=nuevo_correo if nuevo_correo else None,
                    contrasena=nueva_contrasena if nueva_contrasena else None
                )
                print("Cliente modificado exitosamente.")
            else:
                print("Cliente no encontrado.")


        elif opcion == "12":
            print("Saliendo del menú.")
            break

        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
