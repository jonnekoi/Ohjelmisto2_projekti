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

let questions;

let correctAnswer = "";
let answerStreak = 0;
let totalCorrectAnswers = 0;


let playerName;
let points = 0;
let co2_consumed = 0;
let distance = 0;



const leaderboardBody = document.querySelector('#leaderboard-rows');

const pointsElement = document.querySelector('.stats-points-target');
const CO2Element = document.querySelector('.stats-co2-target');
const distanceElement = document.querySelector('.stats-distance-target');
const streakElement = document.querySelector('.stats-streak-target');

const tempElement = document.querySelector('.weather-temp-target');
const weatherImgElement = document.querySelector('.weather-icon-target');

const nameForm = document.querySelector('#nameForm');

const questionModal = document.getElementById("questionModal");

const infoButton = document.querySelector('.info-button');
const popup = document.querySelector('.popup');


document.addEventListener('DOMContentLoaded', async (e) => {
    questions = await getQuestions();

    const leaderboardData = await getScoreboard();
    leaderboardData.forEach((item, index) => {
        const row = `<tr>
                        <td>${index + 1}</td>
                        <td>${item.player}</td>
                        <td>${item.co2_emissions}</td> 
                     </tr>`;
        leaderboardBody.innerHTML += row;
    });


    const current_airport =  await setStartingAirport();

    await getCurrentAirportWeather(current_airport);
    await getClosestAirports(current_airport);        
});



document.addEventListener('DOMContentLoaded', function () {
    const nameButton = document.querySelector('#nameButton');
    const nameInput = document.getElementById('name');

    // Click event listener
    nameButton.addEventListener('click', function (event) {
        event.preventDefault();
        handleFormSubmission();
    });

    // Enter key press event listener
    nameInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            handleFormSubmission();
        }
    });


    function handleFormSubmission() {
        playerName = nameInput.value;

        // Fade out animation
        nameForm.style.transition = 'opacity 1s';
        nameForm.style.opacity = 0;

        // Hide the form after submission
        setTimeout(function () {
            nameForm.style.display = 'none';
        }, 1000);}
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
    const icao = options[Math.floor(Math.random() * options.length)];

    airportMarkers.clearLayers();

    const response = await fetch('http://127.0.0.1:3000/airport/' + icao);
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
        CO2Element.innerText = `${Math.floor(co2_consumed)}KG`;

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

async function getScoreboard() {
    const response = await fetch(`http://127.0.0.1:3000/scoreboard`);
    const scoreboard = await response.json();

    return scoreboard;
}

async function checkAnswer(e){   
    const answerElement = document.querySelector('.correct-co2');
    const animationDiv = document.getElementById("correctAnswerAnimation");


    if (e.innerText === correctAnswer) {

        questionModal.style.display = 'none';
        
        animationDiv.style.backgroundColor = 'rgba(9, 83, 139, 0.7)';
        pointsElement.innerHTML = points;
        streakElement.innerText = answerStreak;

        
        points += 50;
        totalCorrectAnswers += 1;
        answerStreak += 1;

        pointsElement.innerHTML = Math.floor(points);
        streakElement.innerText = answerStreak;
       
        if (answerStreak % 3 === 0) {
            co2_consumed *= .8; 
            
            answerElement.innerText = `Your CO2 was reduced by 20%. \n Current consumption ${Math.floor(co2_consumed)}KG`;
            animationDiv.style.display = 'block';
            animationDiv.style.opacity = 1;
            animationDiv.style.animation = "fadeInOut 8s ease-in-out";

            // Hide the animation after 3 seconds
            setTimeout(() => {
                animationDiv.style.opacity = 0;
                animationDiv.style.animation = 'none';
            }, 8000);
            
        } else {

            answerElement.innerText = 'Correct answer. \n +50 points.'
            animationDiv.style.display = 'block';
            animationDiv.style.opacity = 1;
            animationDiv.style.animation = "fadeInOut 6s ease-in-out";

            // Hide the animation after 3 seconds
            setTimeout(() => {
                animationDiv.style.opacity = 0;
                animationDiv.style.animation = 'none';
            }, 6000);
        }   
    } else {
        questionModal.style.display = 'none';

        answerElement.innerText = 'Wrong answer. \n Points reduced by 10%.'
        animationDiv.style.backgroundColor = 'rgba(255, 72, 0, 0.7)';

        animationDiv.style.display = 'block';
        animationDiv.style.opacity = 1;
        animationDiv.style.animation = "fadeInOut 6s ease-in-out";

            // Hide the animation after 3 seconds
            setTimeout(() => {
                animationDiv.style.opacity = 0;
                animationDiv.style.animation = 'none';
            }, 6000);

        points *= .9;
        answerStreak = 0;  
        
    }

    if (points >= 300) {
        alert('You won! \n Check if you reached the top of the leaderboard.');
        await setPlayerScore(playerName, co2_consumed, distance);
    }
    
}

async function setPlayerScore(name, co2, distance){
    const response = await fetch(`http://127.0.0.1:3000/player/setScore/${name}/${co2}/${distance}`);
    const result = await response.json();

    return result;
}

async function getQuestions(){
    const response = await fetch(`http://127.0.0.1:3000/questions`);
    const questions = await response.json();

    return questions;
}

async function showQuestion() {
    
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