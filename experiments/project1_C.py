import csv
from collections import defaultdict
import bisect

class GradeBook:
    def __init__(self):
        # Main data storage: list of student records
        self.students = []
        # Indexes for fast lookup
        self.indexes = {
            'firstname': defaultdict(list),
            'lastname': defaultdict(list),
            'email': defaultdict(list),
            'phone': defaultdict(list),
            'city': defaultdict(list),
            'score': [],  # Sorted list for score (integer)
            'department': defaultdict(list)
        }
        self.score_to_index = []  # Maps score to student indices

    def import_csv(self, filename):
        """Import gradebook from CSV file."""
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.DictReader(file)
                expected_fields = {'firstname', 'lastname', 'email', 'phone', 'city', 'score', 'department'}
                if not expected_fields.issubset(reader.fieldnames):
                    raise ValueError("CSV file missing required fields")

                self.students = []
                self.indexes = {key: defaultdict(list) if key != 'score' else [] for key in self.indexes}
                self.score_to_index = []

                for row in reader:
                    # Validate score
                    try:
                        score = int(row['score'])
                        if not 0 <= score <= 1000:
                            raise ValueError
                    except ValueError:
                        print(f"Invalid score for {row['firstname']} {row['lastname']}: {row['score']}")
                        continue

                    student = {
                        'firstname': row['firstname'].lower(),
                        'lastname': row['lastname'].lower(),
                        'email': row['email'].lower(),
                        'phone': row['phone'].lower(),
                        'city': row['city'].lower(),
                        'score': score,
                        'department': row['department'].lower()
                    }
                    student_index = len(self.students)
                    self.students.append(student)

                    # Update indexes
                    for field in ['firstname', 'lastname', 'email', 'phone', 'city', 'department']:
                        self.indexes[field][student[field]].append(student_index)
                    # Insert score into sorted score index
                    bisect.insort(self.indexes['score'], (score, student_index))
                    self.score_to_index.append(student_index)

        except FileNotFoundError:
            print(f"File {filename} not found")
        except Exception as e:
            print(f"Error importing CSV: {str(e)}")

    def search(self, search_key):
        """Search across all fields in O(log n + k) time."""
        search_key = search_key.lower()
        results = set()

        # Search string fields using hash table (O(1) lookup per field)
        for field in ['firstname', 'lastname', 'email', 'phone', 'city', 'department']:
            if search_key in self.indexes[field]:
                results.update(self.indexes[field][search_key])

        # Search score field using binary search (O(log n))
        try:
            score_key = int(search_key)
            if 0 <= score_key <= 1000:
                # Find the leftmost score >= search_key
                left = bisect.bisect_left(self.indexes['score'], (score_key, 0))
                if left < len(self.indexes['score']) and self.indexes['score'][left][0] == score_key:
                    # Collect all students with this exact score
                    i = left
                    while i < len(self.indexes['score']) and self.indexes['score'][i][0] == score_key:
                        results.add(self.indexes['score'][i][1])
                        i += 1
        except ValueError:
            pass  # search_key is not a valid integer, skip score search

        # Convert indices to student records
        return [self.students[i] for i in sorted(results)]

def main():
    gradebook = GradeBook()
    
    # Example usage
    gradebook.import_csv('D:\\GW\\Projects\\DAA\\project1\\gwu_gradebook.csv')
    
    while True:
        search_key = input("Enter search key (or 'quit' to exit): ")
        if search_key.lower() == 'quit':
            break
            
        results = gradebook.search(search_key)
        if not results:
            print("No results found.")
        else:
            print(f"Found {len(results)} results:")
            for student in results:
                print(f"Name: {student['firstname']} {student['lastname']}, "
                      f"Email: {student['email']}, Phone: {student['phone']}, "
                      f"City: {student['city']}, Score: {student['score']}, "
                      f"Department: {student['department']}")

if __name__ == "__main__":
    main()