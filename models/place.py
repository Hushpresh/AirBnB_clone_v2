#!/usr/bin/python3
"""This is the place class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id',
                                        onupdate='cascasde',
                                        ondelete='cascade'),
                             primary_key=True)
                      Column('amenities_id', String(60),
                             ForeignKey('amenities.id',
                                        onupdate='cascasde',
                                        ondelete='cascade'),
                             primary_key=True))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship('Review',
                           cascade='all, delete', backref='place')
    amenities = relationship('Amenity',
                             secondary='place_amenity',
                             backref='place_amenity',
                             viewonly=False)

    @property
    def reviews(self):
        """ getter returns list or reviews """
        list_of_reviews = []
        all_reviews = models.strage.all(Review)
        for review in all_reviews.values():
            if review.place_id == self.id:
                list_of_reviews.append(review)
        return list_of_reviews
