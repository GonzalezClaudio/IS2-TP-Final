import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
import platform  # Para obtener el identificador único de la máquina

class Log:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
            cls.table = boto3.resource('dynamodb').Table('CorporateLog')  # Conectar con la tabla de DynamoDB
        return cls._instance

    def delete_logs_by_machine(self):
        try:
            # Filtrar los logs que pertenecen a la máquina actual usando 'cpu_node'
            response = self.table.scan(
                FilterExpression=Attr('cpu_node').eq(platform.node())
            )
            logs = response.get('Items', [])

            # Bucle para eliminar cada log filtrado
            for log in logs:
                self.table.delete_item(
                    Key={
                        'id': log['id']  # Suponiendo que 'id' es la clave primaria
                    }
                )
                print(f"Log eliminado: {log['id']}")

            # Manejo de paginación en caso de que haya más logs
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey'],
                    FilterExpression=Attr('cpu_node').eq(platform.node())
                )
                logs = response.get('Items', [])
                for log in logs:
                    self.table.delete_item(
                        Key={
                            'id': log['id']
                        }
                    )
                    print(f"Log eliminado: {log['id']}")

            print("Eliminación de logs completada para la máquina actual.")

        except ClientError as e:
            print(f"Error al eliminar logs: {str(e)}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {str(e)}")

# Ejemplo de uso
if __name__ == "__main__":
    log_instance = Log()
    log_instance.delete_logs_by_machine()


