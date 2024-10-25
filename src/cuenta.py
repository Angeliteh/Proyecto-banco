
class Cuenta:
    def __init__(self, id_cuenta, cliente, tipo_cuenta, saldo, nip):
        self.id_cuenta = id_cuenta
        self.cliente = cliente
        self.tipo_cuenta = tipo_cuenta
        self.saldo = saldo
        self.nip = nip

    def __repr__(self):
        """Devuelve una representación en cadena de la cuenta."""
        return f"Cuenta {self.id_cuenta}: {self.tipo_cuenta}, Saldo: {self.saldo}"
    
    def realizar_deposito(self, monto):
        print(f"Saldo desde objeto cliente = {self.saldo} de cuenta {self.id_cuenta}")
        self.saldo += monto
        print(f"nuevo actualizado desde objeto cliente = {self.saldo} de cuenta {self.id_cuenta}")

    def realizar_retiro(self, monto):
        if monto <= self.saldo:
            print(f"Saldo desde objeto cliente = {self.saldo} de cuenta {self.id_cuenta}")
            self.saldo -= monto
            print(f"nuevo actualizado desde objeto cliente = {self.saldo} de cuenta {self.id_cuenta}")
        else:
            raise ValueError("Saldo insuficiente.")

    # Getter para saldo
    @property
    def saldo(self):
        return self._saldo
    
    # Setter para saldo con validación
    @saldo.setter
    def saldo(self, nuevo_saldo):
        if nuevo_saldo < 0:
            raise ValueError("El saldo no puede ser negativo.")
        self._saldo = nuevo_saldo

    # Getter para nip
    @property
    def nip(self):
        return self._nip

    # Setter para nip con validación
    @nip.setter
    def nip(self, nuevo_nip):
        if len(str(nuevo_nip)) != 4 or not str(nuevo_nip).isdigit():
            raise ValueError("El NIP debe ser un número de 4 dígitos.")
        self._nip = nuevo_nip