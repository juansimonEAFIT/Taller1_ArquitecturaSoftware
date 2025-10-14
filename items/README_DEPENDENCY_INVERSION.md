# Inversión de Dependencias en `items`

Este cambio aplica el principio de Inversión de Dependencias (D de SOLID) de manera sencilla para la gestión de `Pedido`.

## ¿Qué se hizo?
- Se creó una interfaz `IPedidoRepository` y una implementación concreta `DjangoPedidoRepository` en `items/repositories.py`.
- Las vistas `pedidos_empresa` y `pedido_recibo_pdf` ahora consumen la abstracción (fábrica `get_pedido_repository`) y no dependen directamente del ORM.
- Se añadió `@login_required` a la vista de descarga de PDF para reforzar seguridad.

## ¿Por qué?
- Desacoplar las vistas del ORM facilita pruebas unitarias (podemos inyectar un doble de prueba del repositorio) y hace el código más mantenible.
- Permite cambiar la fuente de datos en el futuro (por ejemplo, mover a un microservicio) sin tocar la lógica de presentación.

## Archivos impactados
- `items/repositories.py` (nuevo): define `IPedidoRepository`, `DjangoPedidoRepository` y `get_pedido_repository`.
- `items/views.py` (editado): utiliza el repositorio en lugar de `Pedido.objects...` para listar/cambiar estado y para servir PDFs.

## Cómo probar
- Vista de empresa (`/items/pedidos_empresa`): aplicar filtros por estado y cambiar estado de un pedido. Debe comportarse igual que antes.
- Descarga de recibo (`/items/pedido/<id>/recibo_pdf`): requiere usuario autenticado y solo sirve el PDF si corresponde al cliente dueño.

## Próximos pasos sugeridos
- Permitir inyección de repositorio por configuración (por ejemplo, usando settings o un contenedor simple).
- Añadir pruebas unitarias para el repositorio y las vistas (mock del repositorio).
- Extender el repositorio con métodos de paginación y consultas optimizadas (`select_related/prefetch_related`).