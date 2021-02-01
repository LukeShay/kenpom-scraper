from bs4 import BeautifulSoup, ResultSet
from lib.domain.fan_match_model import FanMatch
from typing import Tuple
import re


class FanMatchSoup:
    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, "html.parser")

    def get_fan_match_rows(self) -> ResultSet:
        return (
            self._soup.find("table", id="fanmatch-table").find("tbody").find_all("tr")
        )

    @staticmethod
    def get_location_from_row(row) -> str:
        return row.find_all("td")[3].get_text().split("\n")[0].strip()

    @staticmethod
    def get_team_and_score(s: str) -> Tuple[str, int]:
        search = re.search(r"(\d+\s)?(?P<team>[^\d]+)\s(?P<score>\d+)", s)

        if search is not None:
            return search.group("team").strip(), int(search.group("score").strip())

        return "ERROR", -1

    @staticmethod
    def get_teams_and_scores_from_row(row) -> Tuple[str, int, str, int]:
        game = row.find_all("td")[0]

        teams = game.get_text().split(", ")

        assert len(teams) == 2

        winner, winner_score = FanMatchSoup.get_team_and_score(teams[0])
        loser, loser_score = FanMatchSoup.get_team_and_score(teams[1])

        return winner, winner_score, loser, loser_score

    @staticmethod
    def get_favorite_scores_and_percentage_from_row(row) -> Tuple[str, int, int, int]:
        prediction = row.find_all("td")[1]

        matches = re.search(
            r"(?P<team>[^\d]+)(?P<winner_score>\d+)-(?P<loser_score>\d+)\s\((?P<percentage>\d+)\%\)",
            prediction.get_text(),
        )

        if matches is not None:
            return (
                matches.group("team").strip(),
                int(matches.group("winner_score").strip()),
                int(matches.group("loser_score").strip()),
                int(matches.group("percentage").strip()),
            )

        return "ERROR", -1, -1, -1

    def run(self, date) -> [FanMatch]:
        predictions = []

        for row in self.get_fan_match_rows():
            if len(row.find_all("td")) != 7:
                break

            (
                winner,
                winner_score,
                loser,
                loser_score,
            ) = FanMatchSoup.get_teams_and_scores_from_row(row)
            (
                favorite,
                favorite_predicted_score,
                underdog_predicted_score,
                percentage,
            ) = FanMatchSoup.get_favorite_scores_and_percentage_from_row(row)

            location = FanMatchSoup.get_location_from_row(row)

            if winner == favorite:
                predictions.append(
                    FanMatch(
                        date=date,
                        favorite=winner,
                        underdog=loser,
                        favorite_actual_score=winner_score,
                        underdog_actual_score=loser_score,
                        favorite_predicted_score=favorite_predicted_score,
                        underdog_predicted_score=underdog_predicted_score,
                        percentage=percentage,
                        location=location,
                    )
                )
            else:
                predictions.append(
                    FanMatch(
                        date=date,
                        favorite=loser,
                        underdog=winner,
                        favorite_actual_score=loser_score,
                        underdog_actual_score=winner_score,
                        favorite_predicted_score=favorite_predicted_score,
                        underdog_predicted_score=underdog_predicted_score,
                        percentage=percentage,
                        location=location,
                    )
                )

        return predictions
