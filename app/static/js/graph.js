
// scores per week 
// list of students not doing it
// general understanding of who is doing what and the scores recorded

// average score over time
// score per question
// single student's score over time
// download excel sheet.

// begin with single student's score over time.
const xValues = ["1", "2", "3", "4", "5"];
const yValues = [15, 24, 37, 54, 51];

new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: "rgba(210,50,210,0.3)",
      data: yValues
    }]
  },
});