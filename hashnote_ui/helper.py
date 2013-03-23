from hashnote_ui.models import Filter

class FilterProcessor:

    def coarse_filter_using_hashtag(self, hashnotes, filter_value):
        """
        This function finds all records in the HashNote table that contain the
        term <filter_value>
        """
        return hashnotes.filter(content__icontains=filter_value)

    def split_non_alphanumeric(self, old_string):
        """
        This function takes a string and breaks it into alphanumeric tokens.
        For instance '#abc!#def,#ghi' would return [#abc, #def, #ghi]
        Note that the hash character is a special case as that denotes a tag.
        """
        new_string = ''
        for i in xrange(len(old_string)):
            if old_string[i] == '#':
                new_string += ' #'
            elif not old_string[i].isalnum():
                new_string += ' '
            else:
                new_string += old_string[i]
        return new_string.split()

    def fine_filter_using_hashtag(self, hashnotes, filter_value):
        return [note for note in hashnotes
                if filter_value in self.split_non_alphanumeric(note.content)]

    def get_filter_value(self):
        """
        Returns the stored filter term or None if it doesn't exist in the database
        """
        filter_record = Filter.objects
        if not filter_record.count():
            return None
        return filter_record.values()[0]['term']
