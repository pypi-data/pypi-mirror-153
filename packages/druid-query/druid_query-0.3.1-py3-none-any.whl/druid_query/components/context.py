from dataclasses import dataclass
from typing import Optional, Union

from .druid_types import DruidNativeType


@dataclass
class Context:
    timeout: Optional[DruidNativeType] = None
    priority: Optional[DruidNativeType] = None
    lane: Optional[DruidNativeType] = None
    query_id: Optional[DruidNativeType] = None
    broker_service: Optional[DruidNativeType] = None
    use_cache: Optional[bool] = None
    populate_cache: Optional[bool] = None
    use_result_level_cache: Optional[bool] = None
    populate_result_level_cache: Optional[bool] = None
    by_segment: Optional[bool] = None
    finalize: Optional[bool] = None
    max_scatter_gather_bytes: Optional[DruidNativeType] = None
    max_queued_bytes: Optional[DruidNativeType] = None
    serialize_date_time_as_long: Optional[bool] = None
    serialize_date_time_as_long_inner: Optional[bool] = None
    enable_parallel_merge: Optional[bool] = None
    parallel_merge_parallelism: Optional[DruidNativeType] = None
    parallel_merge_initial_yield_rows: Optional[DruidNativeType] = None
    parallel_merge_small_batch_rows: Optional[DruidNativeType] = None
    use_filter_c_n_f: Optional[bool] = None
    secondary_partition_pruning: Optional[bool] = None
    enable_join_left_table_scan_direct: Optional[bool] = None
    debug: Optional[bool] = None
    min_top_n_threshold: Optional[DruidNativeType] = None
    skip_empty_buckets: Optional[bool] = None
    vectorize: Optional[bool] = None
    vector_size: Optional[DruidNativeType] = None
    vectorize_virtual_columns: Optional[bool] = None
    sql_query_id: Optional[str] = None
    sql_time_zone: Optional[str] = None
    sql_stringify_arrays: Optional[bool] = None
    use_approximate_count_distinct: Optional[bool] = None
    use_grouping_set_for_exact_distinct: Optional[bool] = None
    use_approximate_top_n: Optional[bool] = None
