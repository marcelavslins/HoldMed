from flask import Blueprint, request, jsonify
from ai_agent import AIAgent

ai_bp = Blueprint('ai', __name__)

# Instanciar o agente de IA
ai_agent = AIAgent()

@ai_bp.route('/ai-analysis', methods=['POST'])
def analyze_patient_data():
    """
    Endpoint para análise de dados do paciente usando IA
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        patient_id = data.get('patient_id')
        vital_signs = data.get('vital_signs', {})
        lab_results = data.get('lab_results', {})
        
        if not patient_id:
            return jsonify({'error': 'ID do paciente é obrigatório'}), 400
        
        # Realizar análise usando o agente de IA
        # Como o AIAgent não tem método analyze_patient_data, vamos usar predict_complication
        analysis_result = ai_agent.predict_complication(vital_signs)
        
        return jsonify({
            'patient_id': patient_id,
            'analysis': analysis_result,
            'timestamp': '2024-06-22T19:45:00Z'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro na análise: {str(e)}'}), 500

@ai_bp.route('/ai-prediction', methods=['POST'])
def predict_complications():
    """
    Endpoint para predição de complicações
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        patient_data = data.get('patient_data', {})
        
        # Realizar predição usando o agente de IA
        prediction_result = ai_agent.predict_complication(patient_data)
        
        return jsonify({
            'prediction': prediction_result,
            'timestamp': '2024-06-22T19:45:00Z'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro na predição: {str(e)}'}), 500

