import os

import plotly
import plotly.graph_objs as go

from data.Sheets import Sheets

NUM_ROWS = 20
PERCENT_COLUMN = 4
CORRECT_TEAM_COLUMN = 5
COVERED_COLUMN = 6


class KenPomSheets(Sheets):
    def __init__(self):
        Sheets.__init__(self, 'KenPom', os.getcwd() + '/../sheets_api/SportsBettingProgram-sheets1.json')

    def plot_covered_based_on_percent(self):
        x_list = []
        y_list = []
        for num in range(1, NUM_ROWS):
            r_tuple = Sheets.get_row(self, num)
            x_list.append(r_tuple[CORRECT_TEAM_COLUMN])
            y_list.append(r_tuple[PERCENT_COLUMN])

        trace = [go.Scatter(
            x=x_list,
            y=y_list,
            mode='markers'
        )]

        plotly.offline.plot({
            "data": trace,
            "layout": {
                "title": "Percent vs Correct"
            }
        })
