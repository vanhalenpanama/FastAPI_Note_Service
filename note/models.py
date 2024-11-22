from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

note_tag_association = Table(
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(36), ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id")),
)


class Note(Base):
    __tablename__ = "Note"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    tags = relationship(
        "Tag", secondary=note_tag_association, back_populates="notes", lazy="joined"
    )


class Tag(Base):
    __tablename__ = "Tag"
    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes = relationship(
        "Note", secondary=note_tag_association, back_populates="tags", lazy="joined"
    )
