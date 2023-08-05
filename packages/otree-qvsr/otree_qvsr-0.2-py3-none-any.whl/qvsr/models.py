from otree.api import BaseConstants, BaseSubsession, BaseGroup, BasePlayer, models

author = 'josephnoblepal@gmail.com'

doc = """
QVSR Model Demo
"""

categories = [
    {"code": "q_1", "label": "Job opportunities for youths"},
    {"code": "q_2", "label": "Water supply in your location"},
    {"code": "q_3", "label": "Social Amenities"},
    {"code": "q_4", "label": "Road network"},
    {"code": "q_5", "label": "Agricultural products and veterinary services"},
]


class Constants(BaseConstants):
    name_in_url = 'qvsr'
    survey_default_title = "QVSR Survey Demo"
    total_vote_credits = 100
    players_per_group = None
    num_rounds = 1
    categories = sorted(categories, key=lambda x: x['label'])


class Subsession(BaseSubsession):
    def creating_session(self):
        if 'Survey_Title' in self.session.config:
            self.session.config['survey_title'] = self.session.config['Survey_Title']
        else:
            self.session.config['survey_title'] = Constants.survey_default_title

    def vars_for_admin_players(self):
        return dict(payoffs='none')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participant_name = models.StringField(label='What is your name?')
    participant_age = models.IntegerField(label='How old are you?')
    location = models.CharField(label='What is your location?')

    for category in Constants.categories:
        locals()[category['code']] = models.IntegerField(label=category['label'], min=-10, max=10, initial=0)

    del category

    def get_player_data(self):
        res = dict()
        p = self
        question_names = []
        answers = []

        category_labels = []

        for c in categories:
            question_names.append(c['code'])
            category_labels.append(c['label'])

        for q in question_names:
            answers.append(getattr(p, q) * getattr(p, q))  # find the quadratic value of the answer

        res['answers'] = dict(zip(category_labels, answers))

        return res
