from pydantic import BaseModel


class RecipeList(BaseModel):
    id: int
    name: str
    views: int
    cooking_time: int

    class Config:
        from_attributes = True


class RecipeCreate(BaseModel):
    name: str
    cooking_time: int  # >0
    ingredients: str
    description: str


class RecipeDetail(BaseModel):
    id: int
    name: str
    cooking_time: int
    ingredients: str
    description: str
    views: int

    class Config:
        from_attributes = True
        return v.strip()


class RecipeDetail(BaseModel):
    """Schema for recipe details (detail screen)."""

    id: int
    name: str = Field(..., min_length=1, max_length=200)
    cooking_time: int = Field(..., gt=0)
    ingredients: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    views: int = Field(..., ge=0)

    model_config = {"from_attributes": True}
