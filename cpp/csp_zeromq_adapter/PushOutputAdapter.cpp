#include <csp_zeromq_adapter/PushOutputAdapter.h>

namespace csp_zeromq_adapter {

PushOutputAdapter::PushOutputAdapter(Engine* engine, CspTypePtr& type,
                                     PushSocket& socket,
                                     const Dictionary& messageMapper)
    : OutputAdapter(engine), socket_(socket), writer_(type, messageMapper) {};

void PushOutputAdapter::executeImpl() {
  if (writer_.isRawBytes()) {
    const std::string& value = input()->lastValueTyped<std::string>();
    socket_.push(value);
  } else {
    auto [data, len] = writer_.write(input());
    socket_.push(std::string(static_cast<const char*>(data), len));
  }
}
}  // namespace csp_zeromq_adapter