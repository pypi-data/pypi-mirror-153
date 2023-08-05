from qvsr._builtin import Page
from qvsr.models import Constants


class SP0(Page):
    template_name = 'qvsr/SP.html'
    form_model = 'player'
    form_fields = ['participant_name', 'participant_age', 'location']


class PreferencesPage(Page):
    form_model = 'player'
    form_fields = []

    for category in Constants.categories:
        form_fields.append(category['code'])

    def generate_categories(self):
        my_categories = []

        for c in Constants.categories:
            my_categories.append({'code': c['code'], 'label': c['label']})
        return my_categories

    def vars_for_template(self):
        return {'categories': self.generate_categories(),
                'total_votes': Constants.total_vote_credits
                }

    def js_vars(self):
        return dict(
            totalVotes=Constants.total_vote_credits
        )

    def error_message(self, values):
        sum = 0

        for v in list(values.values()):
            sum += v ** 2

        if sum > Constants.total_vote_credits:
            return 'You have exceeded the maximum number of votes.'
        elif sum == 0:
            return 'You have to select at least one category.'
        else:
            pass


class SurveyPage(Page):
    form_model = 'player'

    def generate_filtered_categories(self):
        categories = []
        for c in Constants.categories:
            if getattr(self.player, c['code']) != 0:
                categories.append({'code': c['code'], 'label': c['label'], 'questions': c['questions']})
        self.participant.vars['categories'] = categories

        return categories

    def get_form_fields(self):
        form_fields = []
        for c in self.generate_filtered_categories():
            for q in c['questions']:
                form_fields.append(q['name'])
        return form_fields

    def error_message(self, values):
        categories_sums = []
        for c in self.participant.vars['categories']:
            sum = 0
            for q in c['questions']:
                sum += values[q['name']] ** 2
            categories_sums.append(sum)
            if sum > 100:
                break
        if any(x > 100 for x in categories_sums):
            return 'You have exceeded the maximum number of votes.'

    def vars_for_template(self):

        return {
            'categories': self.participant.vars['categories'],
            'total_votes': Constants.total_vote_credits
        }

    def js_vars(self):
        return dict(
            totalVotes=Constants.total_vote_credits
        )


class EndPage(Page):
    pass


page_sequence = [SP0, PreferencesPage, EndPage]
