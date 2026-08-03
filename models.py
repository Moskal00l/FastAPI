from sqlalchemy import Column, Integer, String, Text
from database import Base


class RecipeDB(Base):
    """Recipe database model."""

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    views = Column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        """String representation of the recipe."""
        return f"<RecipeDB(id={self.id}, name='{self.name}', views={self.views})>"

    def to_dict(self) -> dict:
        """Convert recipe to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "cooking_time": self.cooking_time,
            "ingredients": self.ingredients,
            "description": self.description,
            "views": self.views,
        }
