document.addEventListener('DOMContentLoaded', function () {
    const apiURL = 'http://127.0.0.1:5000/';


    // Function to fetch elements and update the table
    function fetchElements() {
        fetch(apiURL)
            .then(response => response.json())
            .then(data => {
                const bidRates = data['bid']
                const offerRates = data['offer']
                //Create a new json to store the bid and offer for each instrument 
                const ir = data['ir']
                const instrumentRates = [
                    //['GGAL/24', bidRates['GGAL/AGO24'], offerRates['GGAL/AGO24'], "NO"]

                ]
                //iterate over the bidRates and offerRates to create the instrumentRates
                for (const [key, value] of Object.entries(bidRates)) {
                    if (offerRates[key] != "-" && value != "-") {
                        if (value < ir || offerRates[key] > ir) {
                            instrumentRates.push([key, value, offerRates[key], "Hay oportunidad de arbitraje"]);
                        } else {
                            instrumentRates.push([key, value, offerRates[key], "No hay oportunidad de arbitraje"]);
                        }
                    }
                    else {
                        instrumentRates.push([key, value, offerRates[key], "No hay oportunidad de arbitraje"]);
                    }
                }

                const tbody = document.querySelector('#elementsTable tbody');
                tbody.innerHTML = ''; // Clear the existing rows
                console.log(instrumentRates);
                instrumentRates.forEach(element => {
                    addElementToTable(element, tbody);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    // Fetch elements initially and set up periodic fetching
    fetchElements();
    setInterval(fetchElements, 5000); // Fetch data every 5 seconds

    // Function to add a new element to the table
    function addElementToTable(element, tbody) {
        const row = document.createElement('tr');

        const nameCell = document.createElement('td');
        nameCell.textContent = element[0];
        row.appendChild(nameCell);

        const bidCell = document.createElement('td');
        bidCell.textContent = element[1];
        row.appendChild(bidCell);

        const offerCell = document.createElement('td');
        offerCell.textContent = element[2];
        row.appendChild(offerCell);

        const statusCell = document.createElement('td');
        statusCell.textContent = element[3];
        row.appendChild(statusCell);

        tbody.appendChild(row);
    }
});
