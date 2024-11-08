


# Lists to store student, course, and grade information
students = []
courses = []
grades = []

# Load initial data from files
def load_data():
    try:
        # Load student data
        with open('students.txt', 'r') as students_file:
            for line in students_file:
                values = line.strip().split(',')
                students.append([values[0], values[1], int(values[2]), float(values[3])])

        # Load course data
        with open('courses.txt', 'r') as courses_file:
            for line in courses_file:
                values = line.strip().split(',')
                courses.append([values[0], values[1], int(values[2])])

        # Load grade data
        with open('grades.txt', 'r') as grades_file:
            for line in grades_file:
                values = line.strip().split(',')
                grades.append([values[0], values[1], values[2]])

    except FileNotFoundError:
        pass  # Files will be created when data is added for the first time

# Function to save student data to a file
def save_students():
    with open('students.txt', 'w') as students_file:
        for s in students:
            students_file.write(f"{s[0]},{s[1]},{s[2]},{s[3]}\n")

# Function to save course data to a file
def save_courses():
    with open('courses.txt', 'w') as courses_file:
        for c in courses:
            courses_file.write(f"{c[0]},{c[1]},{c[2]}\n")

# Function to save grade data to a file
def save_grades():
    with open('grades.txt', 'w') as grades_file:
        for g in grades:
            grades_file.write(f"{g[0]},{g[1]},{g[2]}\n")

# Function to get information about a specific student
def get_student_info(student_id):
    student_id = str(student_id)  # Convert to string for comparison
    for st in students:
        if st[0] == student_id:
            # Student found
            student_name = st[1]
            gpa = st[3]

            # Find courses and grades for the student
            student_grades = []
            for grade in grades:
                if grade[0] == student_id:
                    student_grades.append((grade[1], grade[2]))

            student_info = {"Name": student_name, "GPA": gpa, "Courses": student_grades}
            return student_info

    # Student not found
    return None

# Function to get a list of students who passed a specific course
def Passed_course(course_number):
    passed_students = []
    for grade in grades:
        if grade[1] == course_number and grade[2] != 'F':
            for student in students:
                if student[0] == grade[0]:
                    passed_students.append(student[1])
    return passed_students

# Function to get the grade from the user
def get_grades():
    grade = input('Enter student grade:')
    if grade == 'A':
        points = 4
    elif grade == 'B':
        points = 3
    elif grade == 'C':
        points = 2
    elif grade == 'D':
        points = 1
    elif grade == 'F':
        points = 0
    else:
        print('Enter a valid grade!')
        return get_grades()
    print(points)
    return grade

# Function to add a grade for a student
def AddGrade():
    # Get student ID from the user
    student_id = input("Student ID: ")
    student_info = get_student_info(student_id)

    if student_info:
        # Display student information
        print(f"Student ID: {student_id}")
        print(f"Student name: {student_info['Name']}")
        
        # Get course code from the user
        course_code = input("Course code: ")
        course_info = None
        for course in courses:
            if course[0] == course_code:
                course_info = course
                break
        
        if course_info:
            # Display course information
            print(f"Course code: {course_info[0]}")
            print(f"Course name: {course_info[1]}")
            
            # Check if the grade for this course and student already exists
            existing_grades = [g[2] for g in grades if g[0] == student_id and g[1] == course_code]
            if existing_grades:
                print(f"Grade already exists for this course and student: {existing_grades[0]}")
            else:
                # Get a valid grade from the user
                valid_grade = False
                while not valid_grade:
                    grade = get_grades().upper()
                    if grade in ['A', 'B', 'C', 'D', 'F']:
                        valid_grade = True
                    else:
                        print("Invalid grade. Try again.")
                
                # Save data to grades list
                grades.append([student_id, course_code, grade])
                
                # Update GPA and save to students.txt
                update_gpa(student_id)
                
                # Save data to grades.txt
                save_grades()
                
                print("Grade added successfully.")
        else:
            print("There is no course with this code.")
    else:
        print("There is no student with this ID.")
    
    main()  # Return to the main menu

# Function to update the GPA for a student
def update_gpa(student_id):
    total_points = 0
    total_credits = 0
    
    for grade in grades:
        if grade[0] == student_id:
            for course in courses:
                if course[0] == grade[1]:
                    points = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}.get(grade[2], 0)
                    total_points += points * course[2]
                    total_credits += course[2]

    if total_credits > 0:
        gpa = total_points / total_credits
        for student in students:
            if student[0] == student_id:
                student[3] = gpa

        # Write the updated data for all students to the file
        save_students()

# Function to add a new student
def AddStudent():
    student_id = input('Enter student id: ')
    student_id = str(student_id)
    stuexist = False
    gpa = float(0)
    
    # Check if the student ID already exists
    for student in students:
        if student[0] == student_id:
            stuexist = True
            print('There is already a student with that id')
            main()  # Return to the main menu

    if not stuexist:
        name = input('Enter student name: ')
        mobile = int(input('Enter student mobile: '))
        
        # Add new student to the list
        students.append([student_id, name, mobile, gpa])
        
        # Save data to students.txt
        save_students()
        
        main()  # Return to the main menu

# Function to add a new course
def AddCourse():
    course_no = input('Enter course number: ')
    course_no = str(course_no)
    course_no = course_no.lower()
    course_exist = False
    
    # Check if the course number already exists
    for course in courses:
        if course[0] == course_no:
            course_exist = True
            print('There is already a course with that number')
            main()  # Return to the main menu

    if not course_exist:
        name = input('Enter course name: ')
        credits = int(input('Enter course credits: '))
        
        # Add new course to the list
        courses.append([course_no, name, credits])
        
        # Save data to courses.txt
        save_courses()
        
        main()  # Return to the main menu

# Function to calculate GPA for a specific student
def GPA():
    total_points = 0
    total_credits = 0

    # Iterate through grades to calculate GPA
    with open('grades.txt', 'r') as grades_file:
        for line in grades_file:
            values = line.strip().split(',')
            student_id = values[0]
            course_num = values[1]
            grade = values[2].strip()  # Strip to remove newline characters
            
            for course in courses:
                if course[0] == course_num:
                    points = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}.get(grade, 0)
                    total_points += points * course[2]
                    total_credits += course[2]

    if total_credits > 0:
        gpa = total_points / total_credits
        print(f"GPA for student {student_id}: {gpa}")
    else:
        print("No grades found for GPA calculation.")

# Function to exit the program
def exit_():
    print("Exiting the program.")

# Function to get the course name for a specific course code
def get_course_name(course_code):
    for course in courses:
        if course[0] == course_code:
            return course[1]
    return None

# Function to display a student's transcript
def show_transcript():
    student_id = input("Student ID: ")
    student_info = get_student_info(student_id)

    if student_info:
        print(f"\nStudent ID: {student_id}")
        print(f"Name: {student_info['Name']}")
        print(f"GPA: {student_info['GPA']:.2f}\n")

        if 'Courses' in student_info and student_info['Courses']:
            for course, grade in student_info['Courses']:
                course_name = get_course_name(course)
                if course_name:
                    print(f"{course} {course_name} {grade}")
                else:
                    print(f"{course} (Unknown Course) {grade}")
        else:
            print("No course information available.")
    else:
        print("There is no student with this ID.")

    # Return to the main menu
    main()

# Function to show students who passed a specific course
def show_passed_students():
    course_code = input("Course code: ")
    course_name = get_course_name(course_code)

    if course_name:
        passed_students = Passed_course(course_code)

        if passed_students:
            print(f"\nCourse code: {course_code}")
            print(f"Course name: {course_name}\n")
            for student in passed_students:
                print(student)
        else:
            print(f"No students have passed the course {course_code}.")
    else:
        print("There is no course with this code.")
        main()  # Return to the main menu

# Main function to display the menu and handle user input
def main():
    try:
        print('Please select one of the following')
        print('1- Add new student')
        print('2- Add new course')
        print('3- Add new grade')
        print('4- Show a student\'s transcript')
        print('5- Show students that have passed a course')
        print('6- Exit')
        choice = int(input('Your Choice: '))
        
        while choice < 1 or choice > 6:
            choice = int(input('Invalid choice. Your Choice: '))
        
        if choice == 1:
            AddStudent()
        elif choice == 2:
            AddCourse()
        elif choice == 3:
            AddGrade()
        elif choice == 4:
            show_transcript()
        elif choice == 5:
            show_passed_students()
        elif choice == 6:
            exit_()
    except ValueError:
        print('Please enter a valid choice.')
        main()

# Load data at the beginning
load_data()

# Start the program
main()
