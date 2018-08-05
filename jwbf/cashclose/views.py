from django.shortcuts import render
from django.views import generic

# Create your views here.

from .models import Store,Statement

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_statements = Statement.objects.all().count()


    context = {
        'num_statements': num_statements,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class StatementListView(generic.ListView):
    model = Statement
    paginate_by = 10

class StatementDetailView(generic.DetailView):
    model = Statement
