from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, database,models, OAuth2


router = APIRouter(prefix='/like', tags=['Like'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db : Session = Depends(database.get_db), current_user: int = Depends(OAuth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {like.post_id} does not exist")

    like_query = db.query(models.Like).filter(models.Like.post_id ==like.post_id, models.Like.user_id == current_user.user_id)

    found_like =like_query.first()

    if like.direction ==1:

        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The user {current_user.user_id} has already liked on post {like.post_id}")
        
        new_like = models.Like(post_id = like.post_id, user_id = current_user.user_id)
        db.add(new_like)
        db.commit()
        return {"Message": "You have successfully liked the post."}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist")
        
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted like"}