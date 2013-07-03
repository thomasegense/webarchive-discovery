from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
import pprint
import solr

solr_url = "http://localhost:8080/discovery"
#solr_url = "http://192.168.45.10:8983/solr/aadda-discovery"

s = solr.Solr(solr_url)
s.select = solr.SearchHandler(s, "/select","__")

# Create your views here.

def search(request):
  q = request.GET.get('q', "*")

  r = s.select(
    q, facet='true', facet__sort='count',
    facet__field=['crawl_year', 'content_type', 'content_ffb'],
    facet__mincount=1, f__crawl_year__facet__mincount=0)

  return render_to_response('search_result_list.html', {'numFound': r.numFound, 'r': r, 'facets': r.facet_counts['facet_fields']})
