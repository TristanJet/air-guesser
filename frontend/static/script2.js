let target = document.getElementById("target")

async function initeval(){
	target.innerHTML = ""

	const resp = await fetch("/api/leaderboard");
	if (!resp.ok) {
		error();
		return;
	}
	const json = await resp.json();
	const lbarr = json.sortedLb;
	if (lbarr == null) {
		error();
		return;
	}
	
	if (lbarr.length == 0){
		console.log("heading into empty")
		empty()
	} else {
		console.log("heading into ranking")
		rankemup(lbarr)
	}
}

function error() {
	console.log("Error fetching leaderboard")
	empty()
}

function rankemup(lbarr){	
	for (i = 0; i < lbarr.length; i++){
		let main = document.createElement("tr")
		
		let rank = document.createElement("td")
		rank.setAttribute("height", "60")
		rank.setAttribute("class", "player-name")
		rank.innerHTML = "#" + (i + 1)
		
		let name = document.createElement("td")
		name.setAttribute("height", "60")
		name.setAttribute("class", "player-name")
		name.innerHTML = lbarr[i]["name"]
		
		let score = document.createElement("td")
		score.setAttribute("height", "60")
		score.setAttribute("class", "score-name")
		score.innerHTML = lbarr[i]["score"]
		
		main.appendChild(rank)
		main.appendChild(name)
		main.appendChild(score)
		
		target.appendChild(main)
	}
}

function empty(){
		let emptymain = document.createElement("tr")
		
		let state = document.createElement("td")
		state.setAttribute("colspan", "5")
		state.setAttribute("height", "100")
		state.setAttribute("class", "empty-state")
		
		let msg = document.createElement("div")
		msg.setAttribute("class", "empty-message")
		
		let icon = document.createElement("div")
		icon.setAttribute("class", "empty-icon")
		icon.innerHTML = "🎮"
		
		let text1 = document.createElement("p")
		text1.innerHTML = "No scores yet!"
		
		let text2 = document.createElement("p")
		text2.setAttribute("class", "empty-subtitle")
		text2.innerHTML = "Be the first to play and make it to the leaderboard!"
		
		msg.appendChild(icon)
		msg.appendChild(text1)
		msg.appendChild(text2)
		
		state.appendChild(msg)
		
		target.appendChild(state)
}

initeval()
