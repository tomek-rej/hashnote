from django.test import TestCase
from hashnote_ui.helper import FilterProcessor
from hashnote_ui.models import HashNote, Filter
from hashnote_ui.views import add_note, index

class MockRequest:
    POST = {}
    META = {}
    session = {}

class FilterTest(TestCase):
    hashnotes = []
    hashnotes.append(HashNote(content='#cat,#dog'))
    hashnotes.append(HashNote(content='dog'))
    hashnotes.append(HashNote(content='#abc'))
    hashnotes.append(HashNote(content='#abc#def'))
    hashnotes.append(HashNote(content='#a?b#c3!#d'))
    filter_processor = FilterProcessor()

    def setUp(self):
        pass

    def test_split_non_alphanumeric_empty(self):
        result = self.filter_processor.split_non_alphanumeric('')
        self.assertEqual(result, [])

    def test_split_non_alphanumeric_one_tag(self):
        result = self.filter_processor.split_non_alphanumeric('#abc')
        self.assertEqual(result, ['#abc'])

    def test_split_non_alphanumeric_comma_separated_tags(self):
        result = self.filter_processor.split_non_alphanumeric('#abc,#def')
        self.assertEqual(result, ['#abc', '#def'])

    def test_split_non_alphanumeric_one_tag_one_text(self):
        result = self.filter_processor.split_non_alphanumeric('#ab+c')
        self.assertEqual(result, ['#ab', 'c'])

    def test_split_non_alphanumeric_hash(self):
        result = self.filter_processor.split_non_alphanumeric('#')
        self.assertEqual(result, ['#'])

    def test_fine_filter_using_hashtag(self):
        result = self.filter_processor.fine_filter_using_hashtag(self.hashnotes, '#abc')
        self.assertEqual(len(result), 2)

    def test_fine_filter_using_hashtag_with_number(self):
        result = self.filter_processor.fine_filter_using_hashtag(self.hashnotes, '#c3')
        self.assertEqual(len(result), 1)

    def test_fine_filter_using_hashtag_after_hashtag(self):
        result = self.filter_processor.fine_filter_using_hashtag(self.hashnotes, '#def')
        self.assertEqual(len(result), 1)

class DatabaseTest(TestCase):
    def setUp(self):
        pass

    def test_insert_into_filter_table(self):
        """Should have only ever one entry
        """
        Filter(term='abc').save()
        last_value = Filter.objects.values()
        self.assertEqual(len(last_value), 1)
        self.assertEqual(last_value[0]['term'], 'abc')

        Filter(term='def').save()
        last_value = Filter.objects.values()
        self.assertEqual(len(last_value), 1)
        self.assertEqual(last_value[0]['term'], 'def')

    def test_delete_from_filter_table(self):
        """Should do nothing
        """
        f = Filter(term='abc')
        f.save()
        last_value = Filter.objects.values()
        self.assertEqual(len(last_value), 1)
        self.assertEqual(last_value[0]['term'], 'abc')
        f.delete()
        last_value = Filter.objects.values()
        self.assertEqual(len(last_value), 1)
        self.assertEqual(last_value[0]['term'], 'abc')

    def test_add_note(self):
        request = MockRequest()
        request.POST['content'] = 'abc'
        response = add_note(request)
        notes = HashNote.objects.values()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['content'], 'abc')

    def test_add_blank_note(self):
        """Should not add the note to the database
        """
        request = MockRequest()
        request.POST['content'] = ''
        response = add_note(request)
        notes = HashNote.objects.values()
        self.assertEqual(len(notes), 0)

class ViewTest(TestCase):
    def setUp(self):
        pass

    def test_add_note_view(self):
        request = MockRequest()
        request.POST['content'] = 'abc'
        response = add_note(request)
        self.assertEqual(response.status_code, 302)

    def test_index_view(self):
        request = MockRequest()
        request.POST['filter'] = 'abc'
        response = index(request)
        self.assertEqual(response.status_code, 200)
