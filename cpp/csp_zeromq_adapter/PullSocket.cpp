#include <csp_zeromq_adapter/PullSocket.h>

namespace csp_zeromq_adapter {

PullSocket::PullSocket(Engine* engine, zmq::context_t& ctx,
                       GenericPushInputAdapter* adapter, std::string uri,
                       bool bind, bool connect, TimeDelta timeout)
    : SocketWrapper(uri, bind, connect, timeout),
      engine_(engine),
      ctx_(ctx),
      socket_(ctx_, zmq::socket_type::pull),
      input_adapter_(adapter),
      timeout_ms_(timeout.asMilliseconds()) {}

void PullSocket::start() {
  connectOrBindSocket(socket_);

  SocketWrapper::start();
}

void PullSocket::run() {
  socket_.set(zmq::sockopt::rcvtimeo, timeout_ms_);
  zmq::message_t msgPart;
  while (engine_running_) {
    PushBatch batch = PushBatch(engine_->rootEngine());
    if (socket_.recv(msgPart, zmq::recv_flags::none)) {
      input_adapter_->onMessage(msgPart.data(), msgPart.size(), &batch);
    }
  }
}

}  // namespace csp_zeromq_adapter