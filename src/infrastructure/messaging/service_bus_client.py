from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json
from src.application.services.user_service import UserService
from src.infrastructure.database.user_repository import UserRepository

connection_string = "Endpoint=sb://buynowservicebus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=sfylUWNBF6nTPcSzIc2Ai6cCZ11d7YAJN+ASbAeXgVQ="
queue_name = "purchase_events"

user_service = UserService(UserRepository())

def send_product_purchase_event(product_id, user_id):
    try:
        # Cria o cliente Service Bus
        servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_string, logging_enable=True)

        # Cria a mensagem com o ID do produto
        message = ServiceBusMessage(json.dumps({"product_id": product_id}))

        # Envia a mensagem para o Service Bus
        with servicebus_client:
            sender = servicebus_client.get_queue_sender(queue_name=queue_name)
            with sender:
                sender.send_messages(message)
                print(f"Evento de compra do produto {product_id} enviado para o Service Bus.")

        # Incrementa o campo 'compras' do usuário após o envio bem-sucedido
        user_service.increment_user_purchases(user_id)

    except Exception as e:
        print(f"Erro ao enviar evento para o Service Bus: {e}")
