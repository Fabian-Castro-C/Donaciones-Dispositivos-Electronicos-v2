// Importar Highcharts desde el CDN
const script = document.createElement('script');
script.src = 'https://code.highcharts.com/highcharts.js';
script.onload = () => {
    // Una vez que Highcharts se ha cargado, ejecuta tu código para los gráficos

    // Gráfico de Tipos de Dispositivos
    fetch('/datos_dispositivos')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const datos = data.datos.map(item => [capitalizeFirstLetter(item.tipo), item.total]);

                Highcharts.chart('graficoDispositivos', {
                    chart: { type: 'column' },
                    title: { text: 'Tipos de Dispositivos' },
                    xAxis: {
                        type: 'category',
                        title: { text: 'Tipo de Dispositivo' }
                    },
                    yAxis: { title: { text: 'Total' } },
                    series: [{ name: 'Total', data: datos }]
                });
            } else {
                console.error('Error al obtener datos:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));

    // Gráfico de Contactos por Comuna
    fetch('/datos_contactos')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const datos = data.datos.map(item => [item.comuna, item.total]);

                Highcharts.chart('graficoContactos', {
                    chart: { type: 'pie' },
                    title: { text: 'Contactos por Comuna' },
                    series: [{ name: 'Total', colorByPoint: true, data: datos }]
                });
            } else {
                console.error('Error al obtener datos:', data.message);
            }
        })
        .catch(error => console.error('Error:', error));
};

// Función para capitalizar la primera letra de una cadena
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

document.head.appendChild(script);