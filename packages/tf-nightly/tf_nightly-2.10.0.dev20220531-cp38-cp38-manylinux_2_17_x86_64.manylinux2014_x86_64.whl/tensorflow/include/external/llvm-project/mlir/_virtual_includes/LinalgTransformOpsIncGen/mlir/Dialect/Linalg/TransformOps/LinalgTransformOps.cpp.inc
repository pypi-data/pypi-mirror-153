/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::transform::TileOp
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace transform {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_LinalgTransformOps0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isa<::mlir::pdl::OperationType>()))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be PDL handle to an `mlir::Operation *`, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_attr_constraint_LinalgTransformOps0(
    ::mlir::Operation *op, ::mlir::Attribute attr, ::llvm::StringRef attrName) {
  if (attr && !(((attr.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(attr.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return attr && (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))); })))) {
    return op->emitOpError("attribute '") << attrName
        << "' failed to satisfy constraint: 64-bit integer array attribute";
  }
  return ::mlir::success();
}
} // namespace transform
} // namespace mlir
namespace mlir {
namespace transform {

//===----------------------------------------------------------------------===//
// ::mlir::transform::TileOp definitions
//===----------------------------------------------------------------------===//

TileOpAdaptor::TileOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs, ::mlir::RegionRange regions) : odsOperands(values), odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("transform.structured.tile", odsAttrs.getContext());
}

TileOpAdaptor::TileOpAdaptor(TileOp op) : odsOperands(op->getOperands()), odsAttrs(op->getAttrDictionary()), odsRegions(op->getRegions()), odsOpName(op->getName()) {}

::mlir::ValueRange TileOpAdaptor::getOperands() {
  return odsOperands;
}

std::pair<unsigned, unsigned> TileOpAdaptor::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::ValueRange TileOpAdaptor::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(odsOperands.begin(), valueRange.first),
           std::next(odsOperands.begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TileOpAdaptor::getTarget() {
  return *getODSOperands(0).begin();
}

::mlir::DictionaryAttr TileOpAdaptor::getAttributes() {
  return odsAttrs;
}

::mlir::ArrayAttr TileOpAdaptor::getSizesAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 0, odsAttrs.end() - 0, TileOp::getSizesAttrName(*odsOpName)).dyn_cast_or_null<::mlir::ArrayAttr>();
    if (!attr)
      attr = ::mlir::Builder(odsAttrs.getContext()).getI64ArrayAttr({});
    return attr;
}

::mlir::ArrayAttr TileOpAdaptor::getSizes() {
  auto attr = getSizesAttr();
    if (!attr)
      return ::mlir::Builder(odsAttrs.getContext()).getI64ArrayAttr({});
  return attr;
}

::mlir::ArrayAttr TileOpAdaptor::getInterchangeAttr() {
  assert(odsAttrs && "no attributes when constructing adapter");
  auto attr = ::mlir::impl::getAttrFromSortedRange(odsAttrs.begin() + 0, odsAttrs.end() - 0, TileOp::getInterchangeAttrName(*odsOpName)).dyn_cast_or_null<::mlir::ArrayAttr>();
    if (!attr)
      attr = ::mlir::Builder(odsAttrs.getContext()).getI64ArrayAttr({});
    return attr;
}

::mlir::ArrayAttr TileOpAdaptor::getInterchange() {
  auto attr = getInterchangeAttr();
    if (!attr)
      return ::mlir::Builder(odsAttrs.getContext()).getI64ArrayAttr({});
  return attr;
}

::mlir::LogicalResult TileOpAdaptor::verify(::mlir::Location loc) {
  auto namedAttrRange = odsAttrs;
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_interchange;
  ::mlir::Attribute tblgen_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end()) {
      break;
    }
    else if (namedAttrIt->getName() == TileOp::getInterchangeAttrName(*odsOpName)) {
      tblgen_interchange = namedAttrIt->getValue();
    }
    else if (namedAttrIt->getName() == TileOp::getSizesAttrName(*odsOpName)) {
      tblgen_sizes = namedAttrIt->getValue();
    }
    ++namedAttrIt;
  }

  if (tblgen_sizes && !(((tblgen_sizes.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_sizes.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return attr && (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))); }))))
    return emitError(loc, "'transform.structured.tile' op ""attribute 'sizes' failed to satisfy constraint: 64-bit integer array attribute");

  if (tblgen_interchange && !(((tblgen_interchange.isa<::mlir::ArrayAttr>())) && (::llvm::all_of(tblgen_interchange.cast<::mlir::ArrayAttr>(), [&](::mlir::Attribute attr) { return attr && (((attr.isa<::mlir::IntegerAttr>())) && ((attr.cast<::mlir::IntegerAttr>().getType().isSignlessInteger(64)))); }))))
    return emitError(loc, "'transform.structured.tile' op ""attribute 'interchange' failed to satisfy constraint: 64-bit integer array attribute");
  return ::mlir::success();
}

void TileOp::getAsmResultNames(::mlir::OpAsmSetValueNameFn setNameFn) {
  auto resultGroup0 = getODSResults(0);
  if (!llvm::empty(resultGroup0))
    setNameFn(*resultGroup0.begin(), "tiled_linalg_op");
  auto resultGroup1 = getODSResults(1);
  if (!llvm::empty(resultGroup1))
    setNameFn(*resultGroup1.begin(), "loops");
}

std::pair<unsigned, unsigned> TileOp::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range TileOp::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TileOp::getTarget() {
  return *getODSOperands(0).begin();
}

::mlir::MutableOperandRange TileOp::getTargetMutable() {
  auto range = getODSOperandIndexAndLength(0);
  auto mutableRange = ::mlir::MutableOperandRange(getOperation(), range.first, range.second);
  return mutableRange;
}

std::pair<unsigned, unsigned> TileOp::getODSResultIndexAndLength(unsigned index) {
  bool isVariadic[] = {false, true};
  int prevVariadicCount = 0;
  for (unsigned i = 0; i < index; ++i)
    if (isVariadic[i]) ++prevVariadicCount;

  // Calculate how many dynamic values a static variadic operand corresponds to.
  // This assumes all static variadic operands have the same dynamic value count.
  int variadicSize = (getOperation()->getNumResults() - 1) / 1;
  // `index` passed in as the parameter is the static index which counts each
  // operand (variadic or not) as size 1. So here for each previous static variadic
  // operand, we need to offset by (variadicSize - 1) to get where the dynamic
  // value pack for this static operand starts.
  int start = index + (variadicSize - 1) * prevVariadicCount;
  int size = isVariadic[index] ? variadicSize : 1;
  return {start, size};
}

::mlir::Operation::result_range TileOp::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

::mlir::Value TileOp::getTiledLinalgOp() {
  return *getODSResults(0).begin();
}

::mlir::Operation::result_range TileOp::getLoops() {
  return getODSResults(1);
}

::mlir::ArrayAttr TileOp::getSizesAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 0, getSizesAttrName()).dyn_cast_or_null<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr TileOp::getSizes() {
  auto attr = getSizesAttr();
    if (!attr)
      return ::mlir::Builder((*this)->getContext()).getI64ArrayAttr({});
  return attr;
}

::mlir::ArrayAttr TileOp::getInterchangeAttr() {
  return ::mlir::impl::getAttrFromSortedRange((*this)->getAttrs().begin() + 0, (*this)->getAttrs().end() - 0, getInterchangeAttrName()).dyn_cast_or_null<::mlir::ArrayAttr>();
}

::mlir::ArrayAttr TileOp::getInterchange() {
  auto attr = getInterchangeAttr();
    if (!attr)
      return ::mlir::Builder((*this)->getContext()).getI64ArrayAttr({});
  return attr;
}

void TileOp::setSizesAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(getSizesAttrName(), attr);
}

void TileOp::setInterchangeAttr(::mlir::ArrayAttr attr) {
  (*this)->setAttr(getInterchangeAttrName(), attr);
}

void TileOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type tiled_linalg_op, ::mlir::TypeRange loops, ::mlir::Value target, ::mlir::ArrayAttr sizes, ::mlir::ArrayAttr interchange) {
  odsState.addOperands(target);
  if (sizes) {
  odsState.addAttribute(getSizesAttrName(odsState.name), sizes);
  }
  if (interchange) {
  odsState.addAttribute(getInterchangeAttrName(odsState.name), interchange);
  }
  odsState.addTypes(tiled_linalg_op);
  odsState.addTypes(loops);
}

void TileOp::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value target, ::mlir::ArrayAttr sizes, ::mlir::ArrayAttr interchange) {
  odsState.addOperands(target);
  if (sizes) {
  odsState.addAttribute(getSizesAttrName(odsState.name), sizes);
  }
  if (interchange) {
  odsState.addAttribute(getInterchangeAttrName(odsState.name), interchange);
  }
  assert(resultTypes.size() >= 1u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void TileOp::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() >= 1u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult TileOp::verifyInvariantsImpl() {
  auto namedAttrRange = (*this)->getAttrs();
  auto namedAttrIt = namedAttrRange.begin();
  ::mlir::Attribute tblgen_interchange;
  ::mlir::Attribute tblgen_sizes;
  while (true) {
    if (namedAttrIt == namedAttrRange.end()) {
      break;
    }
    else if (namedAttrIt->getName() == getInterchangeAttrName()) {
      tblgen_interchange = namedAttrIt->getValue();
    }
    else if (namedAttrIt->getName() == getSizesAttrName()) {
      tblgen_sizes = namedAttrIt->getValue();
    }
    ++namedAttrIt;
  }

  if (::mlir::failed(__mlir_ods_local_attr_constraint_LinalgTransformOps0(*this, tblgen_sizes, "sizes")))
    return ::mlir::failure();

  if (::mlir::failed(__mlir_ods_local_attr_constraint_LinalgTransformOps0(*this, tblgen_interchange, "interchange")))
    return ::mlir::failure();
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_LinalgTransformOps0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSResults(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_LinalgTransformOps0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSResults(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_LinalgTransformOps0(*this, v.getType(), "result", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult TileOp::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace transform
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::transform::TileOp)


#endif  // GET_OP_CLASSES

