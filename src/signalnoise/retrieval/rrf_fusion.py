from collections import defaultdict

class RRFfusion:
    def fuse(self,dense_results,sparse_results,k:int=20):
        source = defaultdict(float)
        documents = {}
        for rank, result in enumerate(dense_results, 1):
            doc_id = result.chunk_id
            score = rank
            source[doc_id] += 1 / (score + k)
            documents[doc_id] = result
        for rank, result in enumerate(sparse_results, 1):
            doc_id = result.chunk_id
            score = rank
            source[doc_id] += 1 / (score + k)
            documents[doc_id] = result

        ranked = sorted(
            source.items(),
            key= lambda x:x[1], 
            reverse=True
        )
        
        return[
            (
                documents[doc_id],
                score
            )
            for doc_id,score in ranked
        ]
