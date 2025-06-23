from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    surgery_type = db.Column(db.String(100))
    surgery_date = db.Column(db.DateTime)
    
    vital_signs = db.relationship('VitalSigns', backref='patient', lazy=True)
    lab_results = db.relationship('LabResults', backref='patient', lazy=True)
    clinical_notes = db.relationship('ClinicalNotes', backref='patient', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'surgery_type': self.surgery_type,
            'surgery_date': self.surgery_date.isoformat() if self.surgery_date else None
        }

class VitalSigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    blood_pressure_systolic = db.Column(db.Float)
    blood_pressure_diastolic = db.Column(db.Float)
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    oxygen_saturation = db.Column(db.Float)
    respiratory_rate = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'timestamp': self.timestamp.isoformat(),
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'heart_rate': self.heart_rate,
            'temperature': self.temperature,
            'oxygen_saturation': self.oxygen_saturation,
            'respiratory_rate': self.respiratory_rate
        }

class LabResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    glucose = db.Column(db.Float)
    hemoglobin = db.Column(db.Float)
    white_blood_cells = db.Column(db.Float)
    creatinine = db.Column(db.Float)
    sodium = db.Column(db.Float)
    potassium = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'timestamp': self.timestamp.isoformat(),
            'glucose': self.glucose,
            'hemoglobin': self.hemoglobin,
            'white_blood_cells': self.white_blood_cells,
            'creatinine': self.creatinine,
            'sodium': self.sodium,
            'potassium': self.potassium
        }

class ClinicalNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    note_type = db.Column(db.String(50))
    content = db.Column(db.Text)
    author = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'timestamp': self.timestamp.isoformat(),
            'note_type': self.note_type,
            'content': self.content,
            'author': self.author
        }

