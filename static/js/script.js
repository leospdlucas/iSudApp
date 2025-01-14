document.addEventListener("DOMContentLoaded", function () {
    // Carrega os dados já salvos
    fetch('/fetch')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const inputs = document.querySelectorAll(`.input-box[data-month="${item.month}"][data-week="${item.week}"][data-day="${item.day}"] input`);
                inputs[0].value = item.dupla_1 || '';
                inputs[1].value = item.dupla_2 || '';
                inputs[2].value = item.dupla_3 || '';
                inputs[3].value = item.dupla_4 || '';

                inputs.forEach(input => {
                    if (input.value) {
                        input.disabled = true; // Bloqueia campos já preenchidos
                    }
                });
            });
        })
        .catch(err => console.error('Erro ao buscar dados:', err));

    // Lida com o evento de clique do botão de salvar
    const saveButtons = document.querySelectorAll('.input-box button');
    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const parentBox = this.closest('.input-box');
            const month = parentBox.dataset.month;
            const week = parentBox.dataset.week;
            const day = parentBox.dataset.day;
            const inputFields = parentBox.querySelectorAll('input');

            // Coleta os valores das entradas
            const data = {
                month,
                week,
                day,
                dupla_1: inputFields[0].value,
                dupla_2: inputFields[1].value,
                dupla_3: inputFields[2].value,
                dupla_4: inputFields[3].value
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
                    // Desabilita os inputs depois de salvar os dados
                    inputFields.forEach(input => {
                        input.disabled = true;
                    });
                    this.disabled = true; // Desabilita o botão após o salvamento
                }
            })
            .catch(err => console.error('Erro ao salvar dados:', err));
        });
    });
});