import holoviews as hv
import panel as pn
hv.extension('bokeh')
from pokemon.visuals import create_chord_plot, generate_html_table, generate_effectiveness_table
from pokemon.constants import create_dataframe, sort_dataframe, TYPE_EFFECTIVENESS


df = create_dataframe()

# Create a table with the HTML tags
df_filtered = df.copy()
df_filtered['Image_HTML'] = df_filtered['Image'].apply(lambda x: f"<img src='{x}' width='100'>")
# Create an HTML table with the data and the images
html_table = df_filtered[['Image_HTML', 'NDex', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].to_html(escape=False, index=False, header=False, classes='my-table')

table_output = pn.pane.HTML(width=700, height=600, sizing_mode='stretch_both')



def update_table(type1, type2, sort_by, name_filter=''):
    #Type drop-downs
    if type1 == 'All' and type2 == 'All':
        df_filtered = df
    elif type1 != 'All' and type2 == 'All':
        df_filtered = df[(df['Type 1'] == type1) | (df['Type 2'] == type1)]
    elif type1 == 'All' and type2 != 'All':
        df_filtered = df[(df['Type 1'] == type2) | (df['Type 2'] == type2)]
    else:
        df_filtered = df[((df['Type 1'] == type1) & (df['Type 2'] == type2)) |
                         ((df['Type 1'] == type2) & (df['Type 2'] == type1))]
        
    # Replace Type 2 value with "None" if it's the same as Type 1
    df_filtered['Type 2'] = df_filtered.apply(lambda x: "None" if x['Type 1'] == x['Type 2'] else x['Type 2'], axis=1)
    
    df_filtered = sort_dataframe(df_filtered, sort_by)
        
    # Apply the name filter if it is not empty
    if name_filter:
        df_filtered = df_filtered[df_filtered['Name'].str.contains(name_filter, case=False)]
    
    html_table = generate_html_table(df_filtered)

    table_output.object = html_table   




#Create text in place of table when no types have been selected
text_output = pn.pane.HTML(width=700, height=400, sizing_mode='stretch_both')

def calculate_type_effectiveness(attacked_type1, attacked_type2, name_filter='', sort_by='NDex'):
    # Clear the output pane
    text_output.object = ''

    # Filter the DataFrame based on the name filter
    if name_filter:
        df_filtered = df[df['Name'].str.contains(name_filter, case=False)]

        df_filtered = sort_dataframe(df_filtered, sort_by)

        if df_filtered.shape[0] > 0:
            first_pokemon = df_filtered.iloc[0]
            attacked_type1 = first_pokemon['Type 1']
            attacked_type2 = first_pokemon['Type 2']
            if attacked_type2 is None:
                effectiveness_dict = TYPE_EFFECTIVENESS[attacked_type1]['effectiveness']
            else:
                type1_dict = TYPE_EFFECTIVENESS[attacked_type1]['effectiveness']
                type2_dict = TYPE_EFFECTIVENESS[attacked_type2]['effectiveness']
                effectiveness_dict = {key: value * type2_dict[key] for key, value in type1_dict.items()}

    
    # If two types are provided, combine the types and calculate the effectiveness against all other types
    if attacked_type1 == 'All' and attacked_type2 == 'All':
        text_output.object += 'Select Pokemon Types to see Type Advantages'
        effectiveness_dict = {}
    elif attacked_type1 == 'All':
        # If first attacked type is 'All', set effectiveness to the value of the second attacked type
        effectiveness_dict = TYPE_EFFECTIVENESS[attacked_type2]['effectiveness']
    elif attacked_type2 == 'All':
        # If second attacked type is 'All', set effectiveness to the value of the first attacked type
        effectiveness_dict = TYPE_EFFECTIVENESS[attacked_type1]['effectiveness']
    else:
        # Two attacked types
        type1_dict = TYPE_EFFECTIVENESS[attacked_type1]['effectiveness']
        type2_dict = TYPE_EFFECTIVENESS[attacked_type2]['effectiveness']
        effectiveness_dict = {key: value * type2_dict[key] for key, value in type1_dict.items()}


    html_table = generate_effectiveness_table(effectiveness_dict, attacked_type1, attacked_type2, TYPE_EFFECTIVENESS)
    text_output.object = html_table

        

#Define a callback function to update the plot when a selector value changes
def on_select_type(event):
    name_filter = name_input.value  
    update_table(type1_selector.value, type2_selector.value, sort_selector.value,name_filter)  
    calculate_type_effectiveness(type1_selector.value, type2_selector.value, name_filter, sort_selector.value)

# Define the options for the type drop-down tabs
type_options = ['All'] + sorted(df['Type 1'].unique().tolist())

# Create the drop-down tabs
type1_selector = pn.widgets.Select(name='Type 1', options=type_options, width =80,)
type2_selector = pn.widgets.Select(name='Type 2', options=type_options, width=80)
sort_selector = pn.widgets.Select(name='Sort By',width=80,\
            options=['Dex #', 'Name', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'])
name_input = pn.widgets.TextInput(name='Search Pokemon', width=120)
reset_button = pn.widgets.Button(name='Reset', button_type='primary', width=80)

# Define the reset function
def reset(event):
    type1_selector.value = 'All'
    type2_selector.value = 'All'
    sort_selector.value = 'NDex'
    name_input.value = ''
    update_table('All', 'All', 'NDex')
    calculate_type_effectiveness('All', 'All')

reset_button.on_click(reset)


#Create table upon initial loading of page
update_table('All', 'All', 'NDex')  
calculate_type_effectiveness('All', 'All')

# Watch the selectors for changes
type1_selector.param.watch(on_select_type, 'value')
type2_selector.param.watch(on_select_type, 'value')
sort_selector.param.watch(on_select_type, 'value')
name_input.param.watch(on_select_type, 'value')
reset_button.param.watch(on_select_type, 'value')


# Create the header row with the drop-down tabs and the title
header_title = "Pokemon Type Combinations"
left_image_url = f'<img src="https://raw.githubusercontent.com/echestnut22/Pokemon-Type-Combinations/main/data/Pokemon%20PNGs/Pokeball.png" width="50" height>'
right_image_url = f'<img src="https://raw.githubusercontent.com/echestnut22/Pokemon-Type-Combinations/main/data/Pokemon%20PNGs/Pokeball.png" width="50" height>'


header = pn.Row(
    pn.Spacer(width=110),
    pn.pane.HTML(left_image_url),
    pn.Spacer(width=0),
    pn.pane.HTML(f'<h1 style="text-align: center; font-size:24px ; white-space: nowrap;">{header_title}</h1>'),
    pn.Spacer(width=0),
    pn.pane.HTML(right_image_url),
    pn.Spacer(width=90),
    reset_button,
    pn.Spacer(width=10),
    name_input,
    pn.Spacer(width=20),
    type1_selector,
    pn.Spacer(width=50),
    type2_selector,
    pn.Spacer(width=50),
    sort_selector,
    pn.Spacer(width=0),
    width_policy='max',
    sizing_mode='stretch_width'
)

#Creating the chord diagram
plot = create_chord_plot(df)

# Create the content row with the chord diagram, table, and text output
content = pn.Column(
    pn.Row(
        pn.Column(
            plot,
            sizing_mode='stretch_width'
        ),
        pn.Column(
            table_output,
            text_output,
        ),
        sizing_mode='stretch_width'
    ),
    sizing_mode='stretch_width'
)


# Create the layout with the header row and the content row
layout = pn.Column(
    header,
    content,
    height_policy='max',
    sizing_mode='stretch_both'
)



if __name__ == "__main__":
    pn.serve(layout)

