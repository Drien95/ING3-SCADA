document.addEventListener('DOMContentLoaded', function() {
    const controlButtons = document.querySelectorAll('.control-button');
    const messageArea = document.getElementById('message');

    controlButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Empêcher la soumission de formulaire (si utilisé dans un formulaire)

            const controlName = this.dataset.control; // Récupérer le nom du contrôle depuis l'attribut data-control
            const state = this.dataset.state;     // Récupérer l'état (true/false) depuis l'attribut data-state

            // Envoi de la requête POST au backend Flask
            fetch('/control', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded', // Type de contenu pour les données de formulaire
                },
                body: `control=${encodeURIComponent(controlName)}&state=${encodeURIComponent(state)}` // Envoi des données au format formulaire
            })
            .then(response => response.json()) // Parse la réponse JSON
            .then(data => {
                if (data.status === 'success') {
                    messageArea.textContent = `Commande "${data.control}" mise à "${data.state.toUpperCase()}" avec succès.`;
                    messageArea.className = 'message-area success-message'; // Ajouter une classe pour le style de succès
                } else {
                    messageArea.textContent = `Erreur: ${data.message}`;
                    messageArea.className = 'message-area error-message'; // Ajouter une classe pour le style d'erreur
                }
                 // Réinitialiser les classes de message après un délai (pour un affichage temporaire)
                setTimeout(() => {
                    messageArea.className = 'message-area'; // Réinitialiser à la classe de base
                    messageArea.textContent = ''; // Effacer le texte
                }, 3000); // Effacer après 3 secondes (3000 ms)
            })
            .catch(error => {
                console.error('Erreur fetch:', error);
                messageArea.textContent = 'Erreur de communication avec le serveur.';
                messageArea.className = 'message-area error-message';
                setTimeout(() => {
                    messageArea.className = 'message-area';
                    messageArea.textContent = '';
                }, 5000); // Effacer après 5 secondes en cas d'erreur de fetch
            });
        });
    });
});
