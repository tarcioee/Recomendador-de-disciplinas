# Sistema de recomendação de disciplinas
O Pinguim Recomendador é uma ferramenta projetada para simplificar a complexa tarefa de escolher disciplinas a cada semestre. Com base em um perfil detalhado do aluno, o sistema utiliza uma lógica personalizada para sugerir grades horárias otimizadas, equilibrando as necessidades acadêmicas com as restrições pessoais do estudante. Disponivel atualmente para o curso de Sistemas de Informação da UFBA.

Índice
✨ Funcionalidades

🚀 Tecnologias Utilizadas

📂 Estrutura do Projeto

✨ Funcionalidades
Recomendação Personalizada: Gera múltiplas sugestões de grades (recomendada, mais fácil e desafiadora) com base em um cálculo de "sobrecarga" que considera a rotina do aluno.

Perfil do Aluno: Leva em conta diversas variáveis do usuário, como tempo disponível para estudo, disciplinas já concluídas, turnos livres e professores a serem evitados.

Agrupamento por Perfil: Classifica o usuário em grupos (ex: "próximos da ufba", "estudiosos", "cdfs") para contextualizar as recomendações e fornecer insights.

Resolução de Conflitos: Monta as grades garantindo que não haja conflitos de horário entre as disciplinas selecionadas.

Priorização Inteligente: Prioriza disciplinas obrigatórias e aquelas que funcionam como pré-requisitos para outras matérias importantes, otimizando o avanço do aluno no curso.

Interface Web Interativa: Uma interface simples e intuitiva construída com Flask e Bootstrap para coletar os dados do aluno e apresentar as recomendações de forma clara.

🚀 Tecnologias Utilizadas
Python
Flask
HTML5
Bootstrap 5
JavaScript

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