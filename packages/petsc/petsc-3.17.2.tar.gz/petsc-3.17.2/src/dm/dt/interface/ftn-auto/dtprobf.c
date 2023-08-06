#include "petscsys.h"
#include "petscfix.h"
#include "petsc/private/fortranimpl.h"
/* dtprob.c */
/* Fortran interface file */

/*
* This file was generated automatically by bfort from the C source
* file.  
 */

#ifdef PETSC_USE_POINTER_CONVERSION
#if defined(__cplusplus)
extern "C" { 
#endif 
extern void *PetscToPointer(void*);
extern int PetscFromPointer(void *);
extern void PetscRmPointer(void*);
#if defined(__cplusplus)
} 
#endif 

#else

#define PetscToPointer(a) (*(PetscFortranAddr *)(a))
#define PetscFromPointer(a) (PetscFortranAddr)(a)
#define PetscRmPointer(a)
#endif

#include "petscdt.h"
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfmaxwellboltzmann1d_ PETSCPDFMAXWELLBOLTZMANN1D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfmaxwellboltzmann1d_ petscpdfmaxwellboltzmann1d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petsccdfmaxwellboltzmann1d_ PETSCCDFMAXWELLBOLTZMANN1D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petsccdfmaxwellboltzmann1d_ petsccdfmaxwellboltzmann1d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfmaxwellboltzmann2d_ PETSCPDFMAXWELLBOLTZMANN2D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfmaxwellboltzmann2d_ petscpdfmaxwellboltzmann2d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petsccdfmaxwellboltzmann2d_ PETSCCDFMAXWELLBOLTZMANN2D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petsccdfmaxwellboltzmann2d_ petsccdfmaxwellboltzmann2d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfmaxwellboltzmann3d_ PETSCPDFMAXWELLBOLTZMANN3D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfmaxwellboltzmann3d_ petscpdfmaxwellboltzmann3d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petsccdfmaxwellboltzmann3d_ PETSCCDFMAXWELLBOLTZMANN3D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petsccdfmaxwellboltzmann3d_ petsccdfmaxwellboltzmann3d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfgaussian1d_ PETSCPDFGAUSSIAN1D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfgaussian1d_ petscpdfgaussian1d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfsamplegaussian1d_ PETSCPDFSAMPLEGAUSSIAN1D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfsamplegaussian1d_ petscpdfsamplegaussian1d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfgaussian2d_ PETSCPDFGAUSSIAN2D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfgaussian2d_ petscpdfgaussian2d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfsamplegaussian2d_ PETSCPDFSAMPLEGAUSSIAN2D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfsamplegaussian2d_ petscpdfsamplegaussian2d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfconstant1d_ PETSCPDFCONSTANT1D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfconstant1d_ petscpdfconstant1d
#endif
#ifdef PETSC_HAVE_FORTRAN_CAPS
#define petscpdfsampleconstant1d_ PETSCPDFSAMPLECONSTANT1D
#elif !defined(PETSC_HAVE_FORTRAN_UNDERSCORE) && !defined(FORTRANDOUBLEUNDERSCORE)
#define petscpdfsampleconstant1d_ petscpdfsampleconstant1d
#endif


/* Definitions of Fortran Wrapper routines */
#if defined(__cplusplus)
extern "C" {
#endif
PETSC_EXTERN void  petscpdfmaxwellboltzmann1d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscPDFMaxwellBoltzmann1D(x,dummy,p);
}
PETSC_EXTERN void  petsccdfmaxwellboltzmann1d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscCDFMaxwellBoltzmann1D(x,dummy,p);
}
PETSC_EXTERN void  petscpdfmaxwellboltzmann2d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscPDFMaxwellBoltzmann2D(x,dummy,p);
}
PETSC_EXTERN void  petsccdfmaxwellboltzmann2d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscCDFMaxwellBoltzmann2D(x,dummy,p);
}
PETSC_EXTERN void  petscpdfmaxwellboltzmann3d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscPDFMaxwellBoltzmann3D(x,dummy,p);
}
PETSC_EXTERN void  petsccdfmaxwellboltzmann3d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscCDFMaxwellBoltzmann3D(x,dummy,p);
}
PETSC_EXTERN void  petscpdfgaussian1d_( PetscReal x[], PetscReal scale[],PetscReal p[], int *__ierr)
{
*__ierr = PetscPDFGaussian1D(x,scale,p);
}
PETSC_EXTERN void  petscpdfsamplegaussian1d_( PetscReal p[], PetscReal dummy[],PetscReal x[], int *__ierr)
{
*__ierr = PetscPDFSampleGaussian1D(p,dummy,x);
}
PETSC_EXTERN void  petscpdfgaussian2d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscPDFGaussian2D(x,dummy,p);
}
PETSC_EXTERN void  petscpdfsamplegaussian2d_( PetscReal p[], PetscReal dummy[],PetscReal x[], int *__ierr)
{
*__ierr = PetscPDFSampleGaussian2D(p,dummy,x);
}
PETSC_EXTERN void  petscpdfconstant1d_( PetscReal x[], PetscReal dummy[],PetscReal p[], int *__ierr)
{
*__ierr = PetscPDFConstant1D(x,dummy,p);
}
PETSC_EXTERN void  petscpdfsampleconstant1d_( PetscReal p[], PetscReal dummy[],PetscReal x[], int *__ierr)
{
*__ierr = PetscPDFSampleConstant1D(p,dummy,x);
}
#if defined(__cplusplus)
}
#endif
