class Cliente:
    def __init__(self, id_cliente, nombre, apellido, email, contrasena):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasena = contrasena
        self.cuentas = []
        
    def __str__(self):
        """Devuelve una representación en cadena del cliente."""
        return f"{self.nombre} {self.apellido} ({self.email})"
    
    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)
        print(f"Cl_ Cuenta con ID {cuenta.id_cuenta} agregada al cliente con ID {self.id_cliente}")
        cuentas_totales = self.obtener_cuentas()
        print (f"cuentas asociadas actuales:{cuentas_totales}")

    def eliminar_cuenta(self, cuenta):
        """Elimina una cuenta del cliente."""
        if cuenta in self.cuentas:
            self.cuentas.remove(cuenta)
            print(f"Cuenta con ID {cuenta.id_cuenta} eliminada del cliente.")
        else:
            print("La cuenta no existe en la lista de cuentas del cliente.")

    def obtener_cuentas(self):
        print(f"Cl_Obteniendo cuentas del cliente con ID {self.id_cliente}")  # Depuración
        return self.cuentas  # Solo devuelve la lista de cuentas

    
