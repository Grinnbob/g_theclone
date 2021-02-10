from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.addon.template as template_schema
from ..models.addon.template import Template
from aiogoogle import Aiogoogle
from app.core.config import settings
from app.providers.google.utills import build_client_creds, build_aiogoogle
from bson.objectid import ObjectId
from aiogoogle.auth.creds import UserCreds, ClientCreds

class TemplateService(BaseService[Template, template_schema.TemplateCreate, template_schema.TemplateUpdate]):
    def __init__(self):
        super().__init__(model=Template)

    async def get_templates(self,
                            account_id: str,
                            limit: int = 1000) -> Any:

        cursor = Template.find({
            'accounts' : {
                '$elemMatch' : {'$eq' : account_id}
            }
        }).limit(limit)

        return list(await cursor.to_list(length=limit))

    async def create(self,
                     payload: template_schema.TemplateCreate) -> Template:

        exist = await Template.find_one({'template_id': payload.template_id})
        if exist:
            raise AppErrors(f"Template already exist template_id={payload.template_id}")

        data = payload.dict(exclude_unset=True)
        template = Template(**data)

        await template.commit()
        await template.reload()

        return template
