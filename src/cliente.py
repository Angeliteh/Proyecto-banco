class Cliente:
    def __init__(self, id_cliente, nombre, apellido, email, contrasena):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self._contrasena = contrasena
        self.cuentas = []
            
    def __str__(self):
        """Devuelve una representación en cadena del cliente."""
        return f"{self.nombre} {self.apellido} {self.email} "
    
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
    
    # Getter para email
    @property
    def email(self):
        return self._email

    # Setter para email con validación
    @email.setter
    def email(self, nuevo_email):
        if "@" not in nuevo_email or "." not in nuevo_email:
            raise ValueError("El formato del email es inválido.")
        self._email = nuevo_email
    
    # Getter para contrasena
    @property
    def contrasena(self):
        return self._contrasena
    
    # Setter para contrasena con validación
    @contrasena.setter
    def contrasena(self, nueva_contrasena):
        if len(nueva_contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        self._contrasena = nueva_contrasena