from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class AppName(Base):
    __tablename__ = "app_names"
    __table_args__ = {"schema": "blibli"}
    id_app = Column(Integer, primary_key=True, index=True)
    app_name = Column(String, unique=True, index=True)
    time = Column(DateTime(timezone=True), default=func.now())

    script_current = relationship("ScriptCurrent", back_populates="app_name")
    script_latest = relationship("ScriptLatest", back_populates="app_name")
    script_cve = relationship("ScriptCve", back_populates="app_name")

class ScriptCurrent(Base):
    __tablename__ = "script_current"
    __table_args__ = {"schema": "blibli"}
    id = Column(Integer, primary_key=True, index=True)
    id_app = Column(Integer, ForeignKey(AppName.id_app), index=True)
    current_url = Column(String, index=True)
    current_selector = Column(String, index=True)
    type = Column(String, index=True)
    time = Column(DateTime(timezone=True), default=func.now())

    app_name = relationship("AppName", back_populates="script_current")

class ScriptLatest(Base):
    __tablename__ = "script_latest"
    __table_args__ = {"schema": "blibli"}
    id = Column(Integer, primary_key=True, index=True)
    id_app = Column(Integer, ForeignKey(AppName.id_app), index=True)
    latest_url = Column(String, index=True)
    latest_xpath = Column(String, index=True)
    release_notes_url = Column(String, index=True)
    type = Column(String, index=True)
    time = Column(DateTime(timezone=True), default=func.now())

    app_name = relationship("AppName", back_populates="script_latest")

class ScriptCve(Base):
    __tablename__ = "script_cve"
    __table_args__ = {"schema": "blibli"}
    id = Column(Integer, primary_key=True, index=True)
    id_app = Column(Integer, ForeignKey(AppName.id_app), index=True)
    cve_xpath = Column(String, index=True)
    cve_url = Column(String, index=True)
    time = Column(DateTime(timezone=True), default=func.now())

    app_name = relationship("AppName", back_populates="script_cve")