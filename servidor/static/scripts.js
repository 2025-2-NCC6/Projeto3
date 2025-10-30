document.addEventListener('DOMContentLoaded', () => {
    
    // --- Funções Auxiliares para Comunicação com o Flask ---
    function sendCommand(endpoint, data = {}) {
        return fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro do servidor: ' + response.statusText);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Erro ao enviar comando:', error);
        });
    }

    // --- 1. Controle do Ascensor (Levantar/Descer) ---
    document.getElementById('btn-levantar').addEventListener('click', () => {
        sendCommand('/comando_ascensor', { action: 'levantar' });
    });

    document.getElementById('btn-descer').addEventListener('click', () => {
        sendCommand('/comando_ascensor', { action: 'descer' });
    });


    // --- 2. Controle da Bancada de Solda (Alternância) ---
    const btnSolda = document.getElementById('btn-solda');

    // Inicializa o botão com o estado inicial do Flask (opcional, melhor carregar no HTML)
    // Para simplificar, vamos deixar o Flask controlar o estado após o primeiro clique.

    btnSolda.addEventListener('click', () => {
        sendCommand('/toggle_solda')
            .then(data => {
                if (data.status === 'sucesso') {
                    // Atualiza a aparência e o texto do botão com o estado retornado pelo Flask
                    btnSolda.textContent = data.novo_texto;
                    btnSolda.classList.remove('off', 'on');
                    if (data.novo_estado) {
                        btnSolda.classList.add('on'); // Verde
                    } else {
                        btnSolda.classList.add('off'); // Vermelho
                    }
                }
            });
    });

    
    // --- 3. Atualização Periódica do Status das Ferramentas (Simulação do input externo) ---
    function updateToolStatus() {
        fetch('/status_ferramentas') // Rota GET para consultar o estado
            .then(response => response.json())
            .then(toolStates => {
                // toolStates é o dicionário JSON retornado pelo Flask: {'tool-1': True, 'tool-2': False, ...}
                
                for (const [id, isOn] of Object.entries(toolStates)) {
                    const toolElement = document.getElementById(id);
                    if (toolElement) {
                        toolElement.classList.remove('status-on', 'status-off');
                        
                        if (isOn) {
                            toolElement.classList.add('status-on'); // Verde
                        } else {
                            toolElement.classList.add('status-off'); // Vermelho
                        }
                    }
                }
            })
            .catch(error => console.error('Erro ao buscar status das ferramentas:', error));
    }

    // Inicia a atualização periódica (Polling) a cada 2 segundos (2000ms)
    setInterval(updateToolStatus, 2000); 

    // Chama a função uma vez ao carregar para mostrar o estado inicial
    updateToolStatus();
});