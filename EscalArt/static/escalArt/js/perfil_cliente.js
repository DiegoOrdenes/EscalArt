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