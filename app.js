'use-strict'

var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = window.innerWidth - margin.left - margin.right,
    height = window.innerHeight - margin.top - margin.bottom;

var MIN_RETWEETS = 25

var users = ["realDonaldTrump",
            "BernieSanders",
            "BarackObama",
            "HillaryClinton",
            //"ChelseaClinton",
            "GovMikeHuckabee",
            "dril",
            "SpeakerRyan",
            //"neiltyson"
    ]

var colors = ["rgb(233,77,60)", "rgb(70,162,108)", "rgb(78,166,220)", "rgb(92,47,142)", "rgb(230, 126, 34)", "rgb(165,15,169)", "rgb(41,77,70)", "rgb(209,121,248)"]

var appState = {
   selectedUsers: [0],
   showTweets: true,
   showAllUsers: false,
   currentData: null,
}


var profilePhotos = { 
    'realDonaldTrump': 'https://pbs.twimg.com/profile_images/1980294624/DJT_Headshot_V2_normal.jpg',
    'BarackObama': 'http://pbs.twimg.com/profile_images/822253020012511233/C0HXLxod_normal.jpg',
    'HillaryClinton': 'http://pbs.twimg.com/profile_images/839938827837976576/leN1zJJx_normal.jpg',
    'GovMikeHuckabee': 'http://pbs.twimg.com/profile_images/797086726929817601/rwcW70Sn_normal.jpg',
    'neiltyson': 'http://pbs.twimg.com/profile_images/74188698/NeilTysonOriginsA-Crop_normal.jpg',
    'dril': 'http://pbs.twimg.com/profile_images/847818629840228354/VXyQHfn0_normal.jpg',
    'SpeakerRyan': 'http://pbs.twimg.com/profile_images/816642042000535552/dU_6-LFL_normal.jpg',
    'BernieSanders': 'http://pbs.twimg.com/profile_images/794596124686487552/kqpbolIc_normal.jpg',
    'ChelseaClinton': 'http://pbs.twimg.com/profile_images/614488068905652224/2tUcF22u_normal.jpg',


}

// parse the date / time
var parseTime = d3.timeParse("%d-%m-%Y");
var timeDisplay = d3.timeFormat('%I:%M %p %e %b %Y');

var beginDate = parseTime('01-05-2014')

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

var colorScale = d3.scaleOrdinal(colors)
// define the line
var valueline = d3.line()
    //.curve(d3.curveCardinal)
    .x(function(d) { return x(parseTime(d.key)); })
    .y(function(d) { return y(d.value); })

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("#vis").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
var container = svg.append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

var callout = d3.select('.callout'),
    calloutImage = callout.select('img')
    calloutText = callout.select('.text')
    calloutTime = callout.select('.time')
    calloutRetweet = callout.select('.retweet')
    calloutReply = callout.select('.reply')
    calloutTrash = callout.select('.trash')

var selector = d3.select('#controls select')
   
  var allPaths = container.selectAll('.avg-path').data(users)

  allPaths.enter()
    .append('path')
    .attr('class',function(d, i) { return 'avg-path path-'+d })
    .attr('stroke', function(d, i) { return colorScale(i) })
/*
var path = svg.append("path")
        .attr("class", "line")
*/
 container.append("text")
      .attr("transform", "rotate(-90)")
      .classed('ylabel', true)
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("replies per retweet");

var voronoiGroup = container.append('g')
    .classed('voronoi', true)

var voronoi = d3.voronoi()
    .x(function(d) { return x(d.date)})
    .y(function(d) { return  y(d.trashiness)})
    //.limit(50)
    .extent([[0, 0], [width, height]]);

//loadData(0)
showLegends()
loadAllData()

function showLegends() {
  var legends = d3.select('#legend').selectAll('.legend').data(users)
  legends.enter().append('span')
  .attr('class', 'legend')
  .style('color',function(d, i) { return colorScale(i) }) 
  .text(function(d)  { return d; })
  .on('click', function(d) {
    var selectedUsers = appState.selectedUsers
    var userIndex = users.indexOf(d)
    var indexIsSelected = selectedUsers.indexOf(userIndex)
    if(indexIsSelected < 0) {
      selectedUsers.push(userIndex) 
    }
    else if(selectedUsers.length > 1) {
      selectedUsers.splice(indexIsSelected, 1)
    }
    appState = Object.assign({}, appState, {selectedUsers: selectedUsers})
    showLegends()
    renderChart() 
  }) 
  .append('span')
    .style('background-color',function(d, i) { 
      return appState.selectedUsers.indexOf(i) > -1 ? colorScale(i) : '#FFF'
    })
    .text(function(d, i) { return appState.selectedUsers.indexOf(i) > -1 ? '\u2713' : '' })
    .style('color',function(d, i) { return '#FFF' })
    .style('border-color',function(d, i) { return colorScale(i) })
  
  legends.selectAll('span') 
    .style('background-color',function(d) { var i = users.indexOf(d);  return appState.selectedUsers.indexOf(i) > -1 ? colorScale(i) : '#FFF'}) 
    .text(function(d, i) { return appState.selectedUsers.indexOf(i) > -1 ? '\u2713' : '' })
}
/*
function loadData(index) {
  var dataFile = 'data/'+users[index]+'.json'
  // Get the data
  d3.json(dataFile, function(error, data) {
    if (error) throw error;
    data = Object.values(data)
    console.log(data)

    data = data.filter(d => d.retweet_count > MIN_RETWEETS)
    // format the data
    data.forEach(function(d) {
        d.date = new Date(d.created_at);//parseTime(d.created_at);
        d.trashiness = d.retweet_count ? d.reply_count/d.retweet_count : 0;
    });

    data = data.filter(d => !isNaN(d.trashiness) && d.date > beginDate)

    appState = Object.assign({}, appState, {currentData: data})

    renderChart(data, index)
  });
}
*/
//loadAllData()
function loadAllData() {
  var q = d3.queue()
  users.forEach(function(user) {
    q.defer(d3.json, 'data/'+user+'.json')
  })
  q.awaitAll(function(errors, values) {
    console.log(values)
    values = values.map(function(d) { 
    
      var data = Object.values(d) 
      data = data.filter(function(d) { return d.retweet_count > MIN_RETWEETS })
      // format the data
      data.forEach(function(d) {
          d.date = new Date(d.created_at);//parseTime(d.created_at);
          d.trashiness = d.retweet_count ? d.reply_count/d.retweet_count : 0;
      });

      data = data.filter(function(d) { return !isNaN(d.trashiness) && d.date > beginDate})
      return data
    })
    appState = Object.assign({}, appState, {allData: values})
    //renderAllUsers(values)
    renderChart()
  })
}

function renderChart() {
   console.log('RENDER') 
    var index = appState.selectedUsers[0]
    console.log(appState, index)
    var data = appState.allData[index]

    console.log(index, data)

    var allAverages = []
    appState.allData//.filter(function(d, i) { return appState.selectedUsers.indexOf(i)> -1}) 
      .forEach(function(data, i) {

      if(appState.selectedUsers.indexOf(i) === -1) {
        allAverages.push([])
      }
      else {
        var averages = d3.nest()
          .key(function(d) { return getWeekDate(d.date)+'-'+('0'+(d.date.getMonth()+1)).slice(-2)+'-'+d.date.getFullYear()})
          .rollup(function(leaves) { return d3.median(leaves, function(d) { return d.trashiness})})
          .entries(data)

        allAverages.push(averages)
      }
    })
    console.log('all avg', allAverages)


    var t = container.transition().duration(750);
    // Scale the range of the data
    if(appState.selectedUsers.length === 1) {
      x.domain(d3.extent(data, function(d) { return d.date; }));
      y.domain([0, appState.showTweets ? 
            d3.max(data, function(d) { return d.trashiness; }) :
            d3.max(averages, function(d) { return d.value; })
      ]);
    }
    else {
      x.domain([
        d3.min(allAverages, function(averages) { return d3.min(averages, function(d) { return parseTime(d.key) }) }),
        d3.max(allAverages, function(averages) { return d3.max(averages, function(d) { return parseTime(d.key) }) }),
      ]);

      y.domain([0, d3.max(allAverages, function(averages) { return d3.max(averages, function(d) { return d.value; }) })]);
    } 
    //var pathData = d3.range(0, users.length).map(function(d, i) { return i===index ? averages: []})
 
    container.selectAll('.avg-path')
      .style('opacity', function(d, i) {  return appState.selectedUsers.indexOf(i)> -1 ? 1 : 0 }) 


    container.selectAll('.avg-path').data(allAverages)
   //   .style('opacity', function(d, i) { return appState.selectedUsers.indexOf(i)> -1 }) 
  .transition(t)  
      .attr("d", function(d, i) { return appState.selectedUsers.indexOf(i)> -1  ? valueline(d, i) : ''});
/* 
    path.data([averages])
        .attr('stroke', colorScale(index))
        .style('opacity', 1)
  
  .transition(t)  
      .attr("d", function(d, i) { return i===index ? valueline(d, i) : ''});
*/
    if(/*appState.showTweets &&*/ appState.selectedUsers.length===1) {
      var tweets = container.selectAll('.tweet').data(data)

      tweets.exit()
        .remove()

      tweets.enter()
        .append('circle')
        .attr('class', function(d, i) { return 'tweet tweets-'+i })
        .attr('r', 2)
        .attr('cx', function(d) { return x(d.date)})
        .attr('cy', function(d) { return y(d.trashiness)})
        .attr('fill', colorScale(index))

      tweets
        .attr('cx', function(d) { return  x(d.date)})
        .attr('cy', function(d) { return y(d.trashiness)})
        .attr('fill', colorScale(index))
      .transition(t)  
        .style('opacity', 0.3)
      
      var voronois = voronoiGroup.selectAll('path')
        .data(voronoi(data).polygons())//d3.merge(data.map(function(d) { return d.trashiness; }))))

      voronois.exit()
        .remove()

      voronois.enter()
        .append('path')
        .attr("d", function(d) { return d ? "M" + d.join("L") + "Z" : null; })
        .on('mouseover', function(d, i)  {
          d3.select('.tweets-'+i).classed('tweets-hover', true) 
          calloutImage.attr('src', profilePhotos[d.data.user])
          calloutText.text(d.data.text)
          calloutTime.text(timeDisplay(d.data.date))
          calloutRetweet.text(d.data.retweet_count.toLocaleString())
          calloutReply.text(d.data.reply_count.toLocaleString())
          calloutTrash.text(d.data.trashiness.toFixed(2))
          callout.style('left', x(d.data.date) < width/2 ? x(d.data.date) + 60 : x(d.data.date) - 260)
          callout.style('top', y(d.data.trashiness) <  height/2 ? y(d.data.trashiness) + 40 : y(d.data.trashiness) - 70)
          callout.style('opacity', 1)
        })
        .on('mouseout', function(d, i)  {
          d3.select('.tweets-'+i).classed('tweets-hover', false)  
          //callout.style('opacity', 0)
        })
        .on('click', function(d, i) {
          if(window.isMobile()) {
            return false;
          }
          var url = `https://twitter.com/${d.data.user}/status/${d.data.id_str}`
          window.open(url ,'_blank')
        })
      
      voronois
        .attr("d", function(d) { return d ? "M" + d.join("L") + "Z" : null; })
        .style('cursor', 'pointer')
        .style('pointer-events', 'all')
    }
    else {
      container.selectAll('.tweet') .transition(t).style('opacity', 0)

      voronoiGroup.selectAll('path')
        .style('cursor', 'default')
        .style('pointer-events', 'none')

      callout.style('opacity', 0)
    }
    var xAxis = container.selectAll('.xaxis').data([1])

    xAxis.enter().append('g')
      .classed('xaxis', true)
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(width < 600 ? 4 : 10));

    var yAxis = container.selectAll('.yaxis').data([1])

    yAxis.enter().append('g')
      .classed('yaxis', true)
      .call(d3.axisLeft(y));


   
    yAxis.transition(t).call(d3.axisLeft(y)) 
    xAxis.transition(t).call(d3.axisBottom(x).ticks(width < 600 ? 4 : 10))

}

function getWeekDate(d) {
  var day = (Math.ceil(d.getDate()/7)*7) + 1
  return ('0'+day).slice(-2)
}

window.onresize = function() {
  width = window.innerWidth - margin.left - margin.right,
  height = window.innerHeight - margin.top - margin.bottom;
  x.range([0, width]);
  y.range([height, 0]);
  svg.attr("width", width + margin.left + margin.right)
  svg.attr("height", height + margin.top + margin.bottom)
  svg.select('.ylabel')
      .attr("x",0 - (height / 2))

  svg.select('.xaxis').attr('transform', 'translate(0, '+ height + ')')
//  container.attr("transform",
//          "translate(" + margin.left + "," + margin.top + ")");

  renderChart()
}
window.isMobile = function() {
  var check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};
