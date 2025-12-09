function addMarkers(locations) {
    const gameLayer = d3.select('.game-layer');

    // Mark previous round markers
    gameLayer.selectAll('.poi-market')
        .classed('previous-round', true)
        .style('fill', '#4e738bff')
        .style('opacity', 0.5)
        .attr('r', 4); 

    // Draw a line connecting the two airports
    if (locations.length === 2) {
        const [point1, point2] = locations;
        const [x1, y1] = projection([point1.lon, point1.lat]);
        const [x2, y2] = projection([point2.lon, point2.lat]);
    
        gameLayer.append('line')
            .attr('class', 'airport-connection')
            .attr('x1', x1)
            .attr('y1', y1)
            .attr('x2', x2)
            .attr('y2', y2)
            .style('stroke', '#005D9B')
            .style('stroke-width', 2)
            .style('stroke-dasharray', '5,5')
            .style('opacity', 0.6);
    }

    locations.forEach(loc => {
        gameLayer.append('circle')
            .attr('class', 'poi-market current-round')
            .attr('cx', projection([loc.lon, loc.lat])[0])
            .attr('cy', projection([loc.lon, loc.lat])[1])
            .attr('r', 6)
            .style('fill', '#c91515ff')
            .style('stroke', 'white')
            .style('stroke-width', 2);
    });
}

const width = 1000;
const height = 750;
console.log('line 71')

// Projection configuration
const projection = d3.geoMercator()
    .scale(150)
    .translate([width / 2, height / 1.7]);

let svg, path, countries;

function createMap(projection) {
    // Clear existing map
    d3.select('#map').selectAll('*').remove();

    // Create SVG
    svg = d3.select('#map')
        .append('svg')
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr('width', width)
        .attr('height', height);

    // Group for zooming
    const g = svg.append('g');

    const mapLayer = g.append('g').attr('class', 'map-layer');
    const gameLayer = g.append('g').attr('class', 'game-layer');

    // Define zoom behavior
    const zoom = d3.zoom()
        .scaleExtent([1, 10])
        .translateExtent([[0, 0], [width, height]])
        .on('zoom', function(event) {
            g.attr('transform', event.transform);
            g.selectAll('.country').style('stroke-width', 1 / event.transform + 'px');
            g.selectAll('.poi-market').attr('r', 6 / event.transform.k)
        });
    
    svg.call(zoom);

    // Zoom buttons
    d3.select('#zoom_in').on('click', function() {
        svg.transition().duration(750).call(zoom.scaleBy, 1.3);
    });

    d3.select('#zoom_out').on('click', function() {
        svg.transition().duration(750).call(zoom.scaleBy, 1 / 1.3)
    });

    // Path generator
    path = d3.geoPath().projection(projection);

    // Tooltip
    const tooltip = d3.select('#tooltip');

    // Load and render world data
    d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
        .then(data => {
            const countriesData = topojson.feature(data, data.objects.countries);

            countries = mapLayer.selectAll('.country')
                .data(countriesData.features)
                .enter()
                .append('path')
                .attr('class', 'country')
                .attr('d', path)
                .attr('data-country-id', d => d.id)
                .attr('data-country-name', d => d.properties.name)
                .on('mouseover', function(event, d) {
                    tooltip
                        .style('opacity', 1)
                        .html(`<strong>${d.properties.name}</strong>`)
                        .style('left', (event.pageX + 10) + 'px')
                        .style('top', (event.pageY - 10) + 'px');
                })
                .on('mousemove', function(event) {
                    tooltip
                        .style('left', (event.pageX + 10) + 'px')
                        .style('top', (event.pageY - 10) + 'px');
                })
                .on('mouseout', function() {
                    tooltip.style('opacity', 0);
                });

            console.log(`Rendered ${countriesData.features.length} individual country SVG paths`);
        })
}

// Initialize map
createMap(projection)
console.log('=== World Map SVG Structure ===');

let q = 0;
let gameData = [];

document.addEventListener('DOMContentLoaded', () => {
    d3.json('/api/newgame').then(data => {
        // The new API structure returns the data directly
        gameData = data;
        console.log("Game Data:", gameData);

        // Show the dots for the FIRST round
        renderRound(0);
    });
    
    const form = document.querySelector('#game-form');
    form.addEventListener('submit', handleGuessSubmit);
});

function renderRound(index) {
    if (!gameData || index >= gameData.length) {
        console.log("Game Over or No Data");
        window.location.href = '/leaderboard'; 
        return;
    }
  
    const round = gameData[index];
    const ap1 = document.querySelector("#airport1");
    const ap2 = document.querySelector("#airport2");
    
    // Access airports array with new structure
    ap1.textContent = round.airports[0].name;
    ap2.textContent = round.airports[1].name;

    // Format data for D3 function with new property names
    const formattedMarkets = [
        {
            lat: round.airports[0].lat,
            lon: round.airports[0].long,
            name: round.airports[0].name
        },
        {
            lat: round.airports[1].lat,
            lon: round.airports[1].long,
            name: round.airports[1].name
        }
    ];

    addMarkers(formattedMarkets);
}

function handleGuessSubmit(e) {
    e.preventDefault();
    const inputField = document.querySelector("#distanceInput");
    const userGuess = parseInt(inputField.value);

    const payload = {
        guess: userGuess
    };

    fetch('/api/distance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    })
    .then(data => {
        console.log("Server Response:", data);
        
        // Show results with blur effect and wait for user click
        showResults(userGuess, data);
        if (data.finished) {
            window.location.replace("/leaderboard");
            return;
        }
        q += 1;
        renderRound(q);
        inputField.value = '';

        
    
    })
    .catch(error => console.error('Error:', error));
}

function showResults(userGuess, data, inputField){
    const round = document.querySelector("#round")
    const score = document.querySelector("#score")
    const map = document.querySelector("#map");
    const tip_section = document.createElement("div")
    const tip_icon = document.createElement("div")
    const tip_text = document.createElement("p")
    const answer_section = document.querySelector(".answer-section")
    // Blur map
    map.classList.add("blurred")

    //tip

    // Overlay
    const overlay = document.createElement("div")
    overlay.className = "results-overlay";
    overlay.innerHTML = `
        <h3>Round ${q + 1} Results</h3>
        <p><strong>Your Guess:</strong> ${userGuess} km</p>
        <p><strong>Actual Distance:</strong> ${data["actual-distance"]} km</p>
        <p><strong>Difference:</strong> ${data["guess-diff"]} km</p>
        <p><strong>Total Score:</strong> ${data["total-diff"]} km</p>
    `;
    document.body.appendChild(overlay);
    answer_section.appendChild(tip_section);

    tip_section.appendChild(tip_icon);
    tip_section.appendChild(tip_text);
    tip_section.id = "tip-section";
    tip_icon.classList.add("tip-icon");
    tip_text.id = "tip-text"
    tip_text.innerText = "Click to continue"
    tip_section.classList.add("show")

    round.innerHTML = `${q + 1}`
    score.innerHTML = `${data["total-diff"]}`

    // Add click to handle overlay
    document.addEventListener("click", () => {
        map.classList.remove("blurred");
        overlay.remove();
        tip_section.remove();

        
    });
}



const round = document.querySelector("#round")
const score = document.querySelector("#score")