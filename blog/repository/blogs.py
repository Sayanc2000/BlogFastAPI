from fastapi import HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas


def get_all_blogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(db: Session, blog: schemas.Blog):
    new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_blog_by_id(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="not_found")
    return blog


def delete_blog(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail="not_found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"
