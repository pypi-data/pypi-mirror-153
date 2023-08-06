
#requiresdefine   'PETSC_HAVE_FORTRAN'
ALL: lib
CPPFLAGS = ${NETCFD_INCLUDE} ${EXODUSII_INCLUDE}
CFLAGS   =
FFLAGS   =
SOURCEC  = plexf.c plexcgnsf.c plexcheckinterfacef.c plexdistributef.c plexegadsf.c plexexodusiif.c plexfemf.c plexfvmf.c plexgmshf.c plexindicesf.c plexinterpolatef.c plexmetricf.c plexnaturalf.c plexorientf.c plexpointf.c plexprojectf.c plexrefinef.c plexreorderf.c plexsubmeshf.c plextreef.c plexcreatef.c plexgeometryf.c plexpartitionf.c
SOURCEF  =
SOURCEH  = 
DIRS     =
LIBBASE  = libpetscdm
LOCDIR   = src/dm/impls/plex/ftn-auto/
include ${PETSC_DIR}/lib/petsc/conf/variables
include ${PETSC_DIR}/lib/petsc/conf/rules
include ${PETSC_DIR}/lib/petsc/conf/test
