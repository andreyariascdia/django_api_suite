from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
   
   def get(self, request):
      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

   def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    """
    Maneja operaciones sobre un recurso individual identificado por <str:id>
    Métodos soportados: PUT, PATCH, DELETE
    """

    # Método auxiliar para buscar un elemento por id
    def _find_item(self, item_id):
        for item in data_list:
            if item.get("id") == item_id:
                return item
        return None

    # PUT: reemplazo completo del recurso (excepto id)
    def put(self, request, item_id):
        data = dict(request.data)
        item = self._find_item(item_id)

        if not item:
            return Response(
                {"error": "Elemento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validación: PUT exige todos los campos
        if not data.get("name") or not data.get("email"):
            return Response(
                {"error": "PUT requiere los campos name y email."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # id no se modifica
        item["name"] = data["name"]
        item["email"] = data["email"]
        if "is_active" in data:
            item["is_active"] = bool(data["is_active"])

        return Response(
            {
                "message": "Elemento actualizado completamente (PUT).",
                "data": item
            },
            status=status.HTTP_200_OK
        )

    # PATCH
    def patch(self, request, item_id):
        data = dict(request.data)
        item = self._find_item(item_id)

        if not item:
            return Response(
                {"error": "Elemento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        allowed_fields = {"name", "email", "is_active"}
        updated = False

        for field in allowed_fields:
            if field in data:
                item[field] = data[field]
                updated = True

        if not updated:
            return Response(
                {"error": "No se enviaron campos válidos para actualizar."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Elemento actualizado parcialmente (PATCH).",
                "data": item
            },
            status=status.HTTP_200_OK
        )

    # DELETE
    def delete(self, request, item_id):
        item = self._find_item(item_id)

        if not item:
            return Response(
                {"error": "Elemento no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        item["is_active"] = False

        return Response(
            {
                "message": "Elemento eliminado lógicamente (DELETE).",
                "data": item
            },
            status=status.HTTP_200_OK
        )
