var fs = require("fs");

class Parser{
	constructor(filePath){
		this.filePath = filePath;
		fs.readFile(filePath,
					"utf8",
					(err, contents) => {if(err){console.log(err);return;} this.file = contents; this.fileLoaded()});
	}
	fileLoaded(){
		//console.log(this.file);
		this.finalObj = {};
		this.finalObj.title = this.getTitle();
		this.finalObj.season = this.getSeason();
		this.finalObj.episode = this.getEpisode();
		this.finalObj.date = this.getDate();
		this.finalObj.authors = this.getAuthors();
		this.finalObj.directors = this.getDirectors();
		this.finalObj.info = this.getInfo();
		this.finalObj.plot = this.getPlot();
		this.finalObj.summary = this.getSummary();
		this.finalObj.firsts = this.getFirsts();
		this.finalObj.deaths = this.getDeaths();
		this.finalObj.cast = this.getCast();
		this.finalObj.castNotes = this.getCastNotes();

		// console.log(this.finalObj)
		this.finalizeJSON()
	}

	getTitle(){
		return /"(.*?)"/.exec(this.file)[1];
	}

	getSeason(){
		return /Season (.*?)\nEpisode/.exec(this.file)[1];
	}

	getEpisode(){
		return /Episode (.*?)\n/.exec(this.file)[1];
	}

	getDate(){
		let string = /Air date\n(.*?)\n/.exec(this.file)[1];
		let data = new Date(string);
		return data.toDateString();
	}

	getAuthors(){
		let authors = /Written by\n(.*?)\n/.exec(this.file)[1].split(/[,&]/);
		for(let i = 0; i < authors.length; i++) {
			authors[i] = this.removeBorderSpaces(authors[i]);
		}
		return authors;
	}

	getDirectors(){
		return /Directed by\n(.*?)\n/.exec(this.file)[1].split(/[,&]/);
	}

	getInfo(){
		return /\n(.*?)\n\nContents/.exec(this.file)[1];
	}

	getPlot(){
		return this.removeBorderSpaces(/PlotEdit\n(.*?)\n/.exec(this.file)[1]);
	}

	getSummary(){
		let startPos = /SummaryEdit\n/.exec(this.file).index + "SummaryEdit\n".length;
		let endPos = /RecapEdit\n/.exec(this.file);
		endPos = (endPos)? endPos.index - 1: /AppearancesEdit\n/.exec(this.file).index - 1;
		let summary = this.file.substring(startPos, endPos);
		let edits = [];//summary.match(/(.*?)Edit/g);
		let scenes = [];
		let match;
		let lengths = [];
		let re = /(.*?)Edit/g;
		while ((match = re.exec(summary)) != null) {
			scenes.push({location: this.removeBorderSpaces(match[1])});
		    edits.push(match.index + match[0].length);
		    lengths.push(match[0].length);
		}

		for (var i = 0; i < edits.length - 1; i++) {
			let sub = this.removeBorderSpaces(summary.substring(edits[i], edits[i+1] - lengths[i+1] + 1));
			scenes[i].content = sub;
		}

		let sub = this.removeBorderSpaces(summary.substring(edits[i], summary.length));
		scenes[i].content = sub;

		// console.log(edits, scenes);
		return scenes;
	}

	getFirsts(){
		let startPos = /(FirstEdit|First AppearancesEdit)\n/.exec(this.file).index + "FirstEdit\n".length;
		let endPos = /(DeathsEdit|CastEdit|ProductionEdit)\n/.exec(this.file).index;
		let sub = this.removeBorderSpaces(this.file.substring(startPos, endPos));
		let firsts = sub.split("\n");
		let final = [];
		for (let i = 0; i < firsts.length; i++) {
			let temp = this.removeBorderSpaces(firsts[i]);
			if(temp == ""){
				continue;
			}
			final.push(temp);
		}
		return final;
	}
	
	getDeaths(){
		let possibleMatch = /DeathsEdit\n/.exec(this.file);
		if(possibleMatch == undefined){
			return [];
		}
		let startPos = possibleMatch.index + "DeathsEdit\n".length;
		let endPos = /(ProductionEdit|CastEdit)\n/.exec(this.file).index;
		let sub = this.removeBorderSpaces(this.file.substring(startPos, endPos));
		let deaths = sub.split("\n");
		let final = [];
		for (let i = 0; i < deaths.length; i++) {
			let temp = this.removeBorderSpaces(deaths[i]);
			if(temp == ""){
				continue;
			}
			final.push(temp);
		}
		return final;
	}

	getCast(){
		let startPos = /Starring\n/.exec(this.file).index + "Starring\n".length;
		let endPos = /(Also [sS]tarring|Guest)/.exec(this.file).index;
		let sub = this.removeBorderSpaces(this.file.substring(startPos, endPos));
		let cast = sub.split("\n");
		let formattedCast = [];
		for (let i = 0; i < cast.length; i++) {
			cast[i] = this.removeBorderSpaces(cast[i]);
			let tempCast = cast[i].split(" as ");
			tempCast[0] = tempCast[0].replace("and", "");
			tempCast[1] = tempCast[1].replace("(credit only)", "");
			formattedCast.push({actor: this.removeBorderSpaces(tempCast[0]), character: this.removeBorderSpaces(tempCast[1])});
		}

		let possibleMatch = /Also [sS]tarring\n/.exec(this.file);
		if(possibleMatch != undefined){
			startPos = possibleMatch.index + "Also starring\n".length;
			endPos = /Guest/.exec(this.file).index;
			sub = this.removeBorderSpaces(this.file.substring(startPos, endPos));
			cast = sub.split("\n");
			for (let i = 0; i < cast.length; i++) {
				cast[i] = this.removeBorderSpaces(cast[i]);
				let tempCast = cast[i].split(" as ");
				tempCast[0] = tempCast[0].replace("and", "");
				formattedCast.push({actor: this.removeBorderSpaces(tempCast[0]), character: this.removeBorderSpaces(tempCast[1])});
			}	
		}

		startPos = /Guest starring\n/.exec(this.file).index + "Guest starring\n".length;
		let possibleEndPos = /(Stunt|Uncredited)/.exec(this.file);
		endPos = (possibleEndPos == undefined)? /Cast notesEdit/.exec(this.file).index : possibleEndPos.index;
		sub = this.removeBorderSpaces(this.file.substring(startPos, endPos));
		cast = sub.split("\n");
		for (let i = 0; i < cast.length; i++) {
			cast[i] = this.removeBorderSpaces(cast[i]);
			let tempCast = cast[i].split(" as ");
			tempCast[0] = tempCast[0].replace("and", "");
			tempCast[1] = tempCast[1].replace("(credit only)", "");
			formattedCast.push({actor: this.removeBorderSpaces(tempCast[0]), character: this.removeBorderSpaces(tempCast[1])});
		}

		if(possibleEndPos == undefined){
			return formattedCast;
		}
		startPos = /Uncredited\n/.exec(this.file).index + "Uncredited\n".length;
		endPos = /Cast [nN]otesEdit/.exec(this.file).index;
		sub = this.removeBorderSpaces(this.file.substring(startPos, endPos));
		cast = sub.split("\n");
		for (let i = 0; i < cast.length; i++) {
			cast[i] = this.removeBorderSpaces(cast[i]);
			let tempCast = cast[i].split(" as ");
			tempCast[0] = tempCast[0].replace("and", "");			
			tempCast[1] = tempCast[1].replace("(credit only)", "");
			formattedCast.push({actor: this.removeBorderSpaces(tempCast[0]), character: this.removeBorderSpaces(tempCast[1])});
		}

		return formattedCast;
	}

	getCastNotes(){
		//To be done...
	}

	removeBorderSpaces(string){
		return string.replace(/^([ \n\t]*)/, "").replace(/([ \n\t]*)$/, "");
	}

	finalizeJSON(){
		console.log(JSON.stringify(this.finalObj));
	}
}

let obj = new Parser("../episodes/season_2/valar_morghulis.txt");