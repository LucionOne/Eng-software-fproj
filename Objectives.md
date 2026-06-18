# Development Objectives

## Completed ✓
- [x] DatabaseManager class (initialization, DB file connection, query methods, tested)

## In Progress 🚀
- [X] DataPuller class
  - [x] Initialization
  - [x] Threading infrastructure
  - [X] URL configuration & mock API integration
  - [X] Database write operations
  - [X] End-to-end execution

## Blocked ⏸️
- [ ] Dashboard implementation (awaiting DataPuller completion)
- [ ] Integration tests (awaiting manager stability)

## Planned 📋
- [ ] Performance optimization & error handling
- [ ] Deployment & monitoring setup



# 13. Guilherme P. Santos
- **Grupo 4** (Eng-software-fproj) · Cenário C1 · Integridade de dados · Esforço ~4-5h
## Validar leituras de sensor na ingestão
Guilherme, na operação real da Horta começaram a aparecer “leituras impossíveis”: o canteiro reportou pH 47 e
temperatura do ar de -300, e isso já contaminou a média do dashboard (/data em src/classes/APIService.py).
Olhando o teu DataPuller.translate_from_api (src/classes/dataPuller.py), ele faz float(sensor["value"])
direto e confia cegamente no recorded_at da API, mesmo o docstring exigindo ISO 8601. O save_to_db ainda
engole a exceção e segue, então a linha corrompida desce até a tabela sensor_logs (schema sem nenhuma
restrição em src/assets/SQL_config.py). O cliente quer uma fronteira de entrada que rejeite leituras fora
de faixa física plausível (por exemplo, umidade de 0 a 100, pH de 0 a 14) e datetime mal-formado, registre o
descarte em log, e nunca deixe o valor inválido entrar no agregado. Entrega: a validação na ingestão mais prova
executável dos dois lados, uma leitura válida que persiste e uma inválida que é rejeitada e logada sem corromper
a média.

**Ponto de partida** : src/classes/dataPuller.py, em translate_from_api e save_to_db; agregado consumidor em src/classes/APIService.py (/data); schema em src/assets/SQL_config.py.
## O que entregar:
- Evidência: teste pytest com 2 casos. Um payload válido persiste; um payload com value fora de faixa
e/ou datetime não-ISO é rejeitado, log emitido, e SELECT AVG(temperature) permanece intacto. (Não
há suíte hoje, então criar tests/test_translate_from_api.py é parte do escopo.)
- Rastreabilidade: validação na fronteira mais log de descarte (logger existente); opcional reforçar com
CHECK no wireframe de SQL_config.py.