from roboys_dash import db

import json
from datetime import datetime

# Admin Member
class AdminMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "nama": self.name,
            "username": self.username,
        }

    def __repr__(self):
        return f'<AdminMember {self.username}>'

# RoBoys Member
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    nis = db.Column(db.String(7), nullable=False, unique=True)
    kelas = db.Column(db.String(15), nullable=False)
    cardUid = db.Column(db.String(12), nullable=True, unique=True)
    absen = db.relationship("Absen", backref="member", cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/7103486"""
        return {
            "id": self.id,
            "nama": self.name,
            "nis": self.nis,
            "kelas": self.kelas,
            "card_uid": self.cardUid,
        }

    def __repr__(self):
        return f'<Member {self.nis}>'

# Absen
class Absen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.String(7), db.ForeignKey("member.nis"), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       """https://stackoverflow.com/a/7103486"""
       return {
           "id": self.id,
           "nis": self.nis,
           "tanggal": datetime.strftime(self.tanggal, "%Y-%m-%d"),
           **self.member.serialize
       }

    def __repr__(self):
        return f'<Absen {self.nis}>'
