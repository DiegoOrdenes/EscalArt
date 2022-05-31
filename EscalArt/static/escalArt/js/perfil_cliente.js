/* perfil cliente vista cliente*/

function mostrarGuardados() {
    document.getElementById('es-comision').style.display = 'none';
    document.getElementById('gl-guardados').style.display = 'flex';
}

function mostrarComisiones() {
    document.getElementById('es-comision').style.display = 'flex';
    document.getElementById('gl-guardados').style.display = 'none';

}







/* perfil cliente Vista artista*/
function mostrarReferencias() {
    document.getElementById('es-comision').style.display = 'none';
    document.getElementById('gl-guardados').style.display = 'block';
    document.getElementById('tareas--').style.display = 'none';
}

function mostrarEsComision() {
    document.getElementById('es-comision').style.display = 'block';
    document.getElementById('gl-guardados').style.display = 'none';
    document.getElementById('tareas--').style.display = 'none';

}

function mostrarTareas() {
    document.getElementById('tareas--').style.display = 'block';
    document.getElementById('gl-guardados').style.display = 'none';
    document.getElementById('es-comision').style.display = 'none';

}

function ver_tareas() {
    if (clicked) {
        document.getElementById('crear-tarea').style.display = 'none';
        clicked = false;
    } else {
        document.getElementById('crear-tarea').style.display = 'block';
        clicked = true;
    }
}


// Info date
const dateNumber = document.getElementById('dateNumber');
const dateText = document.getElementById('dateText');
const dateMonth = document.getElementById('dateMonth');
const dateYear = document.getElementById('dateYear');

// Tasks Container
const tasksContainer = document.getElementById('tasksContainer');

const setDate = () => {
    const date = new Date();
    dateNumber.textContent = date.toLocaleString('es', { day: 'numeric' });
    dateText.textContent = date.toLocaleString('es', { weekday: 'long' });
    dateMonth.textContent = date.toLocaleString('es', { month: 'long' });
    dateYear.textContent = date.toLocaleString('es', { year: 'numeric' });
};

const addNewTask = event => {
    event.preventDefault();
    const { value } = event.target.taskText;
    if (!value) return;
    const task = document.createElement('div');
    task.classList.add('task', 'roundBorder');
    task.addEventListener('click', changeTaskState);
    task.textContent = value;

    tasksContainer.prepend(task);
    event.target.reset();
};

const changeTaskState = event => {
    event.target.classList.toggle('done');
};

const order = () => {
    const done = []; //Tareas echas
    const toDo = []; //Tareas por hacer
    tasksContainer.childNodes.forEach(el => {
        el.classList.contains('done') ? done.push(el) : toDo.push(el)
    })
    return [...toDo, ...done];
}

const renderOrderedTasks = () => {
    order().forEach(el => tasksContainer.appendChild(el))
}

setDate();