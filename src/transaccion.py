class Transaccion:
    def __init__(self, id_transaccion, cuenta_origen, cuenta_destino, tipo_transaccion, monto, fecha):
        self.id_transaccion = id_transaccion
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino
        self.tipo_transaccion = tipo_transaccion
        self.monto = monto
        self.fecha = fecha

    
