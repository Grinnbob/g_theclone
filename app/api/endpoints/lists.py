from typing import List, Any, Optional
from fastapi import APIRouter, Body, Depends, Path, Query, Request

from app.exceptions import *
from app.api.utils import *
from app.core.config import settings
from app.api import deps

from app.services import form_service, list_service
from app.services.models.list import SyncList
from app.services.models.user import User
import app.schemas.models.list as list_schema
import app.schemas.models.form as form_schema


router = APIRouter()

#DASHBOARD routines
@router.post("/", response_model=list_schema.ListInDB)
async def create_list(
    form_id: str,
    current_user: User = Depends(deps.get_current_active_user),
    form_service: form_service.FormService = Depends(deps.get_form_service)
) -> Any:

    return hack_serialize(await form_service.dump(owner_id=current_user.id,
                                    form_id=form_id,
                                    model_class=SyncList))


#DASHBOARD routines
@router.get("/list/", response_model=List[list_schema.ListInDB])
async def list_lists(
    page: int = 0,
    current_user: User = Depends(deps.get_current_active_user),
    service: list_service.ListService = Depends(deps.get_list_service)
) -> Any:

    skip, limit = page_to_raw(page)
    return hack_serialize(await service.get_multi(owner_id=current_user.id,
                                    skip=skip,
                                    limit=limit))

#DASHBOARD routines
@router.get("/", response_model=list_schema.ListInDB)
async def get_list(
    id:str,
    current_user: User = Depends(deps.get_current_active_user),
    service: list_service.ListService = Depends(deps.get_list_service)
) -> Any:

    return hack_serialize(await service.get(
                                    id=id,
                                    owner_id=current_user.id))

@router.delete("/")
async def remove_list(
    id:str,
    current_user: User = Depends(deps.get_current_active_user),
    service: list_service.ListService = Depends(deps.get_list_service)
) -> Any:

    return await service.remove(id=id,
                                owner_id=current_user.id)

