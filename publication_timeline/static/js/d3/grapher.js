function Grapher(target, width, height) {
  this.target = target;
  this.width = width;
  this.height = height;
  this.debug = false;

  this.fill = d3.scale.category20();
  this.vis = d3.select(this.target)
      .append("svg:svg")
        .attr("width", width)
        .attr("height", height)
  this.vis.append('svg:defs')
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
}
  
Grapher.prototype.highlightByGroup = function(links, group){
  var linksToHighlight = links.filter(function(i) {
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

Grapher.prototype.highlight = function(link, links){
    var linkNodeId = link.id.split("link")[1];
    var linkNode = links[linkNodeId];
    linkNode.checked = false;

      var linksToHighlight = [];
      
      var linksToCheck = [linkNode];
      while(linksToCheck.length>0){
          var nextLinks = [];
          linksToCheck.forEach(function(i){
              links.filter(function(j){
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
      d3.selectAll('.link').style('stroke','grey').style('opacity','0.3').attr('marker-end','');
      d3.selectAll(linksToHighlight.join(',')).style('stroke','black').style('opacity','1.0').attr('marker-end','url(#arrow)');
      return linksToHighlight;
}

Grapher.prototype.initializeDependencies = function(helpers, templates) {
  this.find_date = helpers.find_date;
  this.find_doi = helpers.find_doi;
  this.find_path = helpers.find_path;
  this.find_original_author = helpers.find_original_author;
  this.path_or_not = helpers.path_or_not;
  this.clean_duplicate_nodes_and_links = helpers.clean_duplicate_nodes_and_links;
  
  this.listOfTables = (lists)=>{return templates.listOfTables(lists);};
  this.createGroupsList = (nodeList)=>{return templates.createGroupsList(nodeList);};
  
}

Grapher.prototype.setup = function(json, helpers, templates) {
      this.initializeDependencies(helpers, templates);

      if(json == null || json == {}){
        alert('No json data found in timelineData / json');
        return;
      }
      this.json = json;

      // Should probably fix this on the server side, but networkx is being a pain about realizing duplicate entry objects
      json = this.clean_duplicate_nodes_and_links(json);
      // Add helper function to nodes
      json.nodes.getNode=function(i){
        for(var j = 0; j<json.nodes.length; j++){
            if(i == json.nodes[j].index)
                return json.nodes[j];
        }
        return null;
      };

      var max_x = d3.max(json.nodes, (d)=>{return this.find_date(d);});
      var min_x = d3.min(json.nodes, (d)=>{return this.find_date(d);});
      var max_y = d3.max(json.nodes, (d)=>{return this.find_path(d);});
      var min_y = d3.min(json.nodes, (d)=>{return this.find_path(d);});

      this.x = d3.scale.linear().domain([min_x,max_x]).range([50,this.width-50]);
      this.y = d3.scale.linear().domain([min_y,max_y]).range([50,this.height-(this.height*0.4)]);
      
      var node = this.vis.selectAll("g.node")
          .data(json.nodes)
          .enter().append("svg:g")
          .attr("class", "node")
          .attr("data-groups", (d)=>{return d.groups;})
          .attr("id", (d)=>{return this.find_doi(d); })
          .attr("onmouseover", 'javascript:grapher.nodeMouseOver(this)')
          .attr("onclick", 'javascript:grapher.nodeClick(this)')
          .attr("onmouseout", 'javascript:grapher.nodeMouseOut(this)')

      node.append("svg:circle")
          .attr("r", 5).attr("text", (d)=>{return this.find_doi(d);})
          .attr("cx", (d)=>{return this.x(this.find_date(d));})
          .attr("cy", (d)=>{return this.path_or_not(d, this.y);})
          .style("fill", (d)=>{ return this.fill(0); })

      

      node.append("svg:text")
          .attr("height", "auto")
          .attr("width", "500")
          .attr("text-anchor", "start")
          .attr("font-size", "10")
          .attr("dx", (d)=>{return this.x(this.find_date(d))+10;})
          .attr("dy", (d)=>{return this.path_or_not(d, this.y)})
          .text((d)=>{
                  var nodeText = d.key; 
                  if (this.debug) { nodeText +=  +" g:" + d.groups};
                  return nodeText;
          });

      node.append("svg:text")
          .attr("text-anchor", "start")
          .attr("font-size", "10")
          .attr("dx", (d)=>{return this.x(this.find_date(d))+10;})
          .attr("dy", (d)=>{return this.path_or_not(d, this.y);})
          .attr("display", "none")
          .text((d)=>{return this.find_path(d) + ',' + this.find_doi(d)});
          
    // X axis labels      
      this.vis.append("svg:g")
        .attr('transform', 'translate('+ this.x(min_x)  +','+ 0  +')')
        .append("svg:text")
          .attr('font-size', '10')
          .attr('transform', 'rotate(90)')
          .text(new Date(min_x * 1e3).toISOString().slice(0,10));
          
      this.vis.append("svg:g")
        .attr('transform', 'translate('+ this.x(max_x)  +','+ 0  +')')
        .append("svg:text")
          .attr('font-size', '10')
          .attr('transform', 'rotate(90)')
          .text(new Date(max_x * 1e3).toISOString().slice(0,10));
        
          
          
      var diagonal = d3.svg.diagonal()

      var link = this.vis.selectAll("path.link")
           .data(json.links)
           .enter()
           
           link.append("svg:path")
           .attr("id", (d,i)=>{return "link"+i})
           .attr("class",(d)=>{
                    var className = "link";
                    className += " " + "spath" + this.find_path(json.nodes.getNode(d.source));
                    className += " " + "tpath" + this.find_path(json.nodes.getNode(d.target));
                    className += " " + "snode" + d.source;
                    className += " " + "tnode" + d.target;
                    return className;
                })
           .attr("d", (d)=>{
                var i = {}, j = {};
                i.x = this.x(this.find_date(json.nodes.getNode(d.source))); 		
                i.y = this.path_or_not(json.nodes.getNode(d.source), this.y);
                j.x = this.x(this.find_date(json.nodes.getNode(d.target)));
                j.y = this.path_or_not(json.nodes.getNode(d.target), this.y);
                return	diagonal({source: i, target: j});
                })
           .attr("style","fill: none; stroke: grey; opacity: 0.3;")
           .attr('onmouseover', 'javascript:grapher.linkMouseOver(this)')
           .attr('onclick', 'javascript:grapher.linkClick(this)')
           .attr('onmouseout', 'javascript:grapher.linkMouseOut(this)')
           link.append("svg:text")
            .attr('text-anchor', 'middle')
            .attr('font-size', 10)
            .attr('dx', 100)
            .append("svg:textPath")
            .attr('href', (d,i)=>{return "#link"+i})
            .text((d)=>{
              if (this.debug) {
                return d.groups
              }
            });
           
          this.createGroupsList(json);
}

Grapher.prototype.linkMouseOver = function(e) {
  this.highlight(e, this.json.links)
}
Grapher.prototype.linkClick = function(e) {
  links = this.highlight(e, this.json.links)
  var unique = links.filter(function(value, index, self){return self.indexOf(value) === index;})
  linkElements = []
  unique.map(function(e){linkElements.push(document.querySelector(e))});
}
Grapher.prototype.linkMouseOut = function(e) {
  d3.selectAll('.link').style('stroke','grey').style('opacity','0.3').attr('marker-end','');
}
Grapher.prototype.nodeMouseOver = function(e) {
  console.log(e); console.log(this);
}
Grapher.prototype.nodeMouseOut = function(e) {
  console.log(e); console.log(this);
}
Grapher.prototype.nodeClick = function(e) { 
  console.log(e); console.log(this);
}