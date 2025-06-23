from flask import Blueprint, jsonify, request
from models.patient import Patient, VitalSigns, LabResults, ClinicalNotes, db
from datetime import datetime
from ai_agent import AIAgent

patient_bp = Blueprint('patient', __name__)
ai_agent = AIAgent()

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients])

@patient_bp.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    
    # Converter string de data para datetime
    surgery_date = datetime.fromisoformat(data['surgery_date']) if data.get('surgery_date') else None
    
    patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        surgery_type=data['surgery_type'],
        surgery_date=surgery_date
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201

@patient_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient_data = patient.to_dict()
    
    # Incluir dados relacionados
    patient_data['vital_signs'] = [vs.to_dict() for vs in patient.vital_signs]
    patient_data['lab_results'] = [lr.to_dict() for lr in patient.lab_results]
    patient_data['clinical_notes'] = [cn.to_dict() for cn in patient.clinical_notes]
    
    return jsonify(patient_data)

@patient_bp.route('/patients/<int:patient_id>/vital-signs', methods=['POST'])
def add_vital_signs(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    
    vital_signs = VitalSigns(
        patient_id=patient_id,
        blood_pressure_systolic=data.get('blood_pressure_systolic'),
        blood_pressure_diastolic=data.get('blood_pressure_diastolic'),
        heart_rate=data.get('heart_rate'),
        temperature=data.get('temperature'),
        oxygen_saturation=data.get('oxygen_saturation'),
        respiratory_rate=data.get('respiratory_rate')
    )
    db.session.add(vital_signs)
    db.session.commit()
    return jsonify(vital_signs.to_dict()), 201

@patient_bp.route('/patients/<int:patient_id>/lab-results', methods=['POST'])
def add_lab_results(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    
    lab_results = LabResults(
        patient_id=patient_id,
        glucose=data.get('glucose'),
        hemoglobin=data.get('hemoglobin'),
        white_blood_cells=data.get('white_blood_cells'),
        creatinine=data.get('creatinine'),
        sodium=data.get('sodium'),
        potassium=data.get('potassium')
    )
    db.session.add(lab_results)
    db.session.commit()
    return jsonify(lab_results.to_dict()), 201

@patient_bp.route('/patients/<int:patient_id>/clinical-notes', methods=['POST'])
def add_clinical_notes(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    
    clinical_notes = ClinicalNotes(
        patient_id=patient_id,
        note_type=data['note_type'],
        content=data['content'],
        author=data['author']
    )
    db.session.add(clinical_notes)
    db.session.commit()
    return jsonify(clinical_notes.to_dict()), 201

@patient_bp.route('/patients/<int:patient_id>/predict-complications', methods=['GET'])
def predict_complications(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Obter os dados mais recentes do paciente
    latest_vital_signs = VitalSigns.query.filter_by(patient_id=patient_id).order_by(VitalSigns.timestamp.desc()).first()
    latest_lab_results = LabResults.query.filter_by(patient_id=patient_id).order_by(LabResults.timestamp.desc()).first()
    
    if not latest_vital_signs or not latest_lab_results:
        return jsonify({'error': 'Dados insuficientes para predição'}), 400
    
    # Preparar dados para o agente de IA
    patient_data = {
        'sinais_vitais_pressao': latest_vital_signs.blood_pressure_systolic or 0,
        'sinais_vitais_temperatura': latest_vital_signs.temperature or 0,
        'exames_laboratoriais_glicose': latest_lab_results.glucose or 0,
        'idade': patient.age
    }
    
    try:
        # Usar dados simulados para treinar o modelo (em produção, usaria dados históricos reais)
        import pandas as pd
        import numpy as np
        
        # Dados simulados para treinamento
        training_data = pd.DataFrame({
            'sinais_vitais_pressao': np.random.rand(100) * 50 + 80,
            'sinais_vitais_temperatura': np.random.rand(100) * 3 + 36,
            'exames_laboratoriais_glicose': np.random.rand(100) * 50 + 80,
            'idade': np.random.randint(20, 80, 100),
            'complicação': np.random.randint(0, 2, 100)
        })
        
        ai_agent.train_model(training_data, 'complicação')
        prediction = ai_agent.predict_complication(patient_data)
        
        return jsonify({
            'patient_id': patient_id,
            'prediction': prediction,
            'patient_data_used': patient_data
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro na predição: {str(e)}'}), 500

@patient_bp.route('/patients/<int:patient_id>/process-notes', methods=['POST'])
def process_clinical_notes(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.json
    
    if 'notes' not in data:
        return jsonify({'error': 'Campo "notes" é obrigatório'}), 400
    
    try:
        processed_notes = ai_agent.process_clinical_notes(data['notes'])
        return jsonify({
            'patient_id': patient_id,
            'processed_notes': processed_notes
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro no processamento das notas: {str(e)}'}), 500

@patient_bp.route('/patients/<int:patient_id>/dashboard-insights', methods=['GET'])
def get_dashboard_insights(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    # Obter predição de complicações
    latest_vital_signs = VitalSigns.query.filter_by(patient_id=patient_id).order_by(VitalSigns.timestamp.desc()).first()
    latest_lab_results = LabResults.query.filter_by(patient_id=patient_id).order_by(LabResults.timestamp.desc()).first()
    latest_notes = ClinicalNotes.query.filter_by(patient_id=patient_id).order_by(ClinicalNotes.timestamp.desc()).first()
    
    if not latest_vital_signs or not latest_lab_results:
        return jsonify({'error': 'Dados insuficientes para gerar insights'}), 400
    
    try:
        # Preparar dados para predição
        patient_data = {
            'sinais_vitais_pressao': latest_vital_signs.blood_pressure_systolic or 0,
            'sinais_vitais_temperatura': latest_vital_signs.temperature or 0,
            'exames_laboratoriais_glicose': latest_lab_results.glucose or 0,
            'idade': patient.age
        }
        
        # Treinar modelo com dados simulados
        import pandas as pd
        import numpy as np
        
        training_data = pd.DataFrame({
            'sinais_vitais_pressao': np.random.rand(100) * 50 + 80,
            'sinais_vitais_temperatura': np.random.rand(100) * 3 + 36,
            'exames_laboratoriais_glicose': np.random.rand(100) * 50 + 80,
            'idade': np.random.randint(20, 80, 100),
            'complicação': np.random.randint(0, 2, 100)
        })
        
        ai_agent.train_model(training_data, 'complicação')
        prediction = ai_agent.predict_complication(patient_data)
        
        # Processar notas clínicas se disponíveis
        processed_notes = {'keywords': [], 'medical_terms': []}
        if latest_notes:
            processed_notes = ai_agent.process_clinical_notes(latest_notes.content)
        
        # Gerar insights
        insights = ai_agent.generate_dashboard_insights(prediction, processed_notes)
        
        return jsonify({
            'patient_id': patient_id,
            'patient_name': patient.name,
            'insights': insights,
            'prediction': prediction,
            'latest_vital_signs': latest_vital_signs.to_dict() if latest_vital_signs else None,
            'latest_lab_results': latest_lab_results.to_dict() if latest_lab_results else None,
            'processed_notes': processed_notes
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar insights: {str(e)}'}), 500

