const map = L.map('map').setView([60.23, 24.74], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const airportMarkers = L.featureGroup().addTo(map);

document.addEventListener('DOMContentLoaded', async (e) => {
    const current_airport =  await setStartingAirport();

    console.log(`You started at ${current_airport.name}`);

    await getClosestAirports(current_airport.latitude_deg, current_airport.longitude_deg);
});

async function setStartingAirport() {
    const options = ['EGKK', 'EFHK', 'LFPG', 'KJFK', 'KDFW', 'KLAX'];
    const random_icao = options[Math.floor(Math.random() * options.length)];

    airportMarkers.clearLayers();

    const response = await fetch('http://127.0.0.1:3000/airport/' + random_icao);
    const airport = await response.json();

    const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).
        addTo(map).
        bindPopup(airport.name).
        openPopup();
    airportMarkers.addLayer(marker);

    // pan map to selected airport
    map.flyTo([airport.latitude_deg, airport.longitude_deg]);

    return airport;
}

async function getClosestAirports(lat, lon){
    const response = await fetch(`http://127.0.0.1:3000/airport/closest/${lat}/${lon}`);
    const airports = await response.json();

    for (const airport of airports) {
        const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map).bindPopup(airport.name)
        
        marker.on('click', function (e) {
            const co2_emissions = calculateCO2(airport.Distance_KM);

            console.log(`Distance to ${airport.name} is ${Math.floor(airport.Distance_KM)}KM.`);
            console.log(`The trip would use ${co2_emissions} CO2`);

            console.log(airport);

            travelToAirport(airport);

        });
        
        airportMarkers.addLayer(marker);

        
    }
    return airports;
}   

async function travelToAirport(airport){
    const conf = confirm(`Do you want to travel to ${airport.name}`);

    if(conf) {
        airportMarkers.clearLayers();

        const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).
            addTo(map).
            bindPopup(airport.name).
            openPopup();
        airportMarkers.addLayer(marker);

        // pan map to selected airport
        map.flyTo([airport.latitude_deg, airport.longitude_deg]);
        await getClosestAirports(airport.latitude_deg, airport.longitude_deg);

        showQuestion();
    }
}

function calculateCO2(distance) {
    const fuel_burn_per_hour = 500; 
    const cruising_speed_km_hr = 900;

    const co2_per_gallon_fuel = 9.57;
    const fuel_burn_per_km = fuel_burn_per_hour / cruising_speed_km_hr;

    const co2_emissions = distance * fuel_burn_per_km * co2_per_gallon_fuel

    return co2_emissions
}

async function getQuestions(){
    const response = await fetch(`http://127.0.0.1:3000/questions`);
    const questions = await response.json();

    return questions;
}

async function showQuestion() {
    const questions = await getQuestions();

    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];

    document.getElementById("questionText").innerText = randomQuestion.question_text;
    const answers = [randomQuestion.wrong_answer, randomQuestion.answer, randomQuestion.wrong_answer2].filter(a => a);
    const answerButtons = document.getElementsByClassName("answer");
    answers.forEach((answer, index) => {
        answerButtons[index].innerText = answer;
    });


    document.getElementById("questionModal").style.display = "block";
}

const modal = document.getElementById("questionModal");
const closeButton = document.getElementsByClassName("close-button")[0];
closeButton.onclick = function() {
    modal.style.display = "none";
};