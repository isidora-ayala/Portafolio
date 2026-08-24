const formBuscador = document.getElementById('form-buscador');
const inputBuscador = document.getElementById('input-buscador');

// Palabras clave asociadas a cada sección
const secciones = {
    'sobre-mi': ['sobre mi', 'sobre mí', 'isidora', 'quien soy', 'quién soy', 'perfil'],
    'proyectos': ['proyectos', 'proyecto', 'bosques', 'bosques australes', 'trabajos'],
    'contacto': ['contacto', 'email', 'correo', 'github', 'contactar']
};

formBuscador.addEventListener('submit', function (event) {
    event.preventDefault(); // evita que la página se recargue

    const texto = inputBuscador.value.trim().toLowerCase();

    if (texto === '') return;

    // Buscamos si el texto coincide con alguna palabra clave
    let seccionEncontrada = null;

    for (const [idSeccion, palabrasClave] of Object.entries(secciones)) {
        if (palabrasClave.some(palabra => palabra.includes(texto) || texto.includes(palabra))) {
            seccionEncontrada = idSeccion;
            break;
        }
    }

    if (seccionEncontrada) {
        const elemento = document.getElementById(seccionEncontrada);
        elemento.scrollIntoView({ behavior: 'smooth', block: 'start' });
        inputBuscador.value = ''; // limpia el input después de buscar
    } else {
        alert('No se encontró ninguna sección relacionada con "' + texto + '"');
    }
});