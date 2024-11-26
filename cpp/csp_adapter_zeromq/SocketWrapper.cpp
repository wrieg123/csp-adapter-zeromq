#include <csp_adapter_zeromq/SocketWrapper.h>

#include <iostream>

namespace csp_adapter_zeromq {

SocketWrapper::SocketWrapper(std::string uri, bool bind, bool connect,
                             TimeDelta timeout)
    : uri_(uri),
      bind_(bind),
      connect_(connect),
      timeout_(timeout.asMilliseconds()) {}

void SocketWrapper::connectOrBindSocket(zmq::socket_t& socket) {
  try {
    if (bind_) socket.bind(uri_);
  } catch (const std::exception&) {
    CSP_THROW(RuntimeException, "Could not bind to: " << uri_);
  };
  try {
    if (connect_) socket.connect(uri_);
  } catch (const std::exception&) {
    CSP_THROW(RuntimeException, "Could not connect to: " << uri_);
  };
}

void SocketWrapper::start() {
  engine_running_ = true;
  thread_ptr_ = std::make_unique<std::thread>([this]() { run(); });
}

void SocketWrapper::stop() {
  engine_running_ = false;

  if ((bool)thread_ptr_) thread_ptr_->join();
}

}  // namespace csp_adapter_zeromq