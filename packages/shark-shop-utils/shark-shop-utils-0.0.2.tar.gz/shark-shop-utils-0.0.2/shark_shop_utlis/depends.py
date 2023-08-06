from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from httpx import AsyncClient


class UsersEndpoints(Enum):
    ME = "users/me"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


class CurrentUserBase:
    def __init__(self, users_service_url: str):
        self.users_service_url = users_service_url

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        async with AsyncClient() as client:
            url = self.users_service_url + UsersEndpoints.ME.value
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = await client.get(url, headers=headers)
            if response.status_code == 401:
                raise unauthorized_exception
            user = response.json()
        return user


class CurrentUser(CurrentUserBase):
    async def __call__(self, token: str = Depends(oauth2_scheme)):
        return await self.get_current_user(token)


class CurrentSuperUser(CurrentUserBase):
    async def __call__(self, token: str = Depends(oauth2_scheme)):
        user = await self.get_current_user(token)
        if not user['is_superuser']:
            raise unauthorized_exception
        return user
