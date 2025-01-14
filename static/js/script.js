document.addEventListener("DOMContentLoaded", function () {
    fetch('/fetch')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const inputs = document.querySelectorAll(`.input-box[data-month="${item.month}"][data-week="${item.week}"][data-day="${item.day}"]`);
                inputs.forEach((box, index) => {
                    const input = box.querySelector("input");
                    const fieldKey = `dupla_${index + 1}`;
                    if (item[fieldKey]) {
                        input.value = item[fieldKey];
                    }
                });
            });
        })
        .catch(err => console.error('Erro ao buscar dados:', err));

    const saveButtons = document.querySelectorAll('.input-box button');
    saveButtons.forEach(button => {
        button.addEventListener('click', function () {
            const parentBox = this.closest('.input-box');
            const input = parentBox.querySelector("input");

            const month = parentBox.dataset.month;
            const week = parentBox.dataset.week;
            const day = parentBox.dataset.day;
            const field = parentBox.dataset.key;

            const data = {
                month,
                week,
                day,
                field,
                value: input.value
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
                    } else if (result.error) {
                        alert(`Erro: ${result.error}`);
                    }
                })
                .catch(err => console.error('Erro ao salvar dados:', err));
        });
    });
});
