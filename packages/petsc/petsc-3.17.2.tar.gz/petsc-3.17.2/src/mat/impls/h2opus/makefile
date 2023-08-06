-include ../../../../petscdir.mk
#requirespackage 'PETSC_HAVE_H2OPUS'

ALL: lib

FFLAGS    =
SOURCECXX = math2opuscpu.cxx math2opusutilscpu.cxx
SOURCEF   =
SOURCEH   =
LIBBASE   = libpetscmat
DIRS      = cuda
MANSEC    = Mat
LOCDIR    = src/mat/impls/h2opus/

include ${PETSC_DIR}/lib/petsc/conf/variables
include ${PETSC_DIR}/lib/petsc/conf/rules
include ${PETSC_DIR}/lib/petsc/conf/test
