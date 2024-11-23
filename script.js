document.getElementById('optimizationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const barLength = document.getElementById('bar_length').value;
    const cutLoss = document.getElementById('cut_loss').value;
    const cutsInput = document.getElementById('cuts').value.split('\n');
    const cuts = {};
    cutsInput.forEach(line => {
        const [length, qty] = line.split(':');
        cuts[length.trim()] = qty.trim();
    });

    try {
        const response = await fetch('URL_DA_SUA_API/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bar_length: barLength, cut_loss: cutLoss, cuts: cuts })
        });

        const resultDiv = document.getElementById('result');
        if (response.ok) {
            const data = await response.json();
            resultDiv.innerHTML = `<h2>Resultado:</h2>
                <p>Total de barras necessárias: ${data.total_bars}</p>
                <pre>${JSON.stringify(data.bars, null, 2)}</pre>`;
        } else {
            const error = await response.json();
            resultDiv.innerHTML = `<p style="color: red;">Erro: ${error.error}</p>`;
        }
    } catch (error) {
        console.error('Erro:', error);
    }
});
