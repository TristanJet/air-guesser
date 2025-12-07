from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Airport(db.Model):
    __tablename__ = 'airport'

    id = db.Column(db.Integer, nullable=False)
    ident = db.Column(db.String(40), primary_key=True, nullable=False)
    type = db.Column(db.String(40))
    name = db.Column(db.String(40))
    latitude_deg = db.Column(db.Float)  # double -> Float
    longitude_deg = db.Column(db.Float)  # double -> Float
    elevation_ft = db.Column(db.Integer)
    municipality = db.Column(db.String(40))
    iso_country = db.Column(db.String(40), db.ForeignKey('country.iso_country'))

    # Relationship Airport - Country
    country = db.relationship('Country', back_populates='airports')

    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'ident': self.ident,
            'type': self.type,
            'name': self.name,
            'latitude': self.latitude_deg,
            'longitude': self.longitude_deg,
            'elevation_ft': self.elevation_ft,
            'continent': self.continent,
            'iso_country': self.iso_country
        }

    def to_geojson_feature(self):
        """Convert to GeoJSON feature for mapping"""
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [self.longitude_deg, self.latitude_deg]
            },
            'properties': {
                'id': self.id,
                'ident': self.ident,
                'name': self.name,
                'type': self.type,
            }
        }

    def __repr__(self):
        return f'<Airport {self.name} ({self.ident})>'

class Country(db.Model):
    __tablename__ = 'country'

    iso_country = db.Column(db.String(40), primary_key=True, nullable=False)
    name = db.Column(db.String(40))
    continent = db.Column(db.String(40))

    # Relationship Country - Airport
    airports = db.relationship('Airport', back_populates='country')
