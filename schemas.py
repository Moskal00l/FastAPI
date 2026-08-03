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