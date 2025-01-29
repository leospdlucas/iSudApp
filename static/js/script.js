document.addEventListener("DOMContentLoaded", function () {
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

    // Configura os eventos de clique para inputs bloqueados
    document.querySelectorAll('.input-box input').forEach(input => {
        input.addEventListener('click', function () {
            if (this.disabled) {
                const wantsToEdit = confirm("Este campo já está preenchido. Deseja alterar?");
                if (wantsToEdit) {
                    const password = prompt("Insira a senha ADM para desbloquear:");
                    if (password === "senha_adm") { // Substitua pela sua senha correta
                        this.disabled = false;
                        this.focus();
                    } else {
                        alert("Senha incorreta. A alteração não foi permitida.");
                    }
                }
            }
        });
    });

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

            const data = {
                month,
                week,
                day,
                key,
                value: input.value.trim(), // Limpa espaços desnecessários
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
