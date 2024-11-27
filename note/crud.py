from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from ulid import ULID
from main import SessionLocal
from .models import Note, Tag
from .schemas import NoteCreate, NoteUpdate, NoteResponse, NoteList


class NoteService:
    def get_notes(self, user_id: str, page: int, items_per_page: int) -> NoteList:
        with SessionLocal() as db:
            query = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id)
            )
            total = query.count()
            notes = (
                query.offset((page - 1) * items_per_page).limit(items_per_page).all()
            )
            return NoteList(
                total_count=total,
                page=page,
                items_per_page=items_per_page,
                notes=[
                    NoteResponse(
                        **{**note.__dict__, "tags": [tag.name for tag in note.tags]}
                    )
                    for note in notes
                ],
            )

    def get_note(self, user_id: str, id: str) -> NoteResponse:
        with SessionLocal() as db:
            note = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id, Note.id == id)
                .first()
            )
            if not note:
                raise HTTPException(status_code=422)
            return NoteResponse(
                **{**note.__dict__, "tags": [tag.name for tag in note.tags]}
            )

    def create_note(self, user_id: str, note_create: NoteCreate) -> NoteResponse:
        with SessionLocal() as db:
            now = datetime.now()
            tags = []
            for name in note_create.tags:
                tag = db.query(Tag).filter(Tag.name == name).first()
                if not tag:
                    tag = Tag(id=str(ULID()), name=name, created_at=now, updated_at=now)
                tags.append(tag)

            note = Note(
                id=str(ULID()),
                user_id=user_id,
                title=note_create.title,
                content=note_create.content,
                memo_date=note_create.memo_date,
                tags=tags,
                created_at=now,
                updated_at=now,
            )
            db.add(note)
            db.commit()
            db.refresh(note)
            return NoteResponse(
                **{**note.__dict__, "tags": [tag.name for tag in note.tags]}
            )

    def update_note(
        self, user_id: str, id: str, note_update: NoteUpdate
    ) -> NoteResponse:
        with SessionLocal() as db:
            note = (
                db.query(Note)
                .options(joinedload(Note.tags))
                .filter(Note.user_id == user_id, Note.id == id)
                .first()
            )
            if not note:
                raise HTTPException(status_code=422)

            update_data = note_update.model_dump(exclude_unset=True)
            if "tags" in update_data:
                now = datetime.now()
                note.tags = []
                for name in update_data["tags"]:
                    tag = db.query(Tag).filter(Tag.name == name).first()
                    if not tag:
                        tag = Tag(
                            id=str(ULID()), name=name, created_at=now, updated_at=now
                        )
                    note.tags.append(tag)
                del update_data["tags"]

            for key, value in update_data.items():
                setattr(note, key, value)

            db.add(note)
            db.commit()
            db.refresh(note)
            return NoteResponse(
                **{**note.__dict__, "tags": [tag.name for tag in note.tags]}
            )

    def delete_note(self, user_id: str, id: str):
        with SessionLocal() as db:
            note = db.query(Note).filter(Note.user_id == user_id, Note.id == id).first()
            if not note:
                raise HTTPException(status_code=422)
            note.tags = []
            db.delete(note)
            db.commit()
            unused_tags = db.query(Tag).filter(~Tag.notes.any()).all()
            for tag in unused_tags:
                db.delete(tag)
            db.commit()


def get_note_service() -> NoteService:
    return NoteService()
