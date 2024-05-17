from pydantic import BaseModel


class AdminConfigSchema(BaseModel):
    username: str
    password: str
    admin_url: str
    service_key: str
