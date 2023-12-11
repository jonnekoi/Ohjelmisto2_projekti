'use strict';

// CREATE MAP USING LEAFLET & OPENSTREETMAP
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

const nameInput = document.querySelector('#nameInput');
const nameForm = document.querySelector('#nameForm');

const questionModal = document.querySelector("#questionModal");

const animationDiv = document.getElementById("correctAnswerAnimation");
const answerElement = document.querySelector('.correct-co2');

const infoButton = document.querySelector('.info-button');
infoButton.addEventListener('click', () => {
    rulesPopup.style.display = 'block';
});

const rulesPopup = document.querySelector('.rules-popup');
function closeRulesPopup() {
  rulesPopup.style.display = 'none';
}


document.addEventListener('DOMContentLoaded', async (e) => {
    //  HANDLE SUBMIT AND START THE GAME
    nameForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        handleFormSubmission();

        // ASSIGN QUESTIONS
        questions = await getQuestions();

        // GET STARTING CONTINENT & SET NEW AIPPORT ACCORDING TO IT
        const continent = document.querySelector('#startContinent').value; 
        const current_airport =  await setStartingAirport(continent);

        await getCurrentAirportWeather(current_airport);
        await getClosestAirports(current_airport);
        showQuestion();
        
        // SHOW RULES AT THE START OF THE GAME
        rulesPopup.style.display = 'block';
    });

    

    // GET LEADERBOARD DATA & CREATE THE HTML OF IT
    const leaderboardData = await getScoreboard();
    leaderboardData.forEach((item, index) => {
        const row = `<tr>
                        <td>${index + 1}</td>
                        <td>${item.player}</td>
                        <td>${item.co2_emissions}</td> 
                     </tr>`;
        leaderboardBody.innerHTML += row;
    }); 
});


function handleFormSubmission() {
    // SET PLAYER NAME
    playerName = nameInput.value;
    
    // MAKE ELEMENTS CLICKEABLE
    const elements = document.querySelectorAll('*');
    for(const element of elements) {
        if (element.id !== 'game-title') {
            element.style.pointerEvents = 'auto';
        }
    }

    // Fade out animation
    nameForm.style.transition = 'opacity 1s';
    nameForm.style.opacity = 0;

    // Hide the form after submission
    setTimeout(function () {
        nameForm.style.display = 'none';
    }, 1000);
}


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

async function setStartingAirport(continent) {
    let icao;

    const africa = ['FAOR', 'HECA', 'FACT', 'HKJK', 'GMMN'];
    const europe = ['EGLL', 'LFPG', 'EDDF', 'EHAM', 'LEMD'];
    const asia = ['ZBAA', 'RJTT', 'OMDB', 'VHHH', 'VTBS'];
    const oceania =  ['YSSY', 'NZAA', 'YBBN', 'YMML', 'PHNL'];
    const northAmerica = ['KATL', 'KLAX', 'KORD', 'KDFW', 'KDEN'];
    const southAmerica =  ['SBGR', 'SAEZ', 'SBGL', 'SKBO', 'SCEL'];

    switch (continent) {
        case 'af':
            icao = africa[Math.floor(Math.random() * africa.length)];
            break;
        case 'eu': 
            icao = europe[Math.floor(Math.random() * europe.length)];
            break;
        case 'as': 
            icao = asia[Math.floor(Math.random() * asia.length)];
            break;
        case 'oc': 
            icao = oceania[Math.floor(Math.random() * oceania.length)];    
            break;
        case 'na': 
            icao = northAmerica[Math.floor(Math.random() * northAmerica.length)];
            break;    
        case 'sa': 
            icao = southAmerica[Math.floor(Math.random() * southAmerica.length)];
            break;   
        default:
            break;
    }

    // CLEAR ALL MARKERS ON MAP
    airportMarkers.clearLayers();

    // GET CURRENT AIRPORT DATA
    const response = await fetch('http://127.0.0.1:3000/airport/' + icao);
    const airport = await response.json();

    // CREATE MARKER ON THE USING THE DATA
    const marker = L.marker([airport.latitude_deg, airport.longitude_deg], {'icon': startingPointIcon}).
        addTo(map).
        bindPopup(airport.name).
        openPopup();
    airportMarkers.addLayer(marker);

    // PAN MAP TO SELECTED AIRPORT
    map.flyTo([airport.latitude_deg, airport.longitude_deg]);

    return airport;
}

async function getClosestAirports(current_airport){
    // GET 10 CLOSEST AIRPORTS ACCORDING TO THE CURRENT AIRPORT
    const lat = current_airport.latitude_deg;
    const lon = current_airport.longitude_deg;
    const response = await fetch(`http://127.0.0.1:3000/airport/closest/${lat}/${lon}`);
    const airports = await response.json();


    for (const airport of airports) {
        // BECAUSE THE CURRENT AIRPORT WILL BE IN THE DATA, WE DONT WANT TO CALCULATE METRICS & CREATE A MARKER FOR IT.
        if (current_airport.name !== airport.name){
            const co2_emissions = calculateCO2(airport.Distance_KM);

            // THE DATABASE QUERY RETURN THE DISTANCE TO THE AIRPORT ASWELL
            const distance = Math.floor(airport.Distance_KM);

            // CREATE THE MARKERS FOR CLOSEST AIRPORTS WITH HTML IN THE POPUP
            const marker = L.marker([airport.latitude_deg, airport.longitude_deg])
                .addTo(map)
                .bindPopup(`
                            <div id="travelPopup">
                                <h3>${airport.name}</h3>
                                <a class="airport-btn" data-airport-name="${airport.name}">Travel to airport</a>                            
                                <p>Distance: ${distance}KM</p>
                                <p>CO2 consumption: ${co2_emissions}KG</p>
                                <div class="dropdown-confirm">
                                    <div class="confirm-content">
                                        <p>Confirm travel?</p>
                                        <button class="confirm-btn">✔</button>
                                        <button class="cancel-btn">✖</button>
                                    </div>
                                </div>
                            </div>
                            `);
            
            // FANCY WAY OF HANDLING THE CLICK OF THE "TRAVEL TO AIRPORT" BUTTON
            marker.on('popupopen', function (event) {
                setTimeout(() => { // Timeout to ensure the popup's DOM is ready
                    document.querySelectorAll('.airport-btn').forEach(button => {
                        button.addEventListener('click', function () {
                            document.querySelector('.dropdown-confirm').style.display = 'block';
                        });
                        
                        document.querySelector('.confirm-btn').addEventListener('click', function() {
                            // Handle confirm action
                            marker.closePopup();

                            // document.querySelector('.dropdown-confirm').style.display = 'none';
                            travelToAirport(airport, co2_emissions, distance, true);
                        });

                        document.querySelector('.cancel-btn').addEventListener('click', function() {
                            // Handle cancel action
                            // document.querySelector('.dropdown-confirm').style.display = 'none';
                            marker.closePopup();
                        }); 

                    });
                }, 1);
            });
            airportMarkers.addLayer(marker);
        }
    }
    return airports;
}   

async function travelToAirport(airport, co2_emissions, dist, conf){

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

// THIS IS KIND OF UGLY [TOO MUCH NESTING: MAYBE MAKE A SEPARATE FUNCTION FOR WHEN THE ANSWER STREAK IS "HIT" OR PROBABLY COULD PASS THE MSG, COLOR OF THE BG ]
async function checkAnswer(e){   
    console.log('check answer', e.innerText);
    console.log('check answer correct', correctAnswer);
    
    if (e.innerText.toUpperCase() == correctAnswer.toUpperCase()) {
        
        totalCorrectAnswers += 1;
        answerStreak += 1;
        Math.floor(points += 50);
        
        questionModal.style.display = 'none';
        pointsElement.innerHTML = points;
        streakElement.innerText = answerStreak;
       
        // EVERY 3 CORRECT ANSWERS REDUCE CO2 BY 20%
        if (answerStreak % 3 === 0) {
            const text = `Your CO2 was reduced by 20%. \n Current consumption ${Math.floor(co2_consumed)}KG`;
            showAnswerResult(text, 8);
            animationDiv.style.backgroundColor = 'rgba(144, 238, 144, 0.7)';

            co2_consumed *= .8; 
            
        } else {
            const text = 'Correct answer. \n +50 points.';
            showAnswerResult(text, 6);
            animationDiv.style.backgroundColor = 'rgba(144, 238, 144, 0.7)';
        }   
    } else {
        const text = 'Wrong answer. \n Points reduced by 10%.';
        showAnswerResult(text, 6);

        // REDUCE POINTS BY 10% AND RESET THE ANSWER STREAK
        points *= .9;
        answerStreak = 0;  
        streakElement.innerText = answerStreak;
    } 


    if (points >= 1000) {
        await fetch(`http://127.0.0.1:3000/player/setScore/${playerName}/${co2_consumed}/${distance}`);
        alert('You won! \n Check if you reached the top of the leaderboard.');
    }
}

function showAnswerResult(text, time) {
    questionModal.style.display = 'none';

    answerElement.innerText = text;
    animationDiv.style.backgroundColor = 'rgba(255, 72, 0, 0.7)';

    animationDiv.style.display = 'block';
    animationDiv.style.opacity = 1;
    animationDiv.style.animation = `fadeInOut ${time}s ease-in-out`;

        setTimeout(() => {
            animationDiv.style.opacity = 0;
            animationDiv.style.animation = 'none';
            animationDiv.style.display = 'none';
        }, 6000);
}

async function getQuestions(){
    const response = await fetch(`http://127.0.0.1:3000/questions`);
    const questions = await response.json();

    return questions;
}

async function showQuestion() {
    
    // SELECT A RANDOM QUESTION FROM THE QUESTIONS ARRAY
    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];

    // SET THE CORRECT ANSWER TO VARIABLE TO BE USED LATER TO CHECK THAT THE ANSWER IS CORRECT
    correctAnswer = randomQuestion.answer;

    console.log(correctAnswer);

    // SET QUESTIONS TEXT
    document.getElementById("questionText").innerText = randomQuestion.question_text;
    // ASSIGN ANWERS TO ARRAY & RANDOMIZE THE 
    const answers = [randomQuestion.wrong_answer, randomQuestion.answer, randomQuestion.wrong_answer2].filter(a => a);

    // GET 3 ANSWER BUTTON ELEMENTS FROM DOM THEN LOOP THROUGH THEM AND ASSIGN THE TEXT AS ANSWER 
    const answerButtons = document.getElementsByClassName("answer");
    answers.forEach((answer, index) => {
        answerButtons[index].innerText = answer;
    });
    
    // FINALLY SHOW THE MODAL/POPUP FOR THE QUESTION
    questionModal.style.display = "block";
}

