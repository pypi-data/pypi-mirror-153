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

#ifndef INC_HSA_OSTREAM_OPS_H_
#define INC_HSA_OSTREAM_OPS_H_
#ifdef __cplusplus
#include <iostream>

#include "roctracer.h"
#include <string>

namespace roctracer {
namespace hsa_support {
static int HSA_depth_max = 1;
static int HSA_depth_max_cnt = 0;
static std::string HSA_structs_regex = "";
// begin ostream ops for HSA 
// basic ostream ops
template <typename T>
  inline static std::ostream& operator<<(std::ostream& out, const T& v) {
     using std::operator<<;
     static bool recursion = false;
     if (recursion == false) { recursion = true; out << v; recursion = false; }
     return out; }
// End of basic ostream ops

inline static std::ostream& operator<<(std::ostream& out, const hsa_dim3_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_dim3_t::z").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "z=");
      roctracer::hsa_support::operator<<(out, v.z);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_dim3_t::y").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "y=");
      roctracer::hsa_support::operator<<(out, v.y);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_dim3_t::x").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "x=");
      roctracer::hsa_support::operator<<(out, v.x);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_agent_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_cache_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_cache_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_signal_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_group_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_signal_group_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_region_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_region_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_queue_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_queue_t::id").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "id=");
      roctracer::hsa_support::operator<<(out, v.id);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_queue_t::reserved1").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved1=");
      roctracer::hsa_support::operator<<(out, v.reserved1);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_queue_t::size").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "size=");
      roctracer::hsa_support::operator<<(out, v.size);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_queue_t::doorbell_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "doorbell_signal=");
      roctracer::hsa_support::operator<<(out, v.doorbell_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_queue_t::features").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "features=");
      roctracer::hsa_support::operator<<(out, v.features);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_queue_t::type").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "type=");
      roctracer::hsa_support::operator<<(out, v.type);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_kernel_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_kernel_dispatch_packet_t::completion_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "completion_signal=");
      roctracer::hsa_support::operator<<(out, v.completion_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::reserved2").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved2=");
      roctracer::hsa_support::operator<<(out, v.reserved2);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::kernel_object").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "kernel_object=");
      roctracer::hsa_support::operator<<(out, v.kernel_object);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::group_segment_size").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "group_segment_size=");
      roctracer::hsa_support::operator<<(out, v.group_segment_size);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::private_segment_size").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "private_segment_size=");
      roctracer::hsa_support::operator<<(out, v.private_segment_size);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::grid_size_z").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "grid_size_z=");
      roctracer::hsa_support::operator<<(out, v.grid_size_z);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::grid_size_y").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "grid_size_y=");
      roctracer::hsa_support::operator<<(out, v.grid_size_y);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::grid_size_x").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "grid_size_x=");
      roctracer::hsa_support::operator<<(out, v.grid_size_x);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::reserved0").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved0=");
      roctracer::hsa_support::operator<<(out, v.reserved0);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::workgroup_size_z").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "workgroup_size_z=");
      roctracer::hsa_support::operator<<(out, v.workgroup_size_z);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::workgroup_size_y").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "workgroup_size_y=");
      roctracer::hsa_support::operator<<(out, v.workgroup_size_y);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::workgroup_size_x").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "workgroup_size_x=");
      roctracer::hsa_support::operator<<(out, v.workgroup_size_x);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::setup").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "setup=");
      roctracer::hsa_support::operator<<(out, v.setup);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_kernel_dispatch_packet_t::header").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "header=");
      roctracer::hsa_support::operator<<(out, v.header);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_agent_dispatch_packet_t::completion_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "completion_signal=");
      roctracer::hsa_support::operator<<(out, v.completion_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_agent_dispatch_packet_t::reserved2").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved2=");
      roctracer::hsa_support::operator<<(out, v.reserved2);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_agent_dispatch_packet_t::arg").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "arg=");
      roctracer::hsa_support::operator<<(out, v.arg);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_agent_dispatch_packet_t::reserved0").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved0=");
      roctracer::hsa_support::operator<<(out, v.reserved0);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_agent_dispatch_packet_t::type").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "type=");
      roctracer::hsa_support::operator<<(out, v.type);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_agent_dispatch_packet_t::header").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "header=");
      roctracer::hsa_support::operator<<(out, v.header);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_and_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_barrier_and_packet_t::completion_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "completion_signal=");
      roctracer::hsa_support::operator<<(out, v.completion_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_and_packet_t::reserved2").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved2=");
      roctracer::hsa_support::operator<<(out, v.reserved2);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_and_packet_t::dep_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "dep_signal=");
      roctracer::hsa_support::operator<<(out, v.dep_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_and_packet_t::reserved1").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved1=");
      roctracer::hsa_support::operator<<(out, v.reserved1);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_and_packet_t::reserved0").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved0=");
      roctracer::hsa_support::operator<<(out, v.reserved0);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_and_packet_t::header").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "header=");
      roctracer::hsa_support::operator<<(out, v.header);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_or_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_barrier_or_packet_t::completion_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "completion_signal=");
      roctracer::hsa_support::operator<<(out, v.completion_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_or_packet_t::reserved2").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved2=");
      roctracer::hsa_support::operator<<(out, v.reserved2);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_or_packet_t::dep_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "dep_signal=");
      roctracer::hsa_support::operator<<(out, v.dep_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_or_packet_t::reserved1").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved1=");
      roctracer::hsa_support::operator<<(out, v.reserved1);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_or_packet_t::reserved0").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved0=");
      roctracer::hsa_support::operator<<(out, v.reserved0);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_barrier_or_packet_t::header").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "header=");
      roctracer::hsa_support::operator<<(out, v.header);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_isa_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_isa_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_wavefront_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_wavefront_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_reader_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_code_object_reader_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_executable_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_loaded_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_loaded_code_object_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_executable_symbol_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_code_object_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_callback_data_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_callback_data_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_code_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_code_symbol_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_image_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_format_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_image_format_t::channel_order").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "channel_order=");
      roctracer::hsa_support::operator<<(out, v.channel_order);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_format_t::channel_type").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "channel_type=");
      roctracer::hsa_support::operator<<(out, v.channel_type);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_descriptor_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_image_descriptor_t::format").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "format=");
      roctracer::hsa_support::operator<<(out, v.format);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_descriptor_t::array_size").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "array_size=");
      roctracer::hsa_support::operator<<(out, v.array_size);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_descriptor_t::depth").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "depth=");
      roctracer::hsa_support::operator<<(out, v.depth);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_descriptor_t::height").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "height=");
      roctracer::hsa_support::operator<<(out, v.height);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_descriptor_t::width").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "width=");
      roctracer::hsa_support::operator<<(out, v.width);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_descriptor_t::geometry").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "geometry=");
      roctracer::hsa_support::operator<<(out, v.geometry);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_data_info_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_image_data_info_t::alignment").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "alignment=");
      roctracer::hsa_support::operator<<(out, v.alignment);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_data_info_t::size").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "size=");
      roctracer::hsa_support::operator<<(out, v.size);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_region_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_image_region_t::range").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "range=");
      roctracer::hsa_support::operator<<(out, v.range);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_image_region_t::offset").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "offset=");
      roctracer::hsa_support::operator<<(out, v.offset);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_sampler_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_sampler_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_sampler_descriptor_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_sampler_descriptor_t::address_mode").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "address_mode=");
      roctracer::hsa_support::operator<<(out, v.address_mode);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_sampler_descriptor_t::filter_mode").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "filter_mode=");
      roctracer::hsa_support::operator<<(out, v.filter_mode);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_sampler_descriptor_t::coordinate_mode").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "coordinate_mode=");
      roctracer::hsa_support::operator<<(out, v.coordinate_mode);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_images_1_00_pfn_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_images_1_00_pfn_t::hsa_ext_sampler_destroy").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_sampler_destroy=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_sampler_destroy);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_00_pfn_t::hsa_ext_sampler_create").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_sampler_create=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_sampler_create);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_00_pfn_t::hsa_ext_image_copy").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_copy=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_copy);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_00_pfn_t::hsa_ext_image_destroy").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_destroy=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_destroy);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_00_pfn_t::hsa_ext_image_data_get_info").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_data_get_info=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_data_get_info);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_00_pfn_t::hsa_ext_image_get_capability").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_get_capability=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_get_capability);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_images_1_pfn_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_image_data_get_info_with_layout").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_data_get_info_with_layout=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_data_get_info_with_layout);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_image_get_capability_with_layout").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_get_capability_with_layout=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_get_capability_with_layout);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_sampler_destroy").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_sampler_destroy=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_sampler_destroy);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_sampler_create").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_sampler_create=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_sampler_create);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_image_copy").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_copy=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_copy);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_image_destroy").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_destroy=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_destroy);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_image_data_get_info").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_data_get_info=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_data_get_info);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_ext_images_1_pfn_t::hsa_ext_image_get_capability").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "hsa_ext_image_get_capability=");
      roctracer::hsa_support::operator<<(out, v.hsa_ext_image_get_capability);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_vendor_packet_header_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_vendor_packet_header_t::reserved").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved=");
      roctracer::hsa_support::operator<<(out, v.reserved);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_vendor_packet_header_t::AmdFormat").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "AmdFormat=");
      roctracer::hsa_support::operator<<(out, v.AmdFormat);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_vendor_packet_header_t::header").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "header=");
      roctracer::hsa_support::operator<<(out, v.header);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_barrier_value_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_barrier_value_packet_t::completion_signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "completion_signal=");
      roctracer::hsa_support::operator<<(out, v.completion_signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::reserved3").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved3=");
      roctracer::hsa_support::operator<<(out, v.reserved3);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::reserved2").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved2=");
      roctracer::hsa_support::operator<<(out, v.reserved2);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::reserved1").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved1=");
      roctracer::hsa_support::operator<<(out, v.reserved1);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::cond").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "cond=");
      roctracer::hsa_support::operator<<(out, v.cond);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::mask").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "mask=");
      roctracer::hsa_support::operator<<(out, v.mask);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::value").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "value=");
      roctracer::hsa_support::operator<<(out, v.value);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::signal").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "signal=");
      roctracer::hsa_support::operator<<(out, v.signal);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::reserved0").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "reserved0=");
      roctracer::hsa_support::operator<<(out, v.reserved0);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_barrier_value_packet_t::header").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "header=");
      roctracer::hsa_support::operator<<(out, v.header);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_hdp_flush_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_hdp_flush_t::HDP_REG_FLUSH_CNTL").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "HDP_REG_FLUSH_CNTL=");
      roctracer::hsa_support::operator<<(out, v.HDP_REG_FLUSH_CNTL);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_hdp_flush_t::HDP_MEM_FLUSH_CNTL").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "HDP_MEM_FLUSH_CNTL=");
      roctracer::hsa_support::operator<<(out, v.HDP_MEM_FLUSH_CNTL);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_profiling_dispatch_time_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_profiling_dispatch_time_t::end").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "end=");
      roctracer::hsa_support::operator<<(out, v.end);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_profiling_dispatch_time_t::start").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "start=");
      roctracer::hsa_support::operator<<(out, v.start);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_profiling_async_copy_time_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_profiling_async_copy_time_t::end").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "end=");
      roctracer::hsa_support::operator<<(out, v.end);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_profiling_async_copy_time_t::start").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "start=");
      roctracer::hsa_support::operator<<(out, v.start);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_memory_pool_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_memory_pool_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_pitched_ptr_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_pitched_ptr_t::slice").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "slice=");
      roctracer::hsa_support::operator<<(out, v.slice);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_pitched_ptr_t::pitch").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "pitch=");
      roctracer::hsa_support::operator<<(out, v.pitch);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_memory_pool_link_info_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_memory_pool_link_info_t::numa_distance").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "numa_distance=");
      roctracer::hsa_support::operator<<(out, v.numa_distance);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_memory_pool_link_info_t::link_type").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "link_type=");
      roctracer::hsa_support::operator<<(out, v.link_type);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_memory_pool_link_info_t::max_bandwidth").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "max_bandwidth=");
      roctracer::hsa_support::operator<<(out, v.max_bandwidth);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_memory_pool_link_info_t::min_bandwidth").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "min_bandwidth=");
      roctracer::hsa_support::operator<<(out, v.min_bandwidth);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_memory_pool_link_info_t::max_latency").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "max_latency=");
      roctracer::hsa_support::operator<<(out, v.max_latency);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_memory_pool_link_info_t::min_latency").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "min_latency=");
      roctracer::hsa_support::operator<<(out, v.min_latency);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_image_descriptor_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_image_descriptor_t::data").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "data=");
      roctracer::hsa_support::operator<<(out, v.data);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_image_descriptor_t::deviceID").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "deviceID=");
      roctracer::hsa_support::operator<<(out, v.deviceID);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_image_descriptor_t::version").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "version=");
      roctracer::hsa_support::operator<<(out, v.version);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_pointer_info_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_pointer_info_t::global_flags").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "global_flags=");
      roctracer::hsa_support::operator<<(out, v.global_flags);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_pointer_info_t::agentOwner").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "agentOwner=");
      roctracer::hsa_support::operator<<(out, v.agentOwner);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_pointer_info_t::sizeInBytes").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "sizeInBytes=");
      roctracer::hsa_support::operator<<(out, v.sizeInBytes);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_pointer_info_t::type").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "type=");
      roctracer::hsa_support::operator<<(out, v.type);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_pointer_info_t::size").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "size=");
      roctracer::hsa_support::operator<<(out, v.size);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_ipc_memory_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_ipc_memory_t::handle").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "handle=");
      roctracer::hsa_support::operator<<(out, v.handle);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_gpu_memory_fault_info_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_gpu_memory_fault_info_t::fault_reason_mask").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "fault_reason_mask=");
      roctracer::hsa_support::operator<<(out, v.fault_reason_mask);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_gpu_memory_fault_info_t::virtual_address").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "virtual_address=");
      roctracer::hsa_support::operator<<(out, v.virtual_address);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_gpu_memory_fault_info_t::agent").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "agent=");
      roctracer::hsa_support::operator<<(out, v.agent);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_event_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_event_t::event_type").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "event_type=");
      roctracer::hsa_support::operator<<(out, v.event_type);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_svm_attribute_pair_t& v)
{
  roctracer::hsa_support::operator<<(out, '{');
  HSA_depth_max_cnt++;
  if (HSA_depth_max == -1 || HSA_depth_max_cnt <= HSA_depth_max) {
    if (std::string("hsa_amd_svm_attribute_pair_t::value").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "value=");
      roctracer::hsa_support::operator<<(out, v.value);
      roctracer::hsa_support::operator<<(out, ", ");
    }
    if (std::string("hsa_amd_svm_attribute_pair_t::attribute").find(HSA_structs_regex) != std::string::npos)   {
      roctracer::hsa_support::operator<<(out, "attribute=");
      roctracer::hsa_support::operator<<(out, v.attribute);
    }
  };
  HSA_depth_max_cnt--;
  roctracer::hsa_support::operator<<(out, '}');
  return out;
}
// end ostream ops for HSA 
};};

inline static std::ostream& operator<<(std::ostream& out, const hsa_dim3_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_cache_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_signal_group_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_region_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_queue_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_kernel_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_agent_dispatch_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_and_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_barrier_or_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_isa_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_wavefront_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_reader_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_loaded_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_executable_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_code_object_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_callback_data_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_code_symbol_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_format_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_descriptor_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_data_info_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_image_region_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_sampler_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_sampler_descriptor_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_images_1_00_pfn_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_ext_images_1_pfn_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_vendor_packet_header_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_barrier_value_packet_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_hdp_flush_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_profiling_dispatch_time_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_profiling_async_copy_time_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_memory_pool_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_pitched_ptr_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_memory_pool_link_info_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_image_descriptor_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_pointer_info_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_ipc_memory_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_gpu_memory_fault_info_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_event_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

inline static std::ostream& operator<<(std::ostream& out, const hsa_amd_svm_attribute_pair_t& v)
{
  roctracer::hsa_support::operator<<(out, v);
  return out;
}

#endif //__cplusplus
#endif // INC_HSA_OSTREAM_OPS_H_
 
