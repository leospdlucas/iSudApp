document.addEventListener("DOMContentLoaded", function () {

    // Carrega os dados salvos e preenche os campos
    fetch('/fetch')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const inputs = document.querySelectorAll(`.input-box[data-month="${item.month}"][data-week="${item.week}"][data-day="${item.day}"] input`);
                
                // Preenche os valores dos inputs e bloqueia campos preenchidos
                if (inputs.length === 4) {
                    inputs[0].value = item.dupla_1 || '';
                    inputs[1].value = item.dupla_2 || '';
                    inputs[2].value = item.dupla_3 || '';
                    inputs[3].value = item.dupla_4 || '';

                    inputs.forEach(input => {
                        if (input.value) {
                            input.disabled = true;
                        }document.addEventListener("DOMContentLoaded", function () {
                            // Carrega os dados salvos e preenche os campos correspondentes
                            fetch('/fetch')
                                .then(response => response.json())
                                .then(data => {
                                    data.forEach(item => {
                                        // Busca o campo específico para cada dupla
                                        const input = document.querySelector(`.input-box[data-month="${item.month}"][data-week="${item.week}"][data-day="${item.day}"][data-key="${item.key}"] input`);
                                        if (input) {
                                            input.value = item.value || '';
                                            if (input.value) {
                                                input.disabled = true; // Bloqueia campos preenchidos
                                            }
                                        }
                                    });
                                })
                                .catch(err => console.error('Erro ao buscar dados:', err));
                        
                            // Configura os botões de salvar para cada input-box
                            const saveButtons = document.querySelectorAll('.input-box button');
                            saveButtons.forEach(button => {
                                button.addEventListener('click', function () {
                                    const parentBox = this.closest('.input-box');
                                    const month = parentBox.dataset.month;
                                    const week = parentBox.dataset.week;
                                    const day = parentBox.dataset.day;
                                    const key = parentBox.dataset.key;
                                    const input = parentBox.querySelector('input');
                        
                                    // Solicita senha se o campo já estiver preenchido
                                    const password = input.disabled ? prompt('Este campo já está preenchido. Insira a senha para alterar:') : null;
                        
                                    const data = {
                                        month,
                                        week,
                                        day,
                                        key,
                                        value: input.value, // Valor do input
                                        password // Senha para validação
                                    };
                        
                                    // Envia os dados para o backend
                                    fetch('/save', {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify(data)
                                    })
                                    .then(response => response.json())
                                    .then(result => {
                                        if (result.message) {
                                            alert(result.message);
                                            input.disabled = true; // Desabilita o campo após salvar
                                            this.disabled = true; // Desabilita o botão após salvar
                                        } else if (result.error) {
                                            alert(`Erro: ${result.error}`);
                                        }
                                    })
                                    .catch(err => console.error('Erro ao salvar dados:', err));
                                });
                            });
                        });
                        
                    });
                }
            });
        })
        .catch(err => console.error('Erro ao buscar dados:', err));

    // Configura os botões de salvar
    const saveButtons = document.querySelectorAll('.input-box button');
    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const parentBox = this.closest('.input-box');
            const month = parentBox.dataset.month;
            const week = parentBox.dataset.week;
            const day = parentBox.dataset.day;
            const input = this.previousElementSibling; // Input associado ao botão

            // Solicita senha se o campo já estiver preenchido
            const password = input.disabled ? prompt('Este campo já está preenchido. Insira a senha para alterar:') : null;

            const data = {
                month,
                week,
                day,
                value: input.value.trim(), // Limpa espaços desnecessários
                password // Senha para validação
            };

            // Feedback visual durante a requisição
            button.disabled = true;
            button.textContent = "Salvando...";

            // Envia os dados para o backend
            fetch('/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.message) {
                    alert(result.message);
                    input.disabled = true; // Bloqueia o campo após salvar
                } else if (result.error) {
                    alert(`Erro: ${result.error}`);
                }
            })
            .catch(err => {
                console.error('Erro ao salvar dados:', err);
            })
            .finally(() => {
                button.textContent = "Salvar";
                button.disabled = false;
            });
        });
    });
});
