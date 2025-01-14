document.addEventListener("DOMContentLoaded", function () {
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

    const saveButtons = document.querySelectorAll('.input-box button');
    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const parentBox = this.closest('.input-box');
            const month = parentBox.dataset.month;
            const week = parentBox.dataset.week;
            const day = parentBox.dataset.day;

            const input = parentBox.querySelectorAll('input');
            const data = {
                month,
                week,
                day,
                [key]: input.value
                
            };

            fetch('/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.message) {
                    alert(result.message);
                    input.disabled = true;
                    this.disabled = false;
                };
            })
            .catch(err => console.error('Erro ao salvar dados:', err));
        });
    });
});