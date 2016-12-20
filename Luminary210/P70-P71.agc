### FILE="Main.annotation"
## Copyright:   Public domain.
## Filename:    P70-P71.agc
## Purpose:     A section of Luminary revision 210.
##              It is part of the source code for the Lunar Module's (LM)
##              Apollo Guidance Computer (AGC) for Apollo 15-17.
##              This file is intended to be a faithful transcription, except
##              that the code format has been changed to conform to the
##              requirements of the yaYUL assembler rather than the
##              original YUL assembler.
## Reference:   pp. 831-838
## Assembler:   yaYUL
## Contact:     Ron Burkey <info@sandroid.org>.
## Website:     www.ibiblio.org/apollo/index.html
## Mod history: 2016-11-17 JL   Created from Luminary131 version.
##		2016-12-01 RSB	Completed transcription.
##              2016-12-07 HG   Fix pseudo operator ADDRESS -> ADRES
##              2016-12-08 HG   Fix operand LANDISP -> LANADISP

## Page 831
		BANK	21
		SETLOC	R11
		BANK

		EBANK=	DVCNTR
		COUNT*	$$/R11

R10,R11		CS	FLAGWRD7	# IS SERVICER STILL RUNNING?
		MASK	AVEGFBIT
		CCS	A
		TCF	TASKOVER	# LET AVGEND TAKE CARE OF GROUP 2.
		CCS	PIPCTR
		TCF	STORPCTR
		EXTEND
		DCA	NEG0
		DXCH	-PHASE2
		TCF	R10,R11A
		
STORPCTR	TS	PIPCTR1

		CAF	OCT31
		TC	TWIDDLE
		ADRES	R10,R11
R10,R11A	CAF	HFLSHBIT
FLASHH?		MASK	FLGWRD11
		EXTEND
		BZF	FLASHV?		# H FLASH OFF, SO LEAVE ALONE

## In the assembly-listing hardcopy, there is a handwritten note, reading "page 541".
		CA	HLITE
		TS	L
		TC	FLIP		# FLIP H LITE

FLASHV?		CA	VFLSHBIT	# VLASHBIT MUST BE BIT 2.
		MASK	FLGWRD11
		EXTEND
		BZF	10,11		# VFLASH OFF

		CA	VLITE
		TS	L
		TC	FLIP		# FLIP V LITE


10,11		CA	FLAGWRD9	# IS THE LETABORT FLAG SET ?
		MASK	LETABBIT
		EXTEND
		BZF	LANADISP	# NO. PROCEED TO R10.

P71NOW?		CS	MODREG		# YES.  ARE WE IN P71 NOW?
		AD	1DEC71
		EXTEND
## Page 832
		BZF	LANADISP	# YES.  PROCEED TO R10.
		
		CAF	BIT1
		MASK	CHANBKUP
		CCS	A
		TCF	LANADISP	# IGNORE CHAN BITS - ASSUME NO ABORT
		
		EXTEND			# NO. IS AN ABORT STAGE COMMANDED?
		READ	CHAN30		# .
		COM
		TS	L
		MASK	BIT4
		CCS	A
		TCF	P71A		# YES.

P70NOW?		CS	MODREG		# NO. ARE WE IN P70 NOW?
		AD	1DEC70
		EXTEND
		BZF	LANADISP	# YES.  PROCEED TO R10.

		CA	L		# NO.  IS AN ABORT COMMANDED?
		MASK	BIT1
		CCS	A
		TCF	P70A		# YES.
		TCF	LANADISP	# NO.  PROCEED TO R10.

		COUNT*	$$/P70

P70		TC	LEGAL?
P70A		CS	ZERO
		TCF	+3
P71		TC	LEGAL?
P71A		CAF	TWO
   +3		TS	Q
 		INHINT
		EXTEND
		DCA	CNTABTAD
		DTCB

		EBANK=	DVCNTR
CNTABTAD	2CADR	CONTABRT

1DEC70		DEC	70
1DEC71		DEC	71

		BANK	05
		SETLOC	ABORTS1
		BANK
		COUNT*	$$/P70

## Page 833
CONTABRT	CAF	ABRTJADR
		TS	BRUPT
		RESUME

ABRTJADR	TCF	ABRTJASK

ABRTJASK	CAF	OCTAL27
		AD	Q
		TS	L
		COM
		DXCH	-PHASE4
		INDEX	Q
		CAF	MODE70
		TS	MODREG

		TS	DISPDEX		# INSURE DISPDEX IS POSITIVE.

		CCS	Q		# SET APSFLAG IF P71.
		CS	FLGWRD10	# SET APSFLAG PRIOR TO THE ENEMA.
		MASK	APSFLBIT
		ADS	FLGWRD10
		CS	DAPBITS		# DAPBITS = OCT 40640 = BITS 6,8,9,15
		MASK	DAPBOOLS	# RESET ULLAGE,DRIVT,XOVR11MM,AND PULSES
		TS	DAPBOOLS

		CAF	1DEGDB		# INSURE DAP DEADBAND IS SET TO 1 DEGREE
		TS	DB

		CS	FLAGWRD5	# SET ENGONFLG.
		MASK	ENGONBIT
		ADS	FLAGWRD5

		CS	PRIO30		# INSURE THAT THE ENGINE IS ON, IF ARMED.
		EXTEND
		RAND	DSALMOUT
		AD	BIT13
		EXTEND
		WRITE	DSALMOUT

		CAF	LRBYBIT		# TERMINATE R12.
		TS	FLGWRD11

		CS	FLAGWRD0	# SIGNAL THE LAD TO DISPLAY LATVEL IN
		MASK	R10FLBIT	#   INERTIAL COORDINATES AND FORVEL ZERO
		ADS	FLAGWRD0

		EXTEND			# LOAD TEVENT FOR THE DOWNLINK.
		DCA	TIME2
		DXCH	TEVENT

## Page 834
		EXTEND
		DCA	SVEXITAD
		DXCH	AVGEXIT

		TC	ABTKLEAN	# KILL GROUPS 1,3, AND 6.
		
		CAF	THREE		# SET UP 4.3SPOT FOR GOABORT
		TS	L
		COM
		DXCH	-PHASE4

		TC	POSTJUMP
		CADR	ENEMA

		EBANK=	DVCNTR
SVEXITAD	2CADR	SERVEXIT

MODE70		DEC	70
OCTAL27		OCT	27
MODE71		DEC	71

DAPBITS		OCT	40640

1DEGDB		OCT	00554
		BANK	32
		SETLOC	ABORTS
		BANK

		COUNT*	$$/P70

GOABORT		CAF	FOUR
		TS	DVCNTR

		CAF	WHICHADR
		TS	WHICH

		TC	INTPRET
		CLEAR	CLEAR
			FLRCS
			FLUNDISP
		CLEAR	SET
			IDLEFLAG
			ACC4-2FL
		SET	CALL
			P7071FLG
			INITCDUW
		EXIT

		TC	CHECKMM
70DEC		DEC	70
## Page 835
		TCF	P71RET

P70INIT		TC	INTPRET
		CALL
			TGOCOMP
		DLOAD	SL
			MDOTDPS
			4D
		BDDV
			MASS
		STODL	TBUP
			MASS
		DDV	SR1
			K(1/DV)
		STORE	1/DV1
		STORE	1/DV2
		STORE	1/DV3
		BDDV
			K(AT)
		STODL	AT
			100PCTTO
		STORE	TTO
		SLOAD	DCOMP
			DPSVEX
		SR2
		STCALL	VE
			COMMINIT
INJTARG		DLOAD
			ABTRDOT
		STCALL	RDOTD		# INITIALZE RDOTD.
			YCOMP		# COMPUTE Y
		ABS	DSU
			YLIM		# /Y/-DYMAX
		BMN	SIGN		# IF <0, XR<.5DEG, LEAVE YCO AT 0
			YOK		# IF >0, FIX SIGN OF DEFICIT, THIS IS YCO.
			Y
		STORE	YCO
YOK		DLOAD	DSU
			YCO
			Y
		SR
			5D
		STORE	XRANGE
		SET	CALL
			FLVR
			THETCOMP
		DSU	BPL
			THETCRIT
			+4
		VLOAD	GOTO
## Page 836
			J1PARM
			STORPARM
  +4		VLOAD	SET		# IF J2 IS USED, SET THE
 			J2PARM		# ABORT TARGETING FLAG
			ABTTGFLG
STORPARM	STODL	JPARM
			RCO
		STORE	RP
		SET	EXIT
			ROTFLAG

UPTHROT		TC	THROTUP

		TC	PHASCHNG
		OCT	04024

		TC	UPFLAG
		ADRES	FLAP

UPTHROT1	TC	BANKCALL	# VERIFY THAT THE PANEL SWITCHES
		CADR	P40AUTO		# ARE PROPERLY SET.

		TC	THROTUP

		CAF	PRIO17		# LET SERVICER FINISH BEFORE CONNECTING
		TC	PRIOCHNG	#     ASCENT GUIDANCE EQUATIONS.

		EXTEND
		DCA	ATMAGAD
		DXCH	AVGEXIT

GRP4OFF		TC	PHASCHNG	# TERMINATE USE OF GROUP 4.
		OCT	00004

		TCF	ENDOFJOB

P71RET		TC	DOWNFLAG
		ADRES	LETABORT

		CAF	THRESH2		# SET DVMON THRESHOLD TO THE ASCENT VALUE.
		TS	DVTHRUSH

		TC	INTPRET
		CALL
			P12INIT
		BON	CALL
			FLAP
			OLDTIME
			TGOCOMP		# IF FLAP=0, TGO=T-TIG
		GOTO
## Page 837
			INJTARG
OLDTIME		DLOAD	SL1		# IF FLAP=1,GTO=2 TGO
			TGO
		STORE	TGO1
		EXIT

		TC	PHASCHNG
		OCT	04024

		EXTEND
		DCA	TGO1
		DXCH	TGO
		TCF	UPTHROT1

# ***********************************************************************

		BANK	21
		SETLOC	R11
		BANK
		
		COUNT*	$$/P70

LEGAL?		CS	MMNUMBER	# IS THE DESIRED PGM ALREADY IN PROGRESS?
		AD	MODREG
		EXTEND
		BZF	ABORTALM

		CS	FLAGWRD9	# ARE THE ABORTS ENABLED?
		MASK	LETABBIT
		CCS	A
		TCF	ABORTALM

		CA	FLAGWRD7	# IS SERVICER ON THE A1R7
		MASK	AVEGFBIT
		CCS	A
		TC	Q		# YES.  ALL IS WELL.
ABORTALM	TC	FALTON
		TC	RELDSP
		TC	POSTJUMP
		CADR	PINBRNCH

		BANK	32
		SETLOC	ABORTS
		BANK

		COUNT*	$$/P70

# ***********************************************************************

TGOCOMP		RTB	DSU
## Page 838
			LOADTIME
			TIG
		SL
			11D
		STORE	TGO
		RVQ

# ***********************************************************************

THROTUP		CAF	BIT13
		TS	THRUST
		CAF	BIT4
		EXTEND
		WOR	CHAN14
		TC	Q

# ***********************************************************************

10SECS		2DEC	1000

HINJECT		2DEC	18288 B-24	# 60,000 FEET EXPRESSED IN METERS.

(TGO)A		2DEC	37000 B-17

K(AT)		2DEC	.02		# SCALING CONSTANT

WHICHADR	REMADR	ABRTABLE

# ************************************************************************

		EBANK=	DVCNTR
ATMAGAD		2CADR	ATMAG