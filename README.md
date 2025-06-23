# HoldMed - Plataforma de IA para Monitoramento Pós-Operatório

## Descrição

HoldMed é uma plataforma inteligente que utiliza inteligência artificial para monitoramento de pacientes em período trans e pós-operatório. O sistema analisa sinais vitais, resultados laboratoriais e notas clínicas para prever possíveis complicações e auxiliar na tomada de decisões médicas.

## Funcionalidades

- **Monitoramento em Tempo Real**: Acompanhamento contínuo de sinais vitais dos pacientes
- **Análise de IA**: Predição de complicações usando algoritmos de machine learning
- **Dashboard Interativo**: Interface intuitiva para visualização de dados clínicos
- **Gestão de Pacientes**: Cadastro e acompanhamento de pacientes pós-cirúrgicos
- **Relatórios Médicos**: Geração de insights baseados em dados clínicos

## Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **SQLAlchemy**: ORM para banco de dados
- **scikit-learn**: Biblioteca de machine learning
- **spaCy**: Processamento de linguagem natural
- **pandas**: Manipulação de dados
- **Flask-CORS**: Suporte a CORS

### Frontend
- **React**: Biblioteca JavaScript para interfaces
- **Vite**: Build tool e servidor de desenvolvimento
- **CSS3**: Estilização responsiva

## Estrutura do Projeto

```
preinc-holdmedfinal/
├── backend/
│   ├── src/
│   │   ├── main.py
│   │   ├── ai_agent.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── patient.py
│   │   └── routes/
│   │       ├── user.py
│   │       ├── patient.py
│   │       └── ai.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── holdmed-logo.jpg
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
└── README.md
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Node.js 16+
- npm ou yarn

### Configuração do Backend

1. Navegue até o diretório do backend:
```bash
cd preinc-holdmedfinal/backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Baixe o modelo do spaCy para português:
```bash
python -m spacy download pt_core_news_sm
```

6. Execute o servidor:
```bash
cd src
python main.py
```

O backend estará disponível em `http://localhost:5000`

### Configuração do Frontend

1. Navegue até o diretório do frontend:
```bash
cd preinc-holdmedfinal/frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Execute o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## Uso da Aplicação

### Funcionalidades Principais

1. **Dashboard de Pacientes**: Visualize a lista de pacientes em monitoramento
2. **Sinais Vitais**: Acompanhe pressão arterial, frequência cardíaca, temperatura e saturação de oxigênio
3. **Exames Laboratoriais**: Monitore resultados de glicose, hemoglobina e leucócitos
4. **Análise de IA**: Receba alertas sobre possíveis complicações baseados em IA
5. **Tendências**: Visualize a evolução dos dados ao longo do tempo

## API Endpoints

### Usuários
- `GET /api/users` - Listar usuários
- `POST /api/users` - Criar usuário
- `GET /api/users/{id}` - Obter usuário específico
- `PUT /api/users/{id}` - Atualizar usuário
- `DELETE /api/users/{id}` - Deletar usuário

### Pacientes
- `GET /api/patients` - Listar pacientes
- `POST /api/patients` - Criar paciente
- `GET /api/patients/{id}` - Obter paciente específico
- `POST /api/patients/{id}/vital-signs` - Adicionar sinais vitais
- `POST /api/patients/{id}/lab-results` - Adicionar resultados laboratoriais
- `POST /api/patients/{id}/clinical-notes` - Adicionar notas clínicas
- `GET /api/patients/{id}/predict-complications` - Predizer complicações
- `GET /api/patients/{id}/dashboard-insights` - Obter insights para dashboard

### IA
- `POST /api/ai-analysis` - Análise de dados do paciente
- `POST /api/ai-prediction` - Predição de complicações

## Desenvolvimento

### Comandos Úteis

**Backend:**
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor de desenvolvimento
python src/main.py

# Executar testes (quando implementados)
python -m pytest
```

**Frontend:**
```bash
# Instalar dependências
npm install

# Executar servidor de desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

- **Projeto**: HoldMed
- **Versão**: 1.0.0
- **Descrição**: Plataforma de IA para Monitoramento Pós-Operatório

## Notas Técnicas

### Algoritmo de IA

O sistema utiliza Random Forest Classifier para predição de complicações baseado em:
- Sinais vitais (pressão arterial, frequência cardíaca, temperatura, saturação de oxigênio)
- Resultados laboratoriais (glicose, hemoglobina, leucócitos)
- Dados demográficos (idade, gênero)

### Processamento de Linguagem Natural

Utiliza spaCy para processamento de notas clínicas em português, extraindo:
- Entidades médicas
- Palavras-chave relevantes
- Termos médicos específicos

### Segurança

- CORS configurado para permitir requisições do frontend
- Validação de dados de entrada
- Tratamento de erros robusto

## Troubleshooting

### Problemas Comuns

1. **Erro ao instalar spaCy**: Execute `pip install spacy` e depois `python -m spacy download pt_core_news_sm`
2. **Porta já em uso**: Altere a porta no arquivo `main.py` (backend) ou use `npm run dev -- --port 3000` (frontend)
3. **Problemas de CORS**: Verifique se o CORS está configurado corretamente no backend

### Logs

Os logs do sistema são exibidos no console. Para debugging, verifique:
- Console do navegador para erros de frontend
- Terminal do servidor Python para erros de backend
- Network tab do DevTools para problemas de API

