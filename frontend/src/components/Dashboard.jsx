import React, { useState, useEffect } from 'react';
import '../App.css';

const Dashboard = ({ user, onLogout }) => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('vitals');

  // Dados simulados para demonstração
  const mockPatients = [
    {
      id: 1,
      name: "João Silva",
      age: 65,
      gender: "M",
      surgery_type: "Cirurgia Cardíaca",
      surgery_date: "2024-06-20T10:00:00",
      vital_signs: [
        { timestamp: "2024-06-20T12:00:00", blood_pressure_systolic: 130, heart_rate: 75, temperature: 36.5, oxygen_saturation: 98 },
        { timestamp: "2024-06-20T14:00:00", blood_pressure_systolic: 135, heart_rate: 80, temperature: 37.0, oxygen_saturation: 97 },
        { timestamp: "2024-06-20T16:00:00", blood_pressure_systolic: 140, heart_rate: 85, temperature: 37.5, oxygen_saturation: 96 }
      ],
      lab_results: [
        { timestamp: "2024-06-20T12:00:00", glucose: 120, hemoglobin: 12.5, white_blood_cells: 8000 }
      ]
    },
    {
      id: 2,
      name: "Maria Santos",
      age: 45,
      gender: "F",
      surgery_type: "Cirurgia Abdominal",
      surgery_date: "2024-06-21T08:00:00",
      vital_signs: [
        { timestamp: "2024-06-21T10:00:00", blood_pressure_systolic: 120, heart_rate: 70, temperature: 36.8, oxygen_saturation: 99 },
        { timestamp: "2024-06-21T12:00:00", blood_pressure_systolic: 125, heart_rate: 72, temperature: 37.2, oxygen_saturation: 98 }
      ],
      lab_results: [
        { timestamp: "2024-06-21T10:00:00", glucose: 95, hemoglobin: 11.8, white_blood_cells: 7500 }
      ]
    }
  ];

  useEffect(() => {
    setPatients(mockPatients);
    if (mockPatients.length > 0) {
      setSelectedPatient(mockPatients[0]);
    }
  }, []);

  const generateMockInsights = (patient) => {
    const riskLevel = patient.vital_signs[patient.vital_signs.length - 1]?.temperature > 37.3 ? 'high' : 'low';
    return {
      patient_id: patient.id,
      patient_name: patient.name,
      insights: riskLevel === 'high' 
        ? "ALERTA: Alta probabilidade de complicação detectada. Temperatura elevada e tendência de aumento da pressão arterial."
        : "Baixa probabilidade de complicação. Sinais vitais estáveis.",
      prediction: {
        complication_predicted: riskLevel === 'high',
        probabilities: riskLevel === 'high' ? [0.25, 0.75] : [0.80, 0.20]
      },
      latest_vital_signs: patient.vital_signs[patient.vital_signs.length - 1],
      latest_lab_results: patient.lab_results[patient.lab_results.length - 1]
    };
  };

  const handlePatientSelect = (patient) => {
    setSelectedPatient(patient);
    setLoading(true);
    
    // Simular chamada à API
    setTimeout(() => {
      const mockInsights = generateMockInsights(patient);
      setInsights(mockInsights);
      setLoading(false);
    }, 1000);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getRiskBadge = (prediction) => {
    if (!prediction) return <span className="badge">Analisando...</span>;
    
    return prediction.complication_predicted ? 
      <span className="badge badge-danger">Alto Risco</span> :
      <span className="badge badge-success">Baixo Risco</span>;
  };

  return (
    <div className="holdmed-container">
      {/* Header */}
      <div className="dashboard-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <img 
            src="/holdmed-logo.jpg" 
            alt="HoldMed Logo" 
            className="logo"
          />
          <div>
            <h1>HoldMed Dashboard</h1>
            <p style={{ margin: 0, color: '#666' }}>Monitoramento Inteligente Pós-Operatório</p>
          </div>
        </div>
        <div className="user-info">
          <span>Bem-vindo, {user.name}</span>
          <button className="logout-btn" onClick={onLogout}>
            Sair
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px' }}>
        {/* Lista de Pacientes */}
        <div>
          <div className="patient-card">
            <h3>Pacientes ({patients.length})</h3>
            <p style={{ color: '#666', fontSize: '14px' }}>
              {patients.length} pacientes em monitoramento
            </p>
          </div>
          
          {patients.map((patient) => (
            <div
              key={patient.id}
              className={`patient-card ${selectedPatient?.id === patient.id ? 'selected' : ''}`}
              onClick={() => handlePatientSelect(patient)}
              style={{ 
                cursor: 'pointer',
                backgroundColor: selectedPatient?.id === patient.id ? '#e3f2fd' : 'white',
                borderColor: selectedPatient?.id === patient.id ? '#2196f3' : '#e0e0e0'
              }}
            >
              <div style={{ fontWeight: 'bold' }}>{patient.name}</div>
              <div style={{ fontSize: '14px', color: '#666' }}>
                {patient.age} anos, {patient.gender}
              </div>
              <div style={{ fontSize: '12px', color: '#999' }}>
                {patient.surgery_type}
              </div>
              {selectedPatient?.id === patient.id && insights && (
                <div style={{ marginTop: '8px' }}>
                  {getRiskBadge(insights.prediction)}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Dashboard Principal */}
        <div>
          {selectedPatient ? (
            <div>
              {/* Informações do Paciente */}
              <div className="patient-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div>
                    <h2>{selectedPatient.name}</h2>
                    <div style={{ display: 'flex', gap: '20px', marginTop: '8px', fontSize: '14px', color: '#666' }}>
                      <span>👤 {selectedPatient.age} anos, {selectedPatient.gender === 'M' ? 'Masculino' : 'Feminino'}</span>
                      <span>📅 {selectedPatient.surgery_type}</span>
                      <span>🕒 {formatDate(selectedPatient.surgery_date)}</span>
                    </div>
                  </div>
                  {insights && getRiskBadge(insights.prediction)}
                </div>
              </div>

              {/* Insights de IA */}
              {loading ? (
                <div className="patient-card">
                  <div className="loading">
                    <div>🔄 Analisando dados com IA...</div>
                  </div>
                </div>
              ) : insights && (
                <div className={insights.prediction.complication_predicted ? "alert-high" : "alert-normal"}>
                  <strong>⚡ Análise de IA:</strong> {insights.insights}
                  <div style={{ marginTop: '8px', fontSize: '14px' }}>
                    Probabilidade de complicação: {Math.round(insights.prediction.probabilities[1] * 100)}%
                  </div>
                </div>
              )}

              {/* Tabs com Dados */}
              <div className="tabs">
                <div className="tab-list">
                  <button 
                    className={`tab-button ${activeTab === 'vitals' ? 'active' : ''}`}
                    onClick={() => setActiveTab('vitals')}
                  >
                    Sinais Vitais
                  </button>
                  <button 
                    className={`tab-button ${activeTab === 'labs' ? 'active' : ''}`}
                    onClick={() => setActiveTab('labs')}
                  >
                    Exames Laboratoriais
                  </button>
                  <button 
                    className={`tab-button ${activeTab === 'trends' ? 'active' : ''}`}
                    onClick={() => setActiveTab('trends')}
                  >
                    Tendências
                  </button>
                </div>

                <div className="tab-content">
                  {activeTab === 'vitals' && (
                    <div>
                      <div className="vital-signs-grid">
                        {selectedPatient.vital_signs.length > 0 && (
                          <>
                            <div className="vital-sign-item">
                              <div className="vital-sign-value">
                                {selectedPatient.vital_signs[selectedPatient.vital_signs.length - 1]?.blood_pressure_systolic || 'N/A'}
                              </div>
                              <div className="vital-sign-label">📊 Pressão Arterial (mmHg)</div>
                            </div>

                            <div className="vital-sign-item">
                              <div className="vital-sign-value">
                                {selectedPatient.vital_signs[selectedPatient.vital_signs.length - 1]?.heart_rate || 'N/A'}
                              </div>
                              <div className="vital-sign-label">❤️ Frequência Cardíaca (bpm)</div>
                            </div>

                            <div className="vital-sign-item">
                              <div className="vital-sign-value">
                                {selectedPatient.vital_signs[selectedPatient.vital_signs.length - 1]?.temperature || 'N/A'}°C
                              </div>
                              <div className="vital-sign-label">🌡️ Temperatura</div>
                            </div>

                            <div className="vital-sign-item">
                              <div className="vital-sign-value">
                                {selectedPatient.vital_signs[selectedPatient.vital_signs.length - 1]?.oxygen_saturation || 'N/A'}%
                              </div>
                              <div className="vital-sign-label">💧 Saturação O₂</div>
                            </div>
                          </>
                        )}
                      </div>

                      {/* Histórico de Sinais Vitais */}
                      <div className="patient-card">
                        <h3>Histórico de Sinais Vitais</h3>
                        <div style={{ overflowX: 'auto' }}>
                          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                            <thead>
                              <tr style={{ backgroundColor: '#f5f5f5' }}>
                                <th style={{ padding: '8px', textAlign: 'left', border: '1px solid #ddd' }}>Horário</th>
                                <th style={{ padding: '8px', textAlign: 'left', border: '1px solid #ddd' }}>PA Sistólica</th>
                                <th style={{ padding: '8px', textAlign: 'left', border: '1px solid #ddd' }}>FC</th>
                                <th style={{ padding: '8px', textAlign: 'left', border: '1px solid #ddd' }}>Temperatura</th>
                                <th style={{ padding: '8px', textAlign: 'left', border: '1px solid #ddd' }}>SpO₂</th>
                              </tr>
                            </thead>
                            <tbody>
                              {selectedPatient.vital_signs.map((vs, index) => (
                                <tr key={index}>
                                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                                    {formatDate(vs.timestamp)}
                                  </td>
                                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                                    {vs.blood_pressure_systolic} mmHg
                                  </td>
                                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                                    {vs.heart_rate} bpm
                                  </td>
                                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                                    {vs.temperature}°C
                                  </td>
                                  <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                                    {vs.oxygen_saturation}%
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'labs' && (
                    <div>
                      <div className="vital-signs-grid">
                        {selectedPatient.lab_results.length > 0 && (
                          <>
                            <div className="vital-sign-item">
                              <div className="vital-sign-value">
                                {selectedPatient.lab_results[selectedPatient.lab_results.length - 1]?.glucose || 'N/A'}
                              </div>
                              <div className="vital-sign-label">🍯 Glicose (mg/dL)</div>
                            </div>

                            <div className="vital-sign-item">
                              <div className="vital-sign-value">
                                {selectedPatient.lab_results[selectedPatient.lab_results.length - 1]?.hemoglobin || 'N/A'}
                              </div>
                              <div className="vital-sign-label">🩸 Hemoglobina (g/dL)</div>
                            </div>

                            <div className="vital-sign-item">
                              <div className="vital-sign-value">
                                {selectedPatient.lab_results[selectedPatient.lab_results.length - 1]?.white_blood_cells || 'N/A'}
                              </div>
                              <div className="vital-sign-label">🦠 Leucócitos (/μL)</div>
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                  )}

                  {activeTab === 'trends' && (
                    <div className="patient-card">
                      <h3>Análise de Tendências</h3>
                      <p>Gráficos de tendências serão implementados aqui com bibliotecas de gráficos.</p>
                      <div style={{ padding: '40px', textAlign: 'center', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
                        📈 Gráficos de evolução dos sinais vitais ao longo do tempo
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="patient-card">
              <div className="loading">
                Selecione um paciente para visualizar os dados
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

