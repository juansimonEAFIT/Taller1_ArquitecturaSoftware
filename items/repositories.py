from __future__ import annotations

from typing import Optional, Protocol
from django.db.models import QuerySet

from .models import Pedido
from core.models import Empresa


class IPedidoRepository(Protocol):
    """Abstracción para acceso a datos de Pedidos.

    Permite que las vistas dependan de esta interfaz y no de Django ORM directamente.
    """

    def list_for_empresa(self, empresa: Empresa, estado: Optional[str] = None) -> QuerySet[Pedido]:
        ...

    def change_estado(self, pedido_id: int, empresa: Empresa, nuevo_estado: str) -> bool:
        ...

    def get_for_cliente_pdf(self, pedido_id: int, nombre_cliente: str) -> Optional[Pedido]:
        ...


class DjangoPedidoRepository(IPedidoRepository):
    """Implementación basada en Django ORM."""

    def list_for_empresa(self, empresa: Empresa, estado: Optional[str] = None) -> QuerySet[Pedido]:
        qs = Pedido.objects.filter(empresa_encargada=empresa)
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def change_estado(self, pedido_id: int, empresa: Empresa, nuevo_estado: str) -> bool:
        try:
            pedido = Pedido.objects.get(id=pedido_id, empresa_encargada=empresa)
        except Pedido.DoesNotExist:
            return False
        # Validación simple con las opciones del modelo
        if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
            pedido.estado = nuevo_estado
            pedido.save(update_fields=["estado"])
            return True
        return False

    def get_for_cliente_pdf(self, pedido_id: int, nombre_cliente: str) -> Optional[Pedido]:
        try:
            pedido = Pedido.objects.get(id=pedido_id, nombre_cliente=nombre_cliente)
        except Pedido.DoesNotExist:
            return None
        return pedido if pedido.recibo_pdf else None


def get_pedido_repository() -> IPedidoRepository:
    """Fábrica sencilla para obtener la implementación por defecto.

    En pruebas se puede reemplazar por un doble de prueba (mock/fake).
    """
    return DjangoPedidoRepository()
