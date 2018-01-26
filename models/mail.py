from models import Model


class Mail(Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
            ('content', str, ''),
            ('sender_id', str, 0),
            ('receiver_id', str, 0),
            ('sender_user', str, ''),
            ('receiver_user', str, ''),
            ('topic_id', str, '')
        ]
        return names
