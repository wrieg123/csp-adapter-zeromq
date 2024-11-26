#ifndef _IN_ZMQ_SUB_INPUT_ADAPTER_H
#define _IN_ZMQ_SUB_INPUT_ADAPTER_H

#include <csp/adapters/utils/MessageStructConverter.h>
#include <csp/engine/Dictionary.h>
#include <csp/engine/PushInputAdapter.h>
#include <csp/engine/Struct.h>

namespace csp_adapter_zeromq {

using namespace csp;

class GenericPushInputAdapter final : public PushInputAdapter {
 public:
  GenericPushInputAdapter(Engine* engine, CspTypePtr& type, PushMode pushMode,
                          const Dictionary& properties);
  ~GenericPushInputAdapter() {};

  void onMessage(void*, size_t, PushBatch*);

 private:
  adapters::utils::MessageStructConverterPtr m_converter;
};

}  // namespace csp_adapter_zeromq

#endif
