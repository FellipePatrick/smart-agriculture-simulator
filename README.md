# 🌾 Simulador de Agricultura 4.0 com RabbitMQ

Este projeto simula um ambiente de Agricultura 4.0 utilizando comunicação indireta via **RabbitMQ**, onde sensores e atuadores são representados por dispositivos virtuais (scripts ou aplicações que enviam e recebem mensagens).

## 🐇 Tecnologias Utilizadas

- **RabbitMQ** (com painel de administração)
- Docker + Docker Compose
- Scripts simulando sensores e atuadores (Python)

---
## 🐍 Rodando comando para instalar as dependências do Python e Flask

```bash
pip install -r requirements.txt
```
---
## 🚀 Como rodar o RabbitMQ com Docker Compose

### 1. Clone o repositório

```bash
git clone https://github.com/FellipePatrick/smart-agriculture-simulator
cd smart-agriculture-simulator
```

### 2. Suba o container

```bash
docker-compose up -d
```
---

## 🌐 Acessar o RabbitMQ

- Interface de administração: http://localhost:15672

- Porta de comunicação (AMQP): 5672

---
