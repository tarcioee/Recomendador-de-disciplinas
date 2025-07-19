https://raw.githubusercontent.com/user/repo/main/app/static/imagens/pinguim.webp" alt="Pinguim com chapéu de formatura" width="150"/>
Pinguim Recomendador de Matérias 🐧

Uma aplicação web inteligente para auxiliar estudantes da UFBA na montagem da grade horária.


https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python version">
https://img.shields.io/badge/framework-Flask-green.svg" alt="Framework">
https://img.shields.io/badge/license-MIT-lightgrey.svg" alt="License">

O Pinguim Recomendador é uma ferramenta projetada para simplificar a complexa tarefa de escolher disciplinas a cada semestre. Com base em um perfil detalhado do aluno, o sistema utiliza uma lógica personalizada para sugerir grades horárias otimizadas, equilibrando as necessidades acadêmicas com as restrições pessoais do estudante.

Índice
✨ Funcionalidades

🚀 Tecnologias Utilizadas

⚙️ Como Executar

📂 Estrutura do Projeto

✨ Funcionalidades
Recomendação Personalizada: Gera múltiplas sugestões de grades (recomendada, mais fácil e desafiadora) com base em um cálculo de "sobrecarga" que considera a rotina do aluno.

Perfil do Aluno: Leva em conta diversas variáveis do usuário, como tempo disponível para estudo, disciplinas já concluídas, turnos livres e professores a serem evitados.

Agrupamento por Perfil: Classifica o usuário em grupos (ex: "próximos da ufba", "estudiosos", "cdfs") para contextualizar as recomendações e fornecer insights.

Resolução de Conflitos: Monta as grades garantindo que não haja conflitos de horário entre as disciplinas selecionadas.

Priorização Inteligente: Prioriza disciplinas obrigatórias e aquelas que funcionam como pré-requisitos para outras matérias importantes, otimizando o avanço do aluno no curso.

Interface Web Interativa: Uma interface simples e intuitiva construída com Flask e Bootstrap para coletar os dados do aluno e apresentar as recomendações de forma clara.

🚀 Tecnologias Utilizadas
Categoria	Tecnologia
Backend	
Frontend	

Exportar para as Planilhas
⚙️ Como Executar
Para executar o projeto localmente, siga os passos abaixo.

1. Pré-requisitos
Python 3.9+

pip (gerenciador de pacotes do Python)

2. Instalação
Clone o repositório:

Bash

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
Crie e ative um ambiente virtual:

Bash

# Cria o ambiente
python -m venv venv

# Ativa o ambiente (Windows)
.\venv\Scripts\activate

# Ativa o ambiente (macOS/Linux)
source venv/bin/activate
Instale as dependências:
O projeto usa a biblioteca Flask. Crie um arquivo chamado requirements.txt na raiz do projeto com o seguinte conteúdo:

Plaintext

Flask
Em seguida, instale as dependências com o comando:

Bash

pip install -r requirements.txt
3. Execução
Inicie o servidor Flask:

Bash

python run.py
Acesse a aplicação:
Abra seu navegador e acesse a URL: http://127.0.0.1:5000

📂 Estrutura do Projeto
O projeto é organizado com uma arquitetura modular para separar responsabilidades e facilitar a manutenção.

.
├── 📂 app/                # Contém a aplicação Flask e a interface do usuário
│   ├── 📂 static/         # Arquivos estáticos (imagens)
│   └── 📂 templates/      # Arquivos HTML para renderização
├── 📂 core/               # Núcleo da lógica de recomendação
│   ├── 📂 dominio/        # Classes que modelam o problema (Disciplina, Turma)
│   ├── 📂 infraestrutura/ # Classes para acesso a dados (Ementario, Guia)
│   ├── 📂 servicos/       # Classes com a lógica de negócios (Recomendador)
│   └── 📂 utils/          # Funções auxiliares (cálculos, horários)
├── 📂 dados/              # Arquivos JSON com os dados do curso
├── 📜 app.py              # Ponto de entrada da aplicação, define as rotas
└── 📜 run.py              # Script para iniciar o servidor de desenvolvimento