# Import Libraries

import seaborn as sns # Seaborn for making Seaborn plots
from faicons import icon_svg # Library for using icons (font awesome)

from shiny import reactive # From shiny, import just reactive

from shiny.express import input, render, ui # From shiny.express, import render, ui, and inputs if needed

import palmerpenguins # import palmerpenguins package with dataset

# Get Data
# Load the dataset into a pandas DataFrame.
# Use the built-in function to load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

# Define the Shiny UI Page layout
# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI
ui.page_opts(title="Penguins dashboard", fillable=True)

# Add a Shiny UI sidebar for user interaction
# Use the ui.sidebar() function to create a sidebar
with ui.sidebar(title="Filter controls"):
    
# Use ui.input_slider() to create a slider input
# pass in four arguments:
#   the name of the input (in quotes)
#   the label for the input (in quotes)
#   the minimum value for the input (as an integer)
#   the maximum value for the input (as an integer)
#   the default value for the input (as an integer)
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)

# Use ui.input_checkbox_group() to create a checkbox group input
#   pass in five arguments:
#   the name of the input (in quotes)
#   the label for the input (in quotes)
#   a list of options for the input (in square brackets)
#   a list of selected options for the input (in square brackets)
#   a boolean value (True or False) to set the input inline or not
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr() # Use ui.hr() to add a horizontal rule to the sidebar

# Use ui.a() to add a hyperlink to the sidebar
#   pass in two arguments:
#   the text for the hyperlink (in quotes)
#   the URL for the hyperlink (in quotes)
#   set the target parameter to "_blank" to open the link in a new tab
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Use ui.layout_column_wrap to create value boxes
with ui.layout_column_wrap(fill=False):
    
    # Call ui.value_box to create a value box within the ui.layout_column_wrap()
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]
            
    # Call ui.value_box to create a value box within the ui.layout_column_wrap()
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"
   
    # Call ui.value_box to create a value box within the ui.layout_column_wrap()
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Use ui.layout_columns() to create a two-column layout
# And indent the code to place the two cards in the columns
with ui.layout_columns():

    # Create card within columns using ui.card()
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")
        # Create a scatterplot using seaborn(sns)
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )
            
    # Create card within columns using ui.card()
    with ui.card(full_screen=True):
        ui.card_header("Penguin data")
        # Create a data grid using dataframe from library.
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    # create filtered data for reactive calcs above and data to be used in inputs
    # The required function req() is used to ensure that
    # the input.selected_species() function is not empty
    # Use the isin() method to filter the DataFrame
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
