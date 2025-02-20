document.addEventListener('DOMContentLoaded', () => {
    const ratingElements = document.querySelectorAll('.rating');

    ratingElements.forEach((ratingElement) => {
        const productoId = ratingElement.closest('.col-12').dataset.productId;
        ratingElement.innerHTML = `
                                    Rating:                                      
                                    <span class="fa fa-star"></span>
                                    <span class="fa fa-star"></span>
                                    <span class="fa fa-star"></span>
                                    <span class="fa fa-star not_checked"></span>
                                    <span class="fa fa-star not_checked"></span>
                                    <span class="rate">Rate: </span> |
                                    <span class="count">Count: </span>
                                `;

        const stars = ratingElement.querySelectorAll('.fa-star');
        const rateSpan = ratingElement.querySelector('.rate');
        const countSpan = ratingElement.querySelector('.count');

        // Agregar un evento de clic a cada estrella
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                stars.forEach((s, i) => {
                    s.classList.toggle('checked', i <= index);
                });
                enviarRating(productoId, index + 1);
            });

        });

        function enviarRating(productId, newrating) {
            const apiUrl = `http://localhost:1337/etienda/api/productos/${productId}/rating/${newrating}`;

            fetch(apiUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Error de red - ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    mostrarMensajeExito(`Rating enviado correctamente`, data);
                    rateSpan.textContent = `Rate: ${data.rating.rate}`;
                    countSpan.textContent = `Count: ${data.rating.count}`;

                })
                .catch(error => {
                    mostrarMensajeError(`Error al enviar el rating a la API: ${error.message}`);
                });
        }

        function mostrarMensajeExito(mensaje) {
            const mensajeElement = document.createElement('div');
            mensajeElement.classList.add('mensaje-exito');
            mensajeElement.textContent = mensaje;

            document.body.appendChild(mensajeElement);

            setTimeout(() => {
                document.body.removeChild(mensajeElement);
            }, 3000); // Mostrar durante 3 segundos
        }

        function mostrarMensajeError(mensaje) {
            const mensajeElement = document.createElement('div');
            mensajeElement.classList.add('mensaje-error');
            mensajeElement.textContent = mensaje;

            document.body.appendChild(mensajeElement);
        }

    });

});
