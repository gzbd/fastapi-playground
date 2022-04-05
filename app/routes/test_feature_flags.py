from unittest import IsolatedAsyncioTestCase
from httpx import AsyncClient

from ..main import app
from .feature_flags import router
from ..db.db_fixtures import fixtures, requires_db


app.include_router(router)


class TestFeatureFlags(IsolatedAsyncioTestCase):
    @requires_db
    async def test_get(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/feature-flags/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    @requires_db
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
