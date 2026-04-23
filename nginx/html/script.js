/* ═══════════════════════════════════════════════════════
   AgendaPro — script.js
   Consome a API via /api (proxy NGINX → FastAPI)
   ═══════════════════════════════════════════════════════ */

const API = '/api';
let clientesCache = [];

/* ──────── UTILITÁRIOS ───────────────────────────────── */

function showToast(msg, isError = false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast show' + (isError ? ' error' : '');
  setTimeout(() => (t.className = 'toast'), 3000);
}

function openModal(id) {
  document.getElementById(id).classList.add('open');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}

// Fecha modal ao clicar no fundo
document.querySelectorAll('.modal-backdrop').forEach(el => {
  el.addEventListener('click', e => {
    if (e.target === el) el.classList.remove('open');
  });
});

// Navegação entre abas
document.querySelectorAll('.nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    if (btn.dataset.tab === 'agendamentos') carregarAgendamentos();
  });
});

function iniciais(nome) {
  return nome.trim().split(' ').map(p => p[0]).join('').toUpperCase().slice(0, 2);
}

function fmtData(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

function badgeStatus(s) {
  return `<span class="badge badge-${s}">${s}</span>`;
}

/* ──────── HEALTH CHECK (status API) ────────────────── */

async function verificarAPI() {
  const el = document.getElementById('apiStatus');
  try {
    const r = await fetch(`${API}/`);
    if (r.ok) {
      el.className = 'api-status online';
      el.innerHTML = '<span class="dot"></span> API online';
    } else throw new Error();
  } catch {
    el.className = 'api-status offline';
    el.innerHTML = '<span class="dot"></span> API offline';
  }
}

/* ═══════════════════════════════════════════════════════
   CLIENTES
   ═══════════════════════════════════════════════════════ */

async function carregarClientes() {
  const res = await fetch(`${API}/clientes/`);
  clientesCache = await res.json();
  renderClientes(clientesCache);
  popularSelectClientes();
}

function renderClientes(lista) {
  const grid = document.getElementById('listaClientes');
  if (!lista.length) {
    grid.innerHTML = '<div class="empty-state">Nenhum cliente cadastrado.</div>';
    return;
  }
  grid.innerHTML = lista.map(c => `
    <div class="cliente-card" id="card-${c.id}">
      <div class="cliente-card-top">
        <div class="cliente-avatar">${iniciais(c.nome)}</div>
        <div class="cliente-actions">
          <button class="btn-icon" title="Editar" onclick="editarCliente(${c.id})">✎</button>
          <button class="btn-icon del" title="Remover" onclick="removerCliente(${c.id})">✕</button>
        </div>
      </div>
      <div class="cliente-nome">${c.nome}</div>
      <div class="cliente-detalhe">✉ ${c.email}</div>
      <div class="cliente-detalhe">☏ ${c.telefone}</div>
    </div>
  `).join('');
}

function filtrarClientes() {
  const q = document.getElementById('searchCliente').value.toLowerCase();
  const filtrados = clientesCache.filter(c =>
    c.nome.toLowerCase().includes(q) ||
    c.email.toLowerCase().includes(q) ||
    c.telefone.includes(q)
  );
  renderClientes(filtrados);
}

function popularSelectClientes() {
  const sel = document.getElementById('agendamentoClienteId');
  const val = sel.value;
  sel.innerHTML = '<option value="">Selecione um cliente…</option>' +
    clientesCache.map(c => `<option value="${c.id}">${c.nome}</option>`).join('');
  if (val) sel.value = val;
}

// Abrir modal de novo cliente (limpa o form)
document.getElementById('formCliente').addEventListener('reset', () => {
  document.getElementById('clienteId').value = '';
  document.getElementById('modalClienteTitle').textContent = 'Novo cliente';
});

async function salvarCliente(e) {
  e.preventDefault();
  const id = document.getElementById('clienteId').value;
  const payload = {
    nome:     document.getElementById('clienteNome').value.trim(),
    email:    document.getElementById('clienteEmail').value.trim(),
    telefone: document.getElementById('clienteTelefone').value.trim(),
  };
  const url    = id ? `${API}/clientes/${id}` : `${API}/clientes/`;
  const method = id ? 'PUT' : 'POST';
  try {
    const r = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!r.ok) {
      const err = await r.json();
      showToast(err.detail || 'Erro ao salvar cliente.', true);
      return;
    }
    showToast(id ? 'Cliente atualizado!' : 'Cliente criado!');
    closeModal('modalCliente');
    document.getElementById('formCliente').reset();
    carregarClientes();
  } catch {
    showToast('Erro de comunicação com a API.', true);
  }
}

function editarCliente(id) {
  const c = clientesCache.find(x => x.id === id);
  if (!c) return;
  document.getElementById('clienteId').value       = c.id;
  document.getElementById('clienteNome').value     = c.nome;
  document.getElementById('clienteEmail').value    = c.email;
  document.getElementById('clienteTelefone').value = c.telefone;
  document.getElementById('modalClienteTitle').textContent = 'Editar cliente';
  openModal('modalCliente');
}

async function removerCliente(id) {
  if (!confirm('Remover este cliente e todos os seus agendamentos?')) return;
  const r = await fetch(`${API}/clientes/${id}`, { method: 'DELETE' });
  if (r.ok || r.status === 204) {
    showToast('Cliente removido.');
    carregarClientes();
  } else {
    showToast('Erro ao remover cliente.', true);
  }
}

/* ═══════════════════════════════════════════════════════
   AGENDAMENTOS
   ═══════════════════════════════════════════════════════ */

async function carregarAgendamentos() {
  const status = document.getElementById('filterStatus').value;
  const url = `${API}/agendamentos/` + (status ? `?status=${status}` : '');
  const res = await fetch(url);
  const lista = await res.json();
  const tbody = document.getElementById('bodyAgendamentos');

  if (!lista.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="td-empty">Nenhum agendamento encontrado.</td></tr>';
    return;
  }

  tbody.innerHTML = lista.map(ag => {
    const nomeCliente = (clientesCache.find(c => c.id === ag.cliente_id) || {}).nome || `#${ag.cliente_id}`;
    return `
      <tr>
        <td style="color:var(--text-dim);font-size:12px">#${ag.id}</td>
        <td><strong>${nomeCliente}</strong></td>
        <td>${ag.servico}</td>
        <td>${fmtData(ag.data_hora)}</td>
        <td>${badgeStatus(ag.status)}</td>
        <td>
          <div style="display:flex;gap:6px">
            <button class="btn-icon" title="Editar" onclick="editarAgendamento(${ag.id})">✎</button>
            <button class="btn-icon del" title="Remover" onclick="removerAgendamento(${ag.id})">✕</button>
          </div>
        </td>
      </tr>`;
  }).join('');
}

async function salvarAgendamento(e) {
  e.preventDefault();
  const id = document.getElementById('agendamentoId').value;
  const dataLocal = document.getElementById('agendamentoDataHora').value;
  const payload = {
    cliente_id:  parseInt(document.getElementById('agendamentoClienteId').value),
    servico:     document.getElementById('agendamentoServico').value.trim(),
    data_hora:   dataLocal ? new Date(dataLocal).toISOString() : '',
    status:      document.getElementById('agendamentoStatus').value,
    observacoes: document.getElementById('agendamentoObs').value.trim() || null,
  };
  const url    = id ? `${API}/agendamentos/${id}` : `${API}/agendamentos/`;
  const method = id ? 'PUT' : 'POST';
  try {
    const r = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!r.ok) {
      const err = await r.json();
      showToast(err.detail || 'Erro ao salvar agendamento.', true);
      return;
    }
    showToast(id ? 'Agendamento atualizado!' : 'Agendamento criado!');
    closeModal('modalAgendamento');
    document.getElementById('formAgendamento').reset();
    document.getElementById('agendamentoId').value = '';
    carregarAgendamentos();
  } catch {
    showToast('Erro de comunicação com a API.', true);
  }
}

async function editarAgendamento(id) {
  const r   = await fetch(`${API}/agendamentos/${id}`);
  const ag  = await r.json();
  document.getElementById('agendamentoId').value        = ag.id;
  document.getElementById('agendamentoClienteId').value = ag.cliente_id;
  document.getElementById('agendamentoServico').value   = ag.servico;
  // formata para datetime-local
  const dt = new Date(ag.data_hora);
  const pad = n => String(n).padStart(2,'0');
  document.getElementById('agendamentoDataHora').value  =
    `${dt.getFullYear()}-${pad(dt.getMonth()+1)}-${pad(dt.getDate())}T${pad(dt.getHours())}:${pad(dt.getMinutes())}`;
  document.getElementById('agendamentoStatus').value    = ag.status;
  document.getElementById('agendamentoObs').value       = ag.observacoes || '';
  document.getElementById('modalAgendamentoTitle').textContent = 'Editar agendamento';
  openModal('modalAgendamento');
}

async function removerAgendamento(id) {
  if (!confirm('Remover este agendamento?')) return;
  const r = await fetch(`${API}/agendamentos/${id}`, { method: 'DELETE' });
  if (r.ok || r.status === 204) {
    showToast('Agendamento removido.');
    carregarAgendamentos();
  } else {
    showToast('Erro ao remover agendamento.', true);
  }
}

/* ──────── INICIALIZAÇÃO ────────────────────────────── */
(async () => {
  await verificarAPI();
  await carregarClientes();
})();