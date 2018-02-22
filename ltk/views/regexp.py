import re
import time

from django.shortcuts import render
from django.views import View

from ltk.forms import RegexpForm

class Regexp(View):
    form_class = RegexpForm
    initial = {'key': 'value'}
    template_name = 'regexp.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 'index': 0})

    def get_next_match(self):
        index = self.index
        while index:
            try:
                match = self.match_iter.__next__()
            except StopIteration:
                pass
            index -= 1
        start_time = time.time()
        try:
            match = self.match_iter.__next__()
            end_time = time.time()
            self.result.append ('{0}, {1}, {2}, {3:.2f}'.format(match.group(0),match.start(), match.end()-match.start(), end_time - start_time))
        except StopIteration:
            end_time = time.time()            
            self.result.append ('End, Elapsed Time (s): {0:0.2f}'.format(end_time - start_time))                            

    def post(self, request, *args, **kwargs):
        self.form = self.form_class(request.POST)
        self.index = 0
        self.result = []
        if self.form.is_valid():
            data = self.form.cleaned_data
            self.regex = data['search_pattern']
            self.regex_group_index = dict((v,k) for k,v in self.regex.groupindex.items())
            self.text = data['text']
            if 'match' in request.POST or 'next' in request.POST:
                self.result = ['Value, Index, Length, ElapsedTime(s)']
                self.match_iter = self.regex.finditer(self.text)
            if 'match' in request.POST:
                self.get_next_match()
                self.index += 1
            elif 'next' in request.POST:
                self.index = int(request.POST.get('index', 0))
                self.get_next_match()
                self.index += 1
            elif 'replace' in request.POST:
                self.replace_pattern = data['replace_pattern']
                """ validation of search_pattern includes compilation as a side effect
                self.result = [re.sub(self.search_pattern, self.replace_pattern, self.text)]
                """
                self.result = [self.regex.sub(self.replace_pattern, self.text)]
            elif 'split' in request.POST:
                """ validation of search_pattern includes compilation as a side effect
                for s in re.split(self.search_pattern, self.text):
                """
                for s in self.regex.split(self.text):
                    self.result.append(s)

            # <process form cleaned data>
            # return HttpResponseRedirect('/success/')
        return render(request, self.template_name, {'form': self.form, 'index': self.index, 'result': '<br>'.join(self.result)})
