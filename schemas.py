from pydantic import BaseModel, Field, field_validator


class RecipeList(BaseModel):
    """Schema for listing recipes (main screen)."""

    id: int
    name: str = Field(..., min_length=1, max_length=200)
    views: int = Field(..., ge=0)
    cooking_time: int = Field(..., gt=0, description="Время приготовления в минутах")

    model_config = {"from_attributes": True}


class RecipeCreate(BaseModel):
    """Schema for creating a new recipe."""

    name: str = Field(..., min_length=1, max_length=200, description="Название рецепта")
    cooking_time: int = Field(..., gt=0, description="Время приготовления в минутах (должно быть > 0)")
    ingredients: str = Field(..., min_length=1, description="Ингредиенты")
    description: str = Field(..., min_length=1, description="Описание рецепта")

    @field_validator('cooking_time')
    @classmethod
    def validate_cooking_time(cls, v: int) -> int:
        """Validate that cooking time is positive."""
        if v <= 0:
            raise ValueError('Время приготовления должно быть больше 0')
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not empty."""
        if not v or not v.strip():
            raise ValueError('Название не может быть пустым')
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
