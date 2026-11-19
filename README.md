# Análise de requisitos de vaga

Ferramenta local para quem está preparando uma candidatura. Relaciona requisitos obrigatórios e diferenciais às experiências que a própria pessoa declarou. Usa Python 3.10+ e arquivos JSON fictícios.

```sh
python analise.py vaga-exemplo.json evidencias-exemplo.json
python analise.py vaga-exemplo.json evidencias-exemplo.json --json
```

Um requisito tem evidência quando uma habilidade normalizada coincide com o termo ou um alias explícito. O relatório mostra a descrição original e marca lacunas como “a confirmar”. A ferramenta não lê PDF, não verifica declarações nem prevê resultados em ATS.
