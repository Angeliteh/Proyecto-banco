import unittest
from src.banco import Banco
from src.cliente import Cliente
from src.cuenta import Cuenta
from src.database_manager import DatabaseManager

class TestBanco(unittest.TestCase):

    def setUp(self):
        # Utilizamos la base de datos en memoria para las pruebas
        self.db_manager = DatabaseManager(":memory:")
        # Crear las tablas necesarias para las pruebas
        self.db_manager.crear_tablas()
        
        # Crear una instancia de Banco
        self.banco = Banco(self.db_manager)

        # Crear un cliente
        self.cliente = Cliente(None, "Juan", "Pérez", "juan@example.com", "password123")
        self.banco.registrar_cliente(self.cliente.nombre, self.cliente.apellido, self.cliente.email, self.cliente.contrasena)
        
        # Crear cuentas para el cliente
        self.cuenta_ahorros = self.banco.agregar_cuenta(self.cliente, tipo_cuenta="Ahorros", saldo_inicial=1000, nip=1111)
        self.cuenta_corriente = self.banco.agregar_cuenta(self.cliente, tipo_cuenta="Corriente", saldo_inicial=500, nip=1111)
    """
    #def test_registrar_cliente(self):
        # Registrar un nuevo cliente
        nuevo_cliente = Cliente(None, "Carlos", "Gómez", "carlos@example.com", "pass456")
        self.banco.registrar_cliente(nuevo_cliente.nombre, nuevo_cliente.apellido, nuevo_cliente.email, nuevo_cliente.contrasena)
        
        # Obtener el cliente recién registrado desde la base de datos
        clientes = self.db_manager.obtener_clientes()
        
        # Verificar que el cliente fue registrado correctamente
        self.assertEqual(len(clientes), 2)  # Ya existe un cliente creado en setUp
        self.assertEqual(clientes[1][1], "Carlos")
        self.assertEqual(clientes[1][2], "Gómez")
        self.assertEqual(clientes[1][3], "carlos@example.com")

    #def test_registrar_transaccion(self):
        # Realizar un depósito en la cuenta de ahorros
        self.banco.realizar_transaccion(self.cuenta_ahorros, None, "Depósito", 300)
        
        # Obtener todas las transacciones desde la base de datos
        transacciones = self.db_manager.obtener_transacciones()
        
        # Verificar que la transacción fue registrada correctamente
        self.assertEqual(len(transacciones), 1)
        self.assertEqual(transacciones[0][3], "Depósito")  # Tipo de transacción
        self.assertEqual(transacciones[0][4], 300)  # Monto de la transacción
        self.assertEqual(transacciones[0][1], self.cuenta_ahorros.id_cuenta)  # ID de la cuenta origen
        self.assertIsNone(transacciones[0][2])  # ID de la cuenta destino (es None porque es un depósito)

    #def test_agregar_cuenta(self):
        # Crear una nueva cuenta para el cliente
        nueva_cuenta = self.banco.agregar_cuenta(self.cliente, tipo_cuenta="Ahorros", saldo_inicial=2000, nip=1234)
        
        # 1. Verificar que la cuenta fue añadida al objeto cliente
        cuentas_cliente = self.cliente.obtener_cuentas()  # Usar el método del objeto Cliente
        self.assertEqual(len(cuentas_cliente), 3)  # Ya tiene dos cuentas del setUp + la nueva
        self.assertIn(nueva_cuenta, cuentas_cliente)  # Verificar que la nueva cuenta está en la lista

        # 2. Verificar que la cuenta fue añadida correctamente en la base de datos
        cuentas_db = self.db_manager.obtener_cuentas()
        self.assertEqual(len(cuentas_db), 3)  # Ya existen dos cuentas creadas en setUp
        self.assertEqual(cuentas_db[2][2], "Ahorros")  # Tipo de cuenta
        self.assertEqual(cuentas_db[2][3], 2000)  # Saldo inicial
        self.assertEqual(cuentas_db[2][4], "1234")  # NIP

    #def test_agregar_cuenta_a_cliente(self):
        self.cliente.cuentas = []  # Limpiar la lista de cuentas
        # Crear una cuenta para el cliente
        nueva_cuenta = self.banco.agregar_cuenta(self.cliente, tipo_cuenta="Ahorros", saldo_inicial=5000, nip=1234)
        
        # Verificar que la cuenta esté en la lista del cliente
        self.assertIn(nueva_cuenta, self.cliente.obtener_cuentas())
        self.assertEqual(len(self.cliente.obtener_cuentas()), 1)  # Dependiendo de cuántas cuentas tenga
    """
    def test_eliminar_cuenta(self):
        cuentas_db_iniciales = self.db_manager.obtener_cuentas()
        print("Cuentas iniciales:", cuentas_db_iniciales)

        # Eliminar la cuenta de ahorros
        self.banco.eliminar_cuenta(self.cuenta_ahorros.id_cuenta)
        
        
        # Verificar que la cuenta ha sido eliminada de la base de datos
        cuentas_db = self.db_manager.obtener_cuentas()
        self.assertEqual(len(cuentas_db), 1)  # Debería quedar solo una cuenta

        # Verificar que no queden transacciones asociadas a la cuenta eliminada
        transacciones_db = self.db_manager.obtener_transacciones_por_cuenta(self.cuenta_ahorros.id_cuenta)
        self.assertEqual(len(transacciones_db), 0)  # No debería quedar ninguna transacción
        
    
    def test_eliminar_cliente(self):
        # Supongamos que ya tienes un cliente registrado y con cuentas.
        id_cliente = self.cliente.id_cliente  # O el ID que corresponda a tu cliente
        
        # Eliminar el cliente
        self.banco.eliminar_cliente(id_cliente)
        
        # Verificar que no queden cuentas asociadas a ese cliente
        cuentas_db = self.db_manager.obtener_cuentas_por_cliente(id_cliente)
        self.assertEqual(len(cuentas_db), 0)  # No debería quedar ninguna cuenta

        # Verificar que no queden transacciones asociadas a ese cliente
        transacciones_db = self.db_manager.obtener_transacciones_por_cliente(id_cliente)
        self.assertEqual(len(transacciones_db), 0)  # No debería quedar ninguna transacción


    """
    #def test_realizar_deposito(self):
        # Realizar un depósito en la cuenta de ahorros
        self.banco.realizar_transaccion(self.cuenta_ahorros, None, "Depósito", 500)
        self.assertEqual(self.cuenta_ahorros.saldo, 1500)
        
        # Verificar que la transacción se registró correctamente
        transacciones = self.db_manager.obtener_transacciones()
        self.assertEqual(len(transacciones), 1)
        self.assertEqual(transacciones[0][3], "Depósito")  # Tipo de transacción

    #def test_realizar_retiro(self):
        # Realizar un depósito
        self.banco.realizar_transaccion(self.cuenta_ahorros, None, "Depósito", 500)
        # Realizar un retiro
        self.banco.realizar_transaccion(self.cuenta_ahorros, None, "Retiro", 200)
        self.assertEqual(self.cuenta_ahorros.saldo, 1300)
        
        # Verificar que la transacción se registró correctamente
        transacciones = self.db_manager.obtener_transacciones()
        self.assertEqual(len(transacciones), 2)  # Dos transacciones en total
        self.assertEqual(transacciones[1][3], "Retiro")  # Tipo de transacción
    
    #def test_realizar_transferencia(self):
        # Realizar una transferencia desde la cuenta de ahorros a la cuenta corriente
        self.banco.realizar_transaccion(self.cuenta_ahorros, self.cuenta_corriente, "Transferencia", 300)
        
        # Verificar saldos después de la transferencia
        self.assertEqual(self.cuenta_ahorros.saldo, 700)  # Saldo de la cuenta de ahorros reducido
        self.assertEqual(self.cuenta_corriente.saldo, 800)  # Saldo de la cuenta corriente aumentado
        
        # Verificar que la transacción fue registrada correctamente
        transacciones = self.db_manager.obtener_transacciones()
        self.assertEqual(len(transacciones), 1)
        self.assertEqual(transacciones[0][3], "Transferencia")  # Tipo de transacción
        self.assertEqual(transacciones[0][4], 300)  # Monto transferido
        self.assertEqual(transacciones[0][1], self.cuenta_ahorros.id_cuenta)  # ID de la cuenta origen
        self.assertEqual(transacciones[0][2], self.cuenta_corriente.id_cuenta)  # ID de la cuenta destino
    """
if __name__ == '__main__':
    unittest.main()
