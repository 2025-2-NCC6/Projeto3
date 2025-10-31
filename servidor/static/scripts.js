document.addEventListener('DOMContentLoaded', () => {
    
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

    document.getElementById('btn-levantar').addEventListener('click', () => {
        sendCommand('/comando_ascensor', { action: 'levantar' });
    });

    document.getElementById('btn-descer').addEventListener('click', () => {
        sendCommand('/comando_ascensor', { action: 'descer' });
    });


    const btnSolda = document.getElementById('btn-solda');

    btnSolda.addEventListener('click', () => {
        sendCommand('/toggle_solda', { action: 'toggle'})
            .then(data => {
                if (data.status === 'sucesso') {
                    btnSolda.textContent = data.novo_texto;
                    btnSolda.classList.remove('off', 'on');
                    if (data.novo_estado) {
                        btnSolda.classList.add('on');
                    } else {
                        btnSolda.classList.add('off');
                    }
                }
            });
    });

    function updateToolStatus() {
        fetch('/status_ferramentas')
            .then(response => response.json())
            .then(toolStates => {
                for (const [id, isOn] of Object.entries(toolStates)) {
                    const toolElement = document.getElementById(id);
                    if (toolElement) {
                        toolElement.classList.remove('status-on', 'status-off');
                        
                        if (isOn) {
                            toolElement.classList.add('status-on');
                        } else {
                            toolElement.classList.add('status-off');
                        }
                    }
                }
            })
            .catch(error => console.error('Erro ao buscar status das ferramentas:', error));
    }

    setInterval(updateToolStatus, 2000); 
    updateToolStatus();
});