from typing import List, Optional
from datetime import datetime # Python punya
from pydantic import BaseModel

# App Name
class AppNameBase(BaseModel):
    app_name: str

class AppNameCreate(AppNameBase):
    pass

class AppName(AppNameBase):
    id_app: int
    time: datetime = None

    class Config:
        orm_mode = True

# Flag App
class FlagApp(BaseModel):
    id_flag: int
    flag: str

    class Config:
        orm_mode = True

# Current Version
class CurrentVersionBase(BaseModel):
    id_app: int
    current_version: str
    keterangan: str

class CurrentVersionCreate(CurrentVersionBase):
    pass

class CurrentVersion(CurrentVersionBase):
    id_current: int
    time: datetime = None
    id_flag: int

    class Config:
        orm_mode = True

# CVE App
class CveBase(BaseModel):
    id_app: int
    cve: str
    cve_link: str

class CveCreate(CveBase):
    pass

class Cve(CveBase):
    id_cve: int
    time: datetime = None
    id_flag: int

    class Config:
        orm_mode = True

# Latest Version
class LatestVersionBase(BaseModel):
    id_app: int
    latest_version: str
    release_notes: str

class LatestVersionCreate(LatestVersionBase):
    pass

class LatestVersion(LatestVersionBase):
    id_latest: int
    time: datetime = None
    id_flag: int

    class Config:
        orm_mode = True

# Status App
class StatusAppBase(BaseModel):
    id_app: int
    status: str

class StatusAppCreate(StatusAppBase):
    pass

class StatusApp(StatusAppBase):
    id_status: int
    time: datetime = None
    id_flag: int

    class Config:
        orm_mode = True