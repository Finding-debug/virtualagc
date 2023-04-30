### FILE="Main.annotation"
## Copyright:	Public domain.
## Filename:	POWERED_FLIGHT_SUBROUTINES.agc
## Purpose:	A section of Corona revision 261.
##		It is part of the source code for the Apollo Guidance Computer
##		(AGC) for AS-202. No original listings of this software are
##		available; instead, this file was created via disassembly of
##		the core rope modules actually flown on the mission.
## Assembler:	yaYUL
## Contact:	Ron Burkey <info@sandroid.org>.
## Website:	www.ibiblio.org/apollo/index.html
## Mod history:	2023-05-27 MAS  Created from Solarium 55.
## 		2023-07-29 MAS  Updated for Corona.

# THIS ROUTINE ENTERED AT CDUTRIG READS PRESENT CDU REGISTERS AND STORES THEM SCALED AT ONE REVOLUTION AS A DP
# VECTOR IN CDUTEMP. IT COMPUTES SIN,COS(CDUX,Y,Z) AND STORES THEM IN SINCDU,+2,+4 AND COSCDU,+2,+4 RESPECTIVELY
# SCALED AT 2(+1). WHEN ENTERED AT THETRIG THE ROUTINE PERFORMS THE SAME FUNCTION WITH THE DESIRED CDU ANGLE REG-
# ISTERS THETAD,+1,+2. ENTER WITH C(X1) =6 FOR X,Y,Z ( =4 FOR Y,Z ONLY)



		SETLOC	52000
CDUTRIG		EXIT	0

		INHINT
		CS	CDUX
		TS	CDUTEMP
		CS	CDUY
		TS	CDUTEMP +2
		CS	CDUZ
		TS	CDUTEMP +4
		RELINT
		TC	JUMP3

THETRIG		EXIT	0

		INHINT
		CS	THETAD
		TS	CDUTEMP
		CS	THETAD +1
		TS	CDUTEMP +2
		CS	THETAD +2
		TS	CDUTEMP +4
		RELINT

JUMP3		CS	FLAGWRD2	# TEST IF CDUX FLAG SET
		MASK	BIT14		# (CDUXFLAG MASK)
		CCS	A
		TC	JUMP8		# IT IS NOT
		CAF	LOW11
		MASK	CDUTEMP
		TS	CYL
		CS	CYL
		CS	CYL
		CS	CYL
		XCH	CYL
		XCH	CDUTEMP
		
JUMP8		TC	INTPRET

SINCOS		AST,1	0
			2

REPEAT1		SMOVE*	1
		COMP	RTB
			CDUTEMP +6,1
			CDULOGIC
		STORE	CDUTEMP +6,1
		
		NOLOD	1
		SIN
		STORE	SINCDU +6,1
		
		COS*	0
			CDUTEMP +6,1
		STORE	COSCDU +6,1
		
		TIX,1	2
		ABS	TSLT		# TEST IF COS(THETAD+2) LESS THAN COS(60)
		BOV	EXIT
			REPEAT1
			COSCDU +4
			2
			NOGIMLOC	# IT IS NOT. NO NEED TO ALARM
		
		TC	ALARM
		OCT	01407
		
		TC	INTPRET

NOGIMLOC	ITCQ	0

HIGH11		OCT	77760


# THIS ROUTINE COMPUTES DESIRED CDU(GIMBAL) ANGLES GIVEN THE DESIRED NAV. BASE AXES IN XNB AS THREE HALF UNIT
# VECTORS IN STABLE MEMBER COORDINATES. THE DESIRED CDUX,Y,Z APPEAR IN MPAC, +1, +2 AT THE SAME SCALING AS CDUX,
# Y, Z WITH THE INTERPRETER SET TO THE TP MODE



CALCCDU		ITA	1
		ITC
			S1
			CALCGTA
		
		TEST	1		# IF CDUXFLAG SET, RESCALE OGC TO 8 REVS
		RTB
			CDUXFLAG
			GETOGC
			CDUXFIX

GETOGC		VMOVE	1
		RTB	ITCI
			OGC
			V1STO2S
			S1


# THIS ROUTINE COMPUTES THE MATRIX WHICH TRANSFORMS FROM STABLE MEMBER COORDINATES TO NAV. BASE COORDINATES. IT
# REQUIRES SIN,COS(CDUX,Y,Z) IN SINCDU, +2, +4 AND COSCDU, +2, +4 RESPECTIVELY SCALED TO ONE HALF. THE MATRIX IS
# STORED IN X,Y,ZNB AS THREE HALF UNIT ROW VECTORS



CALCSMNB	DMP	1
		COMP
			SINCDU +2
			COSCDU +4
		
		TSRT	0
			SINCDU +4
			1
		
		DMP	1
		VDEF	VSLT
			COSCDU +2
			COSCDU +4
			1
		STORE	XNB
		
		DMP	1
		TSLT
			SINCDU
			SINCDU +4
			1
		STORE	26D
		
		NOLOD	1
		DMP
			SINCDU +2
		
		DMP	1
		DSU
			COSCDU
			COSCDU +2

		DMP	1
		COMP
			SINCDU
			COSCDU +4

		DMP	0
			COSCDU
			SINCDU +2

		DMP	2
		DAD	VDEF
		VSLT
			COSCDU +2
			26D
			-
			1
		STORE	ZNB
		
		NOLOD	1
		VXV	VSLT
			XNB
			1
		STORE	YNB
		
		ITCQ	0


# ROUTINE CALCSCNB TRANSFORMS A MATRIX OF HALF UNIT VECTORS ALONG SPACECRAFT AXES, XSCD, INTO A MATRIX OF HALF
# UNIT VECTORS ALONG NAV. BASE AXES, XNB. ROUTINE CALCNBSC DOES THE INVERSE, STORING THE MATRIX OF UNIT VECTORS
# ALONG SPACECRAFT AXES IN XSC



CALCSCNB	VXSC	0
			XSCD
			COS33
		
		VXSC	1
		BVSU
			ZSCD
			SIN33
		STORE	XNB
		
		VMOVE	0
			YSCD
		STORE	YNB
		
		VXSC	0
			XSCD
			SIN33
		
		VXSC	1
		VAD
			ZSCD
			COS33
		STORE	ZNB
		
		ITCQ	0


CALCNBSC	VXSC	0
			XNB
			COS33
		
		VXSC	1
		VAD
			ZNB
			SIN33
		STORE	XSC
		
		VMOVE	0
			YNB
		STORE	YSC
		
		VXSC	0
			XNB
			SIN33
		
		VXSC	1
		VSU
			ZNB
			COS33
		STORE	ZSC
		
		ITCQ	0

SIN33		2DEC	0.544639000
COS33		2DEC	0.838670600


# THIS ROUTINE COMPUTES INCREMENTAL CHANGES IN CDU(GIMBAL) ANGLES FROM INCREMENTAL ANGULAR CHANGES ABOUT SM AXES.
# IT REQUIRES SM INCREMENTS AS A DP VECTOR IN VAC SCALED AT ONE REVOLUTION, SIN,COS(CDUX,Y,Z) IN SINCDU, +2, +4 
# AND COSCDU, +2, +4 RESPECTIVELY SCALED TO ONE HALF. CDU INCREMENTS APPEAR IN DCDU SCALED AT ONE REV.

SMCDURES	DMP	0
			32D
			COSCDU +2
			
		DMP	1
		BDSU	DDV
			36D
			SINCDU +2
			-
			COSCDU +4
		STORE	DCDU
		
		NOLOD	2
		DMP	TSLT
		BDSU
			SINCDU +4
			1
			34D
		STORE	DCDU +2
		
		DMP	0
			32D
			SINCDU +2
		
		DMP	1
		DAD	TSLT
			36D
			COSCDU +2
			-
			1
		STORE	DCDU +4
		
		ITCQ	0

# THIS ROUTINE COMPUTES INCREMENTAL ANGULAR CHANGES ABOUT NAV. BASE AXES FROM INCREMENTAL CDU ANGLE CHANGES. IT
# REQUIRES THE CDU INCREMENTS AS A DP VECTOR IN DCDU, +2, +4, SCALED AT ONE REVOLUTION. SIN,COS(CDUX,Y,Z) MUST BE
# IN SINCDU, +2, +4, AND COSCDU, +2, +4 RESPECTIVELY SCALED AT ONE HALF. INCREMENTAL NAV. BASE ANGLES APPEAR IN 
# DNB, +2, +4 SCALED AT ONE REVOLUTION



CDUNBRES	DMP	1
		TSLT
			COSCDU +4
			DCDU +2
			1
		STORE	26D
		
		NOLOD	1
		DMP
			SINCDU
		
		DMP	1
		DSU
			COSCDU
			DCDU +4
		
		DMP	0
			26D
			COSCDU
		
		DMP	1
		DAD
			SINCDU
			DCDU +4
		
		TSRT	0
			DCDU
			1
		
		DMP	2
		DAD	VDEF
		VSLT
			SINCDU +4
			DCDU +2
			-
			1
		STORE	DNB
		
		ITCQ	0


# THIS ROUTINE COMPUTES INCREMENTAL CHANGES TO CDU ANGLES FROM INCREMENTAL ANGULAR CHANGES ABOUT NAV. BASE AXES.
# IT REQUIRES THE INCREMENTAL NAV. BASE ANGLES AS A DP VECTOR IN VAC SCALED AT 1 REVOLUTION. SIN,COS(CDUX,Y,Z) 
# MUST BE IN SINCDU, COSCDU RESPECTIVELY SCALED AT 2(+1). IT LEAVES CDU INCREMENTS AS A DP VECTOR IN DCDU AT THE
# SAME SCALING



NBCDURES	DMP	0
			36D
			SINCDU
			
		DMP	1
		DSU	DDV
			34D
			COSCDU
			-
			COSCDU +4
		STORE	DCDU +2
		
		NOLOD	2
		DMP	COMP
		TSLT	DAD
			SINCDU +4
			1
			32D
		STORE	DCDU
		
		DMP	0
			34D
			SINCDU
		
		DMP	1
		DAD	TSLT
			36D
			COSCDU
			-
			1
		STORE	DCDU +4
		
		ITCQ	0


# THIS ROUTINE RESOLVES THE SMALL ANGLE VECTOR STORED AS SM COMPONENTS IN VAC. SCALED TO ONE REVOLUTION, INTO
# COMMANDED CDU ANGLE CHANGES VAC, +2,+4, SCALED TO ONE REVOLUTION, THROUGH THE DESIRED CDU ANGLES DEFINED BY
# THETAD,+1,+2. THE ROUTINE THEN INCREMENTS THETAD,+1,+2 IN 2S COMP. AT CDUX,Y,Z SCALING



CDUDRIVE	ITA	1
		AXT,1	ITC
			S2
			4
			THETRIG

CDUDRVE2	ITC	0
			SMCDURES
		
		TEST	1		# TEST IF CDUX FLAG SET
		TSRT
			CDUXFLAG
			CDUDRVE1
			DCDU
			4
		STORE	DCDU
		
CDUDRVE1	VSLT	1		# RESCALE DCDU AND BRANCH TO
		RTB	ITCI		# INCREMENT THETAD
			DCDU
			1
			INCRCDUS
			S2

CALCTFF		VXV	1
		VSQ	DDV
			UNITR
			VN
			RMAG

		DDV	1
		TSLT	DSU
			MUEARTH
			RMAGSQ
			4

		DOT	0
			VN
			UNITR

		DSQ	0
			2

		EXIT	0

		CAF	NOMBURN		# TEST IF ANY NOMINAL BURN (SPS1,SPS2,
		MASK	FLAGWRD2	# SPS3, SPS4) FLAG SET
		CCS	A
		CS	TWO
		INDEX	FIXLOC		# X1=-2 FOR 400K FT. AND 0 FOR 280K FT.
		TS	X1
		TC	INTPRET
		DMOVE	5
		DSU*	TSLT
		DMP	DAD
		BMN	SQRT
		DAD	TSRT
		DDV	BOV
			RMAG
			R280K,1
			1
			0
			-
			TFFZERO
			-
			11D
			-
			TFFMAX
		STORE	TFF

		ITCQ	0

TFFZERO		DMOVE	1
		RTB
			DPZERO
			FRESHPD
		STORE	TFF

		ITCQ	0

TFFMAX		DMOVE	1
		RTB
			NEARONE
			FRESHPD
		STORE	TFF

		ITCQ	0

R280K		2DEC	6.463509 E6 B-25
R400K		2DEC	6.500085 E6 B-25

NOMBURN		OCT	00170


# THE FOLLOWING SERIES OF CLOSED SUBROUTINES COMPUTE THE REQUIRED VELOCITY VR, SCALED TO 2(+8)M/CS, VELOCITY-TO-BE
# -GAINED VG, SCALED TO 2(+7)M/CS, AND THE MDOIFIED B-VECTOR CBDT, SCALED TO 2(+4)M/CS, FOR THE DIFFERENT PHASES
# OF POWERED FLIGHT.



CALCVGB		VMOVE	0
			VR
		STORE	CBDT		# (CBDT USED HERE AS TEMP. STORAGE FOR VR)
		
		ITA	1
		LXA,1	ITCI
			S2
			XSHIFT
			VRCADR

CALCCBDT	NOLOD	1
		VSU	VSLT
			CBDT		# OLD VR
			4		# D(VR) TO PD SCALED AT 2(+4) M/CS
		
		VXSC	1
		VAD	VXSC
			GRAVITY
			DELTAT
			-
			CFACTOR		# SCALED AT 2(+0)
		STORE	CBDT		# SCALED AT 2(+4) M/CS
		
		VSLT	1
		VSU	STZ
			VR
			1
			VN
			OVFIND		# FIRST PASS THRU CALCVGB MAY OVERFLOW
		STORE	VG		# SCALED AT 2(+7) M/CS
		
		ITCI	0
			S2


# THESE ROUTINES COMPUTE VR FOR THE TWO NOMINAL SPS BURNS OF FLIGHT 202
202SPS1		AXT,1	1		# C(X1) = +0  (SPS1)
		AXT,2	ITC		# C(X2) =+1  (SPS1)
			0
			1
			+5

202SPS2		AXC,1	1		# C(X1) = -2  (SPS2)
		AXC,2			# C(X2) =-1  (SPS2)
			2
			1
		
		DMOVE*	6
		DDV	DSU
		DSQ	DSU*
		ABS	DMP
		DDV*	TSRT
		SQRT	SIGN
		VXSC
			SEMILAT,1	# SCALED AT 2(+27)M
			RMAG		#           2(+25)M
			DP2(-2)
			ESQ(VR),1	# SCALED AT 2(+4)
			MUE		# SCALED AT 2(+38) M(+3)/CS(+2)
			SEMILAT,1
			5
			X2
			UNITR		# VRAD TO PD  SCALED AT 2(+11) M/CS
		
		DMOVE	2
		DMP*	DDV
		SQRT
			MUE
			SEMILAT,1
			RMAGSQ		# SCALED AT 2(+50)M(+2)
					# VHOR MAG. TO PD SCALED AT 2(+9) M/CS
		VXV	1
		UNIT
			RTPACIFC
			UNITR

		NOLOD	1
		DOT	COMP
			UNITW
		STORE	26D

		VXV	1
		VXSC
			UNITR

		SIGN	2
		VXSC	VAD
		VSLT
			NEARONE
			26D
			-
			-
			3
		STORE	VR
		
		ITC	0
			CALCCBDT


# THIS ROUTINE COMPUTES VG, CBDT, FOR LANDING AREA CONTROL DURING BOOST ABORTS ON FLIGHT 202



202ABORT	VXV	0
			RN
			VN
		
		NOLOD	1
		UNIT
		STORE	UNITRXV		# UNIT NORMAL TO PLANE, IP  2(+1)
		
		DSU	1
		TSRT
			RINTALT
			RMAG
			2		# (RE - R) MAG SCALED 2(+27)
		
		VXV	1
		VSLT
			UNITRXV		# IP
			UNITR		# IR
			1		# TIMES 2
		STORE	UNITHORZ	# UNIT HORIZONTAL IN PLANE, IHP  2(+1)
		
		NOLOD	1
		DOT
			VN		# IHP.V  SCALED 2(+8)
		
		DOT	2
		TSRT	DDV
		DMP
			VN
			UNITR		# IR.V  SCALED 2(+8)
			3		# TIMES 2(-3)
			-		# DIVIDE BY IHP.V SCALED 2(+8)
			RINTALT		# RE COT(GAMMA) SCALED  2(+28)
		
		VSQ	1
		DDV
			0		# H SCALED 2(+31)
			MUE		# H(SQ)/MUE = P SCALED 2(+24)
		
		VSQ	1
		TSRT	DDV
			VN		# V(SQ) 2(+14)
			4		# TIMES 2(-4)
			MUE		# V(SQ)/MUE  SCALED 2(-20)
		DDV	2
		DSU	DMP
		BDSU
			DP2(-4)
			RMAG
			-
			RINTALT
			DP2(-4)		# (1+RE((V**2/2 MUE)-1/R))  SCALED 2(+4)
		
		NOLOD	2
		BMN	SQRT
		DMP	TSLT
			SMACHECK	# SMA LESS THAN RE/2
			V400
			2		# VE TO PD SCALED 2(+7)  M/CS
		
		DSU	1
		BPL
			VCRIT		# 22,000 FT/SEC SCALED 2(+7) M/CS
			-		# VE SCALED 2(+7) M/CS
			GETRANGE	# SET RANGE TO MINRANGE
		
		DMP	2
		DAD	DMP
		DAD	TSLT
			14D		# VE SCALED 2(+7)
			KRANGE2
			KRANGE1
			14D		# VE SCALED 2(+7)
			KRANGE0
			4
		STORE	20D		# ENTRY RANGE ANGLE SCALED 2(+0) REVS.

GOTRANGE	NOLOD	1
		COS	VXSC
			RTATLANT	# RADIAL COMP UNIT TARG VECT  2(+2)
		
		SIN	1
		TSLT
			20D
			1		# SINE OF RANGE ANGLE  2(+0)
		
		VXV	1
		UNIT
			RTATLANT
			UNITR
		STORE	22D		# -UNITN, -IN, DESIRED NORMAL SCALED 2(+1)
		
		NOLOD	2
		VXV	VXSC
		VAD	VSLT
			RTATLANT
			-
			-
			1
		STORE	RTARG		# UNIT TARGET VECTOR SCALED 2(+1)
		
		DMP	5
		DDV	DSU
		BMN	SQRT
		DMP	BDSU
		BDDV	BOV
		RTB	TSRT
			RINTALT		# RE SCALED 2(+25)
			-
			-		# P SCALED 2(+24)
			DP2(-6)
			GAMCHECK	# COT(GAMMAE) SQ NEGATIVE
			RMAG		# R COT(GAMMAE) SCALED 2(+28)
			-		# RE COT(GAMMA) SCALED 2(+28)
			-		# (RE - R) SCALED 2(+27)
			TANCHECK	# TAN(THETAFF/2) EXCEEDS ----
			FRESHPD		# ZERO PD POINTER
			7D		# X = TAN(THETAFF/2) SCALED 2(+6)
		
		NOLOD	1
		DSQ	DAD
			DP2(-12)	# DENOMINATOR SCALED 2(+12)
		
		NOLOD	2
		DSU	COMP
		DDV
			DP2(-11)	# 1 - X(SQ) SCALED 2(+12)
			2		# COSEFF SCALED 2(+0)
		
		DOT	2
		TSLT	DSU
		BPL
			UNITR
			RTARG
			2		# COS ANGLE R TO TARG 2(+0)
			4		# COS FREE FALL ANGLE 2(+0)
			PASTIT		# FF ANGLE EXCEEDS ANGLE TO TARGET
		
		TSRT	1
		DDV	VXSC
			0
			5
			2		# SINEFF SCALED 2(+0)
			UNITHORZ	# IHP SINEFF SCALED 2(+1)
		VXSC	1
		VAD	VSU
			UNITR
			4		# IR COSEFF 2(+1)
			-		# UNIT VECTOR ALONG ENTRY-POINT VECT 2(+1)
			RTARG		# MINUS UNIT TARGET VECTOR  2(+1)
		
		NOLOD	1
		ABVAL
		STORE	2		# D SCALED 2(+2)
		
		ABVAL	2
		VXSC	DOT
		TSRT
			VN
			UNITHORZ
			22D		# -UNITN 2(+1)
			1		# DELTA V NORMAL SCALED 2(+11)
		
		ABVAL	2
		BDSU	TSLT
		ABS
			DIFFVECT	# MAG OLD DIFFVECT 2(+2) AFTER ABVAL
			2		# NEW MAG DIFFVECT 2(+2)
			1		# DELD SCALED 2(+1)
		
		NOLOD	0
		STORE	0		# DELD TO PD 0 ALSO
		
		DMP	3
		TSRT	DDV
		DAD	BDDV
		BOV	TSRT
			DELTAT
			2
			13D
			-
			TGOBIAS		# 5 SECS
			-		# ATTEMPT TO COMPUTE NEW ANORMAL 2(-12)
			ANOVFLOW	# IF OVF, ANORMAL = 8 FT/S/S SIGN DELTA V
			3		# SCALE AN TRIAL BACK TO 2(-9)
		STORE	ANORMAL		# ANORMAL SCALED 2(-9) M/CS(+2)
		
GO-ON		NOLOD	1
		VXSC
			UNITRXV		# ANORMAL ALONG IP SCALED 2(-8)
		
		VXSC	1
		ABVAL
			DELV
			KPIP
		STORE	4		# MEASURED DELTA V SCALED 2(+5)
		
		NOLOD	3
		DDV	DMP
		TSLT	VXSC
		VAD	UNIT
			DELTAT
			FULHAM		# APPROX COS OF THRUST ONTO HORIZ PLANE
			5
			UNITHORZ	# COEF OF SIN TERM OF IT SCALED 2(+1)
		
		DDV	1
		ASIN	DAD
			RVH		# RADIUS TO VISUAL HORIZON SCALED 2(+26) M
			RMAG		# R SCALED 2(+25)
			LOOKANG		# PHI SCALED 2(+0) REV.
		
		NOLOD	1
		COS	VXSC
			UNITR		# COS(PHI) IR SCALED 2(+2)
		
		SIN	2
		VXSC	VSU
		VSLT
			18D		# PHI
			12D		# SIN COEF SCALED 2(+1)
			-		# COS(PHI) SCALED 2(+2)
			1		# UNIT FINAL, IT, SCALED 2(+1)
		
		DMP	3
		DDV	TSLT
		BOV	TSRT
		VXSC	RTB
			2		# D  2(+2)
			4		# DELTA V  2(+5)
			0		# DELTA D  2(+1)
			1		# IS MAG VG GR THAN 2(+5) M/CS
			FIXVG		# IF YES, SET MAG VG TO 2(+5) M/CS
			1		# IF NO, SCALE MAG VG BACK TO 2(+6)
			-		# IT  2(+1)
			FRESHPD		# ZERO PD POINTER
		STORE	VG		# VG SCALED 2(+7) M/CS
		
PREXIT		VMOVE	0
			6
		STORE	DIFFVECT	# SAVE NEW DIFFVECT SCALED 2(+1)
		
		VMOVE	0
			ZEROVEC
		STORE	CBDT		# CBDT = 0 FOR 202 ABORTS
		
		ITCI	0
			S2		# RETURN

CHEKEXIT	TC	INTPRET		# EXIT FOR VR CHECK FAILURES

		RTB	1
		ITC
			FRESHPD		# ZERO PD POINTER
			VRFAIL

ANOVFLOW	SIGN	0
			ANPSEUDO	# AN = 8 FT/S/S SIGNED WITH DELTA V
			12D		# DELTA V
		STORE	ANORMAL
		
		ITC	0
			GO-ON

FIXVG		VMOVE	1
		VXSC	RTB
			-		# IT  2(+1)
			DP2(-1)
			FRESHPD		# ZERO PD POINTER
		STORE	VG		# MAG VG 2(+5) M/CS SCALED 2(+7)
		
		ITC	0
			PREXIT		# GO CLOSE OUT 202 ABORT

GETRANGE	DMOVE	0
			MINRANGE
		STORE	20D		# FREEZE RANGE ANGLE AT MINRANGE
		
		ITC	0
			GOTRANGE	# CONTINUE

PASTIT		EXIT	0
		TC	ALARM
		OCT	01403
		TC	CHEKEXIT

SMACHECK	EXIT	0
		TC	ALARM
		OCT	01404
		TC	CHEKEXIT

GAMCHECK	EXIT	0
		TC	ALARM
		OCT	01405
		TC	CHEKEXIT

TANCHECK	EXIT	0
		TC	ALARM
		OCT	01406
		TC	CHEKEXIT

RINTALT		2DEC	6500085 B-25	# 400K FT RADIUS
DP2(-4)		2DEC	0.0625
DP2(-6)		2DEC	0.015625
DP2(-11)	2DEC	0.000488281
DP2(-12)	2DEC	0.000244141
KRANGE0		2DEC	0.188045173	#                 2(+4)
KRANGE1		2DEC	-.713839193	#                 2(+11)
KRANGE2		2DEC	0.681759381	#                 2(+18)
MINRANGE	2DEC	0.019010080	# 6.8436288 DEG   2(+0) REVS.
V400		2DEC	0.865198746	# 110.7454396     2(+7) M/CS
TGOBIAS		2DEC	0.000059605	# 5 SECS          2(+23) CS
VCRIT		2DEC	0.523875000	# 22,000 FT/SEC   2(+7) M/CS
ANPSEUDO	2DEC	0.124846080	# 8 FT/S/S        2(-9) M/CS/CS
RE		2DEC	0.190084130	# 6.378165 E6 M   2(+25) M
RVH		2DEC	0.095042065	# 6.378165 E6 M   2(+26) M
FULHAM		2DEC	0.9397046	# COS 20 DEG.


# THESE ROUTINES COMPUTE VR TO ACHIEVE A CIRCULAR EARTH- OR MOON-CENTERED ORBIT



EARTHORB	DMOVE	1
		ITC
			MUE
			SQRTMU/R

LUNDEBST	DMOVE	1
		INCR,1
			MUM
			6D

SQRTMU/R	NOLOD	2
		DDV	TSLT*
		SQRT
			RMAG
			8D,1		# C(X1) =14-N  (EARTH)
					#       =20-N  (MOON)
		VXV	1
		UNIT	VXSC
			UNITR
			UNITN
		STORE	VR		# VR SCALED AT 2(+8)M/CS
		
		ITC	0
			CALCCBDT


# THIS ROUTINE COMPUTES VR TO ACHIEVE HYPERBOLIC VELOCITY VF FOR TRANSEARTH INJECTION



TRANSEAR	DDV	1
		TSLT*
			MUM
			RMAG
			4,1

		UNIT	0
			VF		# VF SCALED AT 2(+4)M/CS
		STORE	UNITF
		
		NOLOD	4
		DOT	DAD
		DMP	TSLT
		BDDV	DAD
		SQRT
			UNITR
			DP2(-2)
			28D		# (VF SQ)
			3
			-
			DP2(-10)
		STORE	26D		# SCALED AT 2(+5)
		
		NOLOD	1
		DAD	VXSC
			DP2(-5)
			UNITF
		
		DSU	2
		VXSC	VAD
		VXSC	VSLT
			26D
			DP2(-5)
			UNITR
			-
			30D		# (VF)
			2
		STORE	VR		# VR SCALED AT 2(+8)M/CS
		
		ITC	0
			CALCCBDT

DP2(-5)		2DEC	0.03125
DP2(-10)	2DEC	0.000976563


# THIS ROUTINE COMPUTES VR TO ACHIEVE A TRANSLUNAR ELLIPSE DEFINED BY A TARGET VECTOR RTRNSLUN AND A SEMI MAJOR
# AXIS SMA



TRANSLUN	TSLT	1
		SQRT
			MUE
			1
		
		DMOVE	1
		TSRT*
			30D		# (RN)
			10D,1		# RN RESCALED TO 2(+26)M
		
		VMOVE	2
		VSRT*	BVSU
		UNIT	VSRT
			RN
			10D,1		# RTRNSLUN-RMAG SCALED AT 2(+25)M
			RTRNSLUN
			1
		
		VSRT	1
		BVSU
			UNITR
			1
		STORE	UNITD
		
		NOLOD	1
		VAD
			UNITR
		STORE	UNITS
		
		ABVAL	2
		DAD	DAD
		TSRT
			RTRNSLUN
			30D		# (C)
			-		# (RN)
			1
		STORE	S		# S SCALED AT 2(+26)M
		
		NOLOD	1
		DSU	TSLC
			30D		# (C)
			X2
		STORE	DN
		
		NOLOD	1
		TSRT*	BDSU
			6,2
			SMA
		
		DMP	3
		BDDV	INCR,2
		TSLT*	SQRT
		SIGN	VXSC
			SMA
			DN
			-
			16D
			0,2
			SGNTHETA
			UNITS
		
		TSRT	1
		BDSU	TSRT
			S
			6D
			SMA
			4
		
		DMP	4
		BDDV	SQRT
		TSRT	VXSC
		VAD	VSLT
		VXSC
			SMA
			S
			-
			6
			UNITD
			-
			9D
		STORE	VR		# VR SCALED AT 2(+8)M/CS
		
		ITC	0
			CALCCBDT

MUE		2DEC	0.145011008	# 3.98603223 E14 SCALED 2(+38)M(+3)/CS(+2)
MUM		2DEC	0.114151696	# 4.90277800 E08 SCALED 2(+32)M(+3)/CS(+2)


# THIS ROUTINE COMPUTES THE DESIRED THRUST DIRECTION AS A HALF UNIT VECTOR XSC. IT COMPUTES THE HALF UNIT VECTOR
# YSC ALONG RN*XSC  (I.E. DEFINES A PITCH AXIS HORIZONTAL, YAW AXIS UP ROLL ATTITUDE) AND ZSC ALONG XSC*YSC. IT
# REQUIRES PRIOR PASSES THROUGH ROUTINES CALCRVG AND CALCVGB TO ESTABLISH UNITR, VG, AND CBDT. X1 MUST CONTAIN
# 0,2,4... TO LOAD THE APPROPRIATE INTEGRATED INITIAL THRUST ACCELERATION MAGNITUDE ATDT



CALCXSC		UNIT	0
			VG
		STORE	UNITVG
		
		NOLOD	2
		VPROJ	VSLT
		BVSU
			CBDT		# SCALED AT 2(+4)M/CS
			2
			CBDT
		
		NOLOD	5
		ABVAL	DDV*
		DSQ	BDSU
		SQRT	DMP*
		TSLT	VXSC
		VAD	UNIT
			ATDT,1		# SCALED AT 2(+5)M/CS
			NEARONE
			ATDT,1
			2
			UNITVG
		STORE	XSC
		
		NOLOD	2
		VXV	UNIT
		COMP
			UNITR
		STORE	YSC
		
		NOLOD	2
		VXV	UNIT
		COMP
			XSC
		STORE	ZSC
		ITCQ	0


# 	THIS ROUTINE RESOLVES THE VECTOR IN RTINIT THROUGH AN ANGULAR ROTATION WIE(DTEAROT) SCALED AT ONE REV-
# OLUTION ABOUT THE UNIT POLAR AXIS UMITW. IT REQUIRES DTEAROT SCALED AT 2(+28)CS. IT LEAVES THE RESOLVED
# VECTOR IN RT WITH EASTERLY AND NORMAL COMPONENTS IN RTEAST AND RTNORM RESPECTIVELY, AT THE SAME SCALING. FOR
# CONTINUOUS UPDATING ONLY ONE ENTRY AT EARROT1 IS REQUIRED, WITH SUBSEQUENT ENTRIES AT EARROT2



EARROT1		VXV	1
		VSLT
			UNITW
			RTINIT
			2
		STORE	RTEAST
		
		NOLOD	1
		VXV	VSLT
			UNITW
			1
		STORE	RTNORM
		
EARROT2		STZ	1		# BRANCH TO OVERADAY UNTIL DTEAROT
		DDV	BOV		# LESS THAN ONE SIDEREAL DAY
			OVFIND
			DTEAROT
			1/WIE		# TIME FOR ONE SIDEREAL REVOLUTION
			OVERADAY
		STORE	30D
		
		NOLOD	2
		COS	DSU
		VXSC
			DP2(-1)
			RTNORM
		
		SIN	2
		VXSC	VAD
		VAD
			30D
			RTEAST
			RTINIT
		STORE	RT
		
		ITCQ	0
		
OVERADAY	SIGN	1
		BDSU
			1/WIE
			DTEAROT
			DTEAROT
		STORE	DTEAROT
		BPL	0		# GO BACK WITHOUT DISTURBING QPRET.
			1/WIE		# ANY POSITIVE CONSTANT WILL DO.
			EARROT2

1/WIE		2DEC	0.032098629	# 8.61641000 E4 SECS SCALED AT 2(+28)CS


# CONVERSION CONSTANTS FOR FREE FALL INTEGRATION PROGRAM

SCLRAVMD	2DEC	.512
SCLRMDAV	2DEC	1000 B-10
SCLTAVMD	2DEC	4.4384169 B-3
SCLVAVMD	2DEC	.64876819
SCLVMDAV	2DEC	.770691300

# C.G. ROTATION ABOUT Y AND Z S/C AXES
CGY		2DEC	.0438
		2DEC	.0092
CGZ		2DEC	.1286
		2DEC	.0588

# POWERED FLIGHT CONSTANTS. DELCDU SCALED AT KE/2 REVS (KE =A/P GAIN=1.5) EVS (KE =A/P GAIN =1.5)
DELCDU		2DEC	0.00566		#			( =1.02 DEG)
		2DEC	0.00462		#			( =0.83 DEG)
		2DEC	0.00872		#			( =1.57 DEG)

ATDT		2DEC	9.589 E-2 B-5
		2DEC	30.48 E-2 B-5

# ROUTINE CALCMANU COMPUTES THE SEQUENCE OF MANUEVERS REQUIRED IN GOING FROM AN INITIAL ATTITUDE DEFINED BY THE
# EULER ANGLES IN THETAD,+1,+2 WHICH ARE THE PRESENT OUTER, MIDDLE, INNER GIMBAL ANGLES, TO AN ATTITUDE DEFINED
# BY THE MATRIX X,Y,ZSCD, THE DESIRED BODY AXES. CALCMANU WILL EXIT WITH A MANEUVER ANGLE IN THETAMAN SCALED AT
# 1 REV, AND THE HALF UNIT VECTOR IN WC. ROTATIONS ARE BASED ON A PITCH/YAW-THEN ROLL POLICY. IF THIS
# POLICY WOULD CAUSE GIMBAL LOCK, A ROLL-PITCH/YAW-ROLL IS ADOPTED. IN EXTREMELY RARE CASES, INVOLVING MANEU-
# VERS FROM ONE GIMBAL LOCK AREA TO THE OTHER, THE POLICY MAY BE PITCH/YAW-ROLL-PITCH/YAW-ROLL, OR EVEN ROLL-
# PITCH/YAW-ROLL-PITCH/YAW-ROLL. IN ALL CASES, IF THE MANEUVER IS A ROLL, ROLLFLAG WILL BE ON. IF THERE IS NO
# MANEUVER REQUIRED,(VEHICLE LESS THAN ABOUT 3 DEGS AWAY FROM DESIRED ATTITUDE), CALCFLAG WILL BEOFF.
# OTHERWISE, CALCFLAG IS ON. CALCMANU PRESUMES THAT INITIAL CONDITIONS AND FINAL CONDITIONS ARE NOT IN GIMBAL LOCK
		SETLOC	54000
CALCMANU	EXIT	0

		TC	FLAG2UP
		OCT	12000		# SET BACKFLAG, CALCFLAG
		
		TC	FLAG2DWN
		OCT	04600		# REMOVE ROLLFLAG  ,NEGFLAG,BEGINFLG
		
		TC	INTPRET
		
		AXT,1	1
		ITA	ITC
			6
			EXITCADR
			THETRIG
		
		ITC	0
			CALCSMNB	# COMPUTE X,Y,ZNB
		
		ITC	0
			CALCNBSC	# COMPUTE X,Y,ZSC
		
		AXT,2	1
		RTB			# SET X2 TO 0
			0
			FRESHPD		# SET PD POINTER TO 0
		
		DOT	2
		ABS	DSU
		BPL
			XSC
			XSCD
			COS3
			180/ZERO

NOT179		VXV	1
		UNIT
			XSC
			XSCD
		STORE	WC

ACCEPTWC	ABS	1
		DSU	BPL
			WC +2
			COS27		# IF WC IS 27 OR LESS DEGS AWAY FROM
			GETPTCH		# +,- YSM, GIMBAL LOCK IS IMPOSSIBLE
		
		VXV	1		# PITCH/YAW MAY CAUSE GIMBAL LOCK. VARIOUS
		VXV	UNIT		# TESTS MUST BE MADE
			WC
			UNITY		# MP IS POINT OF CLOSEST APPROACH TO +YSM
			WC		# MP TO PD AT 0
		
		
		NOLOD	1
		VXV
			XSCD		# MP*XSCD TO PD AT 6
		
		VXV	1
		DOT	BPL
			0
			XSC
			-		# BRANCH TO BEGINARC IF ARC FROM XSC TO
			BEGINARC	# XSCD DOES NOT INCLUDE MP OR -MP
		
		VAD	1
		DOT	BPL
			XSC
			XSCD
			0
			PLUSPOLE
		
		SWITCH	0
			NEGFLAG		# -MP IS ON ARC
		
PLUSPOLE	ITC	0
			NORMLIMS
		
		ITC	0
			FILENORM

180/ZERO	DOT	1
		BMN
			XSC
			XSCD
			180CASE

		
		DOT	3
		VXSC	VSLT
		VSU	COMP
		UNIT	DOT
			ZSCD
			XSC
			XSC
			2
			ZSCD
			ZSC		# COSROLL TO PD AT 0 SCALED AT 2(2)

		NOLOD	1
		DSU	BPL
			COS3
			CALCSNAP
		
		VXV	1		# ROLL IS REQUIRED
		DOT
			ZSC
			ZSCD
			XSC		# XSC.(ZSC*ZSCD) TO PD AT 2
		
		TSLT	1
		ACOS	SIGN
			0
			1
		STORE	THETAMAN
		
		ABS	2
		DSU	BMN
		ITC
			XSC +2
			COS63
			NOTEST
			ROLLTEST	# SHORT ROLL MAY GO THROUGH GIMBAL LOCK
		
NOTEST		SIGN	1		# ATTACH SIGN OF THETAMAN TO WC
		VXSC
			NEARONE
			THETAMAN
			XSC
		STORE	WC
		
		ABS	0		# THETAMAN MUST BE +VE FOR MANUJOB
			THETAMAN
		STORE	THETAMAN
		EXIT	0
		
		TC	FLAG2UP
		OCT	04000		# SET ROLLFLAG
		
		TC	INTPRET
		
		ITCI	0
			EXITCADR	# EXIT ON THE ROLL WHEN PITCH/YAW IS OVER
		
CALCSNAP	SWITCH	1		# WE ARE THERE
		ITC
			CALCFLAG	# REMOVE CALCFLAG
			CALCSCNB
		
		ITC	0
			CALCCDU		# SET THETAD,S TO CORRECT VALUES
		
		ITCI	0
			EXITCADR	# THIS IS THE LAST EXIT FROM CALCMANU
		
NORMLIMS	ITA	2
		RTB	AXC,1		# SET PD TO 18
		ABS	ACOS
			THETAMAN	# (TEMPORARY STORAGE)
			SETPD18
			2		# -2 TO X1
			2		# C TO 18

BACKLIM		NOLOD	1
		BDSU
			30DEG		# 30-C TO 20 AT 4PI
		
		COS	0
			20D		# COS(30-C) TO PD AT 22
		
		SIN	2
		DDV	DMP
		ACOS	TSRT
			20D
			-
			1/TAN33		# (1/TAN33 SCALED AT 2(1) )
			1		# OKA TO 22 AT 4PI

		DMOVE	0
			90DEG		# 90 DEGREES TO 24

		SMOVE	0
			X1		# X1 TO 26
		DMOVE	2
		COMP	SIGN
		DAD	COMP
			90DEG		# -180 IF X1=-2,0 IF X1=0, TO 24
			-
			-
		
		DMOVE	1
		TEST	COMP
			90DEG		# 90DEG SCALED AT 4PI
			NEGFLAG
			POSPOLE
		STORE	26D

					# +90 IN MPAC IF FLAG=0
					# -90 IN MPAC IF FLAG=1
POSPOLE		NOLOD	1
		SIGN
			WC +2

					# +90 IN 24 IF
					#   A) FLAG=0, WC +2 POS
					#   B) FLAG=1, WC +2 NEG
					# -90 IN 24 IF
					#   A) FLAG=0, WC +2 NEG
					#   B) FLAG=1, WC +2 POS
		NOLOD	1
		DSU
			24D		# 180J-90SIGMIM TO 28
		
		SMOVE	1
		BZE
			X1
			CNEGLIMS	# TO CNEGLIMS IF X1 IS ZERO
		
		DSU	0
			28D
			22D
		STORE	6		# NBL1 TO 6, SCALED AT 4PI
		
		DAD	0
			22D
		STORE	7		# NEL1 TO 7
		
		DSU	1
		BPL
			18D
			3DEG
			ENDNORMS
		
		AXT,1	1
		RTB	COMP
			0		# SET X1 TO 0
			SETPD20
			18D		# COMPLEMENT C
		STORE	18D
		
		ITC	0
			BACKLIM		# BACKLIMITS EXIST IF C LESS THAN 3

CNEGLIMS	DSU	0
			28D
			22D
		STORE	8D		# NBL0 TO 8
		
		DAD	2
		LXA,1	SXA,1
		AXT,1
			28D
			22D
			MPAC
			9D		# NEL0 TO 9, PROTECTING 10
			0		# RESET X1 TO 0
		
ENDNORMS	ITCI	0		# END OF NORMLIMS CALCULATIONS
			THETAMAN	# END OF NORMLIMS CALCS

FILENORM	SMOVE	0
			6D		# 6 INTO 10 IF X1=0 ,OR
		STORE	10D,1		# 6 INTO 12 IF X1=-2
		
		SMOVE	1		# 7 INTO 11 IF X1=0  , OR
		INCR,2			# 7 INTO 13 IF X1=-2
			7
	       -	2		# MOVE LIMIT LIST POINTER BY -2 (TO -2)
		STORE	11D,1
		
		SMOVE	1
		BMN	SWITCH
			X1
			BEGINARC
			BACKFLAG	# SET BACKFLAG
		
		SMOVE	0
			8D
		STORE	12D		# 8 INTO 12 IF X1=0
		
		SMOVE	0
			9D
		STORE	13D		# 9 INTO 13 IF X1=0
		
		
BEGINARC	AXT,1	1
		SWITCH			# SET X1 TO 0
			0
			BEGINFLG	# SET BEGINFLG

ENDCHEK		RTB	1
		EXIT
			SETPD18
		
		TC	FLAG2DWN
		OCT	00400		# REMOVE NEGFLAG
		
		TC	INTPRET
		
		ABS*	1
		BDSU	BPL
			XSC +2,1
			COS63		# IS END CLOSE TO A POLE Q.
			OVERYET		# BRANCH TO OVERYET IF NOT

SETWARN		TEST	1
		SWITCH
			BEGINFLG
			DONTSET		# SET ROLLFLAG IF BEGINNING OF ARC NEAR
			ROLLFLAG	#   LOCK

DONTSET		DMOVE*	1
		BPL	SWITCH
			XSC +2,1
			SOMESUN
			NEGFLAG

SOMESUN		VMOVE*	3
		VXV	VXV*
		UNIT	COMP
		TEST	COMP
			XSC,1
			UNITY
			XSC,1
			NEGFLAG
			POSP1
		STORE	18D
		
POSP1		LXA,1	1
		NOLOD
			X1

		VMOVE*	2
		VXV	DOT
		BPL
			XSC,1
			WC
			18D
			POSP2

		SMOVE	1
		BMN	ITC
			X1
			OVERYET
			POSP3

POSP2		SMOVE	1
		BZE
			X1
			OVERYET

POSP3		ABS*	0
			XSC +2,1

		SMOVE	2
		DSU	TEST
		COMP
			X2
			DP2(-13)
			BEGINFLG
			+2
		STORE	S1

		NOLOD	0
		STORE	S1
		
		DOT	0
			WC
			18D		# TO PD TO SIGN AR IN NEXT EQUATION
		STORE	DTEMP1

		TSRT	1
		DSU	BMN
			24D
			1
			COS3
			POSP4

		SMOVE	0
			X1

		SIGN	0
			DTEMP1
		STORE	DTEMP1

		ITC	0
			NORMLIMS
		
		ITC	0
			ALLSHADE

POSP4		ACOS	1
		TSRT
			24D
			1		# C/2 TO 26 SCALED AT 2PI
		
		NOLOD	1
		DSU	SIN
			1.5DEG		# SIN(C/2-1.5) TO 28
		
		DSU	1
		SIN	DMP
			31.5DEG
			26D		# SIN(C/2-1.5)SIN,31.5-C/2) TO 28
		
		DAD	1
		SIN
			26D		# SIN(C/2+1.5) TO PD AT 30
			1.5DEG
		
		DAD	2
		SIN	DMP
		BDDV	SQRT
			26D
			31.5DEG
		STORE	VACZ
		
		DMOVE	0
			NEARONE
		STORE	VACX
		
		RTB	1		# PD SET TO AVOID CONFLICT WITH ARCTAN
		RTB	BDSU
			SETPD6
			ARCTAN
			DP2(-2)
		STORE	26D		# SA AT 26 SCALED AT 4PI
		
		VMOVE*	4
		VXV	UNIT
		DOT	COMP
		TSLT	ACOS
		SIGN	TSRT
			XSC,1		# POINT.UNIT(WC*XSC,1)
			WC
			18D
			1
			DTEMP1
			1		# AR TO THETAMAN, SCALED AT 4PI
		STORE	THETAMAN
		
		DSU	0
			THETAMAN
			26D
		STORE	12D,2		# AR-SA
		
		RTB	1
		DAD
			SETPD28
			THETAMAN
		STORE	13D,2		# AR+SA

		VXV	3
		INCR,2	VXV
		UNIT	DOT
		ABS	TSLT
			0		# ACOS(ABS(MP.UNITY)) TO 28
			UNITY
			-2
			0
			18D
			2

		DSQ	2
		BDSU	SQRT
		DMP	DMP
			24D
			SIN30
			SIN30

		DMP	0
			COS30
			24D

		DSU	0
			28D
			26D
		STORE	16D		# COSB TO 16 AT 2(2)
		
		DAD	1
		BDSU	BPL
			-
			-
			C33
			OVERYET		# IF C33-COSA POS

		SMOVE	0
			X1

		SIGN	0
			DTEMP1
		STORE	DTEMP1
		
		ITC	0
			NORMLIMS
		
		DSU	1
		BMN
			C33
			16D
			ALLSHADE
		DMOVE*	0
			11D,2		# 11D,2 TO PD FOR PROTECTION
		
		BPL	0
			DTEMP1
			11MANU
		
		SMOVE	0
			6		# NBL1 REPLACES AR-SA
		STORE	10D,2
		
		DMOVE	0
		STORE	11D,2		# NOW REINSERT 11,2
		
		ITC	0
			OVERYET
		
11MANU		SMOVE	0
			7
		STORE	11D,2
		
		ITC	0
			OVERYET

ALLSHADE	BPL	1
		DMOVE
			DTEMP1
			12MANU
			6
		STORE	10D,2
		
		SMOVE	0
			9D
		STORE	11D,2
		
		ITC	0
			OVERYET
		
12MANU		SMOVE	0
			8D
		STORE	10D,2
		
		SMOVE	0
			7
		STORE	11D,2
		
OVERYET		TEST	2		# ENDCHEK IS DONE TWICE, FOR THE
		AXC,1	SWITCH		# BEGINNING AND FOR THE END OF THE ARC
		ITC
			BEGINFLG
			FINISHUP
			18D		# -18 TO X1
			BEGINFLG	# REMOVE BEGINFLG
			ENDCHEK		# GO BACK, GET LIMITS FOR END OF ARC

FINISHUP	SMOVE	1
		BZE
			X2
			GETPTCH		# NO LIMITS DETECTED
		
		RTB	1
		VXV
			SETPD20
			XNB
			XSC		# XNB*XSC TO PD AT 20
		
		VXV	1
		DOT
			WC
			XSC
			20D
		STORE	18D		# (WC*XSC).(XNB*XSC) TO 18
		
		UNIT	3
		DOT	COMP
		TSLT	ACOS
		SIGN	TSRT
			-
			WC
			1
			-
			1
		STORE	12D,2		# SCALED AT 4PI
		
		SMOVE	1
		AXC,2	AXT,1
			X2
			0
			0		# 0 INTO X2 AND X1
		STORE	30D		# SAVE X2
		
22MANU		SMOVE*	1
		DSU
			13D,2
			12D

23MANU		NOLOD	1
		DSU	BPL
			360DEG
			23MANU

20MANU		NOLOD	1
		DAD	BMN
			360DEG
			20MANU
		STORE	0,1
		
		LXA,1	1
		INCR,2	INCR,1
			X1
			-1
			-2
		
		SMOVE	1
		BDSU	BMN
			X2
			30D
			22MANU
		
		DAD	1
		BZE
			30D
			DP2(-13)
			EZCASE
		
		DSU	1
		BMN
			4
			0
			30MANU
		
		DSU	1
		BMN
			2
			0
			31MANU
		
		DSU	1
		BMN
			2
			4
			SPLITMNU
		
		DSU	1
		BMN
			6
			0
			GETPTCH
		
		TEST	2
		TSRT	DSU
		ITC
			BACKFLAG	# (BACKFLAG DOWN MEANS DO BACKTEST
			BACKTEST
			0
			1
			6
			40MANU
		
31MANU		DSU	1
		BMN
			6
			0
			33MANU

333MANU		TEST	2
		DAD	TSRT
		DSU	ITC
			BACKFLAG
			BACKTEST
			0
			2
			1
			6
			40MANU

33MANU		DSU	1
		BMN	ITC
			6
			2
			333MANU
			GETPTCH

30MANU		DSU	1
		BMN
			2
			0
			35MANU

		DSU	1
		BMN		
			6
			4
			GETPTCH

38MANU		TEST	2
		TSRT	DSU
		ITC
			BACKFLAG
			BACKTEST
			4
			1
			6
			40MANU

35MANU		DSU	1
		BMN
			2
			4
			36MANU

		DSU	1
		BMN
			6
			2
			37MANU

		DSU	1
		BPL
			6
			0
			38MANU

		ITC	0
			GETPTCH

36MANU		TEST	2
		DAD	TSRT
		DSU	ITC
			BACKFLAG
			BACKTEST
			4
			2
			1
			6
			40MANU

37MANU		DSU	1
		BMN
			6
			4
			GETPTCH

		TEST	2
		TSRT	DSU
		ITC
			BACKFLAG
			BACKTEST
			4
			1
			6
			40MANU

40MANU		NOLOD	2		# ROLL IS IN MPAC,MPAC +1,SCALED AT 4PI
		DSU	BMN
		DSU	ITC
			DP2(-2)
			41MANU
			DP2(-2)
			42MANU

41MANU		NOLOD	2
		DAD	BPL
		DAD	ITC
			360DEG
			43MANU
			DP2(-2)
			42MANU

43MANU		NOLOD	1
		DSU
			DP2(-2)

42MANU		NOLOD	1
		TSLT
			1
		STORE	THETAMAN	# ROLL IN THETAMAN, SCALED AT 2PI
		
		TEST	0
			ROLLFLAG	# IF ROLLFLAG ISNT ON
			DONE		# WE ARE DONE
		
		ITC	0
			ROLLTEST	# SHORT WAY ROLL MAY HIT GIMBAL LOCK
		
		ITC	0
			DONE

ROLLTEST	RTB	2
		VXV	VXV
		UNIT
			FRESHPD
			XSC
			XNB
			XSC		# TEMP1 TO DP AT 0
		
		SIGN	2
		VXSC	VXV
		VXV	UNIT
			NEARONE
			XSC +2
			XSC
			UNITY
			XSC

		DOT	1
		TSLT	ACOS
			0
			6
			1
		STORE	16D
		
		ABS	1
		DSU	BMN
			THETAMAN
			16D
			ENDTST
		
		VMOVE	2
		VXV	DOT
		BMN
			-
			-
			XSC
			50MANU
		
		DMOVE	1
		BPL	DAD
			THETAMAN
			ENDTST
			NEARONE
		STORE	THETAMAN
		
		ITCQ	0
		
50MANU		DMOVE	1
		BMN	DSU
			THETAMAN
			ENDTST
			NEARONE
		STORE	THETAMAN
		
ENDTST		ITCQ	0


BACKTEST	LXA,2	1
		SWITCH
			30D		# RESET SAVED X2
			BACKFLAG	# TURN BACKFLAG ON (DONT DO AGAIN)
		
		SMOVE	0
			10D
		STORE	12D
		
		LXA,1	1
		SXA,1
			11D
			13D

		ITC	0
			FINISHUP
		
EZCASE		DSU	1
		BMN
			2
			0
			GETPTCH		# NO ROLL REQ,D
		
		TEST	2
		TSRT	DSU
		ITC
			BACKFLAG
			BACKTEST
			0
			1
			2
			40MANU
		
180CASE		ABS	1
		BDSU	BMN
			XSC +2
			COS30
			NOGIMTST

		VXV	0
			XSC
			UNITY

		DOT	0
			XSCD
			0

		SIGN	2
		VXSC	VXV
		UNIT
			NEARONE
			-
			XSC
		STORE	WC

		ABS	1
		DSU	BPL
			WC +2
			COS27
			GETPTCH

		VXV	0
			WC
			XSC
		
		VXV	1
		VXV	UNIT
			XSC
			XNB
			XSC

		DOT	1
		TSLT
			6
			0
			2
		STORE	12D

		VMOVE	1
		VXV	DOT
			-
			-
			XSC

		EXIT	0

		TC	FLAG2UP
		OCT	04000

		TC	INTPRET
		ABS	2
		ACOS	SIGN
		SIGN
			12D
			12D
			-
		STORE	THETAMAN

		ITC	0
			DONE

NOGIMTST	VXV	1
		UNIT
			XSC
			XNB
		STORE	WC

		DMOVE	0
			SIN30
		STORE	THETAMAN
		
		EXIT	0

		TC	FLAG2DWN
		OCT	04000

		TC	INTPRET
		ITCI	0
			EXITCADR
		
DONE		SIGN	1
		VXSC
			NEARONE
			THETAMAN
			XSC
		STORE	WC
		
		ABS	0
			THETAMAN
		STORE	THETAMAN
		
		EXIT	0
		
		TC	FLAG2UP
		OCT	04000		# SET ROLLFLAG
		
		TC	INTPRET
		
		ITCI	0		# EXIT FOR ROLL THAT AVOIDS GIMBAL LOCK IN
			EXITCADR	# SUBSEQUENT PITCH/YAW MANEUVER

SPLITMNU	ABS	1
		DSU	BZE
			34D
			DP2(-13)
			SPLIT1

		DMOVE	1
		BMN
			34D
			SPLIT3

SPLIT2		DSU	1
		BMN
			6
			0
			SPLIT5

		TSRT	1
		DSU	ITC
			0
			1
			6
			40MANU

SPLIT3		DSU	1
		BPL
			6
			4
			SPLIT4

		DSU	1
		BPL
			6
			2
			SPLIT5

SPLIT4		DAD	2
		TSRT	DSU
		ITC
			2
			4
			1
			6
			40MANU

SPLIT1		DMOVE	1
		BMN	ITC
			34D
			SPLIT2
			SPLIT3

SPLIT5		ITC	0
			CALCPTCH
		
		DMOVE	1
		TSRT
			THETAMAN
			1
		STORE	THETAMAN

		EXIT	0

		TC	FLAG2DWN
		OCT	04000		# REMOVE ROLLFLAG

		TC	INTPRET
		ITCI	0
			EXITCADR	# EXIT FOR PITCH/YAW PORTION OF MANEUVER
		
GETPTCH		ITC	0
			CALCPTCH

		EXIT	0

		TC	FLAG2DWN
		OCT	04000		# REMOVE ROLLFLAG
		
		TC	INTPRET
		
		ITCI	0
			EXITCADR	# EXIT FOR PITCH/YAW PORTION OF MANEUVER

CALCPTCH	DOT	1
		TSLT	ACOS
			XSC
			XSCD
			1
		STORE	THETAMAN
		
		ITCQ	0
		
COS3		2DEC	.249657385	# SCALED AT 2(4)
COS27		2DEC	.445503260	# SCALED AT 2(1)
COS63		2DEC	.226995250	# SCALED AT 2(1)
COS30		2DEC	.433012700	# SCALED AT 2(1)
1/TAN33		2DEC	.76993250	# SCALED AT 2(1)
1.5DEG		2DEC	.004166666	# SCALED AT 2PI
31.5DEG		2DEC	.0875		# SCALED AT 2PI
30DEG		2DEC	.08333333	# SCALED AT 2PI
3DEG		2DEC	.00833333	# SCALED AT 2PI
90DEG		2DEC	0.125		# SCALED AT 4PI
DP2(-2)		2DEC	0.25
SIN30		EQUALS	DP2(-2)
DP2(-13)	2OCT	0000200000
C33		2DEC	.209667643
UNITX		2DEC	0.5
ZEROVEC		2DEC	0.0
		2DEC	0.0
UNITY		2DEC	0.0
		2DEC	0.5
		2DEC	0.0
SCNBMAT		2DEC	0.419335300
		2DEC	0.0
		2DEC	-.272319500
		2DEC	0.0
		2DEC	0.5
		2DEC	0.0
		2DEC	0.272319500
		2DEC	0.0
		2DEC	0.419335300
DTH		2DEC	0.005555	# 2.0 DEG SCALED AT 2PI
		2DEC	0.01		# 3.6 DEG
		2DEC	0.020833	# 7.5 DEG


SETPD16		CAF	SIXTN
		AD	FIXLOC
		TS	PUSHLOC
		TC	RE-ENTER

SETPD6		CAF	SIX
		TC	SETPD16 +1

SETPD18		CAF	EIGHTN
		TC	SETPD16 +1

SETPD28		CAF	TWENTY8
		TC	SETPD16 +1

SETPD20		CAF	TWENTY0
		TC	SETPD16 +1

180DEG		EQUALS	UNITX		# SCALED AT 2PI.
DP2(-1)		EQUALS	UNITX
360DEG		EQUALS	UNITX		# SCALED AT 4PI.
CFACTOR		EQUALS	UNITX
