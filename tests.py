from pprint import pprint

from services import get_day_schedule


pprint(get_day_schedule('понедельник', 'числитель'))
print('-----------')
pprint(sorted(get_day_schedule('понедельник', 'числитель'), key=lambda obj: obj['time']))