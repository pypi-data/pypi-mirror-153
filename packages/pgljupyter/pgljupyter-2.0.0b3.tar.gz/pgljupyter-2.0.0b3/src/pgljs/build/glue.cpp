
#include <emscripten.h>

extern "C" {

// Not using size_t for array indices as the values used by the javascript code are signed.

EM_JS(void, array_bounds_check_error, (size_t idx, size_t size), {
  throw 'Array index ' + idx + ' out of bounds: [0,' + size + ')';
});

void array_bounds_check(const int array_size, const int array_idx) {
  if (array_idx < 0 || array_idx >= array_size) {
    array_bounds_check_error(array_idx, array_size);
  }
}

// VoidPtr

void EMSCRIPTEN_KEEPALIVE emscripten_bind_VoidPtr___destroy___0(void** self) {
  delete self;
}

// Color3

PGL::Color3* EMSCRIPTEN_KEEPALIVE emscripten_bind_Color3_Color3_0() {
  return new PGL::Color3();
}

unsigned char EMSCRIPTEN_KEEPALIVE emscripten_bind_Color3_getRed_0(PGL::Color3* self) {
  return self->getRed();
}

unsigned char EMSCRIPTEN_KEEPALIVE emscripten_bind_Color3_getGreen_0(PGL::Color3* self) {
  return self->getGreen();
}

unsigned char EMSCRIPTEN_KEEPALIVE emscripten_bind_Color3_getBlue_0(PGL::Color3* self) {
  return self->getBlue();
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_Color3___destroy___0(PGL::Color3* self) {
  delete self;
}

// BoundingBox

PGL::BoundingBox* EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox_BoundingBox_0() {
  return new PGL::BoundingBox();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox_getXMin_0(PGL::BoundingBox* self) {
  return self->getXMin();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox_getYMin_0(PGL::BoundingBox* self) {
  return self->getYMin();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox_getZMin_0(PGL::BoundingBox* self) {
  return self->getZMin();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox_getXMax_0(PGL::BoundingBox* self) {
  return self->getXMax();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox_getYMax_0(PGL::BoundingBox* self) {
  return self->getYMax();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox_getZMax_0(PGL::BoundingBox* self) {
  return self->getZMax();
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_BoundingBox___destroy___0(PGL::BoundingBox* self) {
  delete self;
}

// Material

PGL::Material* EMSCRIPTEN_KEEPALIVE emscripten_bind_Material_Material_0() {
  return new PGL::Material();
}

PGL::Color3* EMSCRIPTEN_KEEPALIVE emscripten_bind_Material_getAmbient_0(PGL::Material* self) {
  return &self->getAmbient();
}

PGL::Color3* EMSCRIPTEN_KEEPALIVE emscripten_bind_Material_getSpecular_0(PGL::Material* self) {
  return &self->getSpecular();
}

PGL::Color3* EMSCRIPTEN_KEEPALIVE emscripten_bind_Material_getEmission_0(PGL::Material* self) {
  return &self->getEmission();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_Material_getDiffuse_0(PGL::Material* self) {
  return self->getDiffuse();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_Material_getShininess_0(PGL::Material* self) {
  return self->getShininess();
}

float EMSCRIPTEN_KEEPALIVE emscripten_bind_Material_getTransparency_0(PGL::Material* self) {
  return self->getTransparency();
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_Material___destroy___0(PGL::Material* self) {
  delete self;
}

// TriangleSet

PGLJS::TriangleSet* EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_TriangleSet_0() {
  return new PGLJS::TriangleSet();
}

bool EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_isInstanced_0(PGLJS::TriangleSet* self) {
  return self->isInstanced();
}

unsigned int EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_noOfInstances_0(PGLJS::TriangleSet* self) {
  return self->noOfInstances();
}

unsigned int EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_indexSize_0(PGLJS::TriangleSet* self) {
  return self->indexSize();
}

unsigned int EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_pointSize_0(PGLJS::TriangleSet* self) {
  return self->pointSize();
}

unsigned int EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_colorSize_0(PGLJS::TriangleSet* self) {
  return self->colorSize();
}

unsigned int EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_instanceMatrixSize_0(PGLJS::TriangleSet* self) {
  return self->instanceMatrixSize();
}

void* EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_indexData_0(PGLJS::TriangleSet* self) {
  return self->indexData();
}

void* EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_pointData_0(PGLJS::TriangleSet* self) {
  return self->pointData();
}

void* EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_colorData_0(PGLJS::TriangleSet* self) {
  return self->colorData();
}

void* EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_instanceMatrixData_0(PGLJS::TriangleSet* self) {
  return self->instanceMatrixData();
}

PGL::Material* EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_getMaterialForInstance_1(PGLJS::TriangleSet* self, unsigned int i) {
  return self->getMaterialForInstance(i);
}

bool EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_get_hasMaterialPerInstance_0(PGLJS::TriangleSet* self) {
  return self->hasMaterialPerInstance;
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet_set_hasMaterialPerInstance_1(PGLJS::TriangleSet* self, bool arg0) {
  self->hasMaterialPerInstance = arg0;
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_TriangleSet___destroy___0(PGLJS::TriangleSet* self) {
  delete self;
}

// Tesselator

PGLJS::Tesselator* EMSCRIPTEN_KEEPALIVE emscripten_bind_Tesselator_Tesselator_1(char* filename) {
  return new PGLJS::Tesselator(filename);
}

unsigned int EMSCRIPTEN_KEEPALIVE emscripten_bind_Tesselator_trianglesSize_0(PGLJS::Tesselator* self) {
  return self->trianglesSize();
}

PGLJS::TriangleSet* EMSCRIPTEN_KEEPALIVE emscripten_bind_Tesselator_trianglesAt_1(PGLJS::Tesselator* self, unsigned int i) {
  return self->trianglesAt(i);
}

PGL::BoundingBox* EMSCRIPTEN_KEEPALIVE emscripten_bind_Tesselator_bbox_0(PGLJS::Tesselator* self) {
  return self->bbox();
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_Tesselator___destroy___0(PGLJS::Tesselator* self) {
  delete self;
}

// Debug

PGLJS::Debug* EMSCRIPTEN_KEEPALIVE emscripten_bind_Debug_Debug_0() {
  return new PGLJS::Debug();
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_Debug_doLeakCheck_0(PGLJS::Debug* self) {
  self->doLeakCheck();
}

void EMSCRIPTEN_KEEPALIVE emscripten_bind_Debug___destroy___0(PGLJS::Debug* self) {
  delete self;
}

}

