function atualizarMensagens() {
  fetch('/messages')
    .then(res => res.json())
    .then(dados => {
      const tbody = document.querySelector('#tabela tbody');
      tbody.innerHTML = '';
      dados.forEach(msg => {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${msg.timestamp}</td><td>${msg.topic}</td><td>${msg.payload}</td>`;
        tbody.appendChild(tr);
      });
    });
}

setInterval(atualizarMensagens, 2000); // Atualiza a cada 2 segundos
