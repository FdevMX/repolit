class FileView:
    def __init__(self):
        self.files = []

    def display_files(self):
        # Logic to display files
        for file in self.files:
            print(file)

    def add_file(self, file):
        # Logic to add a file
        self.files.append(file)

    def delete_file(self, file):
        # Logic to delete a file
        if file in self.files:
            self.files.remove(file)

    def update_file(self, old_file, new_file):
        # Logic to update a file
        if old_file in self.files:
            index = self.files.index(old_file)
            self.files[index] = new_file