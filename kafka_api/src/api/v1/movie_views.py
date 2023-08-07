import logging
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel

from api.utils.extensions import is_authenticated
from services.movie_view import get_movie_view_service, MovieViewService

router = APIRouter()


class MovieViewRequest(BaseModel):
    film_id: UUID
    number_seconds_viewing: int


class MovieViewResponse(BaseModel):
    number_seconds_viewing: int


@router.get(
    "/number_seconds_viewing",
    response_model=MovieViewResponse
)
async def get_user_movie_timestamp(
    token_sub = Depends(is_authenticated),
    film_id: UUID = Query(description="id фильма, который смотрел пользователь"),
    movie_viewing_service: MovieViewService = Depends(get_movie_view_service),
) -> MovieViewResponse:
    user_id = token_sub.get('user_id')
    number_seconds_viewing = await movie_viewing_service.get_number_seconds_viewing(
        user_id, film_id
    )
    if number_seconds_viewing is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Not found")
    return MovieViewResponse(number_seconds_viewing=number_seconds_viewing)




@router.post(
    "/number_seconds_viewing"
)
async def add_user_movie_timestamp(
    movie_view_request: MovieViewRequest,
    token_sub=Depends(is_authenticated),
    movie_viewing_service: MovieViewService = Depends(get_movie_view_service),
) -> str:
    user_id = token_sub.get('user_id')
    try:
        await movie_viewing_service.add_number_seconds_viewing(
            user_id,
            movie_view_request.film_id,
            movie_view_request.number_seconds_viewing,
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    else:
        return "Ok"
