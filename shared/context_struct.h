#include <stdint.h>

typedef struct {
    uintptr_t rip, rsp, rbp;
} unwind_context_t;

typedef unwind_context_t (*_fde_func_t)(unwind_context_t, uintptr_t);