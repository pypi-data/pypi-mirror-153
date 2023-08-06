#include "omp.h"
#include <Python.h>
#include <stdio.h>

void overlap_parallel_cpp(int *prev, int *curr, Py_ssize_t shape[2],
                          int *output, Py_ssize_t output_cols) {
#ifdef _WIN32
#pragma omp parallel for
#else
#pragma omp parallel for collapse(2)
#endif
  for (int i = 0; i < shape[0]; i++) {
    for (int j = 0; j < shape[1]; j++) {
      int prev_id = prev[i * shape[1] + j];
      int curr_id = curr[i * shape[1] + j];
      int idx = prev_id * output_cols + curr_id;
      if (prev_id && curr_id) {
#ifdef _WIN32
#pragma omp atomic
#else
#pragma omp atomic update
#endif
        output[idx] += 1;
      }
    }
  }
}
