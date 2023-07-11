
import json
from datetime import datetime


async def test_get_progressions(superuser_client):
    response = await superuser_client.get('/employee-progressions')
    assert response.status_code == 200


async def test_get_my_progression(current_user_client):
    response = await current_user_client.get('/employee-progressions/mine')
    assert response.status_code == 200


async def test_add_progression(superuser_client):
    response = await superuser_client.post('/employee-progressions', json={
        "currentPositionDate": "2023-07-11T09:00:47.023Z",
        "salary": 1000,
        "promotionPositionDate": "2023-07-11T09:00:47.023Z",
        "currentPositionLevelId": 1,
        "promotionPositionLevelId": 1
    })

    assert response.status_code == 201
