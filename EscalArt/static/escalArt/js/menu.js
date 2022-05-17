window.addEventListener("scroll", function() {
        var nav = document.querySelector(".nav");
        var config = document.querySelector("#Configuracion");
        nav.classList.toggle("active", window.scrollY > 0);
        config.classList.toggle("active", window.scrollY > 0);
    })
    //----------------------Perfil--------------------------//
function mostrarConfig() {
    document.getElementById('Configuracion').style.display = 'flex';
}

function ocultarConfig() {
    document.getElementById('Configuracion').style.display = 'none';
}