import pytest


@pytest.mark.asyncio
async def test_ready_health(client, monkeypatch):
    async def fake_ping_database() -> None:
        return None

    monkeypatch.setattr("app.api.health.routes.ping_database", fake_ping_database)

    response = await client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
