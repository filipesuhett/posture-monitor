# Sistema de orientação postural para pessoas em home office

**Alunos**: Alunos: Beatriz Auer Mariano,  Filipe Suhett Nogueira Silva, Giovanna Scalfoni Sales, Jessica Nogueira Duque, Marllon Cristiani Ribeiro<br>
**Disciplina**: Inteligência Artificial<br>
**Professor**: Sergio Nery<br>
**Semestre**: 2025/1

## Objetivo geral do sistema

Criar um sistema com parâmetros personalizados para a identificação em tempo real de desvios posturais de um indivíduo trabalhando em home office, com base na posição de pontos corporais, e fornecer feedback visual e sonoro ao usuário quando a ocorre má postura.


## Tecnologias e bibliotecas utilizadas

- Esse trabalho foi desenvolvido em python
- Utiliza OpenCV para acessar a imagem da webcam em tempo real
- Utiliza a biblioteca MediaPipe para a identificação dos pontos do corpo humano

## Requisitos para a instalação

- Python 3
- Instalar as dependências descritas em "requirements.txt"

## How to: iniciar o programa

** Se você estiver rodando em linux, é provável que você precisa especificar a versão do python utilizada nos comandos (ex python3.9)

- Clone esse repositório para a sua máquina local
- Abra um terminal na raíz do projeto
- Instale todas as dependências necessárias: `python -m pip install -r requirements.txt`
> Note: talvez seja preciso criar um ambiente virtual para excutar o programa: `python -m venv venv`
- Inicie o programa: `python web_app.py`
- Abra o programa no navegador com a url indicada na saída do terminal
- Defina a configuração correta de postura clicando no botão
- Enjoy!

## Principais funcionalidades

1. Configuração dos parâmetros pessoais
2. Feedback visual da postura - postura correta
3. Feedback visual da postura - postura incorreta
4. Feedback sonoro - má postura por tempo prolongado

** Por motivos de privacidade, decidimos não colocar prints aqui.

## Limitações

- O programa só consegue identificar posturas quando tem visão de perfil (de lado) da pessoa

## Melhorias futuras

- Transformar em uma extensão para navegadores web
- Verificação postural com câmera de frente