var clicked = false;
window.addEventListener("scroll", function() {
        var nav = document.querySelector(".nav");
        var config = document.querySelector("#Configuracion");
        nav.classList.toggle("active", window.scrollY > 0);
        config.classList.toggle("active", window.scrollY > 0);
    })
    //----------------------Perfil--------------------------//
function mostrarConfig() {
    if (clicked) {
        document.getElementById('Configuracion').style.display = 'none';
        clicked = false;
    } else {
        document.getElementById('Configuracion').style.display = 'flex';
        clicked = true;
    }

}

function ocultarConfig() {
    document.getElementById('Configuracion').style.display = 'none';
}