from unittest import IsolatedAsyncioTestCase
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app
from db import async_db
from feature_flags import router
from db_fixtures import fixtures


app.include_router(router)
client = TestClient(app)


class TestFeatureFlags(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await async_db.connect()

    async def asyncTearDown(self):
        await async_db.disconnect()

    async def test_get(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/feature-flags/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @fixtures("fixtures/feature-flags")
    async def test_get_with_fixtures(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/feature-flags/")
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json(),
            [
                {"name": "feature1", "enabled": True},
                {"name": "feature2", "enabled": False},
            ],
        )
