import json
import uuid
import boto3
import logging
from botocore.exceptions import ClientError
from decimal import Decimal
import sys
import os

# Agregar la carpeta raíz del proyecto al PYTHONPATH para poder importar las librerías
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
  
from config import ID_KEY
from src.corporate_log import CorporateLog  

# Configuración básica de logging
logger = logging.getLogger('CorporateDataLogger')

# Función para activar logging
def enable_logging():
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

# Función para desactivar logging
def disable_logging():
    logger.setLevel(logging.CRITICAL)  

# Función para convertir Decimal a int
def decimal_to_int(data):
    if isinstance(data, Decimal):
        return int(data)  # o float(data) si prefieres
    elif isinstance(data, list):
        return [decimal_to_int(i) for i in data]
    elif isinstance(data, dict):
        return {k: decimal_to_int(v) for k, v in data.items()}
    return data


class CorporateData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CorporateData, cls).__new__(cls)
            cls.dynamodb = boto3.resource('dynamodb')
            cls.table = cls.dynamodb.Table('CorporateData')
            logger.debug("Se ha creado una nueva instancia de CorporateData.")
        return cls._instance
    
    #def __init__(self):
    #    self.dynamodb = boto3.resource('dynamodb')
    #    self.table = self.dynamodb.Table('CorporateData')
    #    logger.debug("Se ha creado una nueva instancia de CorporateData.")
    
    
    # Funcio getData
    def getData(self, uuid_session, uuidCPU, id):
        logger.debug(f"Llamando a getData con uuid_session: {uuid_session}, uuidCPU: {uuidCPU}, id: {id}")

        # Validación de UUIDs
        if not uuid_session or not uuidCPU:
            return json.dumps({"error": "UUIDs vacíos o inválidos"})

        try:
            response = self.table.get_item(Key={'id': id})
            item = response.get('Item')
            if item:
                logger.debug(f"Registro encontrado: {item}")
                return json.dumps({
                    "id": item.get('id'),
                    "domicilio": item.get('domicilio'),
                    "localidad": item.get('localidad'),
                    "cp": item.get('cp'),
                    "provincia": item.get('provincia')
                })
            else:
                logger.debug(f"No se encontró ningún registro para id: {id}")
                return json.dumps({"error": "Registro no encontrado"})
        except ClientError as e:
            logger.error(f"Error al obtener datos: {str(e)}")
            return json.dumps({"error": str(e)})

    def getCUIT(self, uuid_session, uuidCPU, id):
        logger.debug(f"Llamando a getCUIT con uuid_session: {uuid_session}, uuidCPU: {uuidCPU}, id: {id}")

        # Validación de UUIDs
        if not uuid_session or not uuidCPU:
            return json.dumps({"error": "UUIDs vacíos o inválidos"})

        try:
            response = self.table.get_item(Key={'id': id})
            item = response.get('Item')
            if item:
                logger.debug(f"CUIT encontrado: {item['CUIT']}")
                return json.dumps({"CUIT": item['CUIT']})
            else:
                logger.debug(f"No se encontró ningún registro para id: {id}")
                return json.dumps({"error": "Registro no encontrado"})
        except ClientError as e:
            logger.error(f"Error al obtener CUIT: {str(e)}")
            return json.dumps({"error": str(e)})

    def getSeqID(self, uuid_session, uuidCPU, id):
        logger.debug(f"Llamando a getSeqID con uuid_session: {uuid_session}, uuidCPU: {uuidCPU}, id: {id}")

        # Validación de UUIDs
        if not uuid_session or not uuidCPU:
            return json.dumps({"error": "UUIDs vacíos o inválidos"})

        try:
            response = self.table.get_item(Key={'id': id})
            item = response.get('Item')
            if item:
                idSeq = item['idSeq'] + 1
                logger.debug(f"Incrementando idSeq a: {idSeq}")
                self.table.update_item(
                    Key={'id': id},
                    UpdateExpression='SET idSeq = :val',
                    ExpressionAttributeValues={':val': idSeq}
                )
                return idSeq  
            else:
                logger.debug(f"No se encontró ningún registro para id: {id}")
                return json.dumps({"error": "Registro no encontrado"})
        except ClientError as e:
            logger.error(f"Error al obtener idSeq: {str(e)}")
            return json.dumps({"error": str(e)})

    def listCorporateData(self, id, log_event=True): 
        logger.debug(f"Llamando a listCorporateData con id: {id}")
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            logger.debug(f"Items recuperados: {items}")

            # Filtrar los elementos según el id
            items = [decimal_to_int(item) for item in items if item['id'] == id]

            if not items:  
                logger.debug(f"No se encontraron registros para el id: {id}")
                return json.dumps({"error": "No se encontraron registros para el id especificado."})

            if log_event:  
                corporate_log = CorporateLog()
                uuid_session = str(uuid.uuid4())  
                corporate_log.logEvent(uuid_session, "listCorporateData")  

            return json.dumps(items)
        except ClientError as e:
            logger.error(f"Error al listar datos: {str(e)}")
            return json.dumps({"error": str(e)})
        
    def listCorporateLog(self, uuidCPU):
        logger.debug(f"Llamando a listCorporateLog con uuidCPU: {uuidCPU}")
        try:
            corporate_log_table = self.dynamodb.Table('CorporateLog')
            response = corporate_log_table.scan()
            items = response.get('Items', [])
            logger.debug(f"Items recuperados: {items}")

            # Filtrar los elementos por uuidCPU
            items = [decimal_to_int(item) for item in items if item['uuidCPU'] == uuidCPU]

            if not items:
                logger.debug(f"No se encontraron logs para uuidCPU: {uuidCPU}")
                return json.dumps({"error": "No se encontraron logs para el uuidCPU especificado."})

            return json.dumps(items)
        except ClientError as e:
            logger.error(f"Error al listar logs: {str(e)}")
            return json.dumps({"error": str(e)})



