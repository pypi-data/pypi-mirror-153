
! https://numpy.org/devdocs/f2py/python-usage.html
! https://stackoverflow.com/questions/53637455/fortran-matrix-product-slows-when-called-with-f2py-by-python
! https://sites.engineering.ucsb.edu/~shell/che210d/f2py.pdf

subroutine read_dcd(fname, nstr, natom, box, x, y, z)
  implicit none

  ! input variables
  character(len=256), intent(in) :: fname
  integer, intent(in) :: nstr, natom

  ! output variables
  real(kind=8), dimension(nstr, 3), intent(out) :: box
  real, dimension(nstr, natom), intent(out) :: x, y, z

  !f2py box intent(out)
  !f2py x intent(out)
  !f2py y intent(out)
  !f2py z intent(out)

  ! temporary variables
  character(len=80), dimension(1:2) :: title
  character(len=4) :: dcdhdr
  integer, dimension(1:9) :: dumi
  real :: dumr
  real(kind=8) :: dumr8
  integer :: nstr0, ntitle, natom0, i

  ! open dcd file
  open(24, file=trim(fname), status='old', form='unformatted')

  ! header
  !            4a      i         8i     f         9i
  read(24) dcdhdr, nstr0, dumi(1:8), dumr, dumi(1:9)
  if (nstr /= nstr0) then
    print*, 'Error: nstr /= nstr0.'
    stop
  end if
  read(24) ntitle, title(1:ntitle)
  if (ntitle /= 2) then
   print*, 'Error: ntitle /= 2.'
   stop
  end if
  read(24) natom0
  if (natom /= natom0) then
    print*, 'Error: natom /= natom0.'
    stop
  end if

  ! loop over all structures
  do i = 1, nstr, 1
   ! read in box information
   read(24) box(i,1), dumr8, box(i, 2), dumr8, dumr8, box(i, 3)

   ! read in coordinates
   read(24) x(i, 1:natom)
   read(24) y(i, 1:natom)
   read(24) z(i, 1:natom)
  end do

  ! close dcd file
  close(24)
end subroutine read_dcd

