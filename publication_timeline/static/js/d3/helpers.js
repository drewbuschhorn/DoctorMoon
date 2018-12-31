function Helpers(){}
  
Helpers.prototype.find_path = function(node){
  return node.name.split("::")[0];
}
Helpers.prototype.find_date = function(node){
  return node.publication_date;
}
Helpers.prototype.find_doi = function(node){
  return node.name.split("::")[2];
}
Helpers.prototype.find_original_author = function(node){
  return node.name.split("::")[3];
}

Helpers.prototype.path_or_not = function(node, y){
  if(this.find_original_author(node) == 1){
    return y(1);
  }else{
    return y(this.find_path(node));
  }
}

Helpers.prototype.clean_duplicate_nodes_and_links = function(json) {
  json.all_groups = new Set();
  // Should probably fix this on the server side, but networkx is being a pain about realizing duplicate entry objects
  var dupe_map = []
  var all_groups = new Set();
  for (var i in json.nodes) {
    json.all_groups.add(json.nodes[i].group);
    dupe_map[i] = []
    json.nodes[i].groups = new Set();
    json.nodes[i].groups.add(json.nodes[i].group);
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
    json.nodes[i].groups = Array.from(json.nodes[i].groups).sort();
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
