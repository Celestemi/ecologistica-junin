"""Ayudas compartidas de los tests HTTP."""

from httpx import AsyncClient


async def login_headers(client: AsyncClient, correo: str, clave: str) -> dict[str, str]:
    response = await client.post("/api/v1/auth/ingresar", json={"correo": correo, "clave": clave})
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
