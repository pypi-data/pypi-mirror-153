/*******************************************************************************
 *
 * MIT License
 *
 * Copyright (c) 2017 Advanced Micro Devices, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 *******************************************************************************/
#ifndef GUARD_CONFIG_H_IN
#define GUARD_CONFIG_H_IN

#define MIOPEN_BACKEND_OPENCL 0
#define MIOPEN_BACKEND_HIP 1
#define MIOPEN_MODE_NOGPU 0
#define MIOPEN_USE_MIOPENTENSILE 0
#define MIOPEN_USE_MIOPENGEMM 0
#define MIOPEN_USE_ROCBLAS 1
#define MIOPEN_BUILD_DEV 0
#define MIOPEN_GPU_SYNC 0

#define MIOPEN_ENABLE_SQLITE 1
#define MIOPEN_ENABLE_SQLITE_KERN_CACHE 1
#define MIOPEN_DEBUG_FIND_DB_CACHING 1
#define MIOPEN_USE_COMGR 1
#define MIOPEN_USE_HIPRTC 0
#define MIOPEN_USE_HIP_KERNELS 1
#define MIOPEN_DISABLE_USERDB 0
#define MIOPEN_EMBED_DB 0
#define BUILD_SHARED_LIBS 1
#define MIOPEN_DISABLE_SYSDB 0
#define MIOPEN_LOG_FUNC_TIME_ENABLE 0
#define MIOPEN_ENABLE_SQLITE_BACKOFF 1
#define MIOPEN_USE_MLIR 1

// "_PACKAGE_" to avoid name contentions: the macros like
// HIP_VERSION_MAJOR are defined in hip_version.h.
// clang-format off
#define HIP_PACKAGE_VERSION_MAJOR 5
#define HIP_PACKAGE_VERSION_MINOR 1
#define HIP_PACKAGE_VERSION_PATCH 22142
// clang-format on

// clang-format off
#define MIOPEN_AMD_COMGR_VERSION_MAJOR 2
#define MIOPEN_AMD_COMGR_VERSION_MINOR 4
#define MIOPEN_AMD_COMGR_VERSION_PATCH 0
// clang-format on

// Truncation rounding or (default) rounding to nearest even (RNE) is enabled.
// This switch controls two related but different aspects of MIOpen behavior:
// 1.  How host code performs conversions of float to bfloat16, important only
//     for testing.
// 2.  How BF16 kernels (which are kind of mixed-precision now and expected to
//     remain in the future)  perform final conversion (and rounding) of FP32
//     to BF16 results. This affects the main functionality of the library.
#define MIOPEN_USE_RNE_BFLOAT16 1

// clang-format off
#define MIOPEN_DEFAULT_FIND_MODE DynamicHybrid
// clang-format on
#define MIOPEN_AMDGCN_ASSEMBLER "/opt/rocm-5.1.3/llvm/bin/clang"
#define HIP_OC_COMPILER "/opt/rocm-5.1.3/bin/clang-ocl"
#define MIOPEN_HIP_COMPILER "/opt/rocm-5.1.3/llvm/bin/clang++"
/* #undef EXTRACTKERNEL_BIN */
#define MIOPEN_OFFLOADBUNDLER_BIN "/opt/rocm-5.1.3/llvm/bin/clang-offload-bundler"
#define MIOPEN_CACHE_DIR "~/.cache/miopen/"

#define MIOPEN_USE_GEMM (MIOPEN_USE_MIOPENTENSILE || MIOPEN_USE_MIOPENGEMM || MIOPEN_USE_ROCBLAS)

// Usage of "defined" operator within macro expansion is undefined behavior,
// so "defined(NDEBUG)" cannot be used there... unlike the following macro:
#ifdef NDEBUG
#define MIOPEN_NDEBUG 1
#else
#define MIOPEN_NDEBUG 0
#endif

// Installable builds are those which aren't intended for debugging.
// We damp down some diagnostic messages (Error -> Warning) etc.
#define MIOPEN_INSTALLABLE (MIOPEN_NDEBUG && !MIOPEN_BUILD_DEV)

#define MIOPEN_ALLOC_BUFFERS 0

#ifndef HIP_PACKAGE_VERSION_MAJOR
#define HIP_PACKAGE_VERSION_MAJOR 0
#endif
#ifndef HIP_PACKAGE_VERSION_MINOR
#define HIP_PACKAGE_VERSION_MINOR 0
#endif
#ifndef HIP_PACKAGE_VERSION_PATCH
#define HIP_PACKAGE_VERSION_PATCH 0
#endif
// 3 decimal digits for major and minor, 6 digits for patch number.
// Max number is 999,999,999999 == 0xE8,D4A5,0FFF that fits into 64-bit math.
#if HIP_PACKAGE_VERSION_MAJOR > 999 || HIP_PACKAGE_VERSION_MAJOR > 999 || \
    HIP_PACKAGE_VERSION_PATCH > 999999
#error "Too big HIP version number(s)"
#endif
#define HIP_PACKAGE_VERSION_FLAT                                                   \
    ((HIP_PACKAGE_VERSION_MAJOR * 1000ULL + HIP_PACKAGE_VERSION_MINOR) * 1000000 + \
     HIP_PACKAGE_VERSION_PATCH)

#endif
