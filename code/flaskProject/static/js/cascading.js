var subjectObject = {
  "Singapore Polytechnic": {
    "School of Applied Sciences": [],
    "School of Bulit Environment": [],
    "School of Business Management": [],
      "School of Engineering": [],
      "School of Health Sciences": [],
      "School of Information & Digital Technologies": [],
      "School of Maritime Studies": [],
      "School of Media & Design": []
  },
  "Nanyang Polytechnic": {
    "School Of Applied Science": [],
    "School Of Business Management": [],
     "School Of Design & Media": [],
      "School Of Engineering": [],
      "School Of Health & Social Sciences": [],
      "School Of Information Technology": []
  },
  "Ngee Ann Polytechnic": {
    "School of Business & Accountancy": [],
    "School of Design & Environment": [],
      "School of Engineering": [],
      "School of Film & Media Studies": [],
      "School of Health Sciences": [],
      "School of Humanities & Social Sciences": [],
      "School of InfoComm Technology": [],
      "School of Life Sciences & Chemical Technology": []
  },
  "Republic Polytechnic": {
    "School of Applied Science": [],
    "School of Engineering": [],
    "School of Hospitality": [],
    "School of Infocomm": [],
    "School of Sports Health and Leisure": [],
    "School of Management and Communication": [],
    "School of Technology for the Arts": []
  },

  "Temasek Polytechnic": {
    "School of Applied Science": [],
    "School of Business": [],
    "School of Engineering": [],
    "School of Humanities & Social Sciences": [],
    "School of Informatics & IT": [],
    "School of Design": []
  }
}
window.onload = function() {
  var subjectSel = document.getElementById("poly");
  var topicSel = document.getElementById("school");

  for (var x in subjectObject) {
    subjectSel.options[subjectSel.options.length] = new Option(x,x);
  }
  subjectSel.onchange = function() {
  //empty Chapters- and Topics- dropdowns
  topicSel.length = 1;
    //display correct values
    for (var y in subjectObject[this.value]) {
      topicSel.options[topicSel.options.length] = new Option(y, y);
    }
  }

}