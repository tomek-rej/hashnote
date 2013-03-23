from hashnote_ui.models import HashNote, Filter
from hashnote_ui.helper import FilterProcessor
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

def index(request):
    """
    The main view in the application. It renders the main page.
    """
    filter_processor = FilterProcessor()
    filter_value = request.POST.get('filter')
    warning_message = request.session.pop('warning', '')
    if filter_value is None:
        filter_value = filter_processor.get_filter_value()

    if filter_value is not None:
        if not filter_value.startswith('#') and filter_value != '':
            filter_value = '#{0}'.format(filter_value)
        Filter(term=filter_value).save()

    #Only filter the hashnotes if there was a search term passed through and if
    #the search term was not an empty string.
    hashnotes = HashNote.objects
    hashnotes = hashnotes.order_by('-created_at')
    if filter_value:
        hashnotes = filter_processor.coarse_filter_using_hashtag(hashnotes, filter_value)
        hashnotes = filter_processor.fine_filter_using_hashtag(hashnotes, filter_value)

    context = {
        'recent_hashnotes': hashnotes,
        'warning_message': warning_message
    }
    return render(request, 'hashnote_ui/index.html', context)

def add_note(request):
    """
    This view allows a user to add a hashnote. It then gets saved to the database
    and redirects the user to the home page.
    """
    content = request.POST.get('content')

    #Handle the case where the value entered into the text field is empty string.
    if not content:
        request.session['warning'] = 'Hashnote not added must enter a note'
        return index(request) #Render the index view with a custom warning message.
    else:
        note = HashNote(content=content, created_at=datetime.datetime.utcnow())
        note.save()
        return HttpResponseRedirect(reverse('hashnote_ui.views.index'))
