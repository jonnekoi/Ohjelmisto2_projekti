const map = L.map('map').setView([60.23, 24.74], 5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

const airportMarkers = L.featureGroup().addTo(map);

const startingPointIcon = L.icon({
    iconUrl: 'icons/starting_point.png', // Replace with the path to your icon image
    iconSize: [41, 41], // Size of the icon. This is the default size for Leaflet's marker icon.
    iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location.
    popupAnchor: [8, -41] // Point from which the popup should open relative to the iconAnchor.
});

let correctAnswer = "";

let points = 0;
let co2_consumed = 0;
let distance = 0;

let answerStreak = 0;
let totalCorrectAnswers = 0;

const pointsElement = document.querySelector('.stats-points-target');
const CO2Element = document.querySelector('.stats-co2-target');
const distanceElement = document.querySelector('.stats-distance-target');
const streakElement = document.querySelector('.stats-streak-target');

const tempElement = document.querySelector('.weather-temp-target');
const weatherImgElement = document.querySelector('.weather-icon-target');

const infoButton = document.querySelector('.info-button');
const popup = document.querySelector('.popup');

const questionModal = document.getElementById("questionModal");


document.addEventListener('DOMContentLoaded', async (e) => {
    const current_airport =  await setStartingAirport();

    await getCurrentAirportWeather(current_airport);
    await getClosestAirports(current_airport);        
});

function kelvinToCelcius(kelvin){
    return Math.floor(kelvin - 273.15);
}

async function getCurrentAirportWeather(current_airport) {
    const api_key = 'f806590ff13e2499734e34a745c8ee63';
    
    const lat = current_airport.latitude_deg;
    const lon = current_airport.longitude_deg;

    const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${api_key}`);
    const weather = await response.json();

    const icon = weather.weather[0].icon;
    const temp = `${kelvinToCelcius(weather.main.temp)}°C`;

    tempElement.innerText = temp;
    weatherImgElement.src = `https://openweathermap.org/img/wn/${icon}.png`;
}

async function setStartingAirport() {
    const options = ['EGKK', 'EFHK', 'LFPG', 'KJFK', 'KDFW', 'KLAX', 'WSSS'];
    const random_icao = options[Math.floor(Math.random() * options.length)];

    airportMarkers.clearLayers();

    const response = await fetch('http://127.0.0.1:3000/airport/' + random_icao);
    const airport = await response.json();

    const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {'icon': startingPointIcon}).
        addTo(map).
        bindPopup(airport.name).
        openPopup();
    airportMarkers.addLayer(marker);

    // pan map to selected airport
    map.flyTo([airport.latitude_deg, airport.longitude_deg]);

    return airport;
}

async function getClosestAirports(current_airport){
    const lat = current_airport.latitude_deg;
    const lon = current_airport.longitude_deg;
    const response = await fetch(`http://127.0.0.1:3000/airport/closest/${lat}/${lon}`);
    const airports = await response.json();

    for (const airport of airports) {
        if (current_airport.name !== airport.name){
            const co2_emissions = calculateCO2(airport.Distance_KM);
            const distance = Math.floor(airport.Distance_KM);

            const marker = L.marker([airport.latitude_deg, airport.longitude_deg])
                .addTo(map)
                .bindPopup(`
                            <div>
                                <h3>${airport.name}</h3>
                                <button class="airport-btn" data-airport-name="${airport.name}">Travel to airport</button>                            
                                <p>Distance: ${distance}KM</p>
                                <p>CO2 consumption: ${co2_emissions}KG</p>
                            </div>`);
            
            marker.on('popupopen', function (event) {
                setTimeout(() => { // Timeout to ensure the popup's DOM is ready
                    document.querySelectorAll('.airport-btn').forEach(button => {
                        button.addEventListener('click', function () {
                            travelToAirport(airport, co2_emissions, distance);
                        });
                    });
                }, 1);
            });
            airportMarkers.addLayer(marker);
        }
    }
    return airports;
}   

async function travelToAirport(airport, co2_emissions, dist){
    const conf = confirm(`Do you want to travel to ${airport.name}`);

    if(conf) {
        distance += dist;
        co2_consumed += co2_emissions;

        distanceElement.innerText = `${distance}KM`;
        CO2Element.innerText = `${co2_consumed}KG`;

        airportMarkers.clearLayers();

        const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {'icon': startingPointIcon}).
            addTo(map).
            bindPopup(airport.name).
            openPopup();
        airportMarkers.addLayer(marker);

        map.flyTo([airport.latitude_deg, airport.longitude_deg]);

        await getClosestAirports(airport);
        await showQuestion();
        await getCurrentAirportWeather(airport);
    }
}

function calculateCO2(distance) {
    const fuel_burn_per_hour = 500; 
    const cruising_speed_km_hr = 900;

    const co2_per_gallon_fuel = 9.57;
    const fuel_burn_per_km = fuel_burn_per_hour / cruising_speed_km_hr;

    const co2_emissions = distance * fuel_burn_per_km * co2_per_gallon_fuel

    return Math.floor(co2_emissions)
}

function checkAnswer(e){    
    if (e.innerText === correctAnswer) {
        
        points += 50;
        totalCorrectAnswers += 1;
        answerStreak += 1;
        
        pointsElement.innerHTML = points;
        streakElement.innerText = answerStreak;

        if (answerStreak % 3 === 0) {
            co2_consumed *= .8; 

            alert(`Your CO2 was reduced by 20%. \n Current consumption ${co2_consumed}KG`);

            CO2Element.innerText = `${co2_consumed}KG`;
        } 

        questionModal.style.display = 'none';
    } else {
        alert('Wrong answer. \n Points reduced by 10%.');

        points *= .9;
        answerStreak = 0;

        pointsElement.innerHTML = Math.floor(points);
        streakElement.innerText = answerStreak;
        questionModal.style.display = 'none';
    }
}

async function getQuestions(){
    const response = await fetch(`http://127.0.0.1:3000/questions`);
    const questions = await response.json();

    return questions;
}

async function showQuestion() {
    const questions = await getQuestions();
    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];

    correctAnswer = randomQuestion.answer;

    document.getElementById("questionText").innerText = randomQuestion.question_text;
    const answers = [randomQuestion.wrong_answer, randomQuestion.answer, randomQuestion.wrong_answer2].filter(a => a);
    const answerButtons = document.getElementsByClassName("answer");
    answers.forEach((answer, index) => {
        answerButtons[index].innerText = answer;
    });
    
    questionModal.style.display = "block";
}

const modal = document.getElementById("questionModal");
const closeButton = document.getElementsByClassName("close-button")[0];
closeButton.onclick = function() {
    modal.style.display = "none";
};

infoButton.addEventListener('click', () => {
  popup.style.display = 'block';
});

function closePopup() {
  popup.style.display = 'none';
}