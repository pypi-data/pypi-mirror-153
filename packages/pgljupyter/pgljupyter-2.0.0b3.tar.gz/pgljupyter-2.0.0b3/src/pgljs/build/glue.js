
// Bindings utilities

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function WrapperObject() {
}
WrapperObject.prototype = Object.create(WrapperObject.prototype);
WrapperObject.prototype.constructor = WrapperObject;
WrapperObject.prototype.__class__ = WrapperObject;
WrapperObject.__cache__ = {};
Module['WrapperObject'] = WrapperObject;

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant)
    @param {*=} __class__ */
function getCache(__class__) {
  return (__class__ || WrapperObject).__cache__;
}
Module['getCache'] = getCache;

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant)
    @param {*=} __class__ */
function wrapPointer(ptr, __class__) {
  var cache = getCache(__class__);
  var ret = cache[ptr];
  if (ret) return ret;
  ret = Object.create((__class__ || WrapperObject).prototype);
  ret.ptr = ptr;
  return cache[ptr] = ret;
}
Module['wrapPointer'] = wrapPointer;

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function castObject(obj, __class__) {
  return wrapPointer(obj.ptr, __class__);
}
Module['castObject'] = castObject;

Module['NULL'] = wrapPointer(0);

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function destroy(obj) {
  if (!obj['__destroy__']) throw 'Error: Cannot destroy object. (Did you create it yourself?)';
  obj['__destroy__']();
  // Remove from cache, so the object can be GC'd and refs added onto it released
  delete getCache(obj.__class__)[obj.ptr];
}
Module['destroy'] = destroy;

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function compare(obj1, obj2) {
  return obj1.ptr === obj2.ptr;
}
Module['compare'] = compare;

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function getPointer(obj) {
  return obj.ptr;
}
Module['getPointer'] = getPointer;

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function getClass(obj) {
  return obj.__class__;
}
Module['getClass'] = getClass;

// Converts big (string or array) values into a C-style storage, in temporary space

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
var ensureCache = {
  buffer: 0,  // the main buffer of temporary storage
  size: 0,   // the size of buffer
  pos: 0,    // the next free offset in buffer
  temps: [], // extra allocations
  needed: 0, // the total size we need next time

  prepare: function() {
    if (ensureCache.needed) {
      // clear the temps
      for (var i = 0; i < ensureCache.temps.length; i++) {
        Module['_free'](ensureCache.temps[i]);
      }
      ensureCache.temps.length = 0;
      // prepare to allocate a bigger buffer
      Module['_free'](ensureCache.buffer);
      ensureCache.buffer = 0;
      ensureCache.size += ensureCache.needed;
      // clean up
      ensureCache.needed = 0;
    }
    if (!ensureCache.buffer) { // happens first time, or when we need to grow
      ensureCache.size += 128; // heuristic, avoid many small grow events
      ensureCache.buffer = Module['_malloc'](ensureCache.size);
      assert(ensureCache.buffer);
    }
    ensureCache.pos = 0;
  },
  alloc: function(array, view) {
    assert(ensureCache.buffer);
    var bytes = view.BYTES_PER_ELEMENT;
    var len = array.length * bytes;
    len = (len + 7) & -8; // keep things aligned to 8 byte boundaries
    var ret;
    if (ensureCache.pos + len >= ensureCache.size) {
      // we failed to allocate in the buffer, ensureCache time around :(
      assert(len > 0); // null terminator, at least
      ensureCache.needed += len;
      ret = Module['_malloc'](len);
      ensureCache.temps.push(ret);
    } else {
      // we can allocate in the buffer
      ret = ensureCache.buffer + ensureCache.pos;
      ensureCache.pos += len;
    }
    return ret;
  },
  copy: function(array, view, offset) {
    offset >>>= 0;
    var bytes = view.BYTES_PER_ELEMENT;
    switch (bytes) {
      case 2: offset >>>= 1; break;
      case 4: offset >>>= 2; break;
      case 8: offset >>>= 3; break;
    }
    for (var i = 0; i < array.length; i++) {
      view[offset + i] = array[i];
    }
  },
};

/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function ensureString(value) {
  if (typeof value === 'string') {
    var intArray = intArrayFromString(value);
    var offset = ensureCache.alloc(intArray, HEAP8);
    ensureCache.copy(intArray, HEAP8, offset);
    return offset;
  }
  return value;
}
/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function ensureInt8(value) {
  if (typeof value === 'object') {
    var offset = ensureCache.alloc(value, HEAP8);
    ensureCache.copy(value, HEAP8, offset);
    return offset;
  }
  return value;
}
/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function ensureInt16(value) {
  if (typeof value === 'object') {
    var offset = ensureCache.alloc(value, HEAP16);
    ensureCache.copy(value, HEAP16, offset);
    return offset;
  }
  return value;
}
/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function ensureInt32(value) {
  if (typeof value === 'object') {
    var offset = ensureCache.alloc(value, HEAP32);
    ensureCache.copy(value, HEAP32, offset);
    return offset;
  }
  return value;
}
/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function ensureFloat32(value) {
  if (typeof value === 'object') {
    var offset = ensureCache.alloc(value, HEAPF32);
    ensureCache.copy(value, HEAPF32, offset);
    return offset;
  }
  return value;
}
/** @suppress {duplicate} (TODO: avoid emitting this multiple times, it is redundant) */
function ensureFloat64(value) {
  if (typeof value === 'object') {
    var offset = ensureCache.alloc(value, HEAPF64);
    ensureCache.copy(value, HEAPF64, offset);
    return offset;
  }
  return value;
}


// VoidPtr
/** @suppress {undefinedVars, duplicate} @this{Object} */function VoidPtr() { throw "cannot construct a VoidPtr, no constructor in IDL" }
VoidPtr.prototype = Object.create(WrapperObject.prototype);
VoidPtr.prototype.constructor = VoidPtr;
VoidPtr.prototype.__class__ = VoidPtr;
VoidPtr.__cache__ = {};
Module['VoidPtr'] = VoidPtr;

  VoidPtr.prototype['__destroy__'] = VoidPtr.prototype.__destroy__ = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_VoidPtr___destroy___0(self);
};
// Color3
/** @suppress {undefinedVars, duplicate} @this{Object} */function Color3() {
  this.ptr = _emscripten_bind_Color3_Color3_0();
  getCache(Color3)[this.ptr] = this;
};;
Color3.prototype = Object.create(WrapperObject.prototype);
Color3.prototype.constructor = Color3;
Color3.prototype.__class__ = Color3;
Color3.__cache__ = {};
Module['Color3'] = Color3;

Color3.prototype['getRed'] = Color3.prototype.getRed = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_Color3_getRed_0(self);
};;

Color3.prototype['getGreen'] = Color3.prototype.getGreen = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_Color3_getGreen_0(self);
};;

Color3.prototype['getBlue'] = Color3.prototype.getBlue = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_Color3_getBlue_0(self);
};;

  Color3.prototype['__destroy__'] = Color3.prototype.__destroy__ = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_Color3___destroy___0(self);
};
// BoundingBox
/** @suppress {undefinedVars, duplicate} @this{Object} */function BoundingBox() {
  this.ptr = _emscripten_bind_BoundingBox_BoundingBox_0();
  getCache(BoundingBox)[this.ptr] = this;
};;
BoundingBox.prototype = Object.create(WrapperObject.prototype);
BoundingBox.prototype.constructor = BoundingBox;
BoundingBox.prototype.__class__ = BoundingBox;
BoundingBox.__cache__ = {};
Module['BoundingBox'] = BoundingBox;

BoundingBox.prototype['getXMin'] = BoundingBox.prototype.getXMin = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_BoundingBox_getXMin_0(self);
};;

BoundingBox.prototype['getYMin'] = BoundingBox.prototype.getYMin = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_BoundingBox_getYMin_0(self);
};;

BoundingBox.prototype['getZMin'] = BoundingBox.prototype.getZMin = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_BoundingBox_getZMin_0(self);
};;

BoundingBox.prototype['getXMax'] = BoundingBox.prototype.getXMax = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_BoundingBox_getXMax_0(self);
};;

BoundingBox.prototype['getYMax'] = BoundingBox.prototype.getYMax = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_BoundingBox_getYMax_0(self);
};;

BoundingBox.prototype['getZMax'] = BoundingBox.prototype.getZMax = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_BoundingBox_getZMax_0(self);
};;

  BoundingBox.prototype['__destroy__'] = BoundingBox.prototype.__destroy__ = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_BoundingBox___destroy___0(self);
};
// Material
/** @suppress {undefinedVars, duplicate} @this{Object} */function Material() {
  this.ptr = _emscripten_bind_Material_Material_0();
  getCache(Material)[this.ptr] = this;
};;
Material.prototype = Object.create(WrapperObject.prototype);
Material.prototype.constructor = Material;
Material.prototype.__class__ = Material;
Material.__cache__ = {};
Module['Material'] = Material;

Material.prototype['getAmbient'] = Material.prototype.getAmbient = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_Material_getAmbient_0(self), Color3);
};;

Material.prototype['getSpecular'] = Material.prototype.getSpecular = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_Material_getSpecular_0(self), Color3);
};;

Material.prototype['getEmission'] = Material.prototype.getEmission = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_Material_getEmission_0(self), Color3);
};;

Material.prototype['getDiffuse'] = Material.prototype.getDiffuse = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_Material_getDiffuse_0(self);
};;

Material.prototype['getShininess'] = Material.prototype.getShininess = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_Material_getShininess_0(self);
};;

Material.prototype['getTransparency'] = Material.prototype.getTransparency = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_Material_getTransparency_0(self);
};;

  Material.prototype['__destroy__'] = Material.prototype.__destroy__ = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_Material___destroy___0(self);
};
// TriangleSet
/** @suppress {undefinedVars, duplicate} @this{Object} */function TriangleSet() {
  this.ptr = _emscripten_bind_TriangleSet_TriangleSet_0();
  getCache(TriangleSet)[this.ptr] = this;
};;
TriangleSet.prototype = Object.create(WrapperObject.prototype);
TriangleSet.prototype.constructor = TriangleSet;
TriangleSet.prototype.__class__ = TriangleSet;
TriangleSet.__cache__ = {};
Module['TriangleSet'] = TriangleSet;

TriangleSet.prototype['isInstanced'] = TriangleSet.prototype.isInstanced = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return !!(_emscripten_bind_TriangleSet_isInstanced_0(self));
};;

TriangleSet.prototype['noOfInstances'] = TriangleSet.prototype.noOfInstances = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_TriangleSet_noOfInstances_0(self);
};;

TriangleSet.prototype['indexSize'] = TriangleSet.prototype.indexSize = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_TriangleSet_indexSize_0(self);
};;

TriangleSet.prototype['pointSize'] = TriangleSet.prototype.pointSize = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_TriangleSet_pointSize_0(self);
};;

TriangleSet.prototype['colorSize'] = TriangleSet.prototype.colorSize = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_TriangleSet_colorSize_0(self);
};;

TriangleSet.prototype['instanceMatrixSize'] = TriangleSet.prototype.instanceMatrixSize = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_TriangleSet_instanceMatrixSize_0(self);
};;

TriangleSet.prototype['indexData'] = TriangleSet.prototype.indexData = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_TriangleSet_indexData_0(self), VoidPtr);
};;

TriangleSet.prototype['pointData'] = TriangleSet.prototype.pointData = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_TriangleSet_pointData_0(self), VoidPtr);
};;

TriangleSet.prototype['colorData'] = TriangleSet.prototype.colorData = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_TriangleSet_colorData_0(self), VoidPtr);
};;

TriangleSet.prototype['instanceMatrixData'] = TriangleSet.prototype.instanceMatrixData = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_TriangleSet_instanceMatrixData_0(self), VoidPtr);
};;

TriangleSet.prototype['getMaterialForInstance'] = TriangleSet.prototype.getMaterialForInstance = /** @suppress {undefinedVars, duplicate} @this{Object} */function(i) {
  var self = this.ptr;
  if (i && typeof i === 'object') i = i.ptr;
  return wrapPointer(_emscripten_bind_TriangleSet_getMaterialForInstance_1(self, i), Material);
};;

  TriangleSet.prototype['get_hasMaterialPerInstance'] = TriangleSet.prototype.get_hasMaterialPerInstance = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return !!(_emscripten_bind_TriangleSet_get_hasMaterialPerInstance_0(self));
};
    TriangleSet.prototype['set_hasMaterialPerInstance'] = TriangleSet.prototype.set_hasMaterialPerInstance = /** @suppress {undefinedVars, duplicate} @this{Object} */function(arg0) {
  var self = this.ptr;
  if (arg0 && typeof arg0 === 'object') arg0 = arg0.ptr;
  _emscripten_bind_TriangleSet_set_hasMaterialPerInstance_1(self, arg0);
};
    Object.defineProperty(TriangleSet.prototype, 'hasMaterialPerInstance', { get: TriangleSet.prototype.get_hasMaterialPerInstance, set: TriangleSet.prototype.set_hasMaterialPerInstance });
  TriangleSet.prototype['__destroy__'] = TriangleSet.prototype.__destroy__ = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_TriangleSet___destroy___0(self);
};
// Tesselator
/** @suppress {undefinedVars, duplicate} @this{Object} */function Tesselator(filename) {
  ensureCache.prepare();
  if (filename && typeof filename === 'object') filename = filename.ptr;
  else filename = ensureString(filename);
  this.ptr = _emscripten_bind_Tesselator_Tesselator_1(filename);
  getCache(Tesselator)[this.ptr] = this;
};;
Tesselator.prototype = Object.create(WrapperObject.prototype);
Tesselator.prototype.constructor = Tesselator;
Tesselator.prototype.__class__ = Tesselator;
Tesselator.__cache__ = {};
Module['Tesselator'] = Tesselator;

Tesselator.prototype['trianglesSize'] = Tesselator.prototype.trianglesSize = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return _emscripten_bind_Tesselator_trianglesSize_0(self);
};;

Tesselator.prototype['trianglesAt'] = Tesselator.prototype.trianglesAt = /** @suppress {undefinedVars, duplicate} @this{Object} */function(i) {
  var self = this.ptr;
  if (i && typeof i === 'object') i = i.ptr;
  return wrapPointer(_emscripten_bind_Tesselator_trianglesAt_1(self, i), TriangleSet);
};;

Tesselator.prototype['bbox'] = Tesselator.prototype.bbox = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  return wrapPointer(_emscripten_bind_Tesselator_bbox_0(self), BoundingBox);
};;

  Tesselator.prototype['__destroy__'] = Tesselator.prototype.__destroy__ = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_Tesselator___destroy___0(self);
};
// Debug
/** @suppress {undefinedVars, duplicate} @this{Object} */function Debug() {
  this.ptr = _emscripten_bind_Debug_Debug_0();
  getCache(Debug)[this.ptr] = this;
};;
Debug.prototype = Object.create(WrapperObject.prototype);
Debug.prototype.constructor = Debug;
Debug.prototype.__class__ = Debug;
Debug.__cache__ = {};
Module['Debug'] = Debug;

Debug.prototype['doLeakCheck'] = Debug.prototype.doLeakCheck = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_Debug_doLeakCheck_0(self);
};;

  Debug.prototype['__destroy__'] = Debug.prototype.__destroy__ = /** @suppress {undefinedVars, duplicate} @this{Object} */function() {
  var self = this.ptr;
  _emscripten_bind_Debug___destroy___0(self);
};