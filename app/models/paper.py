from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(String, nullable=False)

    doi = Column(String, nullable=True)

    file_name = Column(String, nullable=True)

    storage_key = Column(String, nullable=True)

    processing_status = Column(
        String,
        default="uploaded"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )