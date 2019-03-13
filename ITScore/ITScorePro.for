******************************************************************************
*                                                                            *
*      ITScorePro.for                                                        *
*                                                                            *
*      Copyright (C) 2012  University of Missouri-Columbia                   *
*      All Rights Reserved.                                                  *
*                                                                            *
*      written by Sheng-You Huang in Zou Lab                                 *
*                                                                            *
*      Zou lab: http://zoulab.dalton.missouri.edu/                           *
*                                                                            *
******************************************************************************
*This program is to calculate the ITScorePro scores of a protein structure.
*
*References:
*
*1. Huang, S.-Y., Zou, X. Statistical mechanics-based method to extract atomic 
*distance-dependent potentials from protein structures. Proteins 79:2648-2661, 2011
*
*******************************************************************
      module commonpara
        parameter (nresmax=10000,ntyp=22,rcut=12.2)
        parameter (nmax=62,ddr=0.2,vmax=5.0)

        real :: vvr(ntyp,ntyp,0:nmax)=0.0,record(nresmax)=0.0
        integer :: cij(ntyp,ntyp),countwang,findmatrix(nresmax,100)=0,temp1,temp2

        dimension cpro(nresmax,50,3),ip(nresmax,50),natm(nresmax)
      end module commonpara

***************************************************************

      use commonpara

      character*1 c1,c2,c3,c4
      character*4 resn,atmn
      character*100 line,line0,cmodel,fpdb
      character*100, allocatable :: argv(:)
	  character*80 recordwang(nresmax),temppath
	  character*8 tempreal
************************************************************
      narg=iargc()

      allocate( argv(0:narg) )

      argv=""

      do k=0,narg
        call getarg(k,argv(k))
      end do

      k0=index(argv(0),'         ')-1

      if(narg.lt.1)then
        write(*,*)
        write(*,'(a)')"This program is to calculate "//
     *            "the ITScorePro scores of protein structures."
        write(*,'(a)')"Reference: Huang, S.-Y., Zou, X. Proteins "//
     *            "79:2648-2661, 2011."
        write(*,*)
        write(*,'(a)')'USAGE: ITScorePro'//
     *  ' prot1.pdb [prot2.pdb [prot3.pdb [...]]]'
        write(*,*)
        write(*,'(a)')"The input pdb file(s) can include a single "//
     *  "structure or multiple structures in NMR-style."
        write(*,*)
        write(*,'(a)')"Examples:"
        write(*,'(a)')"       ITScorePro 1BVE.pdb > scores.dat"
        write(*,'(a)')"       ITScorePro 1AJV.pdb 1BVE.pdb > scores.dat"
        write(*,*)
        stop
      end if

**************************************************************
c   reading the potentials
c   Huang, S.-Y., Zou, X. Statistical mechanics-based method to extract atomic 
c   distance-dependent potentials from protein structures. Proteins 79:2648-2661, 2011

      include "potentials.dat"

*************************************************************

      cij=0
      do i=1,ntyp
        do j=1,ntyp
          if(vvr(i,j,1).ne.0.0)cij(i,j)=1
          vvr(i,j,0)=10.0
          do k=1,nmax
            vvr(i,j,k)=min(vvr(i,j,k),vmax)
          end do
        end do
      end do

      do i=1,narg

        cmodel="MODEL        1"
		record=0.0
		findmatrix=0
        open(1,file=argv(i),status='old')

        fend=0

5       natm=0
        nres=0
        ip=0
        line0=""
		countwang=1
        do while(.true.)
          read(1,'(a)',end=10)line
		  recordwang(countwang)=line
		  
          if(line(1:6)=="MODEL")cmodel=line
          if(line(1:6)=="ENDMDL") goto 20

          if(line(1:6)=='ATOM')then
            resn=line(18:20)
            atmn=adjustl(line(13:16))
            if(.not.(line(14:14)=='H'.or.atmn(1:1)=="H"))then
              if(line(18:27).ne.line0(18:27))then
                nres=nres+1
              end if
              natm(nres)=natm(nres)+1
			  findmatrix(nres,natm(nres))=countwang
              read(line(31:),*)(cpro(nres,natm(nres),k),k=1,3)
              ferr=0
              call ctype(resn,atmn,id,ferr)
              ip(nres,natm(nres))=id
              line0=line
            end if
          end if
		  countwang=countwang+1
        end do

10      close (1)
        fend=1

20      continue

        if(nres>0)then

        tscore=0.0

        do i1=1,nres
          do i2=i1+2,nres
            do j1=1,natm(i1)
              do j2=1,natm(i2)
                ip1=ip(i1,j1)
                ip2=ip(i2,j2)
                if(cij(ip1,ip2).ne.0)then
                  dx=cpro(i1,j1,1)-cpro(i2,j2,1)
                  dy=cpro(i1,j1,2)-cpro(i2,j2,2)
                  dz=cpro(i1,j1,3)-cpro(i2,j2,3)
                  rr=sqrt(dx*dx+dy*dy+dz*dz)
                  if(rr < rcut)then
                    kk=nint(rr/ddr)
                    tscore=tscore+vvr(ip1,ip2,kk)
					temp1=findmatrix(i1,j1)
					temp2=findmatrix(i2,j2)
					record(temp1)=record(temp1)+vvr(ip1,ip2,kk)
					record(temp2)=record(temp2)+vvr(ip1,ip2,kk)
                  end if
                end if
              end do
            end do
          end do
        end do

        fpdb=argv(i)
        k0=index(fpdb,"/",back=.true.)

        fpdb=fpdb(k0+1:)

        write(*,'(a,4x,a,2x,f10.2)')trim(fpdb),trim(cmodel),tscore
		lengthtemp=len_trim(argv(i))
		temppath=argv(i)(9:lengthtemp-4)//'_itscore.pdb'
		open(unit=38,file=temppath,status='new')
		do uuu=1,countwang-1
			write(tempreal,'(f8.2)')record(uuu)
			recordwang(uuu)(61:69)=tempreal
			write(38,*)recordwang(uuu)
	     enddo
      write(38,*)'RESULT ',tscore
		
		close(38)
        end if

        if(fend==0) goto 5

      end do

      deallocate ( argv )

      stop
      end


C*****************************************************************
C*****************************************************************
      Subroutine ctype(resn,atmn,id,ferr)

      character*4 resn,atmn
      integer atyp(30)

      resn=adjustl(resn)
      atmn=adjustl(atmn)

      do k=1,30
        atyp(k)=k
      end do

      ferr=0

      if(resn.eq.'GLY')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        end if
      else if(resn.eq.'ALA')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        end if
      else if(resn.eq.'VAL')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG1')then
          id=atyp(6)
        else if(atmn.eq.'CG2')then
          id=atyp(6)
        end if
      else if(resn.eq.'LEU')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(6)
        else if(atmn.eq.'CD1')then
          id=atyp(6)
        else if(atmn.eq.'CD2')then
          id=atyp(6)
        end if
      else if(resn.eq.'ILE')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG1')then
          id=atyp(6)
        else if(atmn.eq.'CG2')then
          id=atyp(6)
        else if(atmn.eq.'CD1')then
          id=atyp(6)
        else if(atmn.eq.'CD')then
          id=atyp(6)
        end if
      else if(resn.eq.'MET'.or.resn.eq.'MSE')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(8)
        else if(atmn.eq.'SD')then
          id=atyp(22)
        else if(atmn.eq.'CE')then
          id=atyp(8)
        end if
      else if(resn.eq.'PRO')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(6)
        else if(atmn.eq.'CD')then
          id=atyp(8)
        end if
      else if(resn.eq.'THR')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(8)
        else if(atmn.eq.'OG1')then
          id=atyp(18)
        else if(atmn.eq.'CG2')then
          id=atyp(6)
        end if
      else if(resn.eq.'PHE')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(5)
        else if(atmn.eq.'CD1')then
          id=atyp(5)
        else if(atmn.eq.'CD2')then
          id=atyp(5)
        else if(atmn.eq.'CE1')then
          id=atyp(5)
        else if(atmn.eq.'CE2')then
          id=atyp(5)
        else if(atmn.eq.'CZ')then
          id=atyp(5)
        end if
      else if(resn.eq.'TRP')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(5)
        else if(atmn.eq.'CD1')then
          id=atyp(5)
        else if(atmn.eq.'CD2')then
          id=atyp(5)
        else if(atmn.eq.'NE1')then
          id=atyp(12)
        else if(atmn.eq.'CE2')then
          id=atyp(5)
        else if(atmn.eq.'CE3')then
          id=atyp(5)
        else if(atmn.eq.'CZ2')then
          id=atyp(5)
        else if(atmn.eq.'CZ3')then
          id=atyp(5)
        else if(atmn.eq.'CH2')then
          id=atyp(5)
        end if
      else if(resn.eq.'SER')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(8)
        else if(atmn.eq.'OG')then
          id=atyp(18)
        end if
      else if(resn.eq.'TYR')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(5)
        else if(atmn.eq.'CD1')then
          id=atyp(5)
        else if(atmn.eq.'CD2')then
          id=atyp(5)
        else if(atmn.eq.'CE1')then
          id=atyp(5)
        else if(atmn.eq.'CE2')then
          id=atyp(5)
        else if(atmn.eq.'CZ')then
          id=atyp(5)
        else if(atmn.eq.'OH')then
          id=atyp(18)
        end if
      else if(resn.eq.'ASN')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(4)
        else if(atmn.eq.'OD1')then
          id=atyp(17)
        else if(atmn.eq.'ND2')then
          id=atyp(11)
        end if
      else if(resn.eq.'GLN')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(6)
        else if(atmn.eq.'CD')then
          id=atyp(4)
        else if(atmn.eq.'OE1')then
          id=atyp(17)
        else if(atmn.eq.'NE2')then
          id=atyp(11)
        end if
      else if(resn.eq.'LYS')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(6)
        else if(atmn.eq.'CD')then
          id=atyp(6)
        else if(atmn.eq.'CE')then
          id=atyp(8)
        else if(atmn.eq.'NZ')then
          id=atyp(14)
        end if
      else if(resn.eq.'CYS')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(8)
        else if(atmn.eq.'SG')then
          id=atyp(21)
        end if
      else if(resn.eq.'GLU')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(6)
        else if(atmn.eq.'CD')then
          id=atyp(2)
        else if(atmn.eq.'OE1')then
          id=atyp(20)
        else if(atmn.eq.'OE2')then
          id=atyp(20)
        end if
      else if(resn.eq.'ASP')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(2)
        else if(atmn.eq.'OD1')then
          id=atyp(20)
        else if(atmn.eq.'OD2')then
          id=atyp(20)
        end if
      else if(resn.eq.'ARG')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(6)
        else if(atmn.eq.'CD')then
          id=atyp(8)
        else if(atmn.eq.'NE')then
          id=atyp(13)
        else if(atmn.eq.'CZ')then
          id=atyp(1)
        else if(atmn.eq.'NH1')then
          id=atyp(10)
        else if(atmn.eq.'NH2')then
          id=atyp(10)
        end if
      else if(resn.eq.'HIS'.or.resn.eq.'HID')then
        if(atmn.eq.'N')then
          id=atyp(9)
        else if(atmn.eq.'CA')then
          id=atyp(7)
        else if(atmn.eq.'C')then
          id=atyp(3)
        else if(atmn.eq.'O')then
          id=atyp(16)
        else if(atmn.eq.'CB')then
          id=atyp(6)
        else if(atmn.eq.'CG')then
          id=atyp(5)
        else if(atmn.eq.'ND1')then
          id=atyp(12)
        else if(atmn.eq.'CD2')then
          id=atyp(5)
        else if(atmn.eq.'CE1')then
          id=atyp(5)
        else if(atmn.eq.'NE2')then
          id=atyp(12)
        end if
      else if(atmn.eq.'OT2')then
        id=atyp(18)
      else if(atmn.eq.'OXT')then
        id=atyp(18)
      else
        id=atyp(22)
c       write(*,*)'ERROR atom type  ',resn,'  ',atmn
        ferr=1
      end if

      return
      end
