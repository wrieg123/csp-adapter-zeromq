#include <csp_zeromq_adapter/SubSocket.h>

namespace csp_zeromq_adapter {

SubSocket::SubSocket(Engine* engine, zmq::context_t& ctx, std::string uri,
                     bool bind, bool connect, TimeDelta timeout)
    : SocketWrapper(uri, bind, connect, timeout), engine_(engine), ctx_(ctx) {}

void SubSocket::addAdapter(std::string topic,
                           GenericPushInputAdapter* adapter) {
  input_adapters_.push_back(
      std::make_pair(zmq::socket_t(ctx_, zmq::socket_type::sub), adapter));
  input_adapters_[input_adapters_.size() - 1].first.set(zmq::sockopt::subscribe,
                                                        topic);
}

void SubSocket::start() {
  for (auto& pair : input_adapters_) {
    connectOrBindSocket(pair.first);
  }

  SocketWrapper::start();
}

void SubSocket::run() {
  std::vector<zmq::pollitem_t> items;
  for (int i = 0; i < input_adapters_.size(); ++i) {
    items.push_back(
        {static_cast<void*>(input_adapters_[i].first), 0, ZMQ_POLLIN, 0});
  }

  zmq::message_t msgPart;
  while (engine_running_) {
    const int n = zmq::poll(items.data(), items.size(), timeout_);
    if (n) {
      PushBatch batch = PushBatch(engine_->rootEngine());
      for (int i = 0; i < input_adapters_.size(); ++i) {
        if (items[i].revents & ZMQ_POLLIN) {
          auto& socket = input_adapters_[i].first;
          while (socket.get(zmq::sockopt::events) & ZMQ_POLLIN) {
            if (!socket.recv(msgPart, zmq::recv_flags::dontwait)) {
              break;
            }
            socket.recv(msgPart, zmq::recv_flags::dontwait);
            input_adapters_[i].second->onMessage(msgPart.data(), msgPart.size(),
                                                 &batch);
          }
        }
      }
    }
  }
}

}  // namespace csp_zeromq_adapter