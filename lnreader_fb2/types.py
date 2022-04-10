import html
from datetime import datetime
from typing import List, Optional

import pydantic


class Base(pydantic.BaseModel):
    pass


class Novel(Base):
    novelId: int
    sourceId: int
    followed: int
    unread: int
    source: str
    novelName: str
    novelSummary: str
    novelUrl: pydantic.HttpUrl
    sourceUrl: pydantic.HttpUrl
    novelCover: pydantic.HttpUrl
    author: Optional[str] = None
    artist: Optional[str] = None
    status: Optional[str] = None
    genre: Optional[str] = None


class Chapter(Base):
    chapterId: int
    chapterUrl: pydantic.HttpUrl
    novelId: int
    chapterName: str
    releaseDate: datetime
    bookmark: int
    read: int
    downloaded: int


class Download(Base):
    downloadId: int
    downloadChapterId: int
    chapterName: str
    chapterText: str

    @pydantic.validator("chapterText")
    def decode(cls, v):
        return html.unescape(v)


class Backup(Base):
    novels: List[Novel]
    chapters: List[Chapter]
    downloads: List[Download]
