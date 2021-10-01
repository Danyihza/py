from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class AppName(Base):
    __tablename__ = "app_names"
    __table_args__ = {"schema": "blibli"}
    id_app = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, unique=True, index=True)
    time = Column(DateTime(timezone=True), default=func.now())

    currentVersion = relationship("CurrentVersion", back_populates="appName")
    cveApp = relationship("Cve", back_populates="appName")
    latestVersion = relationship("LatestVersion", back_populates="appName")
    statusApp = relationship("StatusApp", back_populates="appName")

class FlagApp(Base):
    __tablename__ = "flag_apps"
    __table_args__ = {"schema": "blibli"}
    id_flag = Column(Integer, primary_key=True, index=True)
    flag = Column(String, index=True)

    currentVersion = relationship("CurrentVersion", back_populates="flagApp")
    cveApp = relationship("Cve", back_populates="flagApp")
    latestVersion = relationship("LatestVersion", back_populates="flagApp")
    statusApp = relationship("StatusApp", back_populates="flagApp")

class CurrentVersion(Base):
    __tablename__ = "current_versions"
    __table_args__ = {"schema": "blibli"}
    id_current = Column(Integer, primary_key=True, index=True)
    id_app = Column(Integer, ForeignKey(AppName.id_app), index=True)
    current_version = Column(String, index=True)
    keterangan = Column(String, index=True)
    time = Column(DateTime(timezone=True), default=func.now())
    id_flag = Column(Integer, ForeignKey(FlagApp.id_flag), index=True)

    appName = relationship("AppName", back_populates="currentVersion")
    flagApp = relationship("FlagApp", back_populates="currentVersion")

class Cve(Base):
    __tablename__ = "cves"
    __table_args__ = {"schema": "blibli"}
    id_cve = Column(Integer, primary_key=True, index=True)
    id_app = Column(Integer, ForeignKey(AppName.id_app), index=True)
    cve = Column(String, index=True)
    cve_link = Column(String, index=True)
    time = Column(DateTime(timezone=True), default=func.now())
    id_flag = Column(Integer, ForeignKey(FlagApp.id_flag), index=True)

    appName = relationship("AppName", back_populates="cveApp")
    flagApp = relationship("FlagApp", back_populates="cveApp")

class LatestVersion(Base):
    __tablename__ = "latest_versions"
    __table_args__ = {"schema": "blibli"}
    id_latest = Column(Integer, primary_key=True, index=True)
    id_app = Column(Integer, ForeignKey(AppName.id_app), index=True)
    latest_version = Column(String, index=True)
    release_notes = Column(String, index=True)
    time = Column(DateTime(timezone=True), default=func.now())
    id_flag = Column(Integer, ForeignKey(FlagApp.id_flag), index=True)

    appName = relationship("AppName", back_populates="latestVersion")
    flagApp = relationship("FlagApp", back_populates="latestVersion")

class StatusApp(Base):
    __tablename__ = "status_apps"
    __table_args__ = {"schema": "blibli"}
    id_status = Column(Integer, primary_key=True, index=True)
    id_app = Column(Integer, ForeignKey(AppName.id_app), index=True)
    status = Column(String, index=True)
    time = Column(DateTime(timezone=True), default=func.now())
    id_flag = Column(Integer, ForeignKey(FlagApp.id_flag), index=True)

    appName = relationship("AppName", back_populates="statusApp")
    flagApp = relationship("FlagApp", back_populates="statusApp")
