#include <csp_adapter_zeromq/StructWriter.h>

namespace csp_adapter_zeromq {

StructWriter::StructWriter(CspTypePtr& type, const Dictionary& messageMapper) {
  std::string protocol = messageMapper.get<std::string>("protocol");
  if (protocol == "JSON") {
    msg_writer_ = std::make_shared<utils::JSONMessageWriter>(messageMapper);
  } else if (protocol == "RAW_BYTES") {
  } else {
    CSP_THROW(NotImplemented,
              "msg protocol "
                  << protocol
                  << " not currently supported for csp_adapter_zeromqs");
  }
  if (!isRawBytes())
    data_mapper_ = utils::OutputDataMapperCache::instance().create(
        type, *messageMapper.get<DictionaryPtr>("field_map"));
  else if (type->type() != CspType::Type::STRING)
    CSP_THROW(TypeError,
              "RAW_BYTES output expected ts[str] got ts type " << type->type());
};

std::pair<const void*, size_t> StructWriter::write(
    const TimeSeriesProvider* sourcets) {
  msg_writer_->processTick(*data_mapper_, sourcets);
  return msg_writer_->finalize();
}

}  // namespace csp_adapter_zeromq