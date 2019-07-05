import plotly

from data.Sheets import Sheets

NUM_ROWS = 53
PERCENT_COLUMN = 5
CORRECT_TEAM_COLUMN = 6
COVERED_COLUMN = 7


class KenPomSheetsPage(Sheets):
    def __init__(self):
        Sheets.__init__(self, 'KenPom', 'sheets_api/SportsBettingProgram-sheets1.json')

    def plot_covered_based_on_percent(self):
        x_list = []
        y_list = []
        for num in range(1, NUM_ROWS):
            r_tuple = Sheets.get_row(self, num)
            x_list.append(r_tuple[PERCENT_COLUMN])
            y_list.append(r_tuple[COVERED_COLUMN])

        plotly.offline.plot({
            "data": [{
                "x": x_list,
                "y": y_list
            }],
            "layout": {
                "title": "Percent vs Covered"
            }
        })
