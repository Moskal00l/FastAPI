from sqlalchemy import Column, Integer, String, Text
from database import Base


class RecipeDB(Base):

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    views = Column(Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        if 'views' not in kwargs:
            kwargs['views'] = 0
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<RecipeDB(id={self.id}, name='{self.name}', views={self.views})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "cooking_time": self.cooking_time,
            "ingredients": self.ingredients,
            "description": self.description,
            "views": self.views,
        }
