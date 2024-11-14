import uuid  
import platform  
import sys  
import os  
import json

# Agregar la carpeta raíz del proyecto al PYTHONPATH para poder importar las librerías
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.corporate_log import CorporateLog  

class TestCorporateLog:
    
    def __init__(self):
        # Configuración inicial
        self.corporate_log = CorporateLog()    
        self.uuidCPU = platform.node()
        self.cpu_id = str(uuid.getnode())

    # Probar el registro de un evento exitoso
    def test_log_event_success(self):
        uuid_session = str(uuid.uuid4())
        print(f"Ejecutando test_log_event_success (evento exitoso) con uuid_session: {uuid_session} y uuidCPU: {self.uuidCPU}")
        
        # Registrar el evento
        self.corporate_log.logEvent(uuid_session, "test_log_event_success")  
        
        # Listar los logs después del registro
        logs = self.corporate_log.listLogs(self.cpu_id)  
        
        if len(logs) == 0:
            print("Error en test_log_event_success: No se encontró ningún log después de registrar el evento.")
        else:
            print(f"Total de logs encontrados: {len(logs)}")
            for log in sorted(logs, key=lambda log: log.get('timestamp', '')):
                print(f"Log:\n{json.dumps(log, indent=2)}\n")
            print("test_log_event_success pasó correctamente.")
            print()

    # Probar la lista de logs cuando se proporciona un ID de CPU inválido
    def test_list_logs_no_cpu(self):
        uuid_session = str(uuid.uuid4())
        print(f"Ejecutando test_list_logs_no_cpu (cpu inválido) con uuid_session: {uuid_session} y uuidCPU: {self.uuidCPU}")

        # Registrar el evento
        self.corporate_log.logEvent(uuid_session, "test_list_logs_no_cpu") 
        
        # Intentar obtener logs con un ID de CPU inválido
        logs = self.corporate_log.listLogs("invalid_cpu")  
        
        if logs != []:
            print(f"Error en test_list_logs_no_cpu: Se esperaba una lista vacía para un ID de CPU inválido, pero se obtuvo {logs}")
        else:
            print("No se encontraron logs para un CPU inválido, como se esperaba.")
            print("test_list_logs_no_cpu pasó correctamente.")
            print()

    # Verificar que la clase CorporateLog siga el patrón Singleton
    def test_singleton_corporate_log(self):
        print("Verificando patrón Singleton en CorporateLog")
        
        another_instance = CorporateLog()  
        
        if self.corporate_log is not another_instance:
            print("Error en test_singleton_corporate_log: CorporateLog no es un Singleton. Se han creado múltiples instancias.")
        else:
            print("test_singleton_corporate_log pasó correctamente.")
            print()

# Ejecución de las pruebas
if __name__ == '__main__':
    tester = TestCorporateLog()
    tester.test_list_logs_no_cpu()
    tester.test_log_event_success()
    tester.test_singleton_corporate_log()






