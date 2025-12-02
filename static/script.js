let currentColor = "#2596be";
let gridData = Array(8).fill().map(()=> Array(8).fill("#f6f6f6"));

const grid = document.getElementById("grid");
const output = document.getElementById("output");

function setColor(color){
    currentColor = color;
}

function renderGrid(){
    grid.innerHTML = "";
    for(let i=0;i<8;i++){
        for(let j=0;j<8;j++){
            const cell = document.createElement("div");
            cell.className = "cell";
            cell.style.backgroundColor = gridData[i][j];
            cell.onclick = () => {
                gridData[i][j] = currentColor;
                renderGrid();
            };
            grid.appendChild(cell);
        }
    }
}
renderGrid();

async function exportTurtle(){
    const res = await fetch("/export_turtle", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({grid:gridData}) });
    const data = await res.json();
    output.textContent = data.code;
}

async function exportArsip(){
    const res = await fetch("/export_arsip", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({grid:gridData}) });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "pixel_art.arsip";
    a.click();
}

async function importArsip(){
    const file = document.getElementById("importFile").files[0];
    if(!file) return alert("Wähle eine Datei!");
    const form = new FormData();
    form.append("file", file);
    const res = await fetch("/import_arsip", { method:"POST", body: form });
    const data = await res.json();
    if(data.error) return alert(data.error);
    gridData = data.grid;
    renderGrid();
}
