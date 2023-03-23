from django.shortcuts import render
from .models import Item
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
