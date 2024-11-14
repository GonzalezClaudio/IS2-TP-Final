import json
import uuid
import os
import sys
import platform

# Agregar la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import ID_KEY  # Importa solo ID_KEY desde config
from src.corporate_data import CorporateData  # Asegúrate de que la clase esté importada correctamente
from src.corporate_log import CorporateLog  # Importar CorporateLog


#-----------------------------------------------------------------------------------------------------------------------------------------------
# Prueba para el funcionamiento de GetData y registro en log
#-----------------------------------------------------------------------------------------------------------------------------------------------
def pruebaGetData():
    print("Iniciando prueba de GetData...")  
    # Información del sistema
    VERSION = "1.1"
    CPUid = uuid.getnode()
    CPUplatform = platform.system()
    OSname = platform.platform()
    CPUrelease = platform.release()
    CPUnode = platform.node()
    CPUmachine = platform.machine()

    # Generar UUIDs
    session_id = str(uuid.uuid4())  
    uuid_cpu = platform.node()  

    
    corporate_data = CorporateData()
    print("Creando instancia de CorporateData...")

    # Llamar a getSeqID para incrementar el ID de secuencia
    id_to_increment = ID_KEY  
    try:
        print("Incrementando ID de secuencia...")
        new_id_seq = corporate_data.getSeqID(session_id, uuid_cpu, id_to_increment)  
        print(f"Nuevo ID de secuencia: {new_id_seq}")  
    except Exception as e:
        print(f"Ocurrió un error al incrementar el ID de secuencia: {str(e)}")

    # Obtener datos utilizando getData
    print("Obteniendo datos utilizando getData...")
    data = corporate_data.getData(session_id, uuid_cpu, ID_KEY)  

    # Cargar el JSON y luego imprimirlo de manera legible
    try:
        formatted_data = json.loads(data)
        print("Datos obtenidos y decodificados. Mostrando en formato JSON:")
        print(json.dumps(formatted_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Ocurrió un error al decodificar el JSON: {str(e)}")

    # Capturar información del evento
    event_info = (
        f"Program: {os.path.basename(__file__)} Version {VERSION} UADER-FCyT-IS2 Programa de test y diagnóstico\n"
        f"CPU ID[{CPUid}] OS({OSname}) platform({CPUplatform}) release({CPUrelease}) node({CPUnode}) machine({CPUmachine})\n"
        f"Session ID({session_id})"
    )

    print(event_info)

    # Almacenar el evento en el log
    corporate_log = CorporateLog()
    corporate_log.logEvent(session_id, "PruebaGetData")  
    print("Evento almacenado en el log.")
    print("")


#-----------------------------------------------------------------------------------------------------------------------
# Prueba GetCUIT y almacenar en log
#-----------------------------------------------------------------------------------------------------------------------
def pruebaGetCUIT():
    print("Iniciando prueba de GetCUIT...")  
    # Información del sistema
    VERSION = "1.1"
    CPUid = uuid.getnode()
    CPUplatform = platform.system()
    OSname = platform.platform()
    CPUrelease = platform.release()
    CPUnode = platform.node()
    CPUmachine = platform.machine()

    # Generar UUIDs
    session_id = str(uuid.uuid4())  
    uuid_cpu = platform.node()  

    # Obtener datos corporativos
    corporate_data = CorporateData()
    print("Creando instancia de CorporateData...")

    # Llamar a getSeqID para incrementar el ID de secuencia
    id_to_increment = ID_KEY  
    try:
        print("Incrementando ID de secuencia...")
        new_id_seq = corporate_data.getSeqID(session_id, uuid_cpu, id_to_increment)  
        print(f"Nuevo ID de secuencia: {new_id_seq}")  
    except Exception as e:
        print(f"Ocurrió un error al incrementar el ID de secuencia: {str(e)}")

    # Obtener datos utilizando getCUIT
    print("Obteniendo datos utilizando getCUIT...")
    data = corporate_data.getCUIT(session_id, uuid_cpu, ID_KEY)  

    # Cargar el JSON y luego imprimirlo de manera legible
    try:
        formatted_data = json.loads(data)
        print("Datos obtenidos y decodificados. Mostrando en formato JSON:")
        print(json.dumps(formatted_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Ocurrió un error al decodificar el JSON: {str(e)}")

    # Capturar información del evento
    event_info = (
        f"Program: {os.path.basename(__file__)} Version {VERSION} UADER-FCyT-IS2 Programa de test y diagnóstico\n"
        f"CPU ID[{CPUid}] OS({OSname}) platform({CPUplatform}) release({CPUrelease}) node({CPUnode}) machine({CPUmachine})\n"
        f"Session ID({session_id})"
    )

    print(event_info)

    # Almacenar el evento en el log
    corporate_log = CorporateLog()
    corporate_log.logEvent(session_id, "PruebaGetCUIT")  
    print("Evento almacenado en el log.")
    print("")
#-----------------------------------------------------------------------------------------------------------------------
# Listar todos los logs
#-----------------------------------------------------------------------------------------------------------------------
def listarLogs():
    corporate_log = CorporateLog()  
    
    try:
        # Listar todos los logs y obtener los logs para la CPU actual
        logs = corporate_log.listLogs(platform.node())  

        if logs:
            total_logs = len(logs)
            print(f"Total de logs encontrados: {total_logs}")
            
            # Ordenar los logs por 'timestamp' de forma ascendente
            sorted_logs = sorted(logs, key=lambda log: log['timestamp'])

            # Imprimir todos los logs
            for log in sorted_logs:
                print(f"Log:\n{json.dumps(log, indent=2)}\n")
        else:
            print("No se encontraron logs.")

    except Exception as e:
        print(f"Ocurrió un error al intentar listar los logs: {str(e)}")



if __name__ == "__main__":
    pruebaGetData()
    pruebaGetCUIT()
    listarLogs()  



