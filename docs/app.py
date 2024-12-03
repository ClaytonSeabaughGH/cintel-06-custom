import shiny
from shiny import ui, render, reactive
import pandas as pd
import random
import matplotlib.pyplot as plt

# Fake Data Generation Function (scriptable)
def generate_fake_data(characters=None, stat_ranges=None, num_characters=100):
    # Default character classes if none are provided
    if characters is None:
        characters = ['Wizard', 'Fighter', 'Rogue', 'Cleric', 'Barbarian']
    
    # Default stat ranges if none are provided
    if stat_ranges is None:
        stat_ranges = {
            'Strength': (8, 18),
            'Dexterity': (8, 18),
            'Constitution': (8, 18),
            'Intelligence': (8, 18),
            'Wisdom': (8, 18),
            'Charisma': (8, 18),
        }

    stats = {
        'Character': [random.choice(characters) for _ in range(num_characters)],
        'Strength': [random.randint(stat_ranges['Strength'][0], stat_ranges['Strength'][1]) for _ in range(num_characters)],
        'Dexterity': [random.randint(stat_ranges['Dexterity'][0], stat_ranges['Dexterity'][1]) for _ in range(num_characters)],
        'Constitution': [random.randint(stat_ranges['Constitution'][0], stat_ranges['Constitution'][1]) for _ in range(num_characters)],
        'Intelligence': [random.randint(stat_ranges['Intelligence'][0], stat_ranges['Intelligence'][1]) for _ in range(num_characters)],
        'Wisdom': [random.randint(stat_ranges['Wisdom'][0], stat_ranges['Wisdom'][1]) for _ in range(num_characters)],
        'Charisma': [random.randint(stat_ranges['Charisma'][0], stat_ranges['Charisma'][1]) for _ in range(num_characters)],
    }
    return pd.DataFrame(stats)

# Define UI with Shiny Express
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("strength_range", "Strength Range", min=8, max=18, value=(8, 18)),
            ui.input_slider("dexterity_range", "Dexterity Range", min=8, max=18, value=(8, 18)),
            ui.input_slider("constitution_range", "Constitution Range", min=8, max=18, value=(8, 18)),
        ),
        ui.layout_columns(
            ui.h1("Dungeons and Dragons Dashboard"),
            ui.row(
                ui.card(
                    ui.h3("Character Stats Summary"),
                    ui.output_ui("avg_strength"),
                    ui.output_ui("avg_dexterity"),
                    ui.output_ui("avg_constitution"),
                    ui.output_ui("avg_intelligence"),
                    ui.output_ui("avg_wisdom"),
                    ui.output_ui("avg_charisma"),
                ),
                ui.card(
                    ui.h3("Character Distribution"),
                    ui.output_plot("stats_plot")
                ),
            ),
            ui.row(
                ui.card(
                    ui.h3("Character Grid"),
                    ui.output_table("character_grid"),
                )
            ),
        )
    )
)

# Define server function to handle the logic
def server(input, output, session):
    # Function to get filtered data based on slider values
    @reactive.Calc
    def filtered_data():
        # Extracting the slider values using .get()
        strength_range = input.strength_range.get()
        dexterity_range = input.dexterity_range.get()
        constitution_range = input.constitution_range.get()

        stat_ranges = {
            'Strength': strength_range,
            'Dexterity': dexterity_range,
            'Constitution': constitution_range,
            'Intelligence': (8, 18),  # Default range for other stats
            'Wisdom': (8, 18),
            'Charisma': (8, 18),
        }
        
        df = generate_fake_data(stat_ranges=stat_ranges)
        df = df[
            (df['Strength'] >= strength_range[0]) & (df['Strength'] <= strength_range[1]) &
            (df['Dexterity'] >= dexterity_range[0]) & (df['Dexterity'] <= dexterity_range[1]) &
            (df['Constitution'] >= constitution_range[0]) & (df['Constitution'] <= constitution_range[1])
        ]
        return df

    # Stats summary
    @output
    @render.ui
    def avg_strength():
        df = filtered_data()
        avg = df['Strength'].mean()
        return ui.div(f"Avg Strength: {avg:.2f}", class_="value-box")

    @output
    @render.ui
    def avg_dexterity():
        df = filtered_data()
        avg = df['Dexterity'].mean()
        return ui.div(f"Avg Dexterity: {avg:.2f}", class_="value-box")

    @output
    @render.ui
    def avg_constitution():
        df = filtered_data()
        avg = df['Constitution'].mean()
        return ui.div(f"Avg Constitution: {avg:.2f}", class_="value-box")

    @output
    @render.ui
    def avg_intelligence():
        df = filtered_data()
        avg = df['Intelligence'].mean()
        return ui.div(f"Avg Intelligence: {avg:.2f}", class_="value-box")

    @output
    @render.ui
    def avg_wisdom():
        df = filtered_data()
        avg = df['Wisdom'].mean()
        return ui.div(f"Avg Wisdom: {avg:.2f}", class_="value-box")

    @output
    @render.ui
    def avg_charisma():
        df = filtered_data()
        avg = df['Charisma'].mean()
        return ui.div(f"Avg Charisma: {avg:.2f}", class_="value-box")

    # Generate a plot of character stats
    @output
    @render.plot
    def stats_plot():
        df = filtered_data()
        stats = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
        means = [df[stat].mean() for stat in stats]

        plt.bar(stats, means, color='skyblue')
        plt.xlabel('Stat')
        plt.ylabel('Average Value')
        plt.title('Average Character Stats')
        return plt.gcf()

    # Display character data grid
    @output
    @render.table
    def character_grid():
        df = filtered_data()
        return df[['Character', 'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']].head(10)

# Run the app
app = shiny.App(app_ui, server)
app.run()  # Explicitly start the app
