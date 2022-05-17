//-----------------------------------------------------------Publicaciones/Imagenes----------------------------------------//

//Variables
const btnCierra = document.querySelector('#btn-cierra');

const btnAdelanta = document.querySelector('#btn-adelanta');
const btnRetrocede = document.querySelector('#btn-retrocede');
const imagenes = document.querySelectorAll('#galeria img');
const lightbox = document.querySelector('#contenedor-principal')

const imagenActiva = document.querySelector('#img-activa');
let indiceImagen = 0;

//Abrir el lightbox

const abreLightbox = (event) => {
    imagenActiva.src = event.target.src;
    lightbox.style.display = 'flex';
    indiceImagen = Array.from(imagenes).indexOf(event.target);
}
imagenes.forEach((imagen) => {
    imagen.addEventListener('click', abreLightbox);
});

//Cerrar el lightbox
btnCierra.addEventListener('click', () => {
    lightbox.style.display = 'none';
})

function OcultarPubli() {
    document.getElementById('contenedor-principal').style.display = 'none';
}

// function AbrirPubli() {
//     document.getElementById('contenedor-principal').style.display = 'flex';
// }

//Adelantar imagen
const adelantaImagen = () => {
    if (indiceImagen === imagenes.length - 1) {
        indiceImagen = -1;
    }
    imagenActiva.src = imagenes[indiceImagen + 1].src;
    indiceImagen++;
};

btnAdelanta.addEventListener('click', adelantaImagen);

//Retrocede la imagen

const retrocedeImagen = () => {
    if (indiceImagen === 0) {
        indiceImagen = imagenes.length;
    }
    imagenActiva.src = imagenes[indiceImagen - 1].src;
    indiceImagen--;
};

btnRetrocede.addEventListener('click', retrocedeImagen);




//--------------------------------Calificacion------------------------------------------//
function mostrar() {
    document.getElementById('testimonials').style.display = 'flex';
}

function ocultar() {
    document.getElementById('testimonials').style.display = 'none';
}
//----------------------Perfil--------------------------//
function mostrarConfig() {
    document.getElementById('Configuracion').style.display = 'flex';
}

function ocultarConfig() {
    document.getElementById('Configuracion').style.display = 'none';
}
//----------------------Publicacion-----------------------//
function MostrarPublicacion() {
    document.getElementById('section-publicacion').style.display = 'flex';
}

function OcultarPublicacion() {
    document.getElementById('section-publicacion').style.display = 'none';
}
//-----------------------Configurar-Bio------------------------//
function MostrarConfi_bio() {
    document.getElementById('config-fondo').style.display = 'flex';
}

function OcultarConfi_bio() {
    document.getElementById('config-fondo').style.display = 'none';
}


//-----------------------------------------//

function AbrirPubli() {
    document.getElementById('contenedor-principal').style.display = 'flex';
}

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

const realFileBtn = document.getElementById("real-file");
const CustomBtn = document.getElementById("custom-button");
const realFileBtn2 = document.getElementById("real-file2");
const CustomBtn2 = document.getElementById("custom-button2");
const realFileBtn3 = document.getElementById("real-file3");
const CustomBtn3 = document.getElementById("custom-button3");

CustomBtn.addEventListener("click", function() {
    realFileBtn.click();
});
CustomBtn2.addEventListener("click", function() {
    realFileBtn2.click();
});
CustomBtn3.addEventListener("click", function() {
    realFileBtn3.click();
});
var clicked = false;

function mostrarConfig() {
    if (clicked) {
        document.getElementById('Configuracion').style.display = 'none';
        clicked = false;
    } else {
        document.getElementById('Configuracion').style.display = 'flex';
        clicked = true;
    }

}