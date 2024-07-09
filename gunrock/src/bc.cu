#include <gunrock/algorithms/bc.hxx>
#include <gunrock/util/performance.hxx>
#include <gunrock/io/parameters.hxx>
#include <iostream>
#include <chrono>

using namespace gunrock;
using namespace memory;
using namespace std::chrono;

void test_bc(int num_arguments, char** argument_array) {
  // --
  // Define types

  using vertex_t = int;
  using edge_t = int;
  using weight_t = float;

  // --
  // IO
auto t1 = std::chrono::high_resolution_clock::now();

  gunrock::io::cli::parameters_t params(num_arguments, argument_array,
                                        "Betweenness Centrality");

  io::matrix_market_t<vertex_t, edge_t, weight_t> mm;
  auto [properties, coo] = mm.load(params.filename);

  format::csr_t<memory_space_t::device, vertex_t, edge_t, weight_t> csr;

  if (params.binary) {
    csr.read_binary(params.filename);
  } else {
    csr.from_coo(coo);
  }
  /*
std::cout << csr.row_offsets.size() << "\n";
std::cout << csr.column_indices.size() << "\n";
std::cout << csr.nonzero_values.size() << "\n";
std::cout << "csr.row_offsets" << std::endl;
for (int i = 0; i < csr.row_offsets.size(); ++i) {
std::cout << csr.row_offsets[i] << ", ";
}  
std::cout << std::endl;
std::cout << "csr.column_indices" << std::endl;
for (int i = 0; i < csr.column_indices.size(); ++i) {
std::cout << csr.column_indices[i] << ", ";
}  
std::cout << std::endl;
std::cout << "csr.nonzero_values" << std::endl;
for (int i = 0; i < csr.nonzero_values.size(); ++i) {
std::cout << csr.nonzero_values[i] << ", ";
}  
std::cout << std::endl;
*/
  // --
  // Build graph

  auto G = graph::build<memory_space_t::device>(properties, csr);
auto t2 = std::chrono::high_resolution_clock::now();
std::cout << "BC_LOADING_GRAPH: " << std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count() << "\n";

  // --
  // Params and memory allocation

  size_t n_vertices = G.get_number_of_vertices();
  size_t n_edges = G.get_number_of_edges();
  thrust::device_vector<weight_t> bc_values(n_vertices);

  // Parse sources
  std::vector<int> source_vect;
  gunrock::io::cli::parse_source_string(params.source_string, &source_vect,
                                        n_vertices, params.num_runs);
  // Parse tags
  //std::vector<std::string> tag_vect;
  //gunrock::io::cli::parse_tag_string(params.tag_string, &tag_vect);

  // --
  // GPU Run

  size_t n_runs = source_vect.size();
  std::vector<float> run_times;

  auto benchmark_metrics = std::vector<benchmark::host_benchmark_t>(n_runs);
  for (int i = 0; i < 1; i++) {
    benchmark::INIT_BENCH();

    run_times.push_back(
        gunrock::bc::run(G, bc_values.data().get()));
        //gunrock::bc::run(G, source_vect[i], bc_values.data().get()));

    benchmark::host_benchmark_t metrics = benchmark::EXTRACT();
    benchmark_metrics[i] = metrics;

    benchmark::DESTROY_BENCH();
  }

  // Export metrics
  //if (params.export_metrics) {
  //  gunrock::util::stats::export_performance_stats(
  //      benchmark_metrics, n_edges, n_vertices, run_times, "bc",
  //      params.filename, "market", params.json_dir, params.json_file,
  //      source_vect, tag_vect, num_arguments, argument_array);
  //}

  // --
  // Log

//  std::cout << "Single source : " << source_vect.back() << "\n";
//  print::head(bc_values, 40, "GPU bc values");

  //std::cout << "GPU Elapsed Time : " << run_times[params.num_runs - 1]
  //          << " (ms)" << std::endl;
  std::cout << "BC_GPU_Elapsed_Time: " << run_times[0] << std::endl; // ms


//std::cout << "bc_values" << std::endl;
//for (int i = 0; i < bc_values.size(); ++i) {
//std::cout << bc_values[i] << ", ";
//}  
//std::cout << std::endl;
//std::cout << "run_times" << std::endl;
//for (int i = 0; i < run_times.size(); ++i) {
//std::cout << run_times[i] << ", ";
//}  
//std::cout << std::endl;
}

int main(int argc, char** argv) {
  test_bc(argc, argv);
}
