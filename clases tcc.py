from abc import ABC, abstractmethod

# patron Singleton para la conexión a la base de datos
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = "Conexión establecida a la base de datos."  # simulacion
        return cls._instance

    def get_connection(self):
        return self.connection

# clase Observer (para notificar tecnicos)
class Observer(ABC):
    @abstractmethod
    def actualizar(self, mensaje):
        pass

class Tecnico(Observer):
    def __init__(self, idTecnico, nombre, especialidad):
        self.idTecnico = idTecnico
        self.nombre = nombre
        self.especialidad = especialidad

    def actualizar(self, mensaje):
        print(f"Técnico {self.nombre} notificado: {mensaje}")

    def __str__(self):
        return f"Técnico[ID: {self.idTecnico}, Nombre: {self.nombre}, Especialidad: {self.especialidad}]"

# clase Sujeto (gestionn de las notificaciones)
class Sujeto:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def eliminar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar_observadores(self, mensaje):
        for observador in self._observadores:
            observador.actualizar(mensaje)

# clase Cliente
class Cliente:
    def __init__(self, idCliente, nombre, numero):
        self.id_cliente = idCliente
        self.nombre = nombre
        self.numero = numero

    def guardar_en_base_datos(self):
        db = DatabaseConnection()  # Obtenemos la conexión única
        print(f"Guardando en la base de datos: {self}")
        print(f"Usando conexión: {db.get_connection()}")  # Simulación del uso de la base de datos

    def __str__(self):
        return f"Cliente[ID: {self.id_cliente}, Nombre: {self.nombre}, Contacto: {self.numero}]"
    

# clase Abstracta Servicio, uso de Herencia y polimorfismo en sus subclases
class Servicio(ABC):
    def __init__(self, idServicio, descripcion, costo):
        self.idServicio = idServicio
        self.descripcion = descripcion
        self.costo = costo

    def __str__(self):
        return f"Servicio[ID: {self.idServicio}, Descripción: {self.descripcion}, Costo: {self.costo}]"
    
    @abstractmethod
    def realizarServicio(self):
        pass

# subclases de Servicio, Herencia y polimorfismo
class ServicioReparacion(Servicio):
    def __init__(self, idServicio, descripcion, costo):
        super().__init__(idServicio, descripcion, costo)

    def realizarServicio(self):
        print("Reparación realizada.")

class ServicioSoporteIT(Servicio):
    def __init__(self, idServicio, descripcion, costo):
        super().__init__(idServicio, descripcion, costo)

    def realizarServicio(self):
        print("Soporte técnico brindado.")

# patron Factory para la creación de servicios
class ServicioFactory:
    @staticmethod
    def crear_servicio(tipo, idServicio, descripcion, costo):
        if tipo == "reparacion":
            return ServicioReparacion(idServicio, descripcion, costo)
        elif tipo == "soporteIT":
            return ServicioSoporteIT(idServicio, descripcion, costo)
        else:
            raise ValueError("Tipo de servicio no válido.")

# clase OrdenDeTrabajo
class OrdenDeTrabajo(Sujeto):
    def __init__(self, idOrden, cliente, servicio):
        super().__init__()
        self.idOrden = idOrden
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def actualizarEstado(self, nuevoEstado):
        self.estado = nuevoEstado
        self.notificar_observadores(f"La orden {self.idOrden} ha cambiado su estado a: {nuevoEstado}")

    def guardar_en_base_datos(self):
        db = DatabaseConnection()  # usamos la misma conexión
        print(f"Guardando en la base de datos: {self}")
        print(f"Usando conexión: {db.get_connection()}")  # simulacion

    def __str__(self):
        return (f"OrdenDeTrabajo[ID: {self.idOrden}, Cliente: {self.cliente.nombre}, "
                f"Servicio: {self.servicio.descripcion}, Estado: {self.estado}]")

# crear instancias y usarlas
if __name__ == "__main__":
    
    # objetos de cada clase;
    cliente1 = Cliente(1, "Felix Velazquez", "3012892860")
    cliente1.guardar_en_base_datos()


    tecnico1 = Tecnico(1, "Gabriel Valeta", "Reparación de electrodomésticos")

    # objeto Servicio usando Factory
    servicio1 = ServicioFactory.crear_servicio("reparacion", 1, "Reparación de lavadora", 150.00)

    # objeto de la clase orden de trabajo
    orden1 = OrdenDeTrabajo(1, cliente1, servicio1)

    # agregar tecnico como observador
    orden1.agregar_observador(tecnico1)

    # simulacion de guardar orden y notificar
    orden1.guardar_en_base_datos()
    orden1.actualizarEstado("En Proceso")
    orden1.actualizarEstado("Completada")

