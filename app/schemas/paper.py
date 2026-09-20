from pydantic import BaseModel


class PaperCreate(BaseModel):
    title: str
    doi: str | None = None
    file_name: str | None = None
    storage_key: str | None = None


class PaperUpdate(BaseModel):
    title: str | None = None
    doi: str | None = None
    processing_status: str | None = None