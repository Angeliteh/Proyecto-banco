import sqlite3


class DatabaseManager:
    def __init__(self, db_name="banco.db"):
        self.db_name = db_name
        self.conexion = sqlite3.connect(self.db_name)  # Crear la conexión aquí
        self.crear_tablas()  # Crear tablas al inicializar

    def execute_query(self, query, params=None, fetch=False, return_lastrowid=False):
        cursor = self.conexion.cursor()  # Crear un nuevo cursor
        try:
            #print(f"EQ Ejecutando query: {query}")  # Mensaje de depuración para mostrar la consulta
            if params:
                #print(f"EQ Con parámetros: {params}")  # Mensaje de depuración para parámetros
                cursor.execute(query, params)
                #print(f"EQ query y params ejecutado")
            else:
                cursor.execute(query)

            # Si fetch es True, obtenemos los resultados
            if fetch:
                result = cursor.fetchall()
                #print(f"EQ fetch Resultados obtenidos: {result}")  # Depuración para mostrar los resultados
                return result  # Solo devolver resultados si fetch es True    
            
            # Si return_lastrowid es True, devolvemos el ID generado
            if return_lastrowid:
                lastrowid = cursor.lastrowid
                #print(f"EQ ID de la última fila insertada: {lastrowid}")  # Depuración del lastrowid
                self.conexion.commit()
                return lastrowid
        
            # Si solo es una operación normal, hacemos commit
            self.conexion.commit()
            #print("EQ Query ejecutada exitosamente y cambios confirmados.")  # Confirmación de éxito
        except Exception as e:
            print(f"EQ Error ejecutando query: {e}")  # Captura cualquier error
        finally:
            cursor.close()  # Cerrar el cursor explícitamente
            #print("EQ Cursor cerrado.")  # Mensaje de depuración para confirmar cierre de cursor
        
        
    def close(self):
        self.conexion.close()  # Cierra la conexión

    def crear_tablas(self):
        # Crear las tablas necesarias en la base de datos
        print(f"creando tablas...")
        queries = [
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                apellido TEXT,
                email TEXT,
                contrasena TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS cuentas (
                id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                tipo_cuenta TEXT,
                saldo REAL,
                nip TEXT,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transacciones (
                id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cuenta_origen INTEGER,
                id_cuenta_destino INTEGER,
                tipo_transaccion TEXT,
                monto REAL,
                fecha TEXT,
                FOREIGN KEY (id_cuenta_origen) REFERENCES cuentas(id_cuenta),
                FOREIGN KEY (id_cuenta_destino) REFERENCES cuentas(id_cuenta)
            )
            """
        ]
        for query in queries:
            self.execute_query(query)
        print("tablas creadas exitosamente")
    
    def mostrar_tabla(self, tabla, rows=None):
        """Muestra los datos de una tabla de la base de datos en formato tabular.
        Si se proporcionan filas, muestra solo esas filas; de lo contrario, muestra todas las filas de la tabla."""
        # Obtener la estructura de la tabla
        estructura = self.execute_query(f"PRAGMA table_info({tabla})", fetch=True)
        
        if estructura:
            # Obtener nombres de columnas
            headers = [columna[1] for columna in estructura]
            
            print(f"\nTabla {tabla}:")
            print("-" * (len(headers) * 15))  # Línea divisoria
            print(" | ".join(headers))  # Encabezados
            print("-" * (len(headers) * 15))  # Otra línea divisoria
            
            if rows is None:
                # Obtener los datos de la tabla
                query = f"SELECT * FROM {tabla}"
                rows = self.execute_query(query, fetch=True)
            
            if rows:
                # Imprimir cada fila de datos
                for row in rows:
                    print(" | ".join(str(value) for value in row))
            else:
                # En caso de no haber datos
                print("(No hay datos en la tabla)")
            print("-" * (len(headers) * 15))  # Línea final
        else:
            print(f"La tabla {tabla} no existe o está vacía.")

    def mostrar_todas_las_tablas(self):
        self.mostrar_tabla("clientes")
        
        self.mostrar_tabla("cuentas")
        
        self.mostrar_tabla("transacciones")      

    
    def registrar_cliente(self, id_cliente, nombre, apellido, email, contrasena):
        query = "INSERT INTO clientes (id_cliente, nombre, apellido, email, contrasena) VALUES (?, ?, ?, ?, ?)"
        params = (id_cliente, nombre, apellido, email, contrasena)
        
        return self.execute_query(query, params, return_lastrowid=True)  # Ejecutamos la query y retornamos el lastrowid

    def agregar_cuenta(self, id_cliente, tipo_cuenta, saldo, nip):
        query = "INSERT INTO cuentas (id_cliente, tipo_cuenta, saldo, nip) VALUES (?, ?, ?, ?)"
        params = (id_cliente, tipo_cuenta, saldo, nip)
        # Ejecutamos la query y retornamos el lastrowid
        return self.execute_query(query, params, return_lastrowid=True)

    def registrar_transaccion(self, id_cuenta_origen, id_cuenta_destino, tipo_transaccion, monto, fecha):
        print(f"Registrando transacción EN DB: {tipo_transaccion} - Monto: {monto} - Cuenta Origen: {id_cuenta_origen} - Cuenta Destino: {id_cuenta_destino}")
        query = "INSERT INTO transacciones (id_cuenta_origen, id_cuenta_destino, tipo_transaccion, monto, fecha) VALUES (?, ?, ?, ?, ?)"
        params = (id_cuenta_origen, id_cuenta_destino, tipo_transaccion, monto, fecha)
        return self.execute_query(query, params, return_lastrowid=True)

    def eliminar_cuenta(self, id_cuenta):
        query = "DELETE FROM cuentas WHERE id_cuenta = ?"
        self.execute_query(query, (id_cuenta,))
        print(f"Cuenta con ID {id_cuenta} eliminada de la DB")
        
    def eliminar_cliente(self, id_cliente):
        query = "DELETE FROM clientes WHERE id_cliente = ?"
        self.execute_query(query, (id_cliente,))
        print(f"Cliente con ID {id_cliente} eliminado de la DB.")

    def eliminar_transacciones_por_cuenta(self, id_cuenta):
        query = "DELETE FROM transacciones WHERE id_cuenta_origen = ? OR id_cuenta_destino = ?"
        self.execute_query(query, (id_cuenta, id_cuenta))

    def eliminar_transacciones_por_cliente(self, id_cliente):
        """Elimina todas las transacciones personales asociadas a un cliente."""
        query = "DELETE FROM transacciones WHERE id_cuenta_origen ? OR id_cuenta_destino = ?"
        self.execute_query(query, (id_cliente, id_cliente))

    def obtener_cliente_por_id(self, id_cliente):
        """Obtiene un cliente a partir de su ID."""
        query = "SELECT * FROM clientes WHERE id_cliente = ?"        
        result = self.execute_query(query, (id_cliente,), fetch=True)  # fetch=True para obtener un resultado
        if result:
            return result[0]  # Retorna la fila de la cuenta encontrada
        return None  # Si no se encuentra, retorna None
    
    def obtener_cuenta_por_id(self, id_cuenta):

        """Obtiene una cuenta a partir de su ID."""
        query = "SELECT * FROM cuentas WHERE id_cuenta = ?"
        result = self.execute_query(query, (id_cuenta,), fetch=True)
        if result:
            return result[0]  # Retorna la fila de la cuenta encontrada
        return None  # Si no se encuentra, retorna None
    
    def obtener_transaccion_por_id(self, id_transaccion):
        """Obtiene una transacción a partir de su ID."""
        query = "SELECT * FROM transacciones WHERE id_transaccion = ?"
        result = self.execute_query(query, (id_transaccion,), fetch=True)
        if result:
            return result[0]  # Retorna la fila de la transacción encontrada
        return None  # Si no se encuentra, retorna None
    
    def obtener_transacciones_por_cliente(self, id_cliente):
        query = """
        SELECT * FROM transacciones 
        WHERE id_cuenta_origen IN (SELECT id_cuenta FROM cuentas WHERE id_cliente = ?) OR 
            id_cuenta_destino IN (SELECT id_cuenta FROM cuentas WHERE id_cliente = ?)
        """
        return self.execute_query(query, (id_cliente, id_cliente), fetch=True)
    
    def obtener_transacciones_por_cuenta(self, id_cuenta):
        """Obtiene las transacciones asociadas a una cuenta dada."""
        query = "SELECT * FROM transacciones WHERE id_cuenta_origen = ? OR id_cuenta_destino = ?"
        return self.execute_query(query, (id_cuenta, id_cuenta), fetch=True)

    def obtener_cuentas_por_cliente(self, id_cliente):
        query = "SELECT * FROM cuentas WHERE id_cliente = ?"
        return self.execute_query(query, (id_cliente,), fetch=True)

    def obtener_cuentas(self):
        query = "SELECT * FROM cuentas"
        return self.execute_query(query, fetch=True)
    
    def obtener_clientes(self):
        query = "SELECT * FROM clientes"
        return self.execute_query(query, fetch=True)
    
    def obtener_transacciones(self):
        query = "SELECT * FROM transacciones"
        return self.execute_query(query, fetch=True)

    def actualizar_saldo(self, id_cuenta, nuevo_saldo):
            # Actualiza el saldo de la cuenta en la base de datos
            query = "UPDATE cuentas SET saldo = ? WHERE id_cuenta = ?"
            params = (nuevo_saldo, id_cuenta)
            self.execute_query(query, params)
            print(f"Saldo actualizado desde la base de datos para la cuenta {id_cuenta}: {nuevo_saldo}")

    def actualizar_cliente(self, id_cliente, nombre, apellido, email, contrasena):
        """Actualiza la información de un cliente en la base de datos."""
        query = """
            UPDATE Clientes
            SET nombre = ?, apellido = ?, email = ?, contrasena = ?
            WHERE id_cliente = ?
        """
        # Ejecutar la consulta con los valores pasados, sin depender del objeto Cliente
        self.execute_query(query, (nombre, apellido, email, contrasena, id_cliente))
        print(f"DB_Cliente con ID {id_cliente} actualizado en la base de datos.")



