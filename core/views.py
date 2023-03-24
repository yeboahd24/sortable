from django.shortcuts import render
from .models import Item
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from confluent_kafka import Producer
from Sortable.settings import KAFKA_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID
from confluent_kafka import Consumer, KafkaError

def index(request):
    items = Item.objects.all()
    return render(request, "index.html", {"items": items})


@csrf_exempt
def update_position(request):
    item_id = request.POST.get("id")
    position = request.POST.get("position")

    item = Item.objects.get(id=item_id)
    item.position = position
    item.save()

    return JsonResponse({"success": True})



def send_message(request):
    message = request.GET.get('message', 'Hello, Kafka!')
    producer = Producer({'bootstrap.servers': KAFKA_SERVERS})
    producer.produce(KAFKA_TOPIC, message)
    producer.flush()
    return HttpResponse('Message sent to Kafka: {}'.format(message))



def receive_message(request):
    consumer = Consumer({
        'bootstrap.servers': KAFKA_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([KAFKA_TOPIC])
    messages = []
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached')
            else:
                print('Error while consuming message: {}'.format(msg.error()))
        else:
            message = msg.value().decode('utf-8')
            messages.append(message)
            print('Received message: {}'.format(message))
            if len(messages) >= 10:
                break
    consumer.close()
    return HttpResponse('Messages received from Kafka: {}'.format(', '.join(messages)))
