from datetime import datetime
import os
import uuid
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from sqlmodel import SQLModel, Field, create_engine, Session, select

# -----------------------------
# Config
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/postgres")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# -----------------------------
# Modelos (SQLModel)
# -----------------------------
class Upload(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    filename: str
    content_type: Optional[str] = None
    size_bytes: Optional[int] = None
    stored_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class Sheet(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    upload_id: uuid.UUID = Field(foreign_key="upload.id")
    name: str

# -----------------------------
# App
# -----------------------------
app = FastAPI(title="Saúde MVP API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------
# Rotas básicas
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.post("/files/upload")
def upload_file(file: UploadFile = File(...), session: Session = Depends(get_session)):
    if not file.filename.lower().endswith((".xlsx", ".xlsm")):
        raise HTTPException(status_code=400, detail="Envie um arquivo .xlsx ou .xlsm")

    # salvar no volume
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_id = uuid.uuid4()
    stored_name = f"{file_id}_{file.filename}"
    stored_path = os.path.join(UPLOAD_DIR, stored_name)

    contents = file.file.read()
    with open(stored_path, "wb") as f:
        f.write(contents)

    size_bytes = len(contents)

    # ler abas via pandas
    try:
        xls = pd.ExcelFile(stored_path)
        sheet_names = xls.sheet_names
    except Exception as e:
        # apaga o arquivo se der erro
        if os.path.exists(stored_path):
            os.remove(stored_path)
        raise HTTPException(status_code=400, detail=f"Não consegui ler a planilha: {e}")

    # salvar Upload
    up = Upload(
        id=file_id,
        filename=file.filename,
        content_type=file.content_type,
        size_bytes=size_bytes,
        stored_path=stored_path,
    )
    session.add(up)
    session.commit()

    # salvar Sheets
    for name in sheet_names:
        session.add(Sheet(upload_id=up.id, name=name))
    session.commit()

    return {"upload_id": str(up.id), "filename": up.filename, "sheet_names": sheet_names}

@app.get("/uploads")
def list_uploads(session: Session = Depends(get_session)):
    uploads = session.exec(select(Upload).order_by(Upload.uploaded_at.desc())).all()
    return [
        {
            "id": str(u.id),
            "filename": u.filename,
            "uploaded_at": u.uploaded_at.isoformat(),
            "size_bytes": u.size_bytes,
        } for u in uploads
    ]

@app.get("/sheets")
def list_sheets(upload_id: Optional[str] = None, session: Session = Depends(get_session)):
    query = select(Sheet)
    if upload_id:
        try:
            uid = uuid.UUID(upload_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="upload_id inválido")
        query = query.where(Sheet.upload_id == uid)
    sheets = session.exec(query).all()
    return [{"id": str(s.id), "upload_id": str(s.upload_id), "name": s.name} for s in sheets]

@app.get("/exports/csv")
def export_csv(upload_id: str, session: Session = Depends(get_session)):
    # MVP: exporta só a lista de abas daquele upload
    try:
        uid = uuid.UUID(upload_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="upload_id inválido")
    sheets = session.exec(select(Sheet).where(Sheet.upload_id == uid)).all()
    if not sheets:
        raise HTTPException(status_code=404, detail="Nada encontrado para esse upload_id")

    # Gera CSV em memória
    lines = ["sheet_name"]
    lines += [s.name for s in sheets]
    csv = "\n".join(lines)

    return StreamingResponse(
        iter([csv]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=abas_{upload_id}.csv"},
    )

# Ganchos futuros (stubs)
@app.get("/reports/rdqa/preview")
def rdqa_preview(upload_id: str):
    # Futuro: ler abas específicas, aplicar legenda, regras de negócio e montar prévia
    return {"message": "preview RDQA em construção", "upload_id": upload_id}

@app.get("/reports/rag/preview")
def rag_preview(upload_id: str):
    return {"message": "preview RAG em construção", "upload_id": upload_id}
