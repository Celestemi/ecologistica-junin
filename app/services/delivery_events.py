"""AF-08: evento durable en Bitacora existente, sin nueva columna ni DDL.

Nunca se reconstruye la hora real de entregas antiguas a partir de una ETA.
El lock de active_plan serializa comprobación/idempotencia/inserción.
"""

import json
from datetime import datetime
from sqlalchemy import select
from app.models.identity import Bitacora


async def delivery_events(session) -> dict[int, dict]:
    rows = await session.scalars(select(Bitacora).where(
        Bitacora.accion == 'entrega_confirmada').order_by(Bitacora.id))
    events = {}
    for row in rows:
        try:
            data = json.loads(row.detalle or '')
            if data.get('v') != 1:
                continue
            moment = datetime.fromisoformat(data['at'])
            received = datetime.fromisoformat(data['received'])
            if moment.tzinfo is None or received.tzinfo is None:
                continue
            events.setdefault(int(data['p']), {**data, 'moment': moment,
                'actor_id':row.usuario_id, 'event_id':row.id})
        except (ValueError, TypeError, KeyError, AttributeError):
            continue  # entrada histórica no estructurada: no inventar un evento
    return events


def event_payload(order, body, vehicle_id: int, plan_id: int, received: datetime) -> str:
    value = json.dumps({'v':1, 'p':order.id, 'op':body.operation_id,
        'at':body.delivered_at.isoformat(), 'received':received.isoformat(),
        'vehicle':vehicle_id, 'plan':plan_id}, separators=(',', ':'))
    if len(value) > 400:
        raise ValueError('La evidencia de entrega supera el límite de bitácora.')
    return value
