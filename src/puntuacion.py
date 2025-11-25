# keep track of player scores
class ScoreManager:
    def __init__(self):
        self.scores_escapa = []
        self.scores_cazador = []
        self.max_scores = 5
    
    # add a new score and maintain top scores
    def add_score(self, nombre, puntuacion, modo):
        score_entry = (nombre, puntuacion)
        
        if modo == 'escapa': scores = self.scores_escapa
        elif modo == 'cazador': scores = self.scores_cazador
        else: return False
        
        scores.append(score_entry)
        
        self._sort_scores(scores)
        
        if modo == 'escapa':
            self.scores_escapa = scores[:self.max_scores]
            return score_entry in self.scores_escapa
        else:
            self.scores_cazador = scores[:self.max_scores]
            return score_entry in self.scores_cazador
    
    # get scores for a specific mode
    def get_scores(self, modo):
        if modo == 'escapa': return self.scores_escapa
        elif modo == 'cazador': return self.scores_cazador
        else: return []
    
    # get player's rank after adding new score
    def get_rank(self, nombre, puntuacion, modo):
        scores = self.get_scores(modo)[:]
        scores.append((nombre, puntuacion))
        self._sort_scores(scores)
        
        for i in range(min(len(scores), self.max_scores)):
            if scores[i][0] == nombre and scores[i][1] == puntuacion: return i + 1
        return None
    
    # simple bubble sort for scores in descending order
    def _sort_scores(self, scores):
        n = len(scores)
        for i in range(n):
            for j in range(0, n - i - 1):
                if scores[j][1] < scores[j + 1][1]: scores[j], scores[j + 1] = scores[j + 1], scores[j]
