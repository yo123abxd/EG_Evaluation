#include <gunrock/algorithms/sssp.hxx>
#include "sssp_cpu.hxx"  // Reference implementation
#include <gunrock/util/performance.hxx>
#include <gunrock/io/parameters.hxx>
#include <iostream>
#include <chrono>

using namespace gunrock;
using namespace memory;

void test_sssp(int num_arguments, char** argument_array) {
  // --
  // Define types

  using vertex_t = int;
  using edge_t = int;
  using weight_t = float;

auto t1 = std::chrono::high_resolution_clock::now();
  using csr_t =
      format::csr_t<memory_space_t::device, vertex_t, edge_t, weight_t>;

  // --
  // IO

  gunrock::io::cli::parameters_t params(num_arguments, argument_array,
                                        "Single Source Shortest Path");

  io::matrix_market_t<vertex_t, edge_t, weight_t> mm;
  auto [properties, coo] = mm.load(params.filename);

  csr_t csr;

  if (params.binary) {
    csr.read_binary(params.filename);
  } else {
    csr.from_coo(coo);
  }

  // --
  // Build graph

  auto G = graph::build<memory_space_t::device>(properties, csr);
auto t2 = std::chrono::high_resolution_clock::now();
std::cout << "SSSP_LOADING_GRAPH: " << std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count() << "\n"; // microseconds, not millisecond

  // --
  // Params and memory allocation

  srand(time(NULL));

  size_t n_vertices = G.get_number_of_vertices();
  size_t n_edges = G.get_number_of_edges();

  thrust::device_vector<weight_t> distances(n_vertices);
  thrust::device_vector<vertex_t> predecessors(n_vertices);
  thrust::device_vector<int> edges_visited(1);
  thrust::device_vector<int> vertices_visited(1);

  // Parse sources
  std::vector<int> source_vect;
  gunrock::io::cli::parse_source_string(params.source_string, &source_vect,
                                        n_vertices, params.num_runs);
  // Parse tags
  std::vector<std::string> tag_vect;
  gunrock::io::cli::parse_tag_string(params.tag_string, &tag_vect);

  // --
  // GPU Run

  /// An example of how one can use std::shared_ptr to allocate memory on the
  /// GPU, using a custom deleter that automatically handles deletion of the
  /// memory.
  // std::shared_ptr<weight_t> distances(
  //     allocate<weight_t>(n_vertices * sizeof(weight_t)),
  //     deleter_t<weight_t>());
  // std::shared_ptr<vertex_t> predecessors(
  //     allocate<vertex_t>(n_vertices * sizeof(vertex_t)),
  //     deleter_t<vertex_t>());

  //size_t n_runs = source_vect.size();
  std::vector<float> run_times;

  //auto benchmark_metrics = std::vector<benchmark::host_benchmark_t>(csr.row_offsets.size());
  //for (int i = 1; i < csr.row_offsets.size() - 2; i++) {
  for (int i = 1; i <= n_vertices; i++) {
    benchmark::INIT_BENCH();

    run_times.push_back(gunrock::sssp::run(
        G, i, distances.data().get(), predecessors.data().get()));

    benchmark::host_benchmark_t metrics = benchmark::EXTRACT();
    //benchmark_metrics[i] = metrics;

    benchmark::DESTROY_BENCH();
  }

  // Export metrics
  /*
  if (params.export_metrics && false) {
    gunrock::util::stats::export_performance_stats(
        benchmark_metrics, n_edges, n_vertices, run_times, "sssp",
        params.filename, "market", params.json_dir, params.json_file,
        source_vect, tag_vect, num_arguments, argument_array);
  }
*/
  // --
  // Log

  //print::head(distances, 40, "GPU distances");
  // (ms)
  std::cout << "SSSP_GPU_Elapsed_Time: " << std::accumulate(run_times.begin(), run_times.end(), 0.0) << std::endl;//run_times[params.num_runs - 1]

  // --
  // CPU Run

  if (params.validate && false) {
    thrust::host_vector<weight_t> h_distances(n_vertices);
    thrust::host_vector<vertex_t> h_predecessors(n_vertices);

    float cpu_elapsed = sssp_cpu::run<csr_t, vertex_t, edge_t, weight_t>(
        csr, source_vect.back(), h_distances.data(), h_predecessors.data());

    int n_errors =
        util::compare(distances.data().get(), h_distances.data(), n_vertices);

    print::head(h_distances, 40, "CPU Distances");

    std::cout << "CPU Elapsed Time : " << cpu_elapsed << " (ms)" << std::endl;
    std::cout << "Number of errors : " << n_errors << std::endl;
  }
}

int main(int argc, char** argv) {
  test_sssp(argc, argv);
}
