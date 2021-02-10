from typing import List, Any, Optional
from fastapi import APIRouter, Body, Depends, Path, Query, Request

from app.exceptions import *
from app.api.utils import *
from app.core.config import settings
from app.api import deps

from app.services import form_service
from app.services.models.user import User
import app.schemas.models.form as form_schema


router = APIRouter()

@router.get("/", response_model=form_schema.FormInDB)
async def get_form(
    id:str,
    current_user: User = Depends(deps.get_current_active_user),
    service: form_service.FormService = Depends(deps.get_form_service)
) -> Any:

    return hack_serialize(await service.get(id=id,
                                owner_id=current_user.id))


#DASHBOARD routines
@router.post("/", response_model=form_schema.FormInDB)
async def create_form(
    form_id: str,
    current_user: User = Depends(deps.get_current_active_user),
    service: form_service.FormService = Depends(deps.get_form_service)
) -> Any:
    if not form_id:
        raise AppErrors("form_id can't be empty")

    return hack_serialize(await service.create(owner_id=current_user.id,
                                    form_id=form_id))


#DASHBOARD routines
@router.put("/", response_model=form_schema.FormInDB)
async def update_form(
    form_update: form_schema.FormUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    service: form_service.FormService = Depends(deps.get_form_service)
) -> Any:

    return hack_serialize(await service.update(owner_id=current_user.id,
                                    obj_in=form_update))

@router.delete("/")
async def remove_form(
    id:str,
    current_user: User = Depends(deps.get_current_active_user),
    service: form_service.FormService = Depends(deps.get_form_service)
) -> Any:

    return await service.remove(id=id,
                                owner_id=current_user.id)

