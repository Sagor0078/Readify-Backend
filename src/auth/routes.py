from fastapi import APIRouter, Depends, status
from .service import UserService
from src.config import Config
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from src.db.redis import add_jti_to_blocklist
from src.mail import create_message, mail_config, mail
from src.errors import InvalidCredentials, UserAlreadyExists, UserNotFound, InvalidToken

from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    get_current_user,
    RoleChecker,
)
from .schemas import (
    UserCreateModel,
    UserLoginModel,
    UserModel,
    UserBooksModel,
    EmailsModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel
)

from .utils import (
    create_access_token,
    verify_password,
    decode_token,
    create_url_safe_token,
    decode_url_safe_token,
    generate_password_hash
)

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post("/send_mail")
async def send_mail(emails: EmailsModel):
    emails = emails.address

    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to our app"
    message = create_message(recipients=emails, subject=subject, body=html)
    await mail.send_message(message)
    return {"message": "Email sent successfully"}


@auth_router.post(
    "/signup",status_code=status.HTTP_201_CREATED
)
async def create_user_Account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):

    email = user_data.email
    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user,
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )



@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    # Check if the token is still valid
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})
    raise InvalidToken()


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )

@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):

    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset your password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """

    message = create_message(
        recipients=[email], subject="Reset Your Password", body=html_message
    )

    await mail.send_message(message)

    return JSONResponse(
        content={
            "message": "Please check your email instructions to reset your password"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post("/password-reset-confirm/{token}")
async def verify_user_account(token: str, passwords: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):
    
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(detail="Password do not match", status_code=status.HTTP_404_BAD_REQUEST)
        
    
    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()
        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {"password_hash": password_hash}, session)

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during password reset"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

