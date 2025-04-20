import csv
from collections import defaultdict
from datetime import datetime

# Function to load attendance data from the CSV file
def load_attendance_data(filename):
    attendance_data = defaultdict(lambda: defaultdict(list))  # Nested dictionary {date: {hour: [students]}}
    student_data = defaultdict(list)  # To track student-specific attendance {student_name: [(date, hour)]}

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header

        for row in reader:
            student, date, time = row
            hour = time.split(":")[0]  # Extract the hour from the time
            attendance_data[date][hour].append(student)
            student_data[student].append((date, hour))
    
    return attendance_data, student_data

# Function to view the statistics date-wise
def view_attendance_date_wise(attendance_data):
    print("Attendance Statistics (Date-wise):\n")
    for date, hours in sorted(attendance_data.items()):
        print(f"Date: {date}")
        for hour, students in sorted(hours.items()):
            print(f"  Hour {hour}: {len(students)} students present")
            for student in students:
                print(f"    - {student}")
        print("\n")

# Function to view the statistics hour-wise
def view_attendance_hour_wise(attendance_data):
    print("Attendance Statistics (Hour-wise):\n")
    hour_data = defaultdict(list)  # {hour: [students]} for all dates
    
    # Collect all the students who attended each hour across all dates
    for date, hours in attendance_data.items():
        for hour, students in hours.items():
            hour_data[hour].extend(students)
    
    for hour, students in sorted(hour_data.items()):
        print(f"Hour {hour}: {len(students)} students present")
        for student in students:
            print(f"    - {student}")
        print("\n")

# Function to view student-specific attendance by date or hour
def view_student_attendance(student_data):
    student_name = input("Enter the student's name to view their attendance: ")
    if student_name in student_data:
        print(f"\nAttendance for {student_name}:\n")
        
        # Ask user for the type of statistics
        user_choice = input("Enter '1' for Date-wise attendance or '2' for Hour-wise attendance: ")
        
        if user_choice == '1':  # View date-wise attendance for the student
            date_data = defaultdict(list)  # {date: [hours]}
            for date, hour in student_data[student_name]:
                date_data[date].append(hour)

            for date, hours in sorted(date_data.items()):
                print(f"  Date: {date}")
                for hour in sorted(hours):
                    print(f"    - Hour: {hour}")
        
        elif user_choice == '2':  # View hour-wise attendance for the student
            hour_data = defaultdict(list)  # {hour: [dates]}
            for date, hour in student_data[student_name]:
                hour_data[hour].append(date)

            for hour, dates in sorted(hour_data.items()):
                print(f"  Hour: {hour}")
                for date in sorted(dates):
                    print(f"    - Date: {date}")
        
        else:
            print("Invalid choice. Please enter '1' for Date-wise or '2' for Hour-wise attendance.")
    else:
        print(f"No attendance data found for {student_name}.\n")

# Main execution
if __name__ == "__main__":
    # Load the attendance data
    attendance_data, student_data = load_attendance_data('attendance_log.csv')

    # Ask the user what type of statistics they want to view
    user_choice = input("Enter '1' for Date-wise attendance, '2' for Hour-wise attendance, or '3' for Student-specific attendance: ")

    if user_choice == '1':
        view_attendance_date_wise(attendance_data)
    elif user_choice == '2':
        view_attendance_hour_wise(attendance_data)
    elif user_choice == '3':
        view_student_attendance(student_data)
    else:
        print("Invalid choice. Please enter '1', '2', or '3'.")
