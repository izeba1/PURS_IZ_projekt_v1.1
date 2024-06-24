function dohvatiZadnju() {
    fetch('/zadnja_vrijednost')
    .then(response => response.json())
    .then(data => {
        // Ažuriranje HTML-a sa dobivenim podatcima
        const zadnja = data.zadnja_vrijednost
        document.getElementById('data').innerText = zadnja;
    })
    .catch(error => {
        console.error('Error prilikom dohvaćanja podatka: ', error);
    });
}

// Pozivanje funkcije svaku sekundu
setInterval(dohvatiZadnju, 1000); 
