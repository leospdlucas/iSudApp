document.addEventListener("DOMContentLoaded", function () {
    // Carrega os dados salvos e preenche os campos correspondentes
    fetch('/fetch')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const input = document.querySelector(`.input-box[data-month="${item.month}"][data-week="${item.week}"][data-day="${item.day}"] input`);
                if (input) {
                    input.value = item.value || '';
                }
            });
        })
        .catch(err => console.error('Erro ao buscar dados:', err));

    // Configura eventos de alteração nos campos de input
    const inputs = document.querySelectorAll('.input-box input');
    inputs.forEach(input => {
        input.addEventListener('blur', function () {
            const parentBox = this.closest('.input-box');
            const month = parentBox.dataset.month;
            const week = parentBox.dataset.week;
            const day = parentBox.dataset.day;
            const newValue = this.value.trim();

            // Detecta se houve alteração no valor
            if (newValue !== this.dataset.previousValue) {
                const confirmEdit = confirm('Deseja alterar o valor deste campo?');
                if (confirmEdit) {
                    const password = prompt('Insira a senha de administrador para confirmar:');
                    if (!password) return;

                    const data = {
                        month,
                        week,
                        day,
                        value: newValue,
                        password
                    };

                    // Envia a atualização para o backend
                    fetch('/save', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.message) {
                            alert(result.message);
                            this.dataset.previousValue = newValue; // Atualiza o valor salvo localmente
                        } else if (result.error) {
                            alert(`Erro: ${result.error}`);
                        }
                    })
                    .catch(err => console.error('Erro ao salvar dados:', err));
                }
            }
        });

        // Salva o valor inicial como referência
        input.dataset.previousValue = input.value.trim();
    });

    // Configura os botões de salvar
    const saveButtons = document.querySelectorAll('.input-box button');
    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const parentBox = this.closest('.input-box');
            const month = parentBox.dataset.month;
            const week = parentBox.dataset.week;
            const day = parentBox.dataset.day;
            const input = parentBox.querySelector('input');
            const value = input.value.trim();

            // Feedback visual durante a requisição
            button.disabled = true;
            button.textContent = "Salvando...";

            const data = {
                month,
                week,
                day,
                value
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
