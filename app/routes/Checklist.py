from fastapi import Depends
from app.dependencies import get_current_user  # adjust import to your code
from app import models, schemas
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import APIRouter
router = APIRouter(prefix="/checklist", tags=["Checklist"])
from typing import List
from fastapi import HTTPException
@router.post("/templates", response_model=schemas.ChecklistTemplateOut)
def create_template(
    payload: schemas.ChecklistTemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # ✅ Require logged in user
):
    tpl = models.ChecklistTemplate(
        title=payload.title,
        description=payload.description,
        created_by=current_user.id  # Use user ID as it's an Integer foreign key
    )
    db.add(tpl)
    db.commit()
    db.refresh(tpl)

    for step in payload.steps:
        item = models.ChecklistItem(
            template_id=tpl.id,
            order=step.order,
            label=step.label,
            input_type=step.input_type,
            required=bool(step.required),
            frequency=step.frequency,
            unit=step.unit,
            options=step.options if step.options else None
        )
        db.add(item)
    db.commit()
    db.refresh(tpl)
    return tpl



# for showing the existing templates


@router.get("/templates", response_model=List[schemas.ChecklistTemplateOut])
def get_templates(db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    templates = db.query(models.ChecklistTemplate).all()
    return templates

# for showing the  items of the clicked template
# the reason why this is not working earlier as when we use .first() it return a single row which is a object but we use respose model as list of objects so we need to use .all() to get all the rows as a list of objects
@router.get("/templates/{template_id}", response_model=List[schemas.ChecklistItemOut])
def get_template_items(template_id: int, db: Session = Depends(get_db),currentUser=Depends(get_current_user)):
    items =db.query(models.ChecklistItem).filter(models.ChecklistItem.template_id == template_id).all()
    return items

# for getting both the detils of template and items in frontend page ie TemplateItems.jsx
@router.get("/template_with_items/{template_id}")
def get_template_with_items(template_id: int, db: Session = Depends(get_db),currentUser=Depends(get_current_user)):
    template = db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    items = db.query(models.ChecklistItem).filter(models.ChecklistItem.template_id == template_id).all()

    return {
        "template": template,
        "items": items
    }
