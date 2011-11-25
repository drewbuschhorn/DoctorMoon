var w = 960,
    h = 500,
    fill = d3.scale.category20();

	  function highlight(link){
		var path_one = link.getAttribute('class').split(' ')[1];
		var path_two = link.getAttribute('class').split(' ')[2];
	
		var selector = "";
		if(path_one != "path1"){
		    selector += "."+path_one+",";
		}
		if(path_two != "path1" || selector == ""){
		    selector += "."+path_two;
		}
		selector = selector.replace(/\,$/,'')

		d3.selectAll(selector).style('stroke','black').style('opacity','1.0');
	  }

var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

d3.json("mikedewar.json", function(json) {
  var max_x = d3.max(json.nodes, function(d){return d.name.split("::")[1];});
  var min_x = d3.min(json.nodes, function(d){return d.name.split("::")[1];});
  var max_y = d3.max(json.nodes, function(d){return d.name.split("::")[0];});
  var min_y = d3.min(json.nodes, function(d){return d.name.split("::")[0];});

  var x = d3.scale.linear().domain([min_x,max_x]).range([50,w-50]);
  var y = d3.scale.linear().domain([min_y,max_y]).range([50,h-50]);

  /*
  var link = vis.selectAll("line.link")
    .data(json.links)
    .enter().append("svg:line")
      .attr("class", "link")
      .style("stroke-width", function(d) { return Math.sqrt(d.value); })
      .attr("x1", function(d) { return x(json.nodes[d.source].name.split("::")[1]); })
      .attr("y1", function(d) { 
		if(json.nodes[d.source].name.split("::")[3] == 1){
			return y(1);
		}else{
			return y(json.nodes[d.source].name.split("::")[0]);
		}
	})
      .attr("x2", function(d) { return x(json.nodes[d.target].name.split("::")[1]); })
      .attr("y2", function(d) { 
		if(json.nodes[d.target].name.split("::")[3] == 1){
			return y(1);
		}else{
			return y(json.nodes[d.target].name.split("::")[0]);
		}
	});
  */

 var diagonal = d3.svg.diagonal()

 var link = vis.selectAll("path.link")
       .data(json.links)
       .enter().append("svg:path")
       .attr("id",function(d,i){return "link"+i})
       .attr("class",function(d){
		var className = "link";
		className += " " + "path"+json.nodes[d.source].name.split("::")[0];
		className += " " + "path"+json.nodes[d.target].name.split("::")[0];
		return className;
	})
       .attr("d", function(d){
	
	var i = {}, j = {};
	i.x = x(json.nodes[d.source].name.split("::")[1]); 		
	if(json.nodes[d.source].name.split("::")[3] == 1){
		i.y = y(1);
	}else{
		i.y = y(json.nodes[d.source].name.split("::")[0]);
	}

	j.x = x(json.nodes[d.target].name.split("::")[1]);
	if(json.nodes[d.target].name.split("::")[3] == 1){
		j.y = y(1);
	}else{
		j.y = y(json.nodes[d.target].name.split("::")[0]);
	}

	return	diagonal({source: i, target: j});
	})
       .attr("style","fill:none; stroke: grey; opacity:0.3;")
       .attr("onmouseover","javascript:highlight(this)")
       .attr("onmouseout","javascript: d3.selectAll('.link').style('stroke','grey').style('opacity','0.3');")

  var node = vis.selectAll("g.node")
      .data(json.nodes)
      .enter().append("svg:g")
      .attr("class", "node")
      .attr("id", function(d) { return d.name.split("::")[2]; });

  node.append("svg:circle")
      .attr("r", 5)
      .attr("cx", function(d){return x(d.name.split("::")[1]);})
      .attr("cy", function(d){
		if(d.name.split("::")[3] == 1){
			return y(1);
		}else{
			return y(d.name.split("::")[0]);
		}
	})
      .style("fill", function(d) { return fill(d.group); })
      .attr("onmouseover","javascript:d3.select(this.parentNode.childNodes[1]).attr('display','block');")
      .attr("onmouseout","javascript:d3.select(this.parentNode.childNodes[1]).attr('display','none');")

  node.append("svg:text")
      .attr("text-anchor","start")
      .attr("font-size","10")
      .attr("dx", function(d){return x(d.name.split("::")[1])+10;})
      .attr("dy", function(d){
		if(d.name.split("::")[3] == 1){
			return y(1);
		}else{
			return y(d.name.split("::")[0]);
		}
	})
      .attr("display","none")
      .text(function(d){return d.name.split("::")[0] + ',' + d.name.split("::")[2]});
    
 //   node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
});

