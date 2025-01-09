function saveData(month, week, day) {
    console.log(`Salvando dados para ${month}, Semana ${week}, Dia ${day}`);
    const inputs = document.querySelectorAll(`.input-box[data-month="${month}"][data-week="${week}"][data-day="${day}"] input`);
    const data = {
        month,
        week,
        day,
        mission1: inputs[0]?.value || '',
        mission2: inputs[1]?.value || '',
        mission3: inputs[2]?.value || '',
        mission4: inputs[3]?.value || ''
    };
    fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(response => response.json())
      .then(data => alert('Dados salvos com sucesso!'))
      .catch(err => alert('Erro ao salvar os dados.'));
}
