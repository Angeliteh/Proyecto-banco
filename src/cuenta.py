

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

    