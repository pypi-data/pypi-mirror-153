import httpx
import pytest

pytest.importorskip("starlette")


@pytest.mark.asyncio
async def test_example_starlette() -> None:
    from examples.starlette import app

    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://testserver")
        assert response.status_code == 200
