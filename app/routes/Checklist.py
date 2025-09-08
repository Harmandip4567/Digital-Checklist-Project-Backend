from fastapi import Body
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user
import logging
import os
from fastapi import Form, UploadFile, File

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/checklist",
    tags=["Checklist"],
)


# -----------------------------
# Create Checklist Template
# -----------------------------
@router.post("/templates", response_model=schemas.ChecklistTemplateOut)
def create_template(
    payload: schemas.ChecklistTemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # ✅ Require logged-in user
):
    # Create template
    tpl = models.ChecklistTemplate(
        title=payload.title,
        description=payload.description,
        created_by=current_user.id,  # Use user ID (FK)
    )
    db.add(tpl)
    db.commit()
    db.refresh(tpl)

    # Add steps (items)
    for step in payload.steps:
        item = models.ChecklistItem(
            template_id=tpl.id,
            order=step.order,
            label=step.label,
            input_type=step.input_type,
            required=bool(step.required),
            frequency=step.frequency,
            unit=step.unit,
            options=step.options if step.options else None,
        )
        db.add(item)

    db.commit()
    db.refresh(tpl)
    return tpl


# -----------------------------
# Get all Templates
# -----------------------------
@router.get("/templates", response_model=List[schemas.ChecklistTemplateOut])
def get_templates(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    templates = db.query(models.ChecklistTemplate).all()
    return templates


# -----------------------------
# Get Items of a Template
# -----------------------------
@router.get("/templates/{template_id}", response_model=List[schemas.ChecklistItemOut])
def get_template_items(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    items = (
        db.query(models.ChecklistItem)
        .filter(models.ChecklistItem.template_id == template_id)
        .all()
    )
    return items


# -----------------------------
# Get Template and its Items both
# -----------------------------
@router.get("/template_with_items/{template_id}")
def get_template_with_items(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    template = (
        db.query(models.ChecklistTemplate)
        .filter(models.ChecklistTemplate.id == template_id)
        .first()
    )
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    items = (
        db.query(models.ChecklistItem)
        .filter(models.ChecklistItem.template_id == template_id)
        .all()
    )

    return {"template": template, "items": items}


@router.put("/template/{template_id}", response_model=schemas.ChecklistTemplateOut)
def update_template(template_id: int, data: schemas.TemplateUpdate, db: Session = Depends(get_db)):
    print("Updating template:", template_id, "with data:", data)

    # Fetch template
    template = db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # Update template fields
    template.title = data.title # type: ignore
    template.description = data.description # type: ignore

    # Map existing items by ID
    existing_items = {item.id: item for item in template.items}

    for item_data in data.items:
        if item_data.id and item_data.id in existing_items:
            # Update existing item
            item = existing_items[item_data.id]
            item.label = item_data.label
            item.input_type = item_data.input_type
            item.required = item_data.required
            item.frequency = item_data.frequency
            item.unit = item_data.unit
            del existing_items[item_data.id]  # Mark as processed

    db.commit()
    db.refresh(template)
    return template

# Update checklist status
@router.put("/templates/{template_id}/status")
def update_checklist_status(template_id: int, status: str = Body(..., embed=True), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    template = db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Checklist not found")
    template.status = status # type: ignore
    db.commit()
    db.refresh(template)
    return {"id": template.id, "status": template.status}




# we will use this later for  add the new items in checklistitems
            # # Add new item
            # new_item = models.ChecklistItem(
                  
            #     label=item_data.label,
            #     input_type=item_data.input_type,
            #     required=item_data.required,
            #     frequency=item_data.frequency,
            #     unit=item_data.unit,
            #     template_id=template.id,
            # )
            # db.add(new_item)



# Add a new Item to a existing Template
@router.post("/template/{template_id}/items", response_model=schemas.ChecklistItemOut)
def add_template_item(
    template_id: int,
<<<<<<< Updated upstream
    item_data: schemas.AddNewChecklistItem,
=======
    item_data: schemas.AddChecklistItem,
>>>>>>> Stashed changes
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    logger.info(f"Received order: {item_data.order}")

    template = db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    new_item = models.ChecklistItem(
        template_id=template.id,
        order=item_data.order,
        label=item_data.label,
        input_type=item_data.input_type,
        required=item_data.required,
        frequency=item_data.frequency,
        unit=item_data.unit
        
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# for deletion of a template
@router.delete("/template/{Template_id}")
def delete_template(Template_id:int,db=Depends(get_db),current_user= Depends(get_current_user)):
    templateToDelete=db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id==Template_id).first()
    if not templateToDelete:
        raise HTTPException(status_code =404 ,detail="Template to Delete not found")
    db.delete(templateToDelete)
    db.commit()
    
    return {"message":"template is deleted successfully"}
    
# for deletion of a item
@router.delete("/template/item/{itemId}")
def delete_template_item(itemId:int , db:Session =Depends(get_db),current_User= Depends(get_current_user)):
    itemToDelete = db.query(models.ChecklistItem).filter(models.ChecklistItem.id==itemId).first() 
    if not itemToDelete:
        raise HTTPException(status_code =404 ,detail="item to Delete not found") 
    db.delete(itemToDelete)
    db.commit()
    return {"message":"Item is deleted successfully"}


#------------------------------------------------------------------------
# For Maintianer Use
# Get Checklist Template Details (with items and status)
@router.get("/details/{template_id}", response_model=schemas.ChecklistTemplateOut)
def get_checklist_details(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    template = (
        db.query(models.ChecklistTemplate)
        .filter(models.ChecklistTemplate.id == template_id)
        .first()
    )
    if not template:
        raise HTTPException(status_code=404, detail="Checklist not found")
    # Items are loaded via relationship
    return template

# Update Checklist Status (Pending/Completed)
@router.put("/details/{template_id}/status", response_model=schemas.ChecklistTemplateOut)
async def update_checklist_status(
    template_id: int,
    status: str = Form(...),
    delay_reason: str = Form(None),
    notes: str = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    item_responses: str = Form(None),
    current_user: models.User = Depends(get_current_user),
):
    template = db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Checklist not found")
    if status:
        template.status = status # type: ignore
    if delay_reason is not None:
        template.delay_reason = delay_reason # type: ignore
    if notes is not None:
        template.notes = notes # type: ignore
    if file is not None:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)  # Ensure folder exists
        file_location = f"{upload_dir}/{template_id}_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        template.file_path = file_location # type: ignore
    if item_responses is not None:
        template.item_responses = item_responses # type: ignore
    db.commit()
    db.refresh(template)
    return template


# Getting all the checklists used by maintainer  (ie whose status is completed)

@router.get("/usedByMaintainer", response_model=List[schemas.ChecklistTemplateOut])
def get_used_checklists(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.ChecklistTemplate).filter(models.ChecklistTemplate.status != "pending").all()