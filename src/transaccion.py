class Transaccion:
    def __init__(self, id_transaccion, cuenta_origen, cuenta_destino, tipo_transaccion, monto, fecha):
        self.id_transaccion = id_transaccion
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino
        self.tipo_transaccion = tipo_transaccion
        self.monto = monto
        self.fecha = fecha

    def __str__(self):
        return f"Transacción ID: {self.id_transaccion}, Tipo: {self.tipo_transaccion}, Monto: {self.monto}, Fecha: {self.fecha}"
