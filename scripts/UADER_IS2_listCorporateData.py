import json
import uuid
import os
import sys
import platform

# Agregar la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import ID_KEY  
from src.corporate_data import CorporateData  
from src.corporate_log import CorporateLog  

def list_all_corporate_data():
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
    uuid_cpu = str(uuid.uuid4())  

    # Instanciar la clase
    corporate_data = CorporateData()

    # utiliza getSeqID para que se incremente
    id_to_increment = ID_KEY  
    try:
        new_id_seq = corporate_data.getSeqID(session_id, uuid_cpu, id_to_increment)  
        #print(f"Nuevo ID de secuencia: {new_id_seq}")  
    except Exception as e:
        print(f"Ocurrió un error al incrementar el ID de secuencia: {str(e)}")

    data = corporate_data.listCorporateData(ID_KEY, log_event=False)  

    # Cargar el JSON y luego imprimirlo de manera legible
    formatted_data = json.loads(data)
    print(json.dumps(formatted_data, indent=2, ensure_ascii=False))

    # Capturar información del evento
    event_info = (
        f"Program: {os.path.basename(__file__)} Version {VERSION} UADER-FCyT-IS2 Programa de test y diagnóstico\n"
        f"CPU ID[{CPUid}] OS({OSname}) platform({CPUplatform}) release({CPUrelease}) node({CPUnode}) machine({CPUmachine})\n"
        f"Session ID({session_id})"
    )

    print(event_info)

    # Almacenar el evento en el log pasandole a logEvent de la clase CorporateLog
    corporate_log = CorporateLog()
    corporate_log.logEvent(session_id, "list_all_corporate_data")  

if __name__ == "__main__":
    list_all_corporate_data()