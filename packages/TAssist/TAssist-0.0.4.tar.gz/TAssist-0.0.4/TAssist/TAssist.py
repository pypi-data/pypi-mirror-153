import json
import requests
import TAssist.TA_Graphs
import TAssist.TA_Globals

api_url = "https://api.pegasis.site/public/yrdsb_ta/getmark_v2"

class Mark:
    def __init__(self, name, data):
        if data is not None:
            # Strange fix to compensate for data being in list of size 1. idk why its like this
            data = data[0]
            self.type = name
            self.weight = data["weight"]
            self.score = data["get"]
            self.out_of = data["total"]
            self.finished = data["finished"]

            self.percent = round((self.score / self.out_of * 100), 2)
        else:
            self.type = False
            self.weight = False
            self.score = False
            self.out_of = False
            self.finished = False 
            self.percent = 0
    
    def __repr__(self):
        return f"Mark Object at {hex(id(self))}"

class Assignment:
    def __init__(self, data, course):
        self.course = course

        self.feedback = data["feedback"]
        self.name = data["name"]

        self.KU = Mark("KU", data.get("KU"))
        self.A = Mark("A", data.get("A"))
        self.T = Mark("T", data.get("T"))
        self.C = Mark("C", data.get("C"))

        self.F = Mark("F", data.get("F"))
        self.O = Mark("O", data.get("O"))

        self.marks = {
            "KU": self.KU,
            "A": self.A,
            "T": self.T,
            "C": self.C,
            "O": self.O,
            "F": self.F
        }

        exists = 0
        total = 0
        for mark in self.marks.values():
            if mark.percent: exists += 1
            total += mark.percent
        
        # Caluclate assignment average
        self.avg = total / exists

    def __repr__(self):
        return f"Assignment Object at {hex(id(self))}"

    def get_previous_assignment(self):
        work = self.course.assignments
        pos = work.index(self)
        if pos == 0: return None
        else: return work[pos-1]

    def compare_with_previous(self, cat):
        assignment = self.get_previous_assignment()
        if assignment is None: return ""
        else:
            now = self.marks[cat].percent
            before = assignment.marks[cat].percent

            if now and before:
                if now > before: return f"You scored *{now - before}% better* than your previous assignment: {assignment.name}"
                elif now < before: return f"You scored *{before - now}% worse* than your previous assignment: {assignment.name}"
                else: return ""

class Course:
    def __init__(self, data):
        self.name = data["name"]
        self.code = data["code"]
        self.start = data["start_time"]
        self.end = data["end_time"]
        self.block = data["block"]
        self.room = data["room"]
        self.weight_table = data["weight_table"]
        self.assignments = [Assignment(item, self) for item in data["assignments"]]
        self.assign_len = len(self.assignments)
        self.overall_mark = data["overall_mark"]

        if self.overall_mark is not None:
            self.overall_mark = float(self.overall_mark)

        self.emoji = TAssist.TA_Globals.course_emojis.get(self.code[:2])
        if self.emoji is None: self.emoji = '🏫'

    def __repr__(self):
        return f"Course Object at {hex(id(self))}"

    # For finding if a course identifies with some string. Compares against course block and code
    def __eq__(self, identifier):
        # Legnth check is to make sure a block number identifier wont trigger true on numbers in course code
        if (identifier.upper() in self.code) and (len(identifier) > 1): return True
        elif identifier == self.block: return True
        else: return False

    # Find if assignment exists
    def has_assignment(self, work):
        if work is not None:
            for assignment in self.assignments:
                if work.lower() in assignment.name.lower():
                    return assignment
        return False
    
    # Generates mark graph for
    def generate_mark_graph(self, output):
        graph = TAssist.TA_Graphs.mark_graph(output, self.overall_mark, self.code)
        return graph
    
    # Generates Rose chart and Table
    def generate_grade_tables(self, output):
        # Make table/graph if data present
        if self.weight_table:
            columns = ('Category', 'Weighting', 'Course Weighting', 'Student Achievement')

            rose = TAssist.TA_Graphs.grade_rose_chart(output, self.code, self.weight_table, TAssist.TA_Globals.CATEGORIES, TAssist.TA_Globals.COLORS)
            table = TAssist.TA_Graphs.grade_table_chart(output, self.code, self.weight_table, TAssist.TA_Globals.CATEGORIES, columns, TAssist.TA_Globals.COLORS)
            
            # Return graph objects
            return rose, table
        else:
            return False

    def get_trendline(self, output):
        trend = TAssist.TA_Graphs.course_trendline(output, self.assignments, self.code, TAssist.TA_Globals.CATEGORIES, TAssist.TA_Globals.COLORS)
        return trend

class Student:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.courses = []
        self.data = None
        self.total_average = None

    def __repr__(self):
        return f"Student Object at {hex(id(self))}"

    def has_class(self, input_course):
        for course in self.courses:
            if input_course == course:
                return course
        return False

    def fetch_data(self):
        # Make POST request to API with provided credentials
        credentials = {"number": self.username, "password": self.password}
        self.data = requests.post(api_url, json=credentials)
        status = self.data.status_code

        if status == 503 or status == 500: 
            return "[500] A server error has occured. Please try again later", False, status
        elif status == 401:
            return "[401] Incorrect password/username. Please try again", False, status
        elif status == 400:
            return "[400] Api error", False, status
        
        # Prep/prettify data and initialize it
        self.data = (self.data).json()
        self.initialize_data()
        return "[200] Succesfully connected to Teach Assist!", True, status

    def read_json(self, file):
        # Load json response data
        with open (file, "r") as f:
            self.data = json.load(f)
        self.initialize_data()


    def initialize_data(self):
        for course_info in self.data:
            # Make a new course and add it to a list
            course = Course(course_info)
            self.courses.append(course)

        self.calculte_average()

    # Calculate average from all courses
    def calculte_average(self):
        self.total_average = 0 
        num_courses = 0
        for course in self.courses:
            if course.overall_mark is not None:
                self.total_average += course.overall_mark
                num_courses += 1
        self.total_average /= num_courses