from typing import List
import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    os.environ['ORIGIN_1'],
    os.environ['ORIGIN_2']
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = [
       "GET",
       "POST",
       "PUT" 
    ],
    allow_headers = ["*"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------SET HOME PAGE--------------------------
@app.get("/", status_code=200)
async def home(db: Session = Depends(get_db)):
    return {"message": "Hello, World!"}

# ---------------------------GET ALL DATA---------------------------
@app.get("/all/{id_app}", status_code=200)
async def get_all_data(id_app: int, db: Session = Depends(get_db)):
    app_name = await get_one_app_name(id_app, db)
    current_ver = await get_one_current_version(id_app, db)
    latest_ver = await get_one_latest_version(id_app, db)
    cve = await get_one_cve(id_app, db)
    app_status = await get_one_status(id_app, db)

    data_dict = {
        "app_name": app_name,
        "current_version": current_ver,
        "latest_version": latest_ver,
        "cve": cve,
        "app_status": app_status
    }

    return data_dict

# -----------------------------APP NAME-----------------------------
@app.get("/app-names/", response_model=List[schemas.AppName])
async def get_all_app_names(db: Session = Depends(get_db)):
    get = await crud.get_app_name_all(db)
    return get

@app.get("/app-name/{id_app}", response_model=schemas.AppName)
async def get_one_app_name(id_app: int, db: Session = Depends(get_db)):
    get = await crud.get_app_name(db, id_app=id_app)
    if get is None:
        raise HTTPException(status_code=404, detail="App Name Not Found")
    return get

@app.post("/app-name/", response_model=schemas.AppName, status_code=status.HTTP_201_CREATED)
async def create_new_app_name(app: schemas.AppNameCreate, db: Session = Depends(get_db)):
    get = await crud.get_app_name_by_name(db, app_name=app.app_name)
    if get:
        raise HTTPException(status_code=400, detail="App Name Already Exists")
    post_app_name = await crud.create_app_name(db=db, data=app)
    return post_app_name

# -----------------------------CURRENT VERSION-----------------------------
@app.get("/current-versions/", response_model=List[schemas.CurrentVersion])
async def get_all_current_versions(db: Session = Depends(get_db)):
    get = await crud.get_current_version_all(db)
    return get

@app.get("/current-version/{id_app}", response_model=schemas.CurrentVersion)
async def get_one_current_version(id_app: int, db: Session = Depends(get_db)):
    get = await crud.get_current_version(db, id_app=id_app)
    if get is None:
        raise HTTPException(status_code=404, detail="Current Versions Data Not Found")
    return get

@app.post("/current-version/", status_code=status.HTTP_201_CREATED)
async def create_new_current_version(data: schemas.CurrentVersionCreate, db: Session = Depends(get_db)):
    exists = db.query(models.CurrentVersion).filter(
        models.CurrentVersion.id_app == data.id_app,
        models.CurrentVersion.id_flag == 1
    ).first()

    if exists is not None:
        if (exists.current_version == data.current_version and
            exists.keterangan == data.keterangan):
            raise HTTPException(status_code=400, detail="Current Version Already Exists")
        else:
            exists.id_flag = 2
            return await crud.create_current_version(db=db, data=data)
    else:
        return await crud.create_current_version(db=db, data=data)

 # -----------------------------CVE APP-----------------------------
@app.get("/cves/", response_model=List[schemas.Cve])
async def get_all_cves(db: Session = Depends(get_db)):
    get = await crud.get_cve_all(db)
    return get

@app.get("/cve/{id_app}", response_model=schemas.Cve)
async def get_one_cve(id_app: int, db: Session = Depends(get_db)):
    get = await crud.get_cve(db, id_app=id_app)
    if get is None:
        raise HTTPException(status_code=404, detail="CVE Data Not Found")
    return get

@app.post("/cve/", response_model=schemas.Cve, status_code=status.HTTP_201_CREATED)
async def create_new_cve(data: schemas.CveCreate, db: Session = Depends(get_db)):

    exists = db.query(models.Cve).filter(
        models.Cve.id_app == data.id_app,
        models.Cve.id_flag == 1
        ).first()

    if exists is not None:
        if (exists.cve == data.cve and
            exists.cve_link == data.cve_link):
            raise HTTPException(status_code=400, detail="CVE Already Exists")
        else:
            exists.id_flag = 2
            return await crud.create_cve(db=db, data=data)
    else:
        return await crud.create_cve(db=db, data=data)

# -----------------------------LATEST VERSION-----------------------------
@app.get("/latest-versions/", response_model=List[schemas.LatestVersion])
async def get_all_latest_versions(db: Session = Depends(get_db)):
    get = await crud.get_latest_version_all(db)
    return get

@app.get("/latest-version/{id_app}", response_model=schemas.LatestVersion)
async def get_one_latest_version(id_app: int, db: Session = Depends(get_db)):
    get = await crud.get_latest_version(db, id_app=id_app)
    if get is None:
        raise HTTPException(status_code=404, detail="Latest Version Not Found")
    return get

@app.post("/latest-version/", response_model=schemas.LatestVersion, status_code=status.HTTP_201_CREATED)
async def create_new_latest_version(data: schemas.LatestVersionCreate, db: Session = Depends(get_db)):

    exists = db.query(models.LatestVersion).filter(
        models.LatestVersion.id_app == data.id_app,
        models.LatestVersion.id_flag == 1
        ).first()

    if exists is not None:
        if (exists.latest_version == data.latest_version and
            exists.release_notes == data.release_notes):
            raise HTTPException(status_code=400, detail="Latest Version Already Exists")
        else:
            exists.id_flag = 2
            return await crud.create_latest_version(db=db, data=data)
    else:
        return await crud.create_latest_version(db=db, data=data)

# -----------------------------STATUS APP-----------------------------
@app.get("/status-all/", response_model=List[schemas.StatusApp])
async def get_all_status(db: Session = Depends(get_db)):
    get = await crud.get_status_all(db)
    return get

@app.get("/status/{id_app}", response_model=schemas.StatusApp)
async def get_one_status(id_app: int, db: Session = Depends(get_db)):
    get = await crud.get_status(db, id_app=id_app)
    if get is None:
       return {"app_status": "Status is empty"}
    return get

@app.post("/status/", response_model=schemas.StatusApp, status_code=status.HTTP_201_CREATED)
async def create_new_status(data: schemas.StatusAppCreate, db: Session = Depends(get_db)):

    exists = db.query(models.StatusApp).filter(
        models.StatusApp.id_app == data.id_app,
        models.StatusApp.id_flag == 1
        ).first()

    if exists is not None:
        if  exists.status == data.status:
            raise HTTPException(status_code=400, detail="App Status Already Exists")
        else:
            exists.id_flag = 2
            return await crud.create_status(db=db, data=data)
    else:
        return await crud.create_status(db=db, data=data)