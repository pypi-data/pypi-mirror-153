
subroutine read_dcd_header(fname, nstr, natom)
 implicit none

 ! input variables
 character(len=256), intent(in) :: fname

 ! output variables
 integer, intent(out) :: nstr, natom

 !f2py intent(out) nstr
 !f2py intent(out) natom

 ! temporary variables
 character(len=80), dimension(1:2) :: title
 character(len=4) :: dcdhdr
 integer, dimension(1:9) :: dumi
 real :: dumr
 integer :: ntitle

 ! open dcd file 
 open(24, file=trim(fname), status='old', form='unformatted')

 ! header
 read(24) dcdhdr, nstr, dumi(1:8), dumr, dumi(1:9)
 read(24) ntitle, title(1:ntitle)
 if (ntitle /= 2) then
  print*, 'Error: ntitle /= 2.'
  stop
 end if
 read(24) natom

 ! close dcd file
 close(24)
end subroutine read_dcd_header
