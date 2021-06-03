from typing import List
from ..repository import blogs
from fastapi import APIRouter, Depends, HTTPException, Response

from ..database import get_db
from .. import models, schemas, oauth2

from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Blogs'],
    prefix='/blogs'
)


@router.get("/", response_model=List[schemas.ShowBlog])
def getAll(current_user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return blogs.get_all_blogs(db)


@router.post("/new", status_code=201)
def create(blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = blogs.create_blog(db, blog)
    return {
        "status": "created",
        "data": new_blog
    }


@router.get("/detail/{id}", response_model=schemas.ShowBlog)
def detail(id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogs.get_blog_by_id(db, id)


@router.put("/update/{id}", status_code=202)
def update(id: int, blog: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail="not_found")
    blog.update(blog, synchronize_session=False)
    db.commit()
    return {
        "status": "updated",
    }


@router.delete("/delete/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blogs.delete_blog(db, id)
