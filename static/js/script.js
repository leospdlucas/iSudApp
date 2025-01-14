document.addEventListener("DOMContentLoaded", function () {
    // Carrega os dados salvos
    fetch('/fetch')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const inputs = document.querySelectorAll(`.input-box[data-month="${item.month}"][data-week="${item.week}"][data-day="${item.day}"]`);
                inputs.forEach((box, index) => {
                    const input = box.querySelector("input");
                    const fieldKey = `dupla_${index + 1}`; // Define o campo correspondente

                    if (item[fieldKey]) {
                        input.value = item[fieldKey]; // Preenche o valor
                        input.disabled = true; // Desabilita o campo
                        const button = box.querySelector("button");
                        button.disabled = true; // Desabilita o botão
                    }
                });
            });
        })
        .catch(err => console.error('Erro ao buscar dados:', err));

    // Configura os botões de salvar
    const saveButtons = document.querySelectorAll('.input-box button');
    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const parentBox = this.closest('.input-box');
            const input = parentBox.querySelector("input");

            // Verifica os atributos data-* para enviar ao backend
            const month = parentBox.dataset.month;
            const week = parentBox.dataset.week;
            const day = parentBox.dataset.day;
            const field = parentBox.dataset.key; // Campo específico (dupla_1, dupla_2, etc.)

            if (!field) {
                alert('Erro: Campo não identificado.');
                return;
            }

            // Solicita senha se o campo já estiver preenchido
            const password = input.disabled ? prompt('Este campo já está preenchido. Insira a senha para alterar:') : null;

            // Cria o objeto de dados a ser enviado
            const data = {
                month,
                week,
                day,
                field, // Campo específico
                value: input.value, // Valor do input
                password // Senha para validação
            };

            // Envia os dados ao backend pela rota /save
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