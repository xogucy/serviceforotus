import pytest


@pytest.mark.asyncio
async def test_live_health(client):
    response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
