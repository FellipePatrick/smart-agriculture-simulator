# 🌾 Simulador de Agricultura 4.0 com RabbitMQ

Este projeto simula um ambiente de Agricultura 4.0 utilizando comunicação indireta via **RabbitMQ**, onde sensores e atuadores são representados por dispositivos virtuais (scripts ou aplicações que enviam e recebem mensagens).

## 🐇 Tecnologias Utilizadas

- **RabbitMQ** (com painel de administração)
- Docker + Docker Compose
- Scripts simulando sensores e atuadores (Python)

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

- Usuario e Senha: Admin
  
---

## 🐍 Interface em Flask, sensores e atuadores

### 1. Instalando dependências

```bash
pip install -r requirements.txt
```

### 2. Rodando os sensores
```bash
python sensor.py
```

### 3. Rodando o atuador
```bash
python atuador.py
```

### 4. Rodando o servidor da interface dentro da pasta
```bash
python /interface_monitoramento/app.py
```
---
