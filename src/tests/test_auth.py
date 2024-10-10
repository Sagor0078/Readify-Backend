from src.auth.schemas import UserCreateModel
from .confest import fake_session,fake_user_service,test_client

auth_prefix = f"/api/v1/auth"

def test_user_creation(fake_session, fake_user_service, test_client):
    signup_data = {
        "first_name": "MD",
        "last_name": "Sagor",
        "username": "sagor9",
        "email": "musagor78@gmail.com",
        "password": "123456"
    }
    response = test_client.post(
        url=f"{auth_prefix}/signup",
        json=signup_data,
    )

    user_data = UserCreateModel(**signup_data)

    assert fake_user_service.user_exists_called_once()
    # assert fake_user_service.user_exists_called_once_with(signup_data['email'], fake_session)
    # assert fake_user_service.create_user_called_once()
    # assert fake_user_service.create_user_called_once_with(user_data, fake_session)

"""
  1. didn't solve the warnigs issue 
  2. pip install httx needed to require during the test
  3. continue.... 
"""