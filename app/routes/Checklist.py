from fastapi import Depends
from app.dependencies import get_current_user  # adjust import to your code
from app import models, schemas
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import APIRouter
router = APIRouter(prefix="/checklist", tags=["Checklist"])

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
