document.addEventListener('DOMContentLoaded', function() {
    const controlButtons = document.querySelectorAll('.control-button');
    const messageArea = document.getElementById('message');

    controlButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 

            const controlName = this.dataset.control; 
            const state = this.dataset.state;     


            fetch('/control', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded', 
                },
                body: `control=${encodeURIComponent(controlName)}&state=${encodeURIComponent(state)}` 
            })
            .then(response => response.json()) 
            .then(data => {
                if (data.status === 'success') {
                    messageArea.textContent = `Commande "${data.control}" mise à "${data.state.toUpperCase()}" avec succès.`;
                    messageArea.className = 'message-area success-message'; 
                } else {
                    messageArea.textContent = `Erreur: ${data.message}`;
                    messageArea.className = 'message-area error-message'; 
                }

                setTimeout(() => {
                    messageArea.className = 'message-area'; 
                    messageArea.textContent = ''; 
                }, 3000); 
            })
            .catch(error => {
                console.error('Erreur fetch:', error);
                messageArea.textContent = 'Erreur de communication avec le serveur.';
                messageArea.className = 'message-area error-message';
                setTimeout(() => {
                    messageArea.className = 'message-area';
                    messageArea.textContent = '';
                }, 5000); 
            });
        });
    });
});
