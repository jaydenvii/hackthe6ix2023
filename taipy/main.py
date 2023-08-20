from taipy.gui import Gui, navigate
import pandas as pd
import random

memory_path = None
ext_path = None
data = None

integers_column = None
areas = None
color_dict = None
data_dict = None
options = {
    # Hide the texts
}

column2 = None
color_dict1 = None
data_dict1 = None
options1 = {
    # Hide the texts
}

logo_path = "logo.png"

page_1 = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap');
</style>

<center> <h1> Welcome to FYLY, your AI-powered file organizer. </h1> </center>

<center> <|{logo_path}|image|> </center>

<center> <h2> File Analytics Centre </h2> </center>

<|layout|columns=1 1|
    <|
<br/>
<br/>
<br/>
<br/>
<br/>
<center> Upload a CSV file containing the memory usage of each file in your directory. </center>

<center> <|{memory_path}|file_selector|label=Upload Memory CSV|on_action=memory_action|extensions=.csv|id=memory_upload|> </center>
    |>

    <|
<br/>
<br/>
<br/>
<br/>
<br/>
<center> Upload a CSV file containing the extension make-up of each file in your directory. </center>

<center> <|{ext_path}|file_selector|label=Upload Extensions CSV|on_action=ext_action|extensions=.csv|id=ext_upload|> </center>
    |>
|>
"""

page_2 = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap');
</style>

<center> <h1> Memory Statistics </h1> </center>

<center> <|{data_dict}|chart|type=pie|values=Area|labels=Extensions|layout={color_dict}|options={options}|> </center>
"""

page_3 = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400&display=swap');
</style>

<center> <h1> Extension Statistics </h1> </center>

<center> <|{data_dict1}|chart|type=pie|values=Area|labels=Extensions|layout={color_dict1}|options={options}|> </center>
"""

def memory_action(state):
    global data, integers_column, areas, color_dict, data_dict

    data = pd.read_csv(state.memory_path, sep="\t", header=None, names=["Extensions", "Column2", "Area"])

    # Extract extensions from filenames
    extensions_first_index = [extension.split(",")[0] for extension in data["Extensions"]]

    # Get the unique extensions
    unique_extensions = set(extensions_first_index)
    integers_column = [extension.split(",")[1] for extension in data["Extensions"]]
    integers_column = [int(value) for value in integers_column]
    print(integers_column)

    areas = [extension.split(",")[2] for extension in data["Extensions"]]
    areas = [int(value) for value in areas]
    print(areas)

    # Generate random hex color codes for each unique extension
    color_codes = [
        "#" + "".join(random.choices("0123456789ABCDEF", k=6))
        for _ in range(len(unique_extensions))
    ]

    color_codes = [f"hsl({360*(i-1)/(len(unique_extensions)-1)},90%,60%)" for i in range(1, len(unique_extensions)+1)]

    # Create a dictionary in the desired format
    state.color_dict = {"piecolorway": color_codes, "title": "Memory Usage By File", "showlegend": True}
    # Create a dictionary in the desired format
    state.data_dict = {"Extensions": extensions_first_index, "Area": areas}

    navigate(state, "memory_stats")

def ext_action(state):
    global data, column2, color_dict1, data_dict1
    data = pd.read_csv(state.ext_path, sep="\t", header=None, names=["Extensions", "Area"])

    extensions_first_index1 = [extension.split(",")[0] for extension in data["Extensions"]]
    unique_extensions = set(extensions_first_index1)
    print(extensions_first_index1)

    column2 = [extension.split(",")[1] for extension in data["Extensions"]]
    column2 = [float(value) for value in column2]

    color_codes = [
        "#" + "".join(random.choices("0123456789ABCDEF", k=6))
        for _ in range(len(unique_extensions))
    ]

    color_codes = [f"hsl({360*(i-1)/(len(unique_extensions)-1)},90%,60%)" for i in range(1, len(unique_extensions)+1)]

    state.color_dict1 = {"piecolorway": color_codes, "title": "Extension Make-Up By Percentage", "showlegend": True}

    state.data_dict1 = {"Extensions": extensions_first_index1, "Area": column2}

    navigate(state, "ext_stats")

stylekit = {
    "font_family": "Poppins, sans-serif",
    "color_background_dark": "#1E1E1E",
    "color_primary": "#EA4D2B",
    "color_secondary": "#EA4D2B",
    "border_radius": "8px",
    "color_paper_dark": "#2D2D2D",
}

if __name__ == "__main__":
    pages = {"home": page_1, "memory_stats": page_2, "ext_stats": page_3}
    gui = Gui(pages=pages)
    gui.run(use_reloader=True, stylekit=stylekit)