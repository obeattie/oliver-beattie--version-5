"""Views for the links application."""
from django.shortcuts import render_to_response
from django.template import RequestContext

from obeattie.links import forms as links_forms, models as links_models

def quick_add(request):
    """View for 'quickly adding' a link."""
    if request.method == 'POST':
        form = links_forms.QuickAddForm(request.POST, initial=request.GET)
    else:
        form = links_forms.QuickAddForm(initial=request.GET)
    
    if form.is_bound and form.is_valid():
        # Go ahead and add the linky
        assert False
    else:
        # Display the form
        return render_to_response('links/quick_add.html', {
            'form': form,
        }, context_instance=RequestContext(request))
