from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget ,  CheckboxInput

class MultipleCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)  # prefix_lable=True: checkbox after lable| li tag / instead of select tag
    option_widget = CheckboxInput()                                                   # input tag with checkbox type / instead of option tag  