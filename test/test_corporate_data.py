import uuid  
import platform  
import sys  
import os  

# Agregar la carpeta raíz del proyecto al PYTHONPATH para poder importar las librerías
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.corporate_data import CorporateData 
from src.corporate_log import CorporateLog 
from config import ID_KEY

class TestCorporateData:
    
    def __init__(self):  
        self.corporate_data = CorporateData()  
        self.corporate_log = CorporateLog()  
        self.uuidCPU = platform.node()  

    # Prueba para obtener datos con un ID válido
    def test_get_data_success(self):
        uuid_session = uuid.uuid4()  
        print(f"Ejecutando test_get_data_success (datos validos) con uuid_session: {uuid_session} y uuidCPU: {self.uuidCPU}")

        # Registrar el evento
        self.corporate_log.logEvent(uuid_session, "test_get_data_success")
        print("Evento almacenado en el log.")

        response = self.corporate_data.getData(uuid_session, self.uuidCPU, ID_KEY)  
        print(f"Respuesta obtenida: {response}")
        
        if "error" in response:
            print(f"Error en test_get_data_success: No se esperaba 'error' en la respuesta, pero se obtuvo {response}")
        else:
            print("test_get_data_success pasó correctamente.")
            print()

    # Prueba para obtener datos con un ID inválido
    def test_get_data_invalid_id(self):
        uuid_session = uuid.uuid4()  
        print(f"Ejecutando test_get_data_invalid_id (id invalido) con uuid_session: {uuid_session} y uuidCPU: {self.uuidCPU}")

        # Registrar el evento
        self.corporate_log.logEvent(uuid_session, "test_get_data_invalid_id")
        print("Evento almacenado en el log.")

        response = self.corporate_data.getData(uuid_session, self.uuidCPU, "invalid_id")  
        print(f"Respuesta obtenida: {response}")
        
        if "error" not in response:
            print(f"Error en test_get_data_invalid_id: Se esperaba 'error' en la respuesta al usar un ID inválido, pero se obtuvo {response}")
        else:
            print("test_get_data_invalid_id pasó correctamente.")
            print()

    # Prueba para obtener datos con un ID vacío
    def test_get_data_empty_id(self):
        uuid_session = uuid.uuid4()  
        print(f"Ejecutando test_get_data_empty_id (id vacio) con uuid_session: {uuid_session} y uuidCPU: {self.uuidCPU}")

        # Registrar el evento
        self.corporate_log.logEvent(uuid_session, "test_get_data_empty_id")
        print("Evento almacenado en el log.")

        response = self.corporate_data.getData(uuid_session, self.uuidCPU, "")  
        print(f"Respuesta obtenida: {response}")
        
        if "error" not in response:
            print(f"Error en test_get_data_empty_id: Se esperaba 'error' en la respuesta al usar un ID vacío, pero se obtuvo {response}")
        else:
            print("test_get_data_empty_id pasó correctamente.")
            print()

    # Nueva prueba para ID válido pero campo vacío
    def test_get_data_valid_id_empty_field(self):
        uuid_session = uuid.uuid4()  
        valid_id = ID_KEY  
        print(f"Ejecutando test_get_data_valid_id_empty_field (id valido, campo vacio) con uuid_session: {uuid_session} y uuidCPU vacío")

        # Registrar el evento
        self.corporate_log.logEvent(uuid_session, "test_get_data_valid_id_empty_field")
        print("Evento almacenado en el log.")

        response = self.corporate_data.getData(uuid_session, "", valid_id)  
        print(f"Respuesta obtenida: {response}")
        
        if "error" not in response:
            print(f"Error en test_get_data_valid_id_empty_field: Se esperaba 'error' en la respuesta con campo uuidCPU vacío, pero se obtuvo {response}")
        else:
            print("test_get_data_valid_id_empty_field pasó correctamente.")
            print()

    # Prueba para verificar el patrón Singleton
    def test_singleton_corporate_data(self):  
        print("Verificando patrón Singleton en CorporateData")
        another_instance = CorporateData()  
        
        if self.corporate_data is not another_instance:
            print("Error en test_singleton_corporate_data: CorporateData no es un Singleton. Se han creado múltiples instancias.")
        else:
            print("test_singleton_corporate_data pasó correctamente.")
            print()

# Ejecución de las pruebas
if __name__ == '__main__':
    tester = TestCorporateData()
    tester.test_get_data_success()
    tester.test_get_data_invalid_id()
    tester.test_get_data_empty_id()
    tester.test_get_data_valid_id_empty_field()
    tester.test_singleton_corporate_data()

