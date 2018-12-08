var w = 800,
    h = 600,
    fill = d3.scale.category20();

  function highlightByGroup(group){
    var linksToHighlight = data.links.filter(function(i) {
      for (var j = 0; j < i.groups.length; j++) {
        if (i.groups[j] == group) {
          return true;
        }
      }
    });
    
    linksToHighlight.forEach(function(i,j){
        linksToHighlight[j] = "#link"+i.index;
    });
    d3.selectAll('.link').style('stroke','grey').style('opacity','0.3').attr('marker-end','');
    d3.selectAll(linksToHighlight.join(',')).style('stroke','black').style('opacity','1.0').attr('marker-end','url(#arrow)');
  };  
    
	function highlight(link){
	    var linkNodeId = link.id.split("link")[1];
	    console.log(linkNodeId);
	    var linkNode = data.links[linkNodeId];
	    linkNode.checked = false;

        var linksToHighlight = [];
        
        var linksToCheck = [linkNode];
        while(linksToCheck.length>0){
            var nextLinks = [];
            console.log(linksToCheck);
            linksToCheck.forEach(function(i){
                data.links.filter(function(j){
                                    if(
                                    (i.target == j.source)
                                    && (i.index != j.index)
                                    ){
                                        j.checked = false;
                                        console.log("1target:"+i.target,"1source:"+j.source);
                                        nextLinks.push(j);
                                        return true;
                                    }
                                 });
                i.checked = true;
                linksToHighlight.push(i);
            });
            linksToCheck = jQuery.merge(linksToCheck,nextLinks);
            linksToCheck = linksToCheck.filter(function(i){return !i.checked;});
        }
        
        //We've got the linksToHighlight now.  Do whatever is fastest to highlight them.
        console.log(linksToHighlight);
        
        linksToHighlight.forEach(function(i,j){
            linksToHighlight[j] = "#link"+i.index;
        });
        d3.selectAll('.link').style('stroke','grey').style('opacity','0.3').attr('marker-end','');
        d3.selectAll(linksToHighlight.join(',')).style('stroke','black').style('opacity','1.0').attr('marker-end','url(#arrow)');
        return linksToHighlight;
	}

  function list_of_tables(lists) {
    var host = document.getElementById('host');
    host.innerHTML = "";
    for (var i = 0; i < lists.length; i++) {
      table = table_template(lists[i])
      host.appendChild(table)
    }
  }
  
  function table_template(nodeList) {
    var table = document.createElement('div')
      table.setAttribute("class", "nodeTable")
      for (var i = 0; i < nodeList.length; i++) {
        var nodeData = document.createElement('div')
        nodeData.setAttribute("class", "nodeTableEntry")
        nodeData.innerText = nodeList[i].doi + " <br/> " + nodeList[i].title
        table.appendChilde(nodeData);
      }
    return table;
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
  
  function clean_duplicate_nodes_and_links (json) {
    json.all_groups = new Set();
    // Should probably fix this on the server side, but networkx is being a pain about realizing duplicate entry objects
    var dupe_map = []
    var all_groups = new Set();
    for (var i in json.nodes) {
      json.all_groups.add(json.nodes[i].group);
      dupe_map[i] = []
      json.nodes[i].groups = new Set();
      json.nodes[i].groups.add(json.nodes[i].group);
      console.log('c', json.nodes[i].groups);
      for (var j in json.nodes) {
        if (json.nodes[i].doi == json.nodes[j].doi) {
          json.nodes[i].groups.add(json.nodes[j].group)
          if (dupe_map[i]) {
            dupe_map[i].push(json.nodes[j].index);
          } else {
            dupe_map[i] = [json.nodes[j].index];
          }
        }
      }
      console.log('a',json.nodes[i].groups);
      json.nodes[i].groups = Array.from(json.nodes[i].groups).sort();
      console.log('b', json.nodes[i].groups);
    }
    json.all_groups = Array.from(json.all_groups).sort();
    // Translate links to unduplicated nodes
    for (var i in json.links) {
      json.links[i].source = dupe_map[json.links[i].source][0];
      json.links[i].target = dupe_map[json.links[i].target][0];
      var sourceGroups = json.nodes[json.links[i].source].groups;
      var targetGroups = json.nodes[json.links[i].target].groups;
      var a = new Set(sourceGroups);
      var b = new Set(targetGroups);
      var intersection = new Set(
          [...a].filter(x => b.has(x)));
      json.links[i].groups = Array.from(intersection);
    }
    // Remove unneeded nodes.
    json.nodes = json.nodes.filter(function(i){
      for (var j in json.links) {
        if (json.links[j].source == i.index)
          return true;
        if (json.links[j].target == i.index)
          return true;
      }
      return false;
    });
    json.nodes.sort(function(a, b) {
      if (a.publication_date > b.publication_date){return -1}
      if (a.publication_date < b.publication_date){return 1}
      return 0;
    });
    
    for (var k = 0; k<json.nodes.length; k++){
      json.nodes[k].key = String.fromCharCode('a'.charCodeAt(0) + k);
    }
    
    return json;
  }

var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

    //     <marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth">
    //  <path d="M0,0 L0,6 L9,3 z" fill="#f00" />
    // </marker>
    vis.append('svg:defs')
        .append('svg:marker')
          .attr('id','arrow')
          .attr('markerWidth','5')
          .attr('markerHeight','5')
          .attr('refX','5')
          .attr('refY','3')
          .attr('orient','auto')
          .attr('markerUnits','strokeWidth')
          .append('svg:path')
            .attr('d','M0,0 L0,6 L9,3 z')
            .attr('fill','#fff')
    
    

var x = null;
var y = null;
var data = null;

try{

d3.json("./mikedewar.js", function(json) {
  
  json = myjson;
  data = json;

  if(json == null || json == {}){
	console.log(json);
	//setTimeout(function(){window.location=window.location;},1000);
	return;
  }
  
  // Should probably fix this on the server side, but networkx is being a pain about realizing duplicate entry objects
  json = clean_duplicate_nodes_and_links(json);

  json.nodes.getNode=function(i){
    for(var j = 0; j<json.nodes.length; j++){
        if(i == json.nodes[j].index)
            return json.nodes[j];
    }
    return null;
  };

  var max_x = d3.max(json.nodes, function(d){return find_date(d);});
  var min_x = d3.min(json.nodes, function(d){return find_date(d);});
  var max_y = d3.max(json.nodes, function(d){return find_path(d);});
  var min_y = d3.min(json.nodes, function(d){return find_path(d);});

  x = d3.scale.linear().domain([min_x,max_x]).range([50,w-50]);
  y = d3.scale.linear().domain([min_y,max_y]).range([50,h-(h*0.4)]);

  var node = vis.selectAll("g.node")
      .data(json.nodes)
      .enter().append("svg:g")
      .attr("class", "node")
      .attr("data-groups", function(d) {return d.groups;})
      .attr("id", function(d) { return find_doi(d); })
      .attr("onmouseover", 'javascript:nodeMouseOver(this)')
      .attr("onclick", 'javascript:nodeClick(this)')
      .attr("onmouseout", 'javascript:nodeMouseOut(this)')

  node.append("svg:circle")
      .attr("r", 5).attr("text", function(d){return find_doi(d);})
      .attr("cx", function(d){return x(find_date(d));})
      .attr("cy", function(d){
            return path_or_not(d);
      })
      .style("fill", function(d) { return fill(0); })

  node.append("svg:text")
      .attr("height", "auto")
      .attr("width", "500")
      .attr("text-anchor", "start")
      .attr("font-size", "10")
      .attr("dx", function(d){return x(find_date(d))+10;})
      .attr("dy", function(d){return path_or_not(d)})
      .text(function(d){return d.key +" g:" + d.groups});

  node.append("svg:text")
      .attr("text-anchor", "start")
      .attr("font-size", "10")
      .attr("dx", function(d){return x(find_date(d))+10;})
      .attr("dy", function(d){
              return path_or_not(d);
            })
      .attr("display", "none")
      .text(function(d){return find_path(d) + ',' + find_doi(d)});
      
// X axis labels      
  vis.append("svg:g")
    .attr('transform', 'translate('+ x(min_x)  +','+ 0  +')')
    .append("svg:text")
      .attr('font-size', '10')
      .attr('transform', 'rotate(90)')
      .text(new Date(min_x * 1e3).toISOString().slice(0,10));
      
  vis.append("svg:g")
    .attr('transform', 'translate('+ x(max_x)  +','+ 0  +')')
    .append("svg:text")
      .attr('font-size', '10')
      .attr('transform', 'rotate(90)')
      .text(new Date(max_x * 1e3).toISOString().slice(0,10));
    
      
      
 var diagonal = d3.svg.diagonal()

 var link = vis.selectAll("path.link")
       .data(json.links)
       .enter()
       
       link.append("svg:path")
       .attr("id",function(d,i){return "link"+i})
       .attr("class",function(d){
                var className = "link";
                className += " " + "spath"+find_path(json.nodes.getNode(d.source));
                className += " " + "tpath"+find_path(json.nodes.getNode(d.target));
                className += " " + "snode" + d.source;
                className += " " + "tnode" + d.target;
                return className;
            })
       .attr("d", function(d){
            var i = {}, j = {};
            i.x = x(find_date(json.nodes.getNode(d.source))); 		
            i.y = path_or_not(json.nodes.getNode(d.source));
            j.x = x(find_date(json.nodes.getNode(d.target)));
            j.y = path_or_not(json.nodes.getNode(d.target));
            return	diagonal({source: i, target: j});
            })
       // .attr('marker-end','url(#arrow)')
       .attr("style","fill: none; stroke: grey; opacity: 0.3;")
       .attr('onmouseover', 'javascript:linkMouseOver(this)')
       .attr('onclick', 'javascript:linkClick(this)')
       .attr('onmouseout', 'javascript:linkMouseOut(this)')
       //.attr("onmouseover","javascript: highlight(this)")
       //.attr("onmouseout","javascript: d3.selectAll('.link').style('stroke','grey').style('opacity','0.3').attr('marker-end','');")
       link.append("svg:text")
        .attr('text-anchor', 'middle')
        .attr('font-size', 10)
        .attr('dx', 100)
        .append("svg:textPath")
        .attr('href', function(d,i){return "#link"+i})
        .text(function(d){return d.groups})
       
      
      createGroupsList(json);
});

function createGroupsList(json) {
  $(document).ready(function() {
    console.log("groups",json.all_groups);
    $('#groups_column_text').empty();
    json.all_groups.forEach(function(i){
      var child = document.createElement('ol');
      child.setAttribute('class', 'text_group_ids');
      child.textContent = i;
      child.setAttribute('data-group', i);
      $('#groups_column_text').append(child);
    })
    $('#groups_column_text').show();
    $('.text_group_ids').on('mouseover',function(e){
      var group = e.currentTarget.getAttribute('data-group')
        highlightByGroup(group);
        createPapersList(group);
      });
  });

}

function createPapersList(group) {
  $('#group_data_text').empty();
  var nodes = data.nodes.filter(function(node) {
    for (var i = 0; i < node.groups.length; i++) {
      if (node.groups[i] == group) {
        return true;
      }
    }
  });
  nodes.sort(function(a, b) {
    if (a.publication_date > b.publication_date){return -1}
    if (a.publication_date < b.publication_date){return 1}
    return 0;
  });
  
  var div = document.createElement('div');
  div.setAttribute('class', 'papersList');
  nodes.forEach(function(node) {
    $(div).append(`<div class='paperEntry' style='margin: 5px 0px 5px 5px'>${node.key} - ${node.title} - ${new Date(node.publication_date * 1e3).toISOString().slice(0,10)}</div>`);
  });
  $('#group_data_text').append(div);
}

function linkMouseOver(e) {
  highlight(e)
}

function linkClick(e) {
  links = highlight(e)
  var unique = links.filter(function(value, index, self){return self.indexOf(value) === index;})
  linkElements = []
  unique.map(function(e){linkElements.push(document.querySelector(e))});
  console.log(linkElements);
}

function linkMouseOut(e) {
  d3.selectAll('.link').style('stroke','grey').style('opacity','0.3').attr('marker-end','');
}

function nodeMouseOver(e) {
  console.log(e); console.log('-'); console.log(this);
}
function nodeMouseOut(e) {
  console.log(e); console.log('-'); console.log(this);
}
function nodeClick(e){ 
  console.log(e); console.log('-'); console.log(this);
}

}catch(e){
  console.log(e);
}
