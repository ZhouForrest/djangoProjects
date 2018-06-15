import random


def get_ticket():
    str = 'kl,tryuio567890xqddsfcvbnm,piuytrdfnm,lkfghj,nb'
    ticket = ''
    for _ in range(35):
        ticket += random.choice(str)
    return ticket