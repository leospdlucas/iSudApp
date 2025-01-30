// script.js (Frontend)
document.addEventListener("DOMContentLoaded", function () {
    // Carrega os dados salvos e preenche os campos
    fetch('/fetch')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const input = document.querySelector(`.input-box[data-month="${item.month}"][data-week="${item.week}"][data-day="${item.day}"][data-key="${item.key}"] input`);
                if (input) {
                    input.value = item.value || '';
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

            let value = input.value.trim();

            // Verifica se o valor foi alterado
            if (!value) {
                alert('O valor não pode estar vazio.');
                return;
            }

            const data = { month, week, day, key, value };

            // Se já existe um valor, solicitar senha para alterar
            if (input.dataset.originalValue && input.dataset.originalValue !== value) {
                const password = prompt('Valor já preenchido. Insira a senha de administrador para alterar:');
                data.password = password;
            }

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
                    input.dataset.originalValue = value; // Atualiza valor original
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
