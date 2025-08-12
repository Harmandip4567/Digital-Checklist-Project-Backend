from fastapi import Depends
from app.dependencies import get_current_user  # adjust import to your code
from app import models, schemas
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import APIRouter
from typing import List
from fastapi import HTTPException
router = APIRouter(prefix="/templates", tags=["Templates"])
@router.get("/", response_model=List[schemas.ChecklistTemplateOut])
def get_all_templates(db: Session = Depends(get_db)):
    templates = db.query(models.ChecklistTemplate).all()
    return templates

@router.get("/{template_id}", response_model=schemas.ChecklistTemplateOut)
def get_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    template = db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(template)
    db.commit()
    return {"message": "Template deleted successfully"}
