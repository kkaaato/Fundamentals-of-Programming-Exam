
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'Frostyyy'
prelim = None
midterm = None
final = None
# Home page
@app.route('/')
def home():
    return render_template('Home.html')

# Function for Prelim Grade Calculation
@app.route('/prelim', methods=['GET', 'POST'])
def prelim():
    result = {}
    if request.method == 'POST':
        try:
            absences = int(request.form['absences'])
            prelim_exam = float(request.form['prelim_exam'])
            quizzes = float(request.form['quizzes'])
            requirements = float(request.form['requirements'])
            recitation = float(request.form['recitation'])

            if absences < 0 or prelim_exam < 0 or quizzes < 0 or requirements < 0 or recitation < 0:
                result['error'] = "All inputs must be non-negative."
            elif prelim_exam > 100 or quizzes > 100 or requirements > 100 or recitation > 100:
                result['error'] = "Grades must be between 0 and 100."
            elif absences >= 4:
                result['status'] = "FAILED due to excessive absences."
            else:
                attendance = max(0, 100 - absences * 10)
                class_standing = quizzes * 0.4 + requirements * 0.3 + recitation * 0.3
                prelim_grade = prelim_exam * 0.6 + attendance * 0.1 + class_standing * 0.3
                session['prelim_grade'] = prelim_grade

                required_midterm_pass = (75 - prelim_grade * 0.2 - 0.5 * 75) / 0.3
                required_midterm_deans = (90 - prelim_grade * 0.2 - 0.5 * 90) / 0.3

                required_final_pass = (75 - prelim_grade * 0.2 - 0.3 * 75) / 0.5
                required_final_deans = (90 - prelim_grade * 0.2 - 0.3 * 90) / 0.5

                result['prelim_grade'] = round(prelim_grade, 2)
                result['required_midterm_pass'] = round(required_midterm_pass, 2)
                result['required_midterm_deans'] = round(required_midterm_deans, 2)
                result['required_final_pass'] = round(required_final_pass, 2)
                result['required_final_deans'] = round(required_final_deans, 2)
        except ValueError:
            result['warning'] = "Invalid input. Please enter numeric values."
    return render_template('prelim.html', result=result)

@app.route('/midterm', methods=['GET', 'POST'])
def midterm():
    result = {}
    prelim = session.get('prelim_grade', 0)
    if request.method == 'POST':
        # Shows a warning if prelim grade is missing
        if prelim is None or prelim == 0:
            result['warning'] = "Missing grade. Please access the Prelim Calculator first."
        else:
            try:
                absences = int(request.form['absences'])
                midterm_exam = float(request.form['midterm_exam'])
                quizzes = float(request.form['quizzes'])
                requirements = float(request.form['requirements'])
                recitation = float(request.form['recitation'])

                if absences < 0 or midterm_exam < 0 or quizzes < 0 or requirements < 0 or recitation < 0:
                    result['error'] = "All inputs must be non-negative."
                elif midterm_exam > 100 or quizzes > 100 or requirements > 100 or recitation > 100:
                    result['error'] = "Grades must be between 0 and 100."
                elif absences >= 4:
                    result['status'] = "FAILED due to excessive absences."
                else:
                    attendance = max(0, 100 - absences * 10)
                    class_standing = quizzes * 0.4 + requirements * 0.3 + recitation * 0.3
                    midterm_grade = midterm_exam * 0.6 + attendance * 0.1 + class_standing * 0.3
                    session['midterm_grade'] = midterm_grade

                    required_final_pass = (75 - prelim * 0.2 - midterm_grade * 0.3) / 0.5
                    required_final_deans = (90 - prelim * 0.2 - midterm_grade * 0.3) / 0.5

                    result['midterm_grade'] = round(midterm_grade, 2)
                    result['prelim_grade'] = round(prelim, 2)
                    result['required_final_pass'] = round(required_final_pass, 2)
                    result['required_final_deans'] = round(required_final_deans, 2)
            except ValueError:
                result['error'] = "Invalid input. Please enter numeric values."
    return render_template('midterm.html', result=result)

# Function for Final Grade Calculation
@app.route('/final', methods=['GET', 'POST'])
def final():
    result = {}
    prelim = session.get('prelim_grade', 0)
    midterm = session.get('midterm_grade', 0)
    if request.method == 'POST':
        # Show a warning if prelim or midterm grade are missing
        if prelim == 0 or midterm == 0:
            result['warning'] = "Prelim and/or Midterm grades are missing. Access those first."
        else:
            try:
                absences = int(request.form['absences'])
                final_exam = float(request.form['final_exam'])
                quizzes = float(request.form['quizzes'])
                requirements = float(request.form['requirements'])
                recitation = float(request.form['recitation'])

                if absences < 0 or final_exam < 0 or quizzes < 0 or requirements < 0 or recitation < 0:
                    result['error'] = "All inputs must be non-negative."
                elif final_exam > 100 or quizzes > 100 or requirements > 100 or recitation > 100:
                    result['error'] = "Grades must be between 0 and 100."
                elif absences >= 4:
                    result['status'] = "FAILED due to excessive absences."
                else:
                    attendance = max(0, 100 - absences * 10)
                    class_standing = quizzes * 0.4 + requirements * 0.3 + recitation * 0.3
                    final_term = final_exam * 0.6 + attendance * 0.1 + class_standing * 0.3
                    final_grade = prelim * 0.2 + midterm * 0.3 + final_term * 0.5

                    result['final_term'] = round(final_term, 2)
                    result['final_grade'] = round(final_grade, 2)
                    result['prelim_grade'] = round(prelim, 2)
                    result['midterm_grade'] = round(midterm, 2)
            except ValueError:
                result['error'] = "Invalid input. Please enter numeric values."
    return render_template('final.html', result=result)

# Function to clear grades
@app.route('/clear', methods=['POST'])
def clear_grades():
    session.pop('prelim_grade', None)
    session.pop('midterm_grade', None)
    session.pop('final_grade', None)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
