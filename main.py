from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired
import csv
from wtforms import Form, URLField
from wtforms.validators import InputRequired, URL

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[InputRequired()])
    Location = URLField(label='Location URL', validators=[InputRequired(),
                                                          URL(require_tld=True,
                                                              message='Invalid URL')])
    open_time = StringField(label='open time', validators=[InputRequired()])
    close = StringField(label='closing time', validators=[InputRequired()])
    coffee = SelectField(label='coffee rating', validators=[InputRequired()],
                         choices=[('☕', '☕'), ('☕☕', '☕☕'),
                                  ('☕☕☕', '☕☕☕'),
                                  ('☕☕☕☕', '☕☕☕☕'),
                                  ('☕☕☕☕☕', '☕☕☕☕☕')
                                  ])
    wifi = SelectField('wifi rating', choices=[('✘', '✘'), ('💪', '💪'), ('💪💪',
                                                                        '💪💪'),
                                               ('💪💪💪', '💪💪💪'),
                                               ('💪💪💪💪', '💪💪💪💪'),
                                               ('💪💪💪💪💪', '💪💪💪💪💪')
                                               ], validators=[InputRequired()])
    power = SelectField('power outlet',
                        choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌',
                                                          '🔌🔌'),
                                 ('🔌🔌🔌', '🔌🔌🔌'),
                                 ('🔌🔌🔌🔌', '🔌🔌🔌🔌'),
                                 ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')
                                 ], validators=[InputRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["get", "post"])
def add_cafe():
    form = CafeForm(meta={'csrf': False})
    if form.validate_on_submit():
        data_list = []
        for data in form.data.values():
            if data == True:
                pass
            else:
                data_list.append(data)
        print(data_list)
        with (open('cafe-data.csv','a', newline='', encoding='utf-8') as
              csv_file):
            csv_data = csv.writer(csv_file)
            csv_data.writerow(data_list)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
