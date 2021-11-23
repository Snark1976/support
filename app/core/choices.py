from djchoices import DjangoChoices, ChoiceItem


class StatusTicket(DjangoChoices):
    opened = ChoiceItem("O")
    on_hold = ChoiceItem("H")
    awaiting_reply = ChoiceItem("R")
    completed = ChoiceItem("C")
