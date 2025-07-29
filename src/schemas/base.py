from typing import Optional, Literal, Annotated

from pydantic import BaseModel, Field, StringConstraints


class BaseCollectionRequestParams(BaseModel):
    page: Optional[int] = Field(
        default=1,
        ge=1,
    )
    page_size: Optional[
        Literal[10, 25, 100]
    ] = 100
    search: Optional[
        Annotated[
            str,
            StringConstraints(min_length=2),
        ]
    ] = None
