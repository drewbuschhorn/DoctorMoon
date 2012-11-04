from django.http import HttpResponse,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from drmoon.models import NetworkGraph,UserProfile

import json

@login_required
def index(request):
  network_graph_list = NetworkGraph.objects.filter(user=request.user.id)
  print request.user.id
  paginator = Paginator(network_graph_list, 10)
  
  # Make sure page request is an int. If not, deliver first page.
  try:
      page = int(request.GET.get('page', '1'))
  except ValueError:
      page = 1

  # If page request (9999) is out of range, deliver last page of results.
  try:
      network_graphs = paginator.page(page)
  except (EmptyPage, InvalidPage):
      raise Http404

  return render_to_response('networkgraph/index.html', 
            {'network_graphs': network_graphs},
            context_instance=RequestContext(request))



@login_required
def details(request, network_id):    

    try:
        network = NetworkGraph.objects.get(pk=network_id)
    except NetworkGraph.DoesNotExist:
        raise Http404
    
    if request.user.id is not network.user.id:
	raise PermissionDenied

    return render_to_response('networkgraph/detail.html', 
                                {'network_graph': network},
                                context_instance=RequestContext(request))


@login_required
def form(request):
    return render_to_response('networkgraph/form.html',
	    {'user_key':UserProfile.objects.get_or_create(user=request.user)[0].request_code,'url':request.get_host().split(':')[0]},
	    context_instance=RequestContext(request)
    )

@login_required
def data(request,network_id):
    try:
        network = NetworkGraph.objects.get(pk=network_id)
    except NetworkGraph.DoesNotExist:
        raise Http404

    if request.user.id is not network.user.id:
        raise PermissionDenied

    if network.complete == True:
	data = network.graph_data	
    else:
	data = json.dumps(None)

    return HttpResponse(data, mimetype='application/json')
