from taipy import Gui
import pandas as pd

path = None

page_1 = """
# Hello there!

<|{path}|file_selector|label=Upload dataset|on_action=load_csv_file|extensions=.csv|>
"""

page_2 = """
# Folder Statistics
"""

def load_csv_file(state):
    data = pd.read_csv(state.path)
    print(data)

if __name__ == "__main__":
    pages = {"home": page_1}
    gui = Gui(pages=pages)
    gui.run(use_reloader=True, port=8080)