document.addEventListener("DOMContentLoaded", function () {
    const cutsTable = document.getElementById("cutsTable").querySelector("tbody");
    const addRowButton = document.getElementById("addRow");

    // Adicionar nova linha na tabela
    addRowButton.addEventListener("click", function () {
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td><input type="number" name="length[]" placeholder="Ex.: 1500" required></td>
            <td><input type="number" name="quantity[]" placeholder="Ex.: 3" required></td>
            <td><button type="button" class="remove-row">Remover</button></td>
        `;
        cutsTable.appendChild(newRow);
    });

    // Remover linha da tabela
    cutsTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-row")) {
            e.target.closest("tr").remove();
        }
    });

    // Submeter o formulário
    document.getElementById("optimizationForm").addEventListener("submit", async function (e) {
        e.preventDefault();

        const barLength = document.getElementById("bar_length").value;
        const cutLoss = document.getElementById("cut_loss").value;
        const lengths = document.querySelectorAll("input[name='length[]']");
        const quantities = document.querySelectorAll("input[name='quantity[]']");

        const cuts = {};
        lengths.forEach((lengthInput, index) => {
            const length = lengthInput.value;
            const quantity = quantities[index].value;
            if (length && quantity) cuts[length] = quantity;
        });

        const response = await fetch("https://seu-backend.onrender.com/optimize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                bar_length: barLength,
                cut_loss: cutLoss,
                cuts: cuts,
            }),
        });

        const resultDiv = document.getElementById("result");
        if (response.ok) {
            const data = await response.json();
            resultDiv.innerHTML = `
                <h2>Resultado:</h2>
                <p>Total de barras necessárias: ${data.total_bars}</p>
                <pre>${JSON.stringify(data.bars, null, 2)}</pre>
            `;
        } else {
            const error = await response.json();
            resultDiv.innerHTML = `<p style="color: red;">Erro: ${error.error}</p>`;
        }
    });
});
