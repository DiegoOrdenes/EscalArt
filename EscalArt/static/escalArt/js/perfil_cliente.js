// var clicked = false;
// var clicked_3 = true;

// function mostrarComisiones() {
//     if (clicked) {
//         if (clicked_3) {
//             document.getElementById('es-comision').style.display = 'none';
//             clicked = false;
//         } else {
//             clicked_3 = true;
//         }

//     } else {
//         document.getElementById('gl-guardados').style.display = 'none';
//         document.getElementById('es-comision').style.display = 'flex';
//         clicked = true;
//         clicked_3 = false;
//     }

// }

// var clicked_guardados = false;
// var clicked_2 = true;

// function mostrarGuardados() {
//     if (clicked_guardados) {
//         if (clicked_2) {
//             document.getElementById('gl-guardados').style.display = 'none';
//             clicked_guardados = false;

//         } else {
//             clicked_2 = true
//         }
//     } else {
//         document.getElementById('es-comision').style.display = 'none';
//         document.getElementById('gl-guardados').style.display = 'flex';
//         clicked_guardados = true;
//         clicked_2 = false;
//     }

// }

function mostrarGuardados() {
    document.getElementById('es-comision').style.display = 'none';
    document.getElementById('gl-guardados').style.display = 'flex';
}

function mostrarComisiones() {
    document.getElementById('es-comision').style.display = 'flex';
    document.getElementById('gl-guardados').style.display = 'none';

}
// Alertas
function MostrarAlerta() {
    document.getElementById('AlertaOk').style.display = 'block';
}

function OcultarAlerta() {
    document.getElementById('AlertaOk').style.display = 'none';
}

function MostrarAlerta2() {
    document.getElementById('AlertaOk2').style.display = 'block';
}

function OcultarAlerta2() {
    document.getElementById('AlertaOk2').style.display = 'none';
}

// Fin alertas

// upload files
const realFileBtn2 = document.getElementById("real-file2");
const CustomBtn2 = document.getElementById("custom-button2");
CustomBtn2.addEventListener("click", function() {
    realFileBtn2.click();
});

const realFileBtn3 = document.getElementById("real-file3");
const CustomBtn3 = document.getElementById("custom-button3");
CustomBtn3.addEventListener("click", function() {
    realFileBtn3.click();
});

// fin upload files