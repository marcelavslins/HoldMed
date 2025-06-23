
import spacy
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

# Carregar modelo de linguagem do spaCy para português
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    print("Baixando modelo pt_core_news_sm do spaCy...")
    spacy.cli.download("pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")

class AIAgent:
    def __init__(self):
        self.model = None
        self.features = []

    def train_model(self, data: pd.DataFrame, target_column: str):
        """
        Treina um modelo de classificação para prever complicações.
        data: DataFrame com dados clínicos e laboratoriais.
        target_column: Nome da coluna que indica a complicação (0 para não, 1 para sim).
        """
        # Exemplo simplificado de seleção de features e treinamento
        # Em um cenário real, a seleção de features seria mais complexa e baseada em dados reais.
        self.features = [col for col in data.columns if col != target_column]
        
        if not self.features:
            raise ValueError("Nenhuma feature encontrada para treinamento. Verifique as colunas do DataFrame.")

        X = data[self.features]
        y = data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Modelo treinado com acurácia: {accuracy:.2f}")

    def predict_complication(self, patient_data: dict) -> dict:
        """
        Prevê a probabilidade de complicação para um dado paciente.
        patient_data: Dicionário com os dados do paciente.
        """
        if self.model is None:
            raise ValueError("Modelo de IA não treinado. Por favor, treine o modelo primeiro.")

        # Converter dados do paciente para DataFrame no formato esperado pelo modelo
        patient_df = pd.DataFrame([patient_data])
        
        # Garantir que todas as features usadas no treinamento estão presentes, preenchendo com NaN se necessário
        for feature in self.features:
            if feature not in patient_df.columns:
                patient_df[feature] = np.nan
        
        # Reordenar colunas para corresponder à ordem de treinamento
        patient_df = patient_df[self.features]

        prediction = self.model.predict(patient_df)[0]
        probability = self.model.predict_proba(patient_df)[0].tolist()

        return {"complication_predicted": bool(prediction), "probabilities": probability}

    def process_clinical_notes(self, notes: str) -> dict:
        """
        Processa notas clínicas usando NLP para extrair informações relevantes.
        notes: Texto das notas clínicas.
        """
        doc = nlp(notes)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]

        # Exemplo de extração de termos médicos ou condições
        medical_terms = [token.text for token in doc if token.ent_type_ == "DISEASE" or token.ent_type_ == "SYMPTOM"]

        return {
            "original_notes": notes,
            "extracted_entities": entities,
            "keywords": list(set(keywords)),
            "medical_terms": list(set(medical_terms))
        }

    def generate_dashboard_insights(self, prediction_result: dict, processed_notes: dict) -> str:
        """
        Gera insights para dashboards com base nas previsões e notas processadas.
        """
        insight = ""
        if prediction_result["complication_predicted"]:
            insight += "ALERTA: Alta probabilidade de complicação detectada. "
        else:
            insight += "Baixa probabilidade de complicação. "

        insight += f"Probabilidades: {prediction_result['probabilities']}. "

        if processed_notes["medical_terms"]:
            insight += f"Termos médicos relevantes nas notas: {', '.join(processed_notes['medical_terms'])}. "
        
        if processed_notes["keywords"]:
            insight += f"Palavras-chave das notas: {', '.join(processed_notes['keywords'])}. "

        return insight

# Exemplo de uso (para demonstração e teste)
if __name__ == "__main__":
    agent = AIAgent()

    # Dados de exemplo para treinamento (em um cenário real, seriam dados de pacientes)
    # 'sinais_vitais', 'exames_laboratoriais' seriam colunas numéricas representativas
    # 'complicação' é a coluna alvo (0 = não, 1 = sim)
    data = pd.DataFrame({
        'sinais_vitais_pressao': np.random.rand(100) * 50 + 80,
        'sinais_vitais_temperatura': np.random.rand(100) * 3 + 36,
        'exames_laboratoriais_glicose': np.random.rand(100) * 50 + 80,
        'idade': np.random.randint(20, 80, 100),
        'complicação': np.random.randint(0, 2, 100) # 0 ou 1
    })

    agent.train_model(data, 'complicação')

    # Dados de um novo paciente para predição
    new_patient_data = {
        'sinais_vitais_pressao': 130,
        'sinais_vitais_temperatura': 38.5,
        'exames_laboratoriais_glicose': 150,
        'idade': 65
    }

    prediction = agent.predict_complication(new_patient_data)
    print(f"Predição para o novo paciente: {prediction}")

    # Exemplo de notas clínicas
    clinical_notes = "Paciente apresentou febre alta e dor abdominal intensa após a cirurgia. Exames indicam possível infecção." 
    processed_notes = agent.process_clinical_notes(clinical_notes)
    print(f"Notas clínicas processadas: {processed_notes}")

    # Gerar insights para dashboard
    insights = agent.generate_dashboard_insights(prediction, processed_notes)
    print(f"Insights para Dashboard: {insights}")


