from math import exp

class ConfidenceEngine:
    def normalize_reranker_score(self,score:float) -> float:
        """
        Normalizes the reranker score to a value between 0 and 1.
        Args:
            score (float): The score from the reranker.
        Returns:
            float: The normalized score.
        """
        return 1 / (1 + exp(-score))
    
    def calculate_confidence_score(
        self,
        reranker_score:float,
        rrf_score:float=0.5
    ) -> float:
        """
        Calculates the confidence score for a given query and document.
        Args:
            reranker_score (float): The score from the reranker.
            rrf_score (float): The score from the RRF fusion.
        Returns:
            float: The confidence score.
        """
        normalized_score = self.normalize_reranker_score(reranker_score)
        confidence = 0.7 * normalized_score + 0.3 * rrf_score
        return round(confidence, 4)
        