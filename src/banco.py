from .transaccion import Transaccion
from .cliente import Cliente
from .cuenta import Cuenta
from .database_manager import DatabaseManager
from datetime import datetime


class Banco:
    def __init__(self, db_manager):
        self.db_manager = db_manager


                        #OPERACIONES/LOGICA DEL BANCO 
    
    def obtener_cliente_por_id(self, id_cliente):
        """Obtiene un objeto Cliente a partir de su ID."""
        cliente_data = self.db_manager.obtener_cliente_por_id(id_cliente)
        if cliente_data:
            cliente = Cliente(*cliente_data)  # Desempaquetamos los resultados en el constructor de Cliente

            # Aquí llamamos al método que obtiene las cuentas desde la base de datos y las vinculamos al cliente
            cliente_actualizado = self.obtener_cliente_con_cuentas_DB(cliente)

            cuentas = cliente_actualizado.obtener_cuentas()
            print(f"B_Obteniendo cuentas para el cliente id: {cliente_actualizado.id_cliente}")  # Depuración
            if cuentas:
                print(f"B_El cliente tiene {len(cuentas)} cuentas: {[str(cuenta) for cuenta in cuentas]}")
            else:
                print("B_El cliente no tiene cuentas registradas.")  # Comprobar si no hay cuentas
            return cliente_actualizado
        return None  # Si no se encuentra, retornamos None
        
    def obtener_cuenta_por_id(self, id_cuenta):
        """Obtiene un objeto Cuenta a partir de su ID."""
        cuenta_data = self.db_manager.obtener_cuenta_por_id(id_cuenta)
        if cuenta_data:
            # Extraer los valores necesarios de cuenta_data
            id_cuenta = cuenta_data[0]
            id_cliente = cuenta_data[1]
            tipo_cuenta = cuenta_data[2]
            saldo = cuenta_data[3]
            nip = cuenta_data[4]
            
            # Obtener el cliente asociado
            cliente = self.obtener_cliente_por_id(id_cliente)
            
            # Crear y retornar el objeto Cuenta
            cuenta = Cuenta(id_cuenta, cliente, tipo_cuenta, saldo, nip)
            return cuenta
        return None  # Si no se encuentra, retornamos None
    
    def realizar_transaccion(self, cuenta_origen, cuenta_destino, tipo_transaccion, monto):
        # Realiza el depósito o retiro según el tipo de transacción
        if tipo_transaccion == "Depósito":
            cuenta_origen.realizar_deposito(monto)
            # Actualiza el saldo en la base de datos
            self.db_manager.actualizar_saldo(cuenta_origen.id_cuenta, cuenta_origen.saldo)
        elif tipo_transaccion == "Retiro":
            cuenta_origen.realizar_retiro(monto)
            # Actualiza el saldo en la base de datos
            self.db_manager.actualizar_saldo(cuenta_origen.id_cuenta, cuenta_origen.saldo)
        elif tipo_transaccion == "Transferencia":
            cuenta_origen.realizar_retiro(monto)
            cuenta_destino.realizar_deposito(monto)
            # Actualiza el saldo en la base de datos para ambas cuentas
            self.db_manager.actualizar_saldo(cuenta_origen.id_cuenta, cuenta_origen.saldo)
            self.db_manager.actualizar_saldo(cuenta_destino.id_cuenta, cuenta_destino.saldo)

        # Crear una instancia de Transaccion sin ID inicial se geenra autoimatico
        transaccion = Transaccion(
            id_transaccion=None,  
            cuenta_origen=cuenta_origen,
            cuenta_destino=cuenta_destino,
            tipo_transaccion=tipo_transaccion,
            monto=monto,
            fecha=datetime.now()
        )

        transaccion.id_transaccion = self.db_manager.registrar_transaccion(
            cuenta_origen.id_cuenta,
            cuenta_destino.id_cuenta if cuenta_destino else None,
            transaccion.tipo_transaccion,
            transaccion.monto,
            transaccion.fecha
        )

        return transaccion

    def registrar_cliente(self, nombre, apellido, email, contrasena):
        # Crear el cliente
        nuevo_cliente = Cliente(None, nombre, apellido, email, contrasena)
        print(f"B_Registrando cliente: {nuevo_cliente.nombre} {nuevo_cliente.apellido} ({nuevo_cliente.email})")  # Depuración
        # Llamar al método del DatabaseManager pasando los atributos
        nuevo_cliente.id_cliente = self.db_manager.registrar_cliente(
            nuevo_cliente.id_cliente,
            nuevo_cliente.nombre,
            nuevo_cliente.apellido,
            nuevo_cliente.email,
            nuevo_cliente.contrasena
        )
        if nuevo_cliente.id_cliente:  # Verificar si se asignó un ID
            print(f"B_Cliente registrado con ID: {nuevo_cliente.id_cliente}")  # Depuración
        else:
            print("B_Error al registrar el cliente.")  # Comprobación de errores
        print(f"Cliente creado: {nuevo_cliente.nombre} {nuevo_cliente.apellido} con ID {nuevo_cliente.id_cliente} y cuentas {nuevo_cliente.cuentas}")
        return nuevo_cliente  # Se retorna el objeto Cliente creado ya tiene el id asignado
    
    def agregar_cuenta(self, cliente, tipo_cuenta, saldo_inicial, nip):
        """Crea una nueva cuenta para el cliente y la agrega a la base de datos y al objeto Cliente."""
        print(f"Creando nueva cuenta para el cliente con ID {cliente.id_cliente}")  # Depuración
        # Crear la cuenta sin ID inicial
        nueva_cuenta = Cuenta(None, cliente, tipo_cuenta, saldo_inicial, nip)
        
        # Llamar al método del DatabaseManager pasando los atributos y recuperar el ID generado
        nueva_cuenta.id_cuenta = self.db_manager.agregar_cuenta(
            cliente.id_cliente,
            nueva_cuenta.tipo_cuenta,
            nueva_cuenta.saldo,
            nueva_cuenta.nip
        )
        print(f"B_ cuenta creada: ID: {nueva_cuenta.id_cuenta}, Tipo: {nueva_cuenta.tipo_cuenta}, Saldo: {nueva_cuenta.saldo}, NIP: {nueva_cuenta.nip}")

        # Aquí agregamos la cuenta a la lista de cuentas del cliente
        cliente.agregar_cuenta(nueva_cuenta)
        cuentas_cliente = cliente.obtener_cuentas()
        print(f"B_Cuentas del cliente después de agregar: {[str(cuenta) for cuenta in cuentas_cliente]}")  # Mostrar todas las cuentas

        return nueva_cuenta  # Se retorna la cuenta creada con el ID asignado
    
    def buscar_cliente(self, id_cliente):
        cliente_data = self.db_manager.obtener_cliente_por_id(id_cliente)
        if cliente_data:
            return Cliente(*cliente_data)  # Desempaqueta el tuple en el constructor de Cliente
        return None  # Retorna None si no se encuentra el cliente

    def buscar_cuenta(self, id_cuenta):
        return self.db_manager.obtener_cuenta_por_id(id_cuenta)

    def buscar_transaccion(self, id_transaccion):
        return self.db_manager.obtener_transaccion_por_id(id_transaccion)

    def modificar_cliente(self, cliente, nombre=None, apellido=None, email=None, contrasena=None):
        """Modifica la información de un cliente."""
        if cliente:
            print(f"B_Modificando cliente con ID {cliente.id_cliente}")

            # Almacenar cambios en un diccionario
            cambios = {}

            # Verificar y almacenar cambios en el diccionario solo para verificación
            if nombre is not None and nombre != cliente.nombre:
                cambios['Nombre'] = (cliente.nombre, nombre)
            if apellido is not None and apellido != cliente.apellido:
                cambios['Apellido'] = (cliente.apellido, apellido)
            if email is not None and email != cliente.email:
                cambios['email'] = (cliente.email, email)
            if contrasena is not None and contrasena != cliente.contrasena:
                cambios['Contraseña'] = (cliente.contrasena, contrasena)

            # Actualizar solo si hay cambios
            if cambios:
                # Llamar a DatabaseManager pasando los datos, no el objeto cliente
                self.db_manager.actualizar_cliente(cliente.id_cliente, 
                    nombre or cliente.nombre,
                    apellido or cliente.apellido,
                    email or cliente.email,
                    contrasena or cliente.contrasena
                )

                # **Actualizar el objeto cliente en memoria/objeto también**
                if 'Nombre' in cambios:
                    cliente.nombre = cambios['Nombre'][1]
                if 'Apellido' in cambios:
                    cliente.apellido = cambios['Apellido'][1]
                if 'email' in cambios:
                    cliente.email = cambios['email'][1]
                if 'Contraseña' in cambios:
                    cliente.contrasena = cambios['Contraseña'][1]

                # Mostrar solo los campos que se han modificado
                for campo, (anterior, nuevo) in cambios.items():
                    print(f"{campo} cambiado de '{anterior}' a '{nuevo}'.")
            else:
                print("No se han realizado cambios.")
        else:
            print("B_Cliente no válido.")





    def eliminar_cliente(self, cliente):
        """Elimina un cliente junto con todas sus cuentas y transacciones."""
        if cliente:
            print(f"B_Eliminando cliente con ID {cliente.id_cliente}")
            
            # Obtener las cuentas del cliente
            cuentas_cliente = cliente.obtener_cuentas()

            if cuentas_cliente:  # Solo procedemos si hay cuentas
                print(f"B_ Antes de iterar cuentas, cuentas actuales: {cuentas_cliente}")
                for cuenta in cuentas_cliente[:]:#GRAN ERROR SOLUCIONADO AQUI OSLAMENTE HAY QUE DUPLICAR LA  LISTA PORQUE POR ALGUNA RAZON NO FUNCIONA SI USAS LALISTA ORIGINAL 
                    print(f"B_Eliminando cuenta con ID {cuenta.id_cuenta} de cliente id {cliente.id_cliente}")  # Confirmación de que es un objeto Cuenta
                    self.eliminar_cuenta(cuenta, cliente)  # Usa tu método existente para eliminar cada cuenta
                
            
            # Finalmente, eliminar el cliente de la base de datos
            self.db_manager.eliminar_cliente(cliente.id_cliente)
            print(f"B_Cliente con ID {cliente.id_cliente} y todas sus cuentas/transacciones eliminadas.")
        else:
            print("B_Cliente no válido.")

    def eliminar_cuenta(self, cuenta, cliente):
        """Elimina una cuenta y actualiza al cliente."""
        print(f"B_Eliminando cuenta con ID {cuenta.id_cuenta}")
        self.db_manager.eliminar_transacciones_por_cuenta(cuenta.id_cuenta)
        cliente.eliminar_cuenta(cuenta)  # Asegúrate de que cliente es un objeto, no un ID
        self.db_manager.eliminar_cuenta(cuenta.id_cuenta)
        print(f"B_Cuenta con ID {cuenta.id_cuenta} eliminada.")
        

    def eliminar_transaccion(self, transaccion):
        transaccion = self.buscar_transaccion(transaccion.id_transaccion)
        if transaccion:
            self.db_manager.eliminar_transaccion(transaccion.id_transaccion)  # Asumiendo que tienes este método
            print(f"Transacción con ID {transaccion.id_transaccion} eliminada.")
        else:
            print(f"No se encontró la transacción con ID {transaccion.id_transaccion}.")


    def obtener_cliente_con_cuentas_DB(self, cliente):
        """Vincula las cuentas del cliente desde la base de datos al objeto Cliente."""
        if cliente:
            cuentas_cliente = self.db_manager.obtener_cuentas_por_cliente(cliente.id_cliente)
            
            # Asocia cada cuenta obtenida al cliente
            for cuenta_data in cuentas_cliente[:]:
                cuenta = Cuenta(*cuenta_data)  # Desempaqueta los datos en un objeto Cuenta
                cliente.agregar_cuenta(cuenta)  # Agrega la cuenta al cliente

        return cliente


    def obtener_historial_transacciones_por_cuenta(self, cuenta):
        # Aquí la lógica para interactuar con el db_manager y obtener las transacciones
        transacciones_data = self.db_manager.obtener_transacciones_por_cuenta(cuenta.id_cuenta)
        
        # Puedes procesar `transacciones_data` para convertirlas en objetos Transaccion
        #transacciones = [Transaccion(*data) for data in transacciones_data]
        
        return transacciones_data
