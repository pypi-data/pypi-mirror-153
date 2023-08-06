// automatically generated
/*
Copyright (c) 2018 Advanced Micro Devices, Inc. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

#ifndef INC_HIP_OSTREAM_OPS_H_
#define INC_HIP_OSTREAM_OPS_H_
#ifdef __cplusplus
#include <iostream>

#include "roctracer.h"
#include <string>

namespace roctracer {
namespace hip_support {
static int HIP_depth_max = 1;
static int HIP_depth_max_cnt = 0;
static std::string HIP_structs_regex = "";
// begin ostream ops for HIP 
// basic ostream ops
template <typename T>
  inline static std::ostream& operator<<(std::ostream& out, const T& v) {
     using std::operator<<;
     static bool recursion = false;
     if (recursion == false) { recursion = true; out << v; recursion = false; }
     return out; }
// End of basic ostream ops

inline static std::ostream& operator<<(std::ostream& out, const __locale_struct& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("__locale_struct::__names").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "__names=");
      roctracer::hip_support::operator<<(out, v.__names);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("__locale_struct::__ctype_toupper").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "__ctype_toupper=");
      roctracer::hip_support::operator<<(out, v.__ctype_toupper);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("__locale_struct::__ctype_tolower").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "__ctype_tolower=");
      roctracer::hip_support::operator<<(out, v.__ctype_tolower);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("__locale_struct::__ctype_b").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "__ctype_b=");
      roctracer::hip_support::operator<<(out, v.__ctype_b);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("__locale_struct::__locales").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "__locales=");
      roctracer::hip_support::operator<<(out, v.__locales);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipDeviceArch_t& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipDeviceArch_t::hasDynamicParallelism").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasDynamicParallelism=");
      roctracer::hip_support::operator<<(out, v.hasDynamicParallelism);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::has3dGrid").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "has3dGrid=");
      roctracer::hip_support::operator<<(out, v.has3dGrid);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasSurfaceFuncs").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasSurfaceFuncs=");
      roctracer::hip_support::operator<<(out, v.hasSurfaceFuncs);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasSyncThreadsExt").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasSyncThreadsExt=");
      roctracer::hip_support::operator<<(out, v.hasSyncThreadsExt);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasThreadFenceSystem").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasThreadFenceSystem=");
      roctracer::hip_support::operator<<(out, v.hasThreadFenceSystem);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasFunnelShift").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasFunnelShift=");
      roctracer::hip_support::operator<<(out, v.hasFunnelShift);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasWarpShuffle").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasWarpShuffle=");
      roctracer::hip_support::operator<<(out, v.hasWarpShuffle);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasWarpBallot").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasWarpBallot=");
      roctracer::hip_support::operator<<(out, v.hasWarpBallot);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasWarpVote").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasWarpVote=");
      roctracer::hip_support::operator<<(out, v.hasWarpVote);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasDoubles").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasDoubles=");
      roctracer::hip_support::operator<<(out, v.hasDoubles);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasSharedInt64Atomics").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasSharedInt64Atomics=");
      roctracer::hip_support::operator<<(out, v.hasSharedInt64Atomics);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasGlobalInt64Atomics").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasGlobalInt64Atomics=");
      roctracer::hip_support::operator<<(out, v.hasGlobalInt64Atomics);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasFloatAtomicAdd").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasFloatAtomicAdd=");
      roctracer::hip_support::operator<<(out, v.hasFloatAtomicAdd);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasSharedFloatAtomicExch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasSharedFloatAtomicExch=");
      roctracer::hip_support::operator<<(out, v.hasSharedFloatAtomicExch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasSharedInt32Atomics").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasSharedInt32Atomics=");
      roctracer::hip_support::operator<<(out, v.hasSharedInt32Atomics);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasGlobalFloatAtomicExch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasGlobalFloatAtomicExch=");
      roctracer::hip_support::operator<<(out, v.hasGlobalFloatAtomicExch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceArch_t::hasGlobalInt32Atomics").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hasGlobalInt32Atomics=");
      roctracer::hip_support::operator<<(out, v.hasGlobalInt32Atomics);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipDeviceProp_t& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipDeviceProp_t::pageableMemoryAccessUsesHostPageTables").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "pageableMemoryAccessUsesHostPageTables=");
      roctracer::hip_support::operator<<(out, v.pageableMemoryAccessUsesHostPageTables);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::pageableMemoryAccess").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "pageableMemoryAccess=");
      roctracer::hip_support::operator<<(out, v.pageableMemoryAccess);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::concurrentManagedAccess").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "concurrentManagedAccess=");
      roctracer::hip_support::operator<<(out, v.concurrentManagedAccess);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::directManagedMemAccessFromHost").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "directManagedMemAccessFromHost=");
      roctracer::hip_support::operator<<(out, v.directManagedMemAccessFromHost);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::managedMemory").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "managedMemory=");
      roctracer::hip_support::operator<<(out, v.managedMemory);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::asicRevision").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "asicRevision=");
      roctracer::hip_support::operator<<(out, v.asicRevision);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::isLargeBar").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "isLargeBar=");
      roctracer::hip_support::operator<<(out, v.isLargeBar);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::cooperativeMultiDeviceUnmatchedSharedMem").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "cooperativeMultiDeviceUnmatchedSharedMem=");
      roctracer::hip_support::operator<<(out, v.cooperativeMultiDeviceUnmatchedSharedMem);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::cooperativeMultiDeviceUnmatchedBlockDim").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "cooperativeMultiDeviceUnmatchedBlockDim=");
      roctracer::hip_support::operator<<(out, v.cooperativeMultiDeviceUnmatchedBlockDim);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::cooperativeMultiDeviceUnmatchedGridDim").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "cooperativeMultiDeviceUnmatchedGridDim=");
      roctracer::hip_support::operator<<(out, v.cooperativeMultiDeviceUnmatchedGridDim);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::cooperativeMultiDeviceUnmatchedFunc").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "cooperativeMultiDeviceUnmatchedFunc=");
      roctracer::hip_support::operator<<(out, v.cooperativeMultiDeviceUnmatchedFunc);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::tccDriver").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "tccDriver=");
      roctracer::hip_support::operator<<(out, v.tccDriver);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::ECCEnabled").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "ECCEnabled=");
      roctracer::hip_support::operator<<(out, v.ECCEnabled);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::kernelExecTimeoutEnabled").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "kernelExecTimeoutEnabled=");
      roctracer::hip_support::operator<<(out, v.kernelExecTimeoutEnabled);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::texturePitchAlignment").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "texturePitchAlignment=");
      roctracer::hip_support::operator<<(out, v.texturePitchAlignment);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::textureAlignment").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "textureAlignment=");
      roctracer::hip_support::operator<<(out, v.textureAlignment);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::memPitch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "memPitch=");
      roctracer::hip_support::operator<<(out, v.memPitch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::hdpRegFlushCntl").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hdpRegFlushCntl=");
      roctracer::hip_support::operator<<(out, v.hdpRegFlushCntl);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::hdpMemFlushCntl").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "hdpMemFlushCntl=");
      roctracer::hip_support::operator<<(out, v.hdpMemFlushCntl);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxTexture3D").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxTexture3D=");
      roctracer::hip_support::operator<<(out, v.maxTexture3D);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxTexture2D").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxTexture2D=");
      roctracer::hip_support::operator<<(out, v.maxTexture2D);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxTexture1D").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxTexture1D=");
      roctracer::hip_support::operator<<(out, v.maxTexture1D);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxTexture1DLinear").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxTexture1DLinear=");
      roctracer::hip_support::operator<<(out, v.maxTexture1DLinear);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::cooperativeMultiDeviceLaunch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "cooperativeMultiDeviceLaunch=");
      roctracer::hip_support::operator<<(out, v.cooperativeMultiDeviceLaunch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::cooperativeLaunch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "cooperativeLaunch=");
      roctracer::hip_support::operator<<(out, v.cooperativeLaunch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::integrated").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "integrated=");
      roctracer::hip_support::operator<<(out, v.integrated);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::gcnArchName").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "gcnArchName=");
      roctracer::hip_support::operator<<(out, v.gcnArchName);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::gcnArch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "gcnArch=");
      roctracer::hip_support::operator<<(out, v.gcnArch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::canMapHostMemory").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "canMapHostMemory=");
      roctracer::hip_support::operator<<(out, v.canMapHostMemory);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::isMultiGpuBoard").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "isMultiGpuBoard=");
      roctracer::hip_support::operator<<(out, v.isMultiGpuBoard);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxSharedMemoryPerMultiProcessor").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxSharedMemoryPerMultiProcessor=");
      roctracer::hip_support::operator<<(out, v.maxSharedMemoryPerMultiProcessor);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::pciDeviceID").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "pciDeviceID=");
      roctracer::hip_support::operator<<(out, v.pciDeviceID);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::pciBusID").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "pciBusID=");
      roctracer::hip_support::operator<<(out, v.pciBusID);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::pciDomainID").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "pciDomainID=");
      roctracer::hip_support::operator<<(out, v.pciDomainID);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::concurrentKernels").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "concurrentKernels=");
      roctracer::hip_support::operator<<(out, v.concurrentKernels);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::arch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "arch=");
      roctracer::hip_support::operator<<(out, v.arch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::clockInstructionRate").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "clockInstructionRate=");
      roctracer::hip_support::operator<<(out, v.clockInstructionRate);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::computeMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "computeMode=");
      roctracer::hip_support::operator<<(out, v.computeMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxThreadsPerMultiProcessor").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxThreadsPerMultiProcessor=");
      roctracer::hip_support::operator<<(out, v.maxThreadsPerMultiProcessor);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::l2CacheSize").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "l2CacheSize=");
      roctracer::hip_support::operator<<(out, v.l2CacheSize);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::multiProcessorCount").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "multiProcessorCount=");
      roctracer::hip_support::operator<<(out, v.multiProcessorCount);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::minor").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "minor=");
      roctracer::hip_support::operator<<(out, v.minor);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::major").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "major=");
      roctracer::hip_support::operator<<(out, v.major);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::totalConstMem").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "totalConstMem=");
      roctracer::hip_support::operator<<(out, v.totalConstMem);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::memoryBusWidth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "memoryBusWidth=");
      roctracer::hip_support::operator<<(out, v.memoryBusWidth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::memoryClockRate").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "memoryClockRate=");
      roctracer::hip_support::operator<<(out, v.memoryClockRate);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::clockRate").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "clockRate=");
      roctracer::hip_support::operator<<(out, v.clockRate);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxGridSize").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxGridSize=");
      roctracer::hip_support::operator<<(out, v.maxGridSize);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxThreadsDim").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxThreadsDim=");
      roctracer::hip_support::operator<<(out, v.maxThreadsDim);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::maxThreadsPerBlock").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxThreadsPerBlock=");
      roctracer::hip_support::operator<<(out, v.maxThreadsPerBlock);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::warpSize").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "warpSize=");
      roctracer::hip_support::operator<<(out, v.warpSize);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::regsPerBlock").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "regsPerBlock=");
      roctracer::hip_support::operator<<(out, v.regsPerBlock);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::sharedMemPerBlock").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "sharedMemPerBlock=");
      roctracer::hip_support::operator<<(out, v.sharedMemPerBlock);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::totalGlobalMem").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "totalGlobalMem=");
      roctracer::hip_support::operator<<(out, v.totalGlobalMem);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipDeviceProp_t::name").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "name=");
      roctracer::hip_support::operator<<(out, v.name);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipPointerAttribute_t& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipPointerAttribute_t::allocationFlags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "allocationFlags=");
      roctracer::hip_support::operator<<(out, v.allocationFlags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipPointerAttribute_t::isManaged").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "isManaged=");
      roctracer::hip_support::operator<<(out, v.isManaged);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipPointerAttribute_t::device").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "device=");
      roctracer::hip_support::operator<<(out, v.device);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipPointerAttribute_t::memoryType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "memoryType=");
      roctracer::hip_support::operator<<(out, v.memoryType);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipChannelFormatDesc& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipChannelFormatDesc::f").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "f=");
      roctracer::hip_support::operator<<(out, v.f);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipChannelFormatDesc::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipChannelFormatDesc::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipChannelFormatDesc::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipChannelFormatDesc::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HIP_ARRAY_DESCRIPTOR& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("HIP_ARRAY_DESCRIPTOR::NumChannels").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "NumChannels=");
      roctracer::hip_support::operator<<(out, v.NumChannels);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY_DESCRIPTOR::Format").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Format=");
      roctracer::hip_support::operator<<(out, v.Format);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY_DESCRIPTOR::Height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Height=");
      roctracer::hip_support::operator<<(out, v.Height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY_DESCRIPTOR::Width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Width=");
      roctracer::hip_support::operator<<(out, v.Width);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HIP_ARRAY3D_DESCRIPTOR& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("HIP_ARRAY3D_DESCRIPTOR::Flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Flags=");
      roctracer::hip_support::operator<<(out, v.Flags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY3D_DESCRIPTOR::NumChannels").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "NumChannels=");
      roctracer::hip_support::operator<<(out, v.NumChannels);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY3D_DESCRIPTOR::Format").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Format=");
      roctracer::hip_support::operator<<(out, v.Format);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY3D_DESCRIPTOR::Depth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Depth=");
      roctracer::hip_support::operator<<(out, v.Depth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY3D_DESCRIPTOR::Height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Height=");
      roctracer::hip_support::operator<<(out, v.Height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_ARRAY3D_DESCRIPTOR::Width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Width=");
      roctracer::hip_support::operator<<(out, v.Width);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipArray& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipArray::textureType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "textureType=");
      roctracer::hip_support::operator<<(out, v.textureType);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipArray::NumChannels").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "NumChannels=");
      roctracer::hip_support::operator<<(out, v.NumChannels);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipArray::Format").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Format=");
      roctracer::hip_support::operator<<(out, v.Format);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipArray::depth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "depth=");
      roctracer::hip_support::operator<<(out, v.depth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipArray::height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "height=");
      roctracer::hip_support::operator<<(out, v.height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipArray::width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "width=");
      roctracer::hip_support::operator<<(out, v.width);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipArray::type").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "type=");
      roctracer::hip_support::operator<<(out, v.type);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipArray::desc").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "desc=");
      roctracer::hip_support::operator<<(out, v.desc);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hip_Memcpy2D& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hip_Memcpy2D::Height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Height=");
      roctracer::hip_support::operator<<(out, v.Height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::WidthInBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "WidthInBytes=");
      roctracer::hip_support::operator<<(out, v.WidthInBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::dstPitch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstPitch=");
      roctracer::hip_support::operator<<(out, v.dstPitch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::dstArray").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstArray=");
      roctracer::hip_support::operator<<(out, v.dstArray);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::dstDevice").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstDevice=");
      roctracer::hip_support::operator<<(out, v.dstDevice);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::dstMemoryType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstMemoryType=");
      roctracer::hip_support::operator<<(out, v.dstMemoryType);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::dstY").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstY=");
      roctracer::hip_support::operator<<(out, v.dstY);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::dstXInBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstXInBytes=");
      roctracer::hip_support::operator<<(out, v.dstXInBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::srcPitch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcPitch=");
      roctracer::hip_support::operator<<(out, v.srcPitch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::srcArray").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcArray=");
      roctracer::hip_support::operator<<(out, v.srcArray);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::srcDevice").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcDevice=");
      roctracer::hip_support::operator<<(out, v.srcDevice);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::srcMemoryType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcMemoryType=");
      roctracer::hip_support::operator<<(out, v.srcMemoryType);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::srcY").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcY=");
      roctracer::hip_support::operator<<(out, v.srcY);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hip_Memcpy2D::srcXInBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcXInBytes=");
      roctracer::hip_support::operator<<(out, v.srcXInBytes);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipMipmappedArray& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipMipmappedArray::format").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "format=");
      roctracer::hip_support::operator<<(out, v.format);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::max_mipmap_level").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "max_mipmap_level=");
      roctracer::hip_support::operator<<(out, v.max_mipmap_level);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::min_mipmap_level").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "min_mipmap_level=");
      roctracer::hip_support::operator<<(out, v.min_mipmap_level);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::depth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "depth=");
      roctracer::hip_support::operator<<(out, v.depth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "height=");
      roctracer::hip_support::operator<<(out, v.height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "width=");
      roctracer::hip_support::operator<<(out, v.width);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::type").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "type=");
      roctracer::hip_support::operator<<(out, v.type);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMipmappedArray::desc").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "desc=");
      roctracer::hip_support::operator<<(out, v.desc);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HIP_TEXTURE_DESC& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("HIP_TEXTURE_DESC::reserved").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "reserved=");
      roctracer::hip_support::operator<<(out, v.reserved);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::borderColor").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "borderColor=");
      roctracer::hip_support::operator<<(out, v.borderColor);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::maxMipmapLevelClamp").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxMipmapLevelClamp=");
      roctracer::hip_support::operator<<(out, v.maxMipmapLevelClamp);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::minMipmapLevelClamp").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "minMipmapLevelClamp=");
      roctracer::hip_support::operator<<(out, v.minMipmapLevelClamp);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::mipmapLevelBias").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "mipmapLevelBias=");
      roctracer::hip_support::operator<<(out, v.mipmapLevelBias);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::mipmapFilterMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "mipmapFilterMode=");
      roctracer::hip_support::operator<<(out, v.mipmapFilterMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::maxAnisotropy").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxAnisotropy=");
      roctracer::hip_support::operator<<(out, v.maxAnisotropy);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::filterMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "filterMode=");
      roctracer::hip_support::operator<<(out, v.filterMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_TEXTURE_DESC::addressMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "addressMode=");
      roctracer::hip_support::operator<<(out, v.addressMode);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipResourceDesc& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipResourceDesc::resType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "resType=");
      roctracer::hip_support::operator<<(out, v.resType);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HIP_RESOURCE_DESC& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("HIP_RESOURCE_DESC::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_DESC::resType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "resType=");
      roctracer::hip_support::operator<<(out, v.resType);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipResourceViewDesc& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipResourceViewDesc::lastLayer").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "lastLayer=");
      roctracer::hip_support::operator<<(out, v.lastLayer);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipResourceViewDesc::firstLayer").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "firstLayer=");
      roctracer::hip_support::operator<<(out, v.firstLayer);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipResourceViewDesc::lastMipmapLevel").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "lastMipmapLevel=");
      roctracer::hip_support::operator<<(out, v.lastMipmapLevel);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipResourceViewDesc::firstMipmapLevel").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "firstMipmapLevel=");
      roctracer::hip_support::operator<<(out, v.firstMipmapLevel);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipResourceViewDesc::depth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "depth=");
      roctracer::hip_support::operator<<(out, v.depth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipResourceViewDesc::height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "height=");
      roctracer::hip_support::operator<<(out, v.height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipResourceViewDesc::width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "width=");
      roctracer::hip_support::operator<<(out, v.width);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipResourceViewDesc::format").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "format=");
      roctracer::hip_support::operator<<(out, v.format);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HIP_RESOURCE_VIEW_DESC& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("HIP_RESOURCE_VIEW_DESC::reserved").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "reserved=");
      roctracer::hip_support::operator<<(out, v.reserved);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::lastLayer").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "lastLayer=");
      roctracer::hip_support::operator<<(out, v.lastLayer);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::firstLayer").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "firstLayer=");
      roctracer::hip_support::operator<<(out, v.firstLayer);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::lastMipmapLevel").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "lastMipmapLevel=");
      roctracer::hip_support::operator<<(out, v.lastMipmapLevel);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::firstMipmapLevel").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "firstMipmapLevel=");
      roctracer::hip_support::operator<<(out, v.firstMipmapLevel);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::depth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "depth=");
      roctracer::hip_support::operator<<(out, v.depth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "height=");
      roctracer::hip_support::operator<<(out, v.height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "width=");
      roctracer::hip_support::operator<<(out, v.width);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_RESOURCE_VIEW_DESC::format").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "format=");
      roctracer::hip_support::operator<<(out, v.format);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipPitchedPtr& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipPitchedPtr::ysize").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "ysize=");
      roctracer::hip_support::operator<<(out, v.ysize);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipPitchedPtr::xsize").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "xsize=");
      roctracer::hip_support::operator<<(out, v.xsize);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipPitchedPtr::pitch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "pitch=");
      roctracer::hip_support::operator<<(out, v.pitch);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipExtent& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipExtent::depth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "depth=");
      roctracer::hip_support::operator<<(out, v.depth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExtent::height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "height=");
      roctracer::hip_support::operator<<(out, v.height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExtent::width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "width=");
      roctracer::hip_support::operator<<(out, v.width);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipPos& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipPos::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipPos::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipPos::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipMemcpy3DParms& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipMemcpy3DParms::kind").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "kind=");
      roctracer::hip_support::operator<<(out, v.kind);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemcpy3DParms::extent").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "extent=");
      roctracer::hip_support::operator<<(out, v.extent);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemcpy3DParms::dstPtr").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstPtr=");
      roctracer::hip_support::operator<<(out, v.dstPtr);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemcpy3DParms::dstPos").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstPos=");
      roctracer::hip_support::operator<<(out, v.dstPos);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemcpy3DParms::dstArray").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstArray=");
      roctracer::hip_support::operator<<(out, v.dstArray);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemcpy3DParms::srcPtr").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcPtr=");
      roctracer::hip_support::operator<<(out, v.srcPtr);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemcpy3DParms::srcPos").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcPos=");
      roctracer::hip_support::operator<<(out, v.srcPos);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemcpy3DParms::srcArray").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcArray=");
      roctracer::hip_support::operator<<(out, v.srcArray);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const HIP_MEMCPY3D& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("HIP_MEMCPY3D::Depth").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Depth=");
      roctracer::hip_support::operator<<(out, v.Depth);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::Height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "Height=");
      roctracer::hip_support::operator<<(out, v.Height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::WidthInBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "WidthInBytes=");
      roctracer::hip_support::operator<<(out, v.WidthInBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstHeight").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstHeight=");
      roctracer::hip_support::operator<<(out, v.dstHeight);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstPitch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstPitch=");
      roctracer::hip_support::operator<<(out, v.dstPitch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstArray").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstArray=");
      roctracer::hip_support::operator<<(out, v.dstArray);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstDevice").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstDevice=");
      roctracer::hip_support::operator<<(out, v.dstDevice);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstMemoryType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstMemoryType=");
      roctracer::hip_support::operator<<(out, v.dstMemoryType);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstLOD").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstLOD=");
      roctracer::hip_support::operator<<(out, v.dstLOD);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstZ").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstZ=");
      roctracer::hip_support::operator<<(out, v.dstZ);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstY").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstY=");
      roctracer::hip_support::operator<<(out, v.dstY);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::dstXInBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "dstXInBytes=");
      roctracer::hip_support::operator<<(out, v.dstXInBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcHeight").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcHeight=");
      roctracer::hip_support::operator<<(out, v.srcHeight);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcPitch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcPitch=");
      roctracer::hip_support::operator<<(out, v.srcPitch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcArray").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcArray=");
      roctracer::hip_support::operator<<(out, v.srcArray);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcDevice").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcDevice=");
      roctracer::hip_support::operator<<(out, v.srcDevice);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcMemoryType").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcMemoryType=");
      roctracer::hip_support::operator<<(out, v.srcMemoryType);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcLOD").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcLOD=");
      roctracer::hip_support::operator<<(out, v.srcLOD);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcZ").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcZ=");
      roctracer::hip_support::operator<<(out, v.srcZ);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcY").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcY=");
      roctracer::hip_support::operator<<(out, v.srcY);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("HIP_MEMCPY3D::srcXInBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "srcXInBytes=");
      roctracer::hip_support::operator<<(out, v.srcXInBytes);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uchar1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uchar1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uchar2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uchar2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uchar2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uchar3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uchar3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uchar3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uchar3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uchar4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uchar4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uchar4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uchar4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uchar4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const char1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("char1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const char2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("char2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("char2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const char3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("char3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("char3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("char3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const char4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("char4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("char4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("char4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("char4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ushort1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ushort1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ushort2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ushort2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ushort2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ushort3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ushort3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ushort3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ushort3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ushort4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ushort4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ushort4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ushort4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ushort4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const short1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("short1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const short2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("short2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("short2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const short3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("short3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("short3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("short3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const short4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("short4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("short4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("short4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("short4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uint1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uint1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uint2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uint2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uint2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uint3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uint3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uint3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uint3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const uint4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("uint4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uint4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uint4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("uint4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const int1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("int1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const int2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("int2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("int2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const int3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("int3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("int3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("int3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const int4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("int4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("int4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("int4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("int4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulong1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulong1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulong2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulong2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulong2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulong3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulong3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulong3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulong3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulong4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulong4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulong4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulong4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulong4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const long1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("long1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const long2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("long2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("long2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const long3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("long3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("long3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("long3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const long4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("long4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("long4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("long4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("long4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulonglong1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulonglong1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulonglong2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulonglong2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulonglong2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulonglong3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulonglong3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulonglong3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulonglong3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const ulonglong4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("ulonglong4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulonglong4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulonglong4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("ulonglong4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const longlong1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("longlong1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const longlong2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("longlong2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("longlong2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const longlong3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("longlong3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("longlong3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("longlong3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const longlong4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("longlong4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("longlong4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("longlong4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("longlong4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const float1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("float1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const float2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("float2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("float2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const float3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("float3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("float3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("float3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const float4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("float4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("float4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("float4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("float4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const double1& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("double1::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const double2& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("double2::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("double2::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const double3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("double3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("double3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("double3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const double4& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("double4::w").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "w=");
      roctracer::hip_support::operator<<(out, v.w);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("double4::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("double4::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("double4::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const textureReference& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("textureReference::format").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "format=");
      roctracer::hip_support::operator<<(out, v.format);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::numChannels").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "numChannels=");
      roctracer::hip_support::operator<<(out, v.numChannels);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::textureObject").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "textureObject=");
      roctracer::hip_support::operator<<(out, v.textureObject);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::maxMipmapLevelClamp").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxMipmapLevelClamp=");
      roctracer::hip_support::operator<<(out, v.maxMipmapLevelClamp);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::minMipmapLevelClamp").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "minMipmapLevelClamp=");
      roctracer::hip_support::operator<<(out, v.minMipmapLevelClamp);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::mipmapLevelBias").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "mipmapLevelBias=");
      roctracer::hip_support::operator<<(out, v.mipmapLevelBias);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::mipmapFilterMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "mipmapFilterMode=");
      roctracer::hip_support::operator<<(out, v.mipmapFilterMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::maxAnisotropy").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxAnisotropy=");
      roctracer::hip_support::operator<<(out, v.maxAnisotropy);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::sRGB").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "sRGB=");
      roctracer::hip_support::operator<<(out, v.sRGB);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::channelDesc").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "channelDesc=");
      roctracer::hip_support::operator<<(out, v.channelDesc);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::filterMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "filterMode=");
      roctracer::hip_support::operator<<(out, v.filterMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::readMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "readMode=");
      roctracer::hip_support::operator<<(out, v.readMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("textureReference::normalized").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "normalized=");
      roctracer::hip_support::operator<<(out, v.normalized);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipTextureDesc& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipTextureDesc::maxMipmapLevelClamp").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxMipmapLevelClamp=");
      roctracer::hip_support::operator<<(out, v.maxMipmapLevelClamp);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::minMipmapLevelClamp").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "minMipmapLevelClamp=");
      roctracer::hip_support::operator<<(out, v.minMipmapLevelClamp);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::mipmapLevelBias").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "mipmapLevelBias=");
      roctracer::hip_support::operator<<(out, v.mipmapLevelBias);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::mipmapFilterMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "mipmapFilterMode=");
      roctracer::hip_support::operator<<(out, v.mipmapFilterMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::maxAnisotropy").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxAnisotropy=");
      roctracer::hip_support::operator<<(out, v.maxAnisotropy);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::normalizedCoords").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "normalizedCoords=");
      roctracer::hip_support::operator<<(out, v.normalizedCoords);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::borderColor").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "borderColor=");
      roctracer::hip_support::operator<<(out, v.borderColor);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::sRGB").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "sRGB=");
      roctracer::hip_support::operator<<(out, v.sRGB);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::readMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "readMode=");
      roctracer::hip_support::operator<<(out, v.readMode);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipTextureDesc::filterMode").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "filterMode=");
      roctracer::hip_support::operator<<(out, v.filterMode);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const surfaceReference& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("surfaceReference::surfaceObject").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "surfaceObject=");
      roctracer::hip_support::operator<<(out, v.surfaceObject);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipIpcMemHandle_t& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipIpcMemHandle_t::reserved").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "reserved=");
      roctracer::hip_support::operator<<(out, v.reserved);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipIpcEventHandle_t& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipIpcEventHandle_t::reserved").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "reserved=");
      roctracer::hip_support::operator<<(out, v.reserved);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipFuncAttributes& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipFuncAttributes::sharedSizeBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "sharedSizeBytes=");
      roctracer::hip_support::operator<<(out, v.sharedSizeBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::ptxVersion").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "ptxVersion=");
      roctracer::hip_support::operator<<(out, v.ptxVersion);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::preferredShmemCarveout").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "preferredShmemCarveout=");
      roctracer::hip_support::operator<<(out, v.preferredShmemCarveout);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::numRegs").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "numRegs=");
      roctracer::hip_support::operator<<(out, v.numRegs);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::maxThreadsPerBlock").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxThreadsPerBlock=");
      roctracer::hip_support::operator<<(out, v.maxThreadsPerBlock);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::maxDynamicSharedSizeBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "maxDynamicSharedSizeBytes=");
      roctracer::hip_support::operator<<(out, v.maxDynamicSharedSizeBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::localSizeBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "localSizeBytes=");
      roctracer::hip_support::operator<<(out, v.localSizeBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::constSizeBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "constSizeBytes=");
      roctracer::hip_support::operator<<(out, v.constSizeBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::cacheModeCA").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "cacheModeCA=");
      roctracer::hip_support::operator<<(out, v.cacheModeCA);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipFuncAttributes::binaryVersion").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "binaryVersion=");
      roctracer::hip_support::operator<<(out, v.binaryVersion);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const dim3& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("dim3::z").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "z=");
      roctracer::hip_support::operator<<(out, v.z);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("dim3::y").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "y=");
      roctracer::hip_support::operator<<(out, v.y);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("dim3::x").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "x=");
      roctracer::hip_support::operator<<(out, v.x);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipLaunchParams& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipLaunchParams::stream").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "stream=");
      roctracer::hip_support::operator<<(out, v.stream);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipLaunchParams::sharedMem").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "sharedMem=");
      roctracer::hip_support::operator<<(out, v.sharedMem);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipLaunchParams::blockDim").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "blockDim=");
      roctracer::hip_support::operator<<(out, v.blockDim);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipLaunchParams::gridDim").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "gridDim=");
      roctracer::hip_support::operator<<(out, v.gridDim);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipExternalMemoryHandleDesc& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipExternalMemoryHandleDesc::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalMemoryHandleDesc::size").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "size=");
      roctracer::hip_support::operator<<(out, v.size);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalMemoryHandleDesc_st::union ::handle.fd").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "handle.fd=");
      roctracer::hip_support::operator<<(out, v.handle.fd);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalMemoryHandleDesc::type").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "type=");
      roctracer::hip_support::operator<<(out, v.type);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipExternalMemoryBufferDesc& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipExternalMemoryBufferDesc::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalMemoryBufferDesc::size").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "size=");
      roctracer::hip_support::operator<<(out, v.size);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalMemoryBufferDesc::offset").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "offset=");
      roctracer::hip_support::operator<<(out, v.offset);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipExternalSemaphoreHandleDesc& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipExternalSemaphoreHandleDesc::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalSemaphoreHandleDesc_st::union ::handle.fd").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "handle.fd=");
      roctracer::hip_support::operator<<(out, v.handle.fd);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalSemaphoreHandleDesc::type").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "type=");
      roctracer::hip_support::operator<<(out, v.type);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipExternalSemaphoreSignalParams& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipExternalSemaphoreSignalParams::reserved").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "reserved=");
      roctracer::hip_support::operator<<(out, v.reserved);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalSemaphoreSignalParams::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipExternalSemaphoreWaitParams& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipExternalSemaphoreWaitParams::reserved").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "reserved=");
      roctracer::hip_support::operator<<(out, v.reserved);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipExternalSemaphoreWaitParams::flags").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "flags=");
      roctracer::hip_support::operator<<(out, v.flags);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipHostNodeParams& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipHostNodeParams::fn").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "fn=");
      roctracer::hip_support::operator<<(out, v.fn);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipKernelNodeParams& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipKernelNodeParams::sharedMemBytes").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "sharedMemBytes=");
      roctracer::hip_support::operator<<(out, v.sharedMemBytes);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipKernelNodeParams::gridDim").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "gridDim=");
      roctracer::hip_support::operator<<(out, v.gridDim);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipKernelNodeParams::blockDim").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "blockDim=");
      roctracer::hip_support::operator<<(out, v.blockDim);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hipMemsetParams& v)
{
  roctracer::hip_support::operator<<(out, '{');
  HIP_depth_max_cnt++;
  if (HIP_depth_max == -1 || HIP_depth_max_cnt <= HIP_depth_max) {
    if (std::string("hipMemsetParams::width").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "width=");
      roctracer::hip_support::operator<<(out, v.width);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemsetParams::value").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "value=");
      roctracer::hip_support::operator<<(out, v.value);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemsetParams::pitch").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "pitch=");
      roctracer::hip_support::operator<<(out, v.pitch);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemsetParams::height").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "height=");
      roctracer::hip_support::operator<<(out, v.height);
      roctracer::hip_support::operator<<(out, ", ");
    }
    if (std::string("hipMemsetParams::elementSize").find(HIP_structs_regex) != std::string::npos)   {
      roctracer::hip_support::operator<<(out, "elementSize=");
      roctracer::hip_support::operator<<(out, v.elementSize);
    }
  };
  HIP_depth_max_cnt--;
  roctracer::hip_support::operator<<(out, '}');
  return out;
}
// end ostream ops for HIP 
};};

inline static std::ostream& operator<<(std::ostream& out, const __locale_struct& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipDeviceArch_t& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipDeviceProp_t& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipPointerAttribute_t& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipChannelFormatDesc& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HIP_ARRAY_DESCRIPTOR& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HIP_ARRAY3D_DESCRIPTOR& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipArray& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hip_Memcpy2D& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipMipmappedArray& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HIP_TEXTURE_DESC& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipResourceDesc& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HIP_RESOURCE_DESC& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipResourceViewDesc& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HIP_RESOURCE_VIEW_DESC& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipPitchedPtr& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipExtent& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipPos& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipMemcpy3DParms& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const HIP_MEMCPY3D& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uchar1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uchar2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uchar3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uchar4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const char1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const char2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const char3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const char4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ushort1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ushort2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ushort3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ushort4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const short1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const short2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const short3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const short4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uint1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uint2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uint3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const uint4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const int1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const int2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const int3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const int4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulong1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulong2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulong3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulong4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const long1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const long2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const long3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const long4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulonglong1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulonglong2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulonglong3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const ulonglong4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const longlong1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const longlong2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const longlong3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const longlong4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const float1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const float2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const float3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const float4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const double1& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const double2& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const double3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const double4& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const textureReference& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipTextureDesc& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const surfaceReference& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipIpcMemHandle_t& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipIpcEventHandle_t& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipFuncAttributes& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const dim3& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipLaunchParams& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipExternalMemoryHandleDesc& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipExternalMemoryBufferDesc& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipExternalSemaphoreHandleDesc& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipExternalSemaphoreSignalParams& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipExternalSemaphoreWaitParams& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipHostNodeParams& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipKernelNodeParams& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hipMemsetParams& v)
{
  roctracer::hip_support::operator<<(out, v);
  return out;
}

#endif //__cplusplus
#endif // INC_HIP_OSTREAM_OPS_H_
 
