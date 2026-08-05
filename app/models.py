from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class RecipeDB(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cooking_time = Column(Integer)
    ingredients = Column(Text)
    description = Column(Text)
    views = Column(Integer, default=0)
