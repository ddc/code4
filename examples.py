# -*- coding: utf-8 -*-
from main import LazyCollection
from pythonLogs import TimedRotatingLog
from pythonLogs.settings import LogSettings


logger = TimedRotatingLog(level=LogSettings().level).init()


# ##################################
# Lazy Evaluation: Operations are only evaluated when needed
# No computation happens until we collect
# ##################################
result = (
    LazyCollection.range(1000000)
    .filter(lambda x: x % 2 == 0)
    .map(lambda x: x * 2)
    .take(10)
    .collect()
)
logger.info(f"Result: {result}")
# [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]


# ##################################
# Composable Operations: Methods can be chained together
# Chaining multiple operations
# ##################################
names = (
    LazyCollection(["alice", "bob", "charlie", "david"])
    .map(str.capitalize)
    .filter(lambda x: len(x) > 3)
    .collect()
)
logger.info(f"Names: {names}")
# ['Alice', 'Charlie', 'David']


# ##################################
# Pagination example
# ##################################
page3 = (
    LazyCollection.range(100)
    .paginate(page=3, per_page=10)
    .collect()
)
logger.info(f"Page 3: {page3}")
# [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]


# ##################################
# Chunking example
# ##################################
chunks = (
    LazyCollection.range(10)
    .chunk(3)
    .collect()
)
logger.info(f"Chunks: {chunks}")
# [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]



# ##################################
# Memory Efficiency: Only processes what's needed.
# Only processes first 5 elements, not the entire range
# ##################################
first_positive = (
    LazyCollection.range(-1000000, 1000000)
    .filter(lambda x: x > 0)
    .first()
)
logger.info(f"First Positive: {first_positive}")
# 1


# ##################################
# Counting
# ##################################
count = LazyCollection.range(100).filter(lambda x: x % 3 == 0).count()
logger.info(f"Count: {count}")
# 34


# ##################################
# Reducing
# ##################################
sum_of_squares = LazyCollection.range(5).reduce(lambda acc, x: acc + x*x, 0)
logger.info(f"Sum of Squares: {sum_of_squares}")
# 30 (0 + 1 + 4 + 9 + 16)


# ##################################
# Grouping
# ##################################
grouped = (
    LazyCollection(["apple", "banana", "cherry", "date"])
    .group_by(len)
)
logger.info(f"Grouped: {grouped}")
# {5: ['apple'], 6: ['banana', 'cherry'], 4: ['date']}
