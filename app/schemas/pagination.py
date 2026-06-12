from django.views.defaults import page_not_found
from pydantic import BaseModel
from fastapi import Query
from typing import Generic, TypeVar, List

from sqlalchemy.ext.orderinglist import ordering_list

#Using generic variable
T = TypeVar("T")

class PaginationParams:
    """
    Class for pagination/sorting params from URL query string
    """
    def __init__(
            self,
            page: int = Query(default=1, ge=1, description="Page number"),
            page_size: int = Query(default=10, ge=1, le=100, description="Elements per page"),
            sort_by: str = Query(default="created_at", description="Sort field"),
            order : str = Query(default="desc", pattern="^(asc|desc)$", description="sort order"),
    ):
                self.page = page
                self.page_size = page_size
                self.sort_by = sort_by
                self.order = order

class PaginatedResponse(BaseModel,Generic[T]):
    """
    Paginated Response Generic
    Specify type of item at use : PaginatedResponse[TaskOut], PaginatedResponse[UserOut]
    """

    items: List[T] #List of items from current page
    total: int #Total of elements in db
    page: int #current page
    page_size: int #number of element per page
    total_pages: int #total number of pages from service


