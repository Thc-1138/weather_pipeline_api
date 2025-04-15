"""
models.py - (Optional) ORM Model Definitions or Schema Constants

This module is reserved for defining ORM models if you choose to use
an ORM (e.g., SQLAlchemy) instead of executing raw SQL queries.
Currently, the project uses raw SQL in the 'sql/schema.sql' script.
"""

# Example (commented out) using SQLAlchemy:
#
# from sqlalchemy import Column, Integer, String, Float, DateTime
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class WeatherData(Base):
#     __tablename__ = 'weather_data'
#     id = Column(Integer, primary_key=True)
#     venue_id = Column(String, nullable=False)
#     timestamp = Column(DateTime, nullable=False)
#     temperature = Column(Float)
#     precipitation = Column(Float)
#     snowfall = Column(Float)
#     cloudcover = Column(Integer)
#     windspeed = Column(Float)
#     relative_humidity = Column(Float)
#     apparent_temperature = Column(Float)
#     precipitation_probability = Column(Float)
#     windgusts = Column(Float)
#     pressure_msl = Column(Float)
#     wind_direction = Column(Integer)
#     weathercode = Column(Integer)
#     rain = Column(Float)
#     surface_pressure = Column(Float)
#
# # To create the tables:
# # from sqlalchemy import create_engine
# # engine = create_engine(os.getenv("DATABASE_URL"))
# # Base.metadata.create_all(engine)
