# Jamie Martin
# N10212361
from scipy import stats

from topic import get_topic_statements, get_collections
from benchmark import get_benchmarks
from training import calculate_bm25, output_bm25, output_bl_result, calculate_w4, output_lr_result
import testing

if __name__ == "__main__":
    topic_statements = get_topic_statements()
    collections = get_collections(topic_statements)

    # --- Part 1 ---

    # --- Q1_2 ---
    bl = calculate_bm25(collections, topic_statements)
    output_bm25(collections, topic_statements, bl)
    
    # --- Q1_3 ---
    # Transform into ranks
    for collection, topic in zip(collections, topic_statements):
        topic = topic["id"] 
        scores = bl[topic]
        
        for id, score in scores.items():
            result = lambda score: 1 if score > 1 else 0
            bl[topic][id] = result(score)

    output_bl_result(collections, topic_statements, bl)

    # --- Part 2 ---

    # --- Q2_5 ---
    lr = calculate_w4(collections, topic_statements, bl)
    output_lr_result(collections, topic_statements, lr)

    # Transform into ranks
    for collection, topic in zip(collections, topic_statements):
        topic = topic["id"] 
        scores = lr[topic]

        for id, score in scores.items():
            result = lambda score: 1 if score > 1 else 0
            lr[topic][id] = result(score)

    # --- PART 3 ---

    # --- Q3_6 ---
    benchmarks = get_benchmarks()
    bl_test = testing.test(collections, topic_statements, benchmarks, bl)
    lr_test = testing.test(collections, topic_statements, benchmarks, lr)

    testing.output(bl_test, lr_test)