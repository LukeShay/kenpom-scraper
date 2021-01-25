class KenPomPrediction:
    def __init__(
        self,
        date,
        favorite,
        underdog,
        favorite_predicted_score,
        underdog_predicted_score,
        favorite_actual_score,
        underdog_actual_score,
        percentage,
        home_team,
    ):
        self.date = date
        self.favorite = favorite
        self.underdog = underdog
        self.favorite_predicted_score = favorite_predicted_score
        self.underdog_predicted_score = underdog_predicted_score
        self.favorite_actual_score = favorite_actual_score
        self.underdog_actual_score = underdog_actual_score
        self.percentage = percentage
        self.home_team = home_team

        self.predicted_spread = (
            self.underdog_predicted_score - self.favorite_predicted_score
        )
        self.actual_spread = self.underdog_actual_score - self.favorite_actual_score

        self.covered = self.actual_spread < self.predicted_spread
        self.winner_predicted = self.favorite_actual_score > self.underdog_actual_score

    def __str__(self):
        return f"{self.date},{self.favorite},{self.underdog},{self.home_team},{self.favorite_predicted_score},{self.underdog_predicted_score},{self.predicted_spread},{self.percentage},{self.favorite_actual_score},{self.underdog_actual_score},{self.actual_spread},{self.covered},{self.winner_predicted}"

    @staticmethod
    def column_headers():
        return "date,favorite,underdog,home_team,favorite_predicted_score,underdog_predicted_score,predicted_spread,percentage,favorite_actual_score,underdog_actual_score,actual_spread,covered,winner_predicted"
