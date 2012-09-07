var w = 800,
    h = 600,
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

	function find_path(node){
		return node.name.split("::")[0];
	}
	function find_date(node){
		return node.name.split("::")[1];
	}
	function find_doi(node){
		return node.name.split("::")[2];
	}
	function find_original_author(node){
		return node.name.split("::")[3];
	}

	function path_or_not(node){
		if(find_original_author(node) == 1){
			return y(1);
		}else{
			return y(find_path(node));
		}
	}

var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

var x = null;
var y = null;

try{

d3.json("/networkgraphs/data/"+ENTRY_ID+"/", function(json) {

  if(json == null || json == {}){
	console.log(json);
	setTimeout(function(){window.location=window.location;},1000);
	return;
  }

  var max_x = d3.max(json.nodes, function(d){return find_date(d);});
  var min_x = d3.min(json.nodes, function(d){return find_date(d);});
  var max_y = d3.max(json.nodes, function(d){return find_path(d);});
  var min_y = d3.min(json.nodes, function(d){return find_path(d);});

  x = d3.scale.linear().domain([min_x,max_x]).range([50,w-50]);
  y = d3.scale.linear().domain([min_y,max_y]).range([50,h-(h*0.4)]);

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
		className += " " + "path"+find_path(json.nodes[d.source]);
		className += " " + "path"+find_path(json.nodes[d.target]);
		return className;
	})
       .attr("d", function(d){
	
	var i = {}, j = {};
	i.x = x(find_date(json.nodes[d.source])); 		
	i.y = path_or_not(json.nodes[d.source]);
	j.x = x(find_date(json.nodes[d.target]));
	j.y = path_or_not(json.nodes[d.target]);

	return	diagonal({source: i, target: j});
	})
       .attr("style","fill:none; stroke: grey; opacity:0.3;")
       .attr("onmouseover","javascript:highlight(this)")
       .attr("onmouseout","javascript: d3.selectAll('.link').style('stroke','grey').style('opacity','0.3');")

  var node = vis.selectAll("g.node")
      .data(json.nodes)
      .enter().append("svg:g")
      .attr("class", "node")
      .attr("id", function(d) { return find_doi(d); });

  node.append("svg:circle")
      .attr("r", 5)
      .attr("cx", function(d){return x(find_date(d));})
      .attr("cy", function(d){
		return path_or_not(d);
	})
      .style("fill", function(d) { return fill(d.group); })
      .attr("onmouseover","javascript:d3.select(this.parentNode.childNodes[1]).attr('display','block');")
      .attr("onmouseout","javascript:d3.select(this.parentNode.childNodes[1]).attr('display','none');")
      .attr("onclick","javascript:document.getElementById(\"viewport\").src=\"http://dx.doi.org/\"+this.parentNode.childNodes[1].firstChild.nodeValue.split(',')[1]+'#contentHeader';return false;")

  node.append("svg:text")
      .attr("text-anchor","start")
      .attr("font-size","10")
      .attr("dx", function(d){return x(find_date(d))+10;})
      .attr("dy", function(d){
		return path_or_not(d);
	})
      .attr("display","none")
      .text(function(d){return find_path(d) + ',' + find_doi(d)});
    
 //   node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
});

}catch(e){
console.log(e);
setTimeout(function(){window.location=window.location;},1000);
}
