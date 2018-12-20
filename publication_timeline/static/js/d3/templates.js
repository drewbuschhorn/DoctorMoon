function Templates(host) {
  this.nodeTable = 'nodeTable';
  this.nodeTableEntry = 'nodeTableEntry';
  this.groupsColumnTextId = 'groups_column_text';
  this.groupDataText = 'group_data_text';
  this.groupDataType = 'data-group';
  this.textGroupIdsClass = 'text_group_ids';
  this.papersList = 'papersList';
  this.paperEntry = 'paperEntry';
}  
  
Templates.prototype.listOfTables = function(lists) {
    host.innerHTML = "";
    for (var i = 0; i < lists.length; i++) {
      table = this.tableTemplate(lists[i])
      host.appendChild(table)
    }
  }
  
Templates.prototype.tableTemplate = function(nodeList) {
  var table = document.createElement('div')
    table.setAttribute("class", this.nodeTable)
    for (var i = 0; i < nodeList.length; i++) {
      var nodeData = document.createElement('div')
      nodeData.setAttribute("class", this.nodeTableEntry)
      nodeData.innerText = nodeList[i].doi + " <br/> " + nodeList[i].title
      table.appendChilde(nodeData);
    }
  return table;
}

Templates.prototype.createGroupsList = function(json) {
    $('#' + this.groupsColumnTextId).empty();
    json.all_groups.forEach((i)=>{
      var child = document.createElement('ol');
      child.setAttribute('class', this.textGroupIdsClass);
      child.textContent = i;
      child.setAttribute(this.groupDataType, i);
      $('#'+this.groupsColumnTextId).append(child);
    })
    $('#'+this.groupsColumnTextId).show();
    $('.'+this.textGroupIdsClass).on('mouseover',function(e){
      var group = e.currentTarget.getAttribute(this.groupDataType)
        Grapher.prototype.highlightByGroup(json.links, group);
        this.createPapersList(group, json.nodes);
      }.bind(this));
}

Templates.prototype.createPapersList = function(group, nodes) {
  $('#'+this.groupDataText).empty();
  var nodes = nodes.filter(function(node) {
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
  div.setAttribute('class', this.papersList);
  nodes.forEach((node)=>{
  $(div).append(`<div class='${this.paperEntry}' style='margin: 5px 0px 5px 5px'>${node.key} - ${node.title} - ${new Date(node.publication_date * 1e3).toISOString().slice(0,10)} - ${node.authors}</div>`);
  });
  $('#'+this.groupDataText).append(div);
}

