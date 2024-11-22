#ifndef _IN_ZMQ_STRUCT_WRITER_H
#define _IN_ZMQ_STRUCT_WRITER_H

#include <csp/adapters/utils/JSONMessageWriter.h>
#include <csp/adapters/utils/MessageWriter.h>
#include <csp/core/Exception.h>
#include <csp/engine/CspType.h>
#include <csp/engine/Dictionary.h>
#include <csp/engine/TimeSeriesProvider.h>

namespace csp_zeromq_adapter {

using namespace csp;
using namespace csp::adapters;

class StructWriter {
 public:
  StructWriter(CspTypePtr& type, const Dictionary& messageMapper);

  bool isRawBytes() const { return (bool)!msg_writer_; }
  std::pair<const void*, size_t> write(const TimeSeriesProvider* sourcets);

 private:
  utils::OutputDataMapperPtr data_mapper_;
  std::shared_ptr<utils::MessageWriter> msg_writer_;
};

}  // namespace csp_zeromq_adapter

#endif