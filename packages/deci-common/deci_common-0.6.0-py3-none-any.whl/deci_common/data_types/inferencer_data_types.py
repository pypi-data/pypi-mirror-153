import json

from deci_common.abstractions.base_model import Schema


class InferencerBenchmarkResult(Schema):
    batch_size: int = None
    batch_inf_time: float = None
    batch_inf_time_variance: float = None

    memory: float = None

    pre_inference_memory_used: float = None
    post_inference_memory_used: float = None
    total_memory_size: float = None
    throughput: float = None
    sample_inf_time: float = None
    include_io: bool = None
    framework_type: str = None
    framework_version: str = None
    inference_hardware: str = None
    infery_version: str = None
    date: str = None
    ctime: int = None
    h_to_d_mean: float = None
    d_to_h_mean: float = None
    h_to_d_variance: float = None
    d_to_h_variance: float = None

    def __str__(self):
        benchmarks_dict = self.dict()

        # Adding ms and fps to __repr__ output.
        results_benchmarks_dict = dict()
        for k, v in benchmarks_dict.items():
            if isinstance(v, float):
                if k == "throughput":
                    results_benchmarks_dict[k] = f"{v:.2f} fps"
                elif "memory" in k:
                    results_benchmarks_dict[k] = f"{v:.2f} mb"
                else:
                    results_benchmarks_dict[k] = f"{v:.2f} ms"
            else:
                results_benchmarks_dict[k] = v

        return f"<ModelBenchmarks: {json.dumps(results_benchmarks_dict, indent=4)}>"

    def __repr__(self):
        return str(self)
