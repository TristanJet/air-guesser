function addMarkers(locations) {
        const gameLayer = d3.select('.game-layer');

        // // Clear any old markers
        // gameLayer.selectAll('.poi-market').remove();

        // Draw markets
         gameLayer.selectAll('.poi-market')
            .classed('previous-round', true)  // Add a class for styling
            .style('fill', '#4e738bff')         // Lighter red
            .style('opacity', 0.5)            // Semi-transparent
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
            .style('stroke-dasharray', '5,5')  // Dashed line
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
            //console.log(d3.select('#map').selectAll('*').remove())

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
                .scaleExtent([1, 10]) // Limit zoom: 1x to 8x
                .translateExtent([[0, 0], [width, height]]) // Limit panning to map edges
                .on('zoom', function(event) {
                    // Apply move + scale to the g
                    g.attr('transform', event.transform);

                    // Keep country borders thin
                    g.selectAll('.country').style('stroke-width', 1 / event.transform + 'px');

                    // Keep markers to stay small
                    g.selectAll('.poi-market').attr('r', 6 / event.transform.k)
                });
            // Attach Zoom to svg
            svg.call(zoom);

            // Connect Zoom buttons
            // Zoom In
            d3.select('#zoom_in').on('click', function() {
                svg.transition().duration(750).call(zoom.scaleBy, 1.3);
            });

            // Zoom Out
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
                    // Convert TopoJSON to GeoJSON
                    const countriesData = topojson.feature(data, data.objects.countries);

                    // Create a group for each country (individual SVG element)
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
                    //console.log(`Using projection ${projection}`)
                })
        }

        // Initialize map
        createMap(projection)
        console.log('=== World Map SVG Structure ===');


        let q = 0;
        let gameData = [];

        document.addEventListener('DOMContentLoaded', () => {
            d3.json('/api/airports').then(data => {
                gameData = data.map(innerArray => innerArray[0]);
                console.log("Game Data Fixed:", gameData);

                // Show the dots for the FIRST round
                renderRound(0);
            });
            const form = document.querySelector('#game-form');
            form.addEventListener('submit', handleGuessSubmit);
        
        });
        
        function renderRound(index) {
            if (!gameData || index >= gameData.length) {
                console.log("Game Over or No Data");
                return;                                 //TODO return game.fin
            }
          
            const round = gameData[index];
            const ap1 = document.querySelector("#airport1")
            const ap2 = document.querySelector("#airport2")
            ap1.textContent = round.point1.ap1_name
            ap2.textContent = round.point2.ap2_name


            // Format data for your D3 function
            const formattedMarkets = [
                {
                    lat: round.point1.ap1_lat,
                    lon: round.point1.ap1_long,
                    name: round.point1.ap1_name
                },
                {
                    lat: round.point2.ap2_lat,
                    lon: round.point2.ap2_long,
                    name: round.point2.ap2_name
                }
            ];

            addMarkers(formattedMarkets)
        }

        function handleGuessSubmit(e) {
            e.preventDefault();
            const inputField = document.querySelector("#distanceInput");
            const userGuess = parseInt(inputField.value)

            // JSON
            const payload = {
                guess: userGuess
            };

            // Send to Backend
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
                if (data.finished) {
                    alert("Game Over! Your total score is: " + data.total_score); // You might need to send score back
                    window.location.replace("leaderboard.html"); // or wherever the end screen is
                    return;
                }

                q += 1;
                renderRound(q); // Draw next dots

                inputField.value = '';
            })
            .catch(error => console.error('Error:', error));
        }
      