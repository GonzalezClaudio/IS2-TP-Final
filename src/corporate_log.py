import logging
import uuid
import platform
import datetime
from botocore.exceptions import ClientError
import boto3  
from boto3.dynamodb.conditions import Key, Attr  

# Configuración básica de logging
logger = logging.getLogger('CorporateLogLogger')

# Función para activar logging
def enable_logging():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

# Función para desactivar logging
def disable_logging():
    logger.setLevel(logging.CRITICAL)  # Solo muestra errores críticos

class Log:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
            cls.logs = []  
            cls.table = boto3.resource('dynamodb').Table('CorporateLog')  
        return cls._instance

    def post(self, uuid_session, method_name):
        cpu_info = platform.uname()  # Obtener información de la CPU
        timestamp = datetime.datetime.now().isoformat()  # Obtener timestamp
        

        log_entry = {
            "id": str(uuid.uuid4()),  
            "uuid_session": str(uuid_session),
            "method_name": method_name,
            "cpu_system": cpu_info.system,  
            "cpu_node": cpu_info.node,
            "cpu_release": cpu_info.release,
            "cpu_version": cpu_info.version,
            "cpu_machine": cpu_info.machine,
            "cpu_processor": cpu_info.processor,
            "timestamp": timestamp
        }

        # Almacenar el log en DynamoDB
        try:
            self.table.put_item(Item=log_entry)  
            logger.debug(f"Log registrado en DynamoDB: {log_entry}")
        except ClientError as e:
            logger.error(f"Error al registrar el log en DynamoDB: {str(e)}")

    
    
    def list(self, cpu_id, uuid_session=None):
        try:
        
            response = self.table.scan(
                FilterExpression=Attr('cpu_node').eq(cpu_id)  # Filtrar por el atributo
            )

            return response.get('Items', [])
        except ClientError as e:
            logger.error(f"Error al listar logs desde DynamoDB: {str(e)}")
            return []

class CorporateLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CorporateLog, cls).__new__(cls)
            cls.log = Log()  # Inicializar la clase Log
            logger.debug("Se ha creado una nueva instancia de CorporateLog.")
        return cls._instance

    #Registrar un evento
    def logEvent(self, uuid_session, method_name):
        logger.debug(f"Registrando evento con UUID de sesión: {uuid_session}, método: {method_name}")
        self.log.post(uuid_session, method_name)

    #llama a la funcion list de la clase log
    def listLogs(self, cpu_id, uuid_session=None):
        return self.log.list(cpu_id, uuid_session)
    
    











