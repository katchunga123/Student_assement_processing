import csv
import sys

def read_student_data(filename):
    """
    Reads student data from a CSV file.
    
    Args:
        filename (str): The name of the CSV file containing the student data.

    Returns:
        list: A list of dictionaries containing student data (name, math, science, english scores).
    """
    data = []

    try:
        # Open the CSV file for reading
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header (first row)

            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Skip rows that don't have enough data
                if len(row) < 4:
                    print(f"Incomplete data in row: {row}")
                    continue
                try:
                    # Ensure the scores are integers and handle any non-integer input
                    data.append({
                        'name': row[0],
                        'math': int(row[1]),
                        'science': int(row[2]),
                        'english': int(row[3])
                    })
                except ValueError as e:
                    # Handle case where the score is not an integer
                    print(f"Invalid data in row {row}: {e}")
                    print("Only integer scores are allowed. Goodbye!")
                    sys.exit(1)  # Exit the program with status 1 (error)

    except FileNotFoundError:
        # Handle case when the file is not found
        print(f"Error: {filename} not found.")
        print("Goodbye!")
        sys.exit(1)  # Exit the program with status 1 (error)
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")
        print("Goodbye!")
        sys.exit(1)  # Exit the program with status 1 (error)

    return data


def calculate_average(student):
    """
    Calculates the average score for a student.
    
    Args:
        student (dict): The dictionary containing student data (name, scores for math, science, english).

    Returns:
        float: The average score for the student, or None if data is missing.
    """
    try:
        # Calculate the total score by summing up individual subject scores
        total = student['math'] + student['science'] + student['english']
        # Calculate the average by dividing total by the number of subjects (3)
        average = total / 3
        return average
    except KeyError as e:
        # Handle case if some data (e.g., scores) is missing for the student
        print(f"Missing data for {e}")
        return None


def assign_grade(score):
    """
    Assigns a letter grade based on a student's score.
    
    Args:
        score (float): The score of the student.

    Returns:
        str: The letter grade (A, B, C, D, E, or F) based on the score.
    """
    # Determine the grade based on score
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    elif score >= 50:
        return "E"
    else:
        return "F"


def calculate_min_max_range(student_scores):
    """
    Calculates the minimum, maximum, and range for a given list of student scores.
    
    Args:
        student_scores (list): A list of student scores for math, science, and english.

    Returns:
        tuple: A tuple containing the minimum score, maximum score, and range (max - min).
    """
    min_score = min(student_scores)
    max_score = max(student_scores)
    score_range = max_score - min_score
    return min_score, max_score, score_range


def process_student_results(students_data):
    """
    Processes student data, calculates averages, grades, and additional statistics, and returns the results.
    
    Args:
        students_data (list): A list of dictionaries containing student data.

    Returns:
        list: A list of dictionaries containing student results (scores, averages, grades, pass/fail).
    """
    results = []

    for student in students_data:
        # Get the scores for math, science, and english
        student_scores = [student['math'], student['science'], student['english']]
        
        # Calculate the average score for the student
        average = calculate_average(student)
        if average is not None:
            # Assign a grade based on the average score
            grade = assign_grade(average)
            
            # Calculate the minimum, maximum, and range of scores
            min_score, max_score, score_range = calculate_min_max_range(student_scores)
            
            # Determine if the student passed or failed
            pass_fail = "Congratulations, you passed!" if average >= 50 else "Fail"
            
            # Create a dictionary with the student's data and calculated results
            student_results = {
                'name': student['name'],
                'math': student['math'],
                'science': student['science'],
                'english': student['english'],
                'average': average,
                'grade': grade,
                'min_score': min_score,
                'max_score': max_score,
                'score_range': score_range,
                'pass_fail': pass_fail  # Added pass/fail message
            }
            results.append(student_results)

    return results


def write_results_to_csv(results, filename):
    """
    Writes the processed student results to a new CSV file.
    
    Args:
        results (list): A list of dictionaries containing student results.
        filename (str): The name of the CSV file to save the results.
    """
    if results:
        # Define the header for the CSV file
        header = ['name', 'math', 'science', 'english', 'average', 'grade', 'min_score', 'max_score', 'score_range', 'pass_fail']
        
        # Open the CSV file for writing
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()  # Write the header row
            writer.writerows(results)  # Write the student results

        print(f"Results written to {filename}")
    else:
        print("No results to write.")


if __name__ == "__main__":
    # The name of the input CSV file containing student data
    filename = "students.csv"  # Replace with your actual CSV file name
    students_data = read_student_data(filename)

    if students_data:
        # Process the student data to calculate averages and grades
        results = process_student_results(students_data)
        # Write the processed results to a new CSV file
        write_results_to_csv(results, 'student_results.csv')

    print("Goodbye!")  # Exit message before ending the program