from typing import List
from fastapi import APIRouter, Depends, Query
from auth import get_current_user, CurrentUser
from .schemas import NoteCreate, NoteUpdate, NoteResponse, NoteList
from .crud import NoteService, get_note_service

router = APIRouter()


@router.post("", response_model=NoteResponse, status_code=201)
async def create_note(
    body: NoteCreate,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    return note_service.create_note(user_id=current_user.id, note_create=body)


@router.get("", response_model=NoteList)
async def get_notes(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    return note_service.get_notes(
        user_id=current_user.id,
        page=page,
        items_per_page=items_per_page,
    )


@router.get("/{id}", response_model=NoteResponse)
async def get_note(
    id: str,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    return note_service.get_note(user_id=current_user.id, id=id)


@router.put("/{id}", response_model=NoteResponse)
async def update_note(
    id: str,
    body: NoteUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    return note_service.update_note(user_id=current_user.id, id=id, note_update=body)


@router.delete("/{id}", status_code=204)
async def delete_note(
    id: str,
    current_user: CurrentUser = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    note_service.delete_note(user_id=current_user.id, id=id)
