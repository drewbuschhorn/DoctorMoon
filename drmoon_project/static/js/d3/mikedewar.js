    var w = $('#chart').width();
    var h = 700;
    var fixed_highlighting = false;

    fill = d3.scale.category20();

	function highlight(link){
	
	    var linkNodeId = link.id.split("link")[1];
	    var linkNode = data.links[linkNodeId];
	    linkNode.checked = false;

        var linksToHighlight = [];
        
        var linksToCheck = [linkNode];
        while(linksToCheck.length>0){
            var nextLinks = [];
            linksToCheck.forEach(function(i){
                data.links.filter(function(j){
                                    if(
                                    (i.target == j.source)
                                    && (i.index != j.index)
                                    ){
                                        j.checked = false;
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
        linksToHighlight.forEach(function(i,j){
            linksToHighlight[j] = "#link"+i.index;
        });
        d3.selectAll(linksToHighlight.join(',')).style('stroke','black').style('opacity','1.0');
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
	
	function node_highlight(node_id){
            if(fixed_highlighting!==false){
                var _oldNode = fixed_highlighting;
                d3.selectAll('.link').style('stroke','grey').style('opacity','0.3');
                fixed_highlighting = false;
                if(_oldNode == node_id){
                    return;
                }
            }
      
            // TODO: Uselss debugging code - delete before release.
            var e = $(data.nodes).filter(function(){return node_id == this.index;});
            document.getElementById("viewport").src="http://dx.doi.org/"+e[0].doi+'#contentHeader';
            //End useless code
            
            $(data.links)
            .filter(function(){return (this.source==node_id)}) //||(this.target==node_id)})
            .each(function(){
                var a = this.index;
                highlight($("#link"+this.index)[0]);
                fixed_highlighting = node_id;
            })	
	}
	

var vis = d3.select("#chart")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

var x = null;
var y = null;
var data = null;


try{
var url = "/networkgraphs/data/"+ENTRY_ID+"/";

d3.json(url, function(json) {
  data = json;

  if(json == null || json == {}){
    throw new Exception('No json received from '+url+'.');
	return;
  }

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

  x = d3.scale.linear().domain([min_x,max_x]).range([w*.05,w-(w*.05)]);
  y = d3.scale.linear().domain([min_y,max_y]).range([h*.05,h-(h*0.4)]);

 var diagonal = d3.svg.diagonal();

 var link = vis.selectAll("path.link")
       .data(json.links).enter()
       .append("svg:path")
       .attr("style","fill:none; stroke: grey; opacity:0.3;")
       .attr("onmouseover","javascript:if(fixed_highlighting===false){highlight(this)}")
       .attr("onmouseout", "javascript:if(fixed_highlighting===false){d3.selectAll('.link').style('stroke','grey').style('opacity','0.3');}")
       .attr("id",function(d,i){return "link"+i})
       .attr("class",function(d){
		    var className = "link";
		    className += " " + "path"+find_path(json.nodes.getNode(d.source));
		    className += " " + "path"+find_path(json.nodes.getNode(d.target));
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

  var node = vis.selectAll("g.node")
      .data(json.nodes).enter()
      .append("svg:g")
      .attr("class", "node")
      .attr("id", function(d) {return find_doi(d);})
      .attr("data:json_index", function(d) {return d.index;});

  node.append("svg:circle")
      .attr("r", 5).attr("text",function(d){return find_doi(d);})
      .attr("cx", function(d){return x(find_date(d));})
      .attr("cy", function(d){return path_or_not(d);})
      .style("fill", function(d){return fill(d.group);})
      .attr("onclick",function(d){return "javascript:node_highlight("+d.index+");"});

  node.append("svg:text")
      .attr("text-anchor","start")
      .attr("font-size","10")
      .attr("display","none")
      .attr("dx", function(d){return x(find_date(d))+10;})
      .attr("dy", function(d){return path_or_not(d);})
      .text(function(d){return find_path(d)+','+find_doi(d)});

    //Generate path list for sidebar
    path_setup(); 
    
    });

}catch(e){
console.log(e);
}

function path_setup(){

        path_list = new Array();
        $(data.nodes).each(
            function(index,value){
                if(jQuery.inArray(value.path_index,path_list)==-1)
                { path_list.push(value.path_index); };
            }
        );
        path_list.sort(
            function(a,b){
                if(a>b){return 1;}else{return -1;}
            }
        );
        
        d3.select("#well").append("ul")
            .selectAll("li")
            .data(path_list).enter()
            .append("li")
                .html(function(d){
                var src = "javascript:if(fixed_highlighting===false){d3.selectAll('.link').style('stroke','grey').style('opacity','0.3'); d3.selectAll('.path"+d+"').style('stroke','black').style('opacity','1')}";
                return "<a href=\""+src+"\">Path "+d+"</a>"
                })
                .attr("id",function(d){return "_"+d;});       
}
