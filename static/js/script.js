document.addEventListener('DOMContentLoaded', function () {
    // Gráfico de Casos
    let casosCtx = document.getElementById('casosChart').getContext('2d');
    let casosChart = new Chart(casosCtx, {
        type: 'pie',
        data: {
            labels: JSON.parse(document.getElementById('casosLabels').textContent),
            datasets: [{
                data: JSON.parse(document.getElementById('casosValues').textContent),
                backgroundColor: [
                    'rgba(40, 167, 69, 0.2)',    // Verde
                    'rgba(255, 7, 0, 0.2)',      // Rojo oscuro
                    'rgba(23, 162, 184, 0.2)',   // Teal
                    'rgba(108, 117, 125, 0.2)',  // Gris oscuro
                    'rgba(255, 193, 7, 0.2)',    // Amarillo
                    'rgba(0, 123, 255, 0.2)',    // Azul fuerte
                    'rgba(255, 0, 0, 0.2)'       // Rojo
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',      // Verde
                    'rgba(255, 7, 0, 1)',        // Rojo oscuro
                    'rgba(23, 162, 184, 1)',     // Teal
                    'rgba(108, 117, 125, 1)',    // Gris oscuro
                    'rgba(255, 193, 7, 1)',      // Amarillo
                    'rgba(0, 123, 255, 1)',      // Azul fuerte
                    'rgba(255, 0, 0, 1)'         // Rojo
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend:{
                    position: 'top'
                },
                tooltip: {
                    callbacks:{
                        label: function(tooltipItem) {
                            const label = tooltipItem.label;
                            const customTexts = {
                                'A': 'Dengue sin signos de alarma ni comorbilidades:',
                                'B': ' Dengue sin signos de alarma con comorbilidades o riesgo social:',
                                'C': 'Dengue con signos de alarma:',
                            };
                            const customText = customTexts[label]
                            return `${customText} ${tooltipItem.raw}`;
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Número de Pacientes por Caso',
                    font: {
                        size: 18
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            }
        },
    });

    // Gráfico de Sexo
    let sexoCtx = document.getElementById('sexoChart').getContext('2d');
    let sexoChart = new Chart(sexoCtx, {
        type: 'pie',
        data: {
            labels: JSON.parse(document.getElementById('sexoLabels').textContent),
            datasets: [{
                data: JSON.parse(document.getElementById('sexoValues').textContent),
                backgroundColor: [
                    'rgba(0, 123, 255, 0.2)', 
                    'rgba(23, 162, 184, 0.2)',   
                    'rgba(255, 7, 0, 0.2)',
                    'rgba(40, 167, 69, 0.2)',     
                    'rgba(255, 193, 7, 0.2)',     
                    'rgba(255, 0, 0, 0.2)',    
                    'rgba(108, 117, 125, 0.2)'      
                ],
                borderColor: [
                    'rgba(0, 123, 255, 1)',
                    'rgba(23, 162, 184, 1)',
                    'rgba(255, 7, 0, 1)',     
                    'rgba(40, 167, 69, 1)',                          
                    'rgba(255, 193, 7, 1)',        
                    'rgba(255, 0, 0, 1)',              
                    'rgba(108, 117, 125, 1)'           
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.raw;
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Número de Pacientes por Sexo',
                    font: {
                        size: 18
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            }
        }
    });
    // Gráfico de Departamentos
    let departamentosCtx = document.getElementById('departamentosChart').getContext('2d');
    let departamentosChart = new Chart(departamentosCtx, {
        type: 'pie',
        data: {
            labels: JSON.parse(document.getElementById('departamentosLabels').textContent),
            datasets: [{
                data: JSON.parse(document.getElementById('departamentosValues').textContent),
                backgroundColor: [
                    'rgba(255, 193, 7, 0.2)',     
                    'rgba(23, 162, 184, 0.2)',    
                    'rgba(255, 0, 0, 0.2)',      
                    'rgba(0, 123, 255, 0.2)',   
                    'rgba(108, 117, 125, 0.2)',   
                    'rgba(40, 167, 69, 0.2)',
                    'rgba(255, 7, 0, 0.2)'        
                ],
                borderColor: [
                    'rgba(255, 193, 7, 1)',       
                    'rgba(23, 162, 184, 1)',      
                    'rgba(255, 0, 0, 1)',          
                    'rgba(0, 123, 255, 1)',       
                    'rgba(108, 117, 125, 1)',      
                    'rgba(40, 167, 69, 1)',        
                    'rgba(255, 7, 0, 1)'           
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.raw;
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Número de Pacientes por Departamento',
                    font: {
                        size: 18
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            }
        }
    });

    // Gráfico de Edades
    let edadesCtx = document.getElementById('edadesChart').getContext('2d');
    let edadesChart = new Chart(edadesCtx, {
        type: 'pie',
        data: {
            labels: JSON.parse(document.getElementById('edadesLabels').textContent),
            datasets: [{
                data: JSON.parse(document.getElementById('edadesValues').textContent),
                backgroundColor: [
                    'rgba(255, 0, 0, 0.2)',       
                    'rgba(108, 117, 125, 0.2)',   
                    'rgba(23, 162, 184, 0.2)',    
                    'rgba(40, 167, 69, 0.2)',     
                    'rgba(255, 193, 7, 0.2)',     
                    'rgba(255, 7, 0, 0.2)',       
                    'rgba(0, 123, 255, 0.2)'      
                ],
                borderColor: [
                    'rgba(255, 0, 0, 1)',         
                    'rgba(108, 117, 125, 1)',
                    'rgba(23, 162, 184, 0.2)',     
                    'rgba(40, 167, 69, 1)',        
                    'rgba(255, 193, 7, 1)',        
                    'rgba(255, 7, 0, 1)',          
                    'rgba(0, 123, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.raw;
                        }
                    }
                },
                title: {
                    display: true,
                    text: 'Número de Pacientes por Edad',
                    font: {
                        size: 18
                    },
                    padding: {
                        top: 10,
                        bottom: 20
                    }
                }
            }
        }
    });
});
