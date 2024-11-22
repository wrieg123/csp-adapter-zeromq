#include <csp_zeromq_adapter/PubOutputAdapter.h>

namespace csp_zeromq_adapter {

PubOutputAdapter::PubOutputAdapter(Engine* engine, CspTypePtr& type,
                                   PubSocket& socket, const std::string& topic,
                                   const Dictionary& messageMapper)
    : OutputAdapter(engine),
      socket_(socket),
      topic_(topic),
      writer_(type, messageMapper) {};

void PubOutputAdapter::executeImpl() {
  if (writer_.isRawBytes()) {
    const std::string& value = input()->lastValueTyped<std::string>();
    socket_.push(topic_, value);
  } else {
    auto [data, len] = writer_.write(input());
    socket_.push(topic_, std::string(static_cast<const char*>(data), len));
  }
}

}  // namespace csp_zeromq_adapter