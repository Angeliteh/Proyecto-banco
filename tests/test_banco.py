import unittest
from src.banco import Banco
from src.cliente import Cliente
from src.cuenta import Cuenta
from src.database_manager import DatabaseManager

class TestBanco(unittest.TestCase):

    def setUp(self):
        # Inicializar DatabaseManager y Banco antes de cada prueba
        self.db_manager = DatabaseManager(":memory:")  # Usar base de datos en memoria para pruebas
        self.db_manager.crear_tablas()
        self.banco = Banco(self.db_manager)

        # Registrar cliente de prueba
        self.cliente = Cliente(None, "Juan", "Pérez", "juan@example.com", "password123")
        self.banco.registrar_cliente(self.cliente.nombre, self.cliente.apellido, self.cliente.email, self.cliente.contrasena)
        self.cuenta_ahorros = self.banco.agregar_cuenta(self.cliente, "Ahorros", 1000, 1111)

    def test_registrar_cliente(self):
        # Probar que el cliente se registra correctamente
        nuevo_cliente = Cliente(None, "Carlos", "Gómez", "carlos@example.com", "pass456")
        self.banco.registrar_cliente(nuevo_cliente.nombre, nuevo_cliente.apellido, nuevo_cliente.email, nuevo_cliente.contrasena)
        clientes = self.db_manager.obtener_clientes()
        self.assertEqual(len(clientes), 2)  # Debería haber 2 clientes

    def test_realizar_deposito(self):
        # Probar realizar depósito en cuenta de ahorros
        self.banco.realizar_transaccion(self.cuenta_ahorros, None, "Depósito", 500)
        self.assertEqual(self.cuenta_ahorros.saldo, 1500)  # Saldo debe ser 1500

    def test_realizar_retiro(self):
        # Probar que se realiza un retiro correctamente
        self.cuenta_ahorros.realizar_retiro(300)
        self.assertEqual(self.cuenta_ahorros.saldo, 700)  # Saldo debe ser 700 después del retiro

        # Probar que lanza una excepción con saldo insuficiente
        with self.assertRaises(ValueError):
            self.cuenta_ahorros.realizar_retiro(800)

    def test_eliminar_cuenta(self):
        # Probar la eliminación de una cuenta
        self.banco.eliminar_cuenta(self.cuenta_ahorros, self.cliente)
        cuentas_db = self.db_manager.obtener_cuentas()
        self.assertEqual(len(cuentas_db), 0)  # No debería haber cuentas

    def test_eliminar_cliente(self):
        # Probar la eliminación de un cliente y sus cuentas
        self.banco.eliminar_cliente(self.cliente.id_cliente)
        cuentas_db = self.db_manager.obtener_cuentas_por_cliente(self.cliente.id_cliente)
        self.assertEqual(len(cuentas_db), 0)  # No debería haber cuentas del cliente eliminado

    def test_setter_y_getter_email(self):
        # Probar el setter y getter de email
        self.cliente.email = "nuevo_email@example.com"
        self.assertEqual(self.cliente.email, "nuevo_email@example.com")

        # Probar que lanza una excepción con un email inválido
        with self.assertRaises(ValueError):
            self.cliente.email = "email_invalido"

    def test_setter_y_getter_nip(self):
        # Probar el setter y getter de NIP
        self.cuenta_ahorros.nip = 1234
        self.assertEqual(self.cuenta_ahorros.nip, 1234)

        # Probar que lanza una excepción con un NIP inválido
        with self.assertRaises(ValueError):
            self.cuenta_ahorros.nip = 123  # NIP debe ser de 4 dígitos

if __name__ == '__main__':
    unittest.main()
