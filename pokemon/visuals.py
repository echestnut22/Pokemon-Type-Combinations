import pandas as pd
import holoviews as hv
import panel as pn
from holoviews import opts, dim
hv.extension('bokeh')
from .constants import TYPE_COLORS
from .hyperlink import assign_hyperlink

def create_chord_plot(df):

    type_cmap = hv.Cycle(list(TYPE_COLORS.values()))

    nodes_df_with_color = pd.DataFrame({'Type 1': df['Type 1'].unique()})
    nodes_df_with_color['color'] = nodes_df_with_color['Type 1'].map(TYPE_COLORS)
    
    # Fill NaN values with same as Type 1. Will display single type pokemon on chord diagram
    df['Type 2'] = df['Type 2'].fillna(df['Type 1'])

    """USE THIS LINE OF CODE INSTEAD IF ONLY WANT DUAL TYPE POKEMON ON CHORD DIAGRAM
    df_twotypes = df[df['Type 2'].notna()]"""

    df_twotypes = df.copy()

    # Group by Type 1 and Type 2 and count the number of occurrences
    grouped = df_twotypes.groupby(['Type 1', 'Type 2']).size().reset_index(name='value')

    # Loop through Dataframe to assign each type combination for chord diagram 
    links = []
    for i, row in grouped.iterrows():
        source_type = row['Type 1']
        target_type = row['Type 2']
        source_color = nodes_df_with_color.loc[nodes_df_with_color['Type 1'] == source_type, 'color'].values[0]
        target_color = nodes_df_with_color.loc[nodes_df_with_color['Type 1'] == target_type, 'color'].values[0]
        source_pokemon = df.loc[df['Type 1'] == source_type, 'Name'].iloc[0]
        target_pokemon = df.loc[df['Type 1'] == target_type, 'Name'].iloc[0]
        links.append({
            'source': source_type,
            'target': target_type,
            'value': row['value'],
            'source_color': source_color,
            'target_color': target_color})

    #Chord diagram creation and customization 
    links_ds = hv.Dataset(pd.DataFrame(links), ['source', 'target'])

    nodes = hv.Dataset(nodes_df_with_color, 'Type 1', 'color')

    chord = hv.Chord((links_ds, nodes))

    chord.opts(
        opts.Chord(cmap=type_cmap, edge_cmap=type_cmap, edge_color=dim('source_color').str(),
                   labels='Type 1', node_color='color', height=750, width=750)
    )

    plot = pn.pane.HoloViews(chord)
    
    return plot

def generate_html_table(df_filtered):

    pokemon_data = assign_hyperlink(df_filtered)

    pokemon_df = pd.DataFrame(pokemon_data, columns=['', 'Dex #', 'Name', 'Type(s)','Total', 'HP', 'Atk', 'Def', 'Sp. Atk', 'Sp. Def', 'Spd'])

    # Convert the DataFrame to an HTML table with styling
    html_table = pokemon_df.to_html(index=False, escape=False, header=True, classes='my-table" id="pokemon-table"')
    html_table = html_table.replace('<table', "<table id='pokemon-table' style='border-collapse: collapse; width: 100%; background-color: #f1f1f1; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);'")
    html_table = html_table.replace('<td', "<td style='padding: 5px; border: 2px solid black; font-family: Arial, sans-serif; font-size: 14px; color: #333; text-align: center;'")
    html_table = html_table.replace('<th>', "<th style='text-align: center; border-top: 2px solid black; border-right: 2px solid black; border-left: 2px solid black;'>")


    #Table customization
    css_style = """
    <style>
        .fixed-width {
            width: 100px; //
        }
    </style>
    """

    html_table = css_style + html_table

    html_table = html_table.replace('<td style=', "<td class='fixed-width' style=")

    html_table = f"<div style='max-height: 500px; overflow-y: scroll;'><table style='max-width:100%;'>{html_table}</table></div>"

    return html_table


def generate_effectiveness_table(effectiveness_dict, attacked_type1, attacked_type2, TYPE_EFFECTIVENESS):
    # Group the effectiveness values into categories
    # Group the effectiveness values into categories for calculation
    categories = {
        0: [],
        0.25: [],
        0.5: [],
        1: [],
        2: [],
        4: []
    }
    for key, value in effectiveness_dict.items():
        if value == 0:
            categories[0].append(key)
        elif value == 0.25:
            categories[0.25].append(key)
        elif value == 0.5:
            categories[0.5].append(key)
        elif value == 1:
            categories[1].append(key)
        elif value == 2:
            categories[2].append(key)
        elif value == 4:
            categories[4].append(key)
  
    
    # Generate an HTML table
    # Generate table for type effectiveness values calculator
    table_html = '<table style="border-collapse: collapse; width: 100%; background-color: #f1f1f1; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);">'
    if attacked_type1 == 'All' and attacked_type2 == 'All':
        table_html += '<tr><td colspan="0" style="padding: 0px; border: 0px solid black; font-family: Arial, sans-serif; font-size: 20px;">Select Pokemon Types to see Type Advantages</td></tr>'
    else:
        if categories[4]:
            table_html += '<tr style="border: 2px solid black;"><td style="padding: 15px; border: 2px solid black; font-family: Arial, sans-serif; font-size: 14px; color: #333;"><b>4x weak to:</b></td><td>'
            for type in categories[4]:
                table_html += f'<img src="{TYPE_EFFECTIVENESS[type]["image_url"]}" width="70px">'
            table_html += '</td></tr>'
        if categories[2]:
            table_html += '<tr style="border: 2px solid black;"><td style="padding: 15px; border: 2px solid black; font-family: Arial, sans-serif; font-size: 14px; color: #333;"><b>2x weak to:</b></td><td>'
            for type in categories[2]:
                table_html += f'<img src="{TYPE_EFFECTIVENESS[type]["image_url"]}" width="70px">'
            table_html += '</td></tr>'
        if categories[1]:
            table_html += '<tr style="border: 2px solid black;"><td style="padding: 15px; border: 2px solid black; font-family: Arial, sans-serif; font-size: 14px; color: #333;"><b>Neutral to:</b></td><td>'
            for type in categories[1]:
                table_html += f'<img src="{TYPE_EFFECTIVENESS[type]["image_url"]}" width="70px">'
            table_html += '</td></tr>'
        if categories[0.5]:
            table_html += '<tr style="border: 2px solid black;"><td style="padding: 15px; border: 2px solid black; font-family: Arial, sans-serif; font-size: 14px; color: #333;"><b>.5 Resistant to:</b></td><td>'
            for type in categories[0.5]:
                table_html += f'<img src="{TYPE_EFFECTIVENESS[type]["image_url"]}" width="70px">'
            table_html += '</td></tr>'
        if categories[0.25]:
            table_html += '<tr style="border: 2px solid black;"><td style="padding: 15px; border: 2px solid black; font-family: Arial, sans-serif; font-size: 14px; color: #333;"><b>.25 Resistant to:</b></td><td>'
            for type in categories[0.25]:
                table_html += f'<img src="{TYPE_EFFECTIVENESS[type]["image_url"]}" width="70px">'
            table_html += '</td></tr>'
        if categories[0]:
            table_html += '<tr style="border: 2px solid black;"><td style="padding: 15px; border: 2px solid black; font-family: Arial, sans-serif; font-size: 14px; color: #333;"><b>Immune to:</b></td><td>'
            for type in categories[0]:
                table_html += f'<img src="{TYPE_EFFECTIVENESS[type]["image_url"]}" width="70px">'
            table_html += '</td></tr>'
        
    table_html += '</table>'
    
    return table_html
