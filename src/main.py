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
    print("9. Salir")
    print("-----------------------")

def main():
    db_manager = DatabaseManager("banco.db")  # Cambia a un archivo de base de datos persistente
    db_manager.crear_tablas()  # Crear las tablas necesarias
    banco = Banco(db_manager)  # Crear instancia de Banco

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre del cliente: ")
            apellido = input("Apellido del cliente: ")
            email = input("Email del cliente: ")
            contrasena = input("Contraseña del cliente: ")
            cliente = banco.registrar_cliente(nombre, apellido, email, contrasena)
            print(f"Cliente registrado exitosamente con ID: {cliente.id_cliente}")  # Mensaje de depuració

        elif opcion == "2":
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

        elif opcion == "3":
            id_cuenta = int(input("ID de la cuenta: "))
            monto = float(input("Monto a depositar: "))
            cuenta = banco.obtener_cuenta_por_id(id_cuenta)  # Método que debes implementar en Banco
            if cuenta:
                banco.realizar_transaccion(cuenta, None, "Depósito", monto)
                print("Depósito realizado exitosamente.")
            else:
                print("Cuenta no encontrada.")

        elif opcion == "4":
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

        elif opcion == "5":  # Opción de transferencia
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


        elif opcion == "6":
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


        elif opcion == "8":
            print("Saliendo del menú.")
            break

        else:
            print("Opción no válida, por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
