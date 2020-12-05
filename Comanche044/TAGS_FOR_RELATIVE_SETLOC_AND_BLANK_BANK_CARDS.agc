### FILE="Main.annotation"
## Copyright:   Public domain.
## Filename:    TAGS_FOR_RELATIVE_SETLOC_AND_BLANK_BANK_CARDS.agc
## Purpose:     A section of Comanche revision 044.
##              It is part of the reconstructed source code for the
##              original release of the flight software for the Command
##              Module's (CM) Apollo Guidance Computer (AGC) for Apollo 10.
##              The code has been recreated from a copy of Comanche 055. It
##              has been adapted such that the resulting bugger words
##              exactly match those specified for Comanche 44 in NASA drawing
##              2021153D, which gives relatively high confidence that the
##              reconstruction is correct.
## Assembler:   yaYUL
## Contact:     Ron Burkey <info@sandroid.org>.
## Website:     www.ibiblio.org/apollo/index.html
## Mod history: 2020-12-03 MAS  Created from Comanche 51.
##              2020-12-04 MAS  Removed the tags S3435LOC, MODCHG1, and
##                              MODCHG2 (the former is from 45-51, and the
##                              latter are from 51-55).

## Page 27
FIXED		MEMORY	120000 - 167777
		COUNT	BANKSUM

# MODULE 1 CONTAINS BANKS 0 THROUGH 5

		BLOCK	02
FFTAG1		EQUALS
FFTAG2		EQUALS
FFTAG3		EQUALS
FFTAG4		EQUALS
FFTAG7		EQUALS
FFTAG8		EQUALS
FFTAG9		EQUALS
FFTAG10		EQUALS
FFTAG12		EQUALS
P30SUBS		EQUALS
STOPRAT		EQUALS
P23S		EQUALS
		BNKSUM	02
		
		BLOCK	03
FFTAG5		EQUALS
FFTAG6		EQUALS
DAPS9		EQUALS
FFTAG13		EQUALS
		BNKSUM	03
		
		BANK	00
DLAYJOB		EQUALS
		BNKSUM	00
		
		BANK	01
RESTART		EQUALS
		BNKSUM	01
		
		BANK	4
VERB37		EQUALS
CONICS1		EQUALS
PINBALL4	EQUALS
CSI/CDH1	EQUALS
INTPRET2	EQUALS
IMUCAL1		EQUALS

## Page 28

STBLEORB	EQUALS
E/PROG		EQUALS
MIDDGIM		EQUALS

		BNKSUM	04
		
		BANK	5
FRANDRES	EQUALS
DOWNTELM	EQUALS
DAPMASS		EQUALS
CDHTAG		EQUALS
		BNKSUM	05
		
# MODULE 2 CONTAINS BANKS 6 THROUGH 13

		BANK	6
IMUCOMP		EQUALS
T4RUP		EQUALS
IMUCAL2		EQUALS
CSIPROG		EQUALS
		BNKSUM	06
	
		BANK	7
SXTMARKE	EQUALS
R02		EQUALS
MODESW		EQUALS
XANG		EQUALS
KEYRUPT		EQUALS
CSIPROG6	EQUALS
		BNKSUM	07
		
		BANK	10
DISPLAYS	EQUALS
PHASETAB	EQUALS
COMGEOM2	EQUALS
SXTMARK1	EQUALS
P60S4		EQUALS
OPTDRV		EQUALS
CSIPROG8	EQUALS
		BNKSUM	10
		
		BANK	11
ORBITAL		EQUALS
ORBITAL1	EQUALS			# CONSTANTS

## Page 29

INTVEL		EQUALS
S52/2		EQUALS
CSIPROG5	EQUALS
INTINIT1	EQUALS
		BNKSUM	11
		
		BANK	12
CONICS		EQUALS
CSIPROG2	EQUALS
CSI/CDH2	EQUALS
		BNKSUM	12
		
		BANK	13
P76LOC		EQUALS
LATLONG		EQUALS
INTINIT		EQUALS
SR52/1		EQUALS
ORBITAL2	EQUALS
CDHTAGS		EQUALS
E/PROG1		EQUALS
		BNKSUM	13

# SPACER
	
#          MODULE 3 CONTAINS BANKS 14 THROUGH 21

		BANK 	14
STARTAB		EQUALS
RT53		EQUALS
P50S1		EQUALS
MEASINC2	EQUALS
CSI/CDH3	EQUALS
		BNKSUM	14	

		BANK	15
P50S		EQUALS
ETRYDAP		EQUALS
S52/3		EQUALS
		BNKSUM	15
		
		BANK	16
P40S1		EQUALS

## Page 30

DAPROLL		EQUALS
P50S2		EQUALS
P23S1		EQUALS
RTE2		EQUALS
		BNKSUM	16
		
		BANK	17
DAPS4		EQUALS
DAPS5		EQUALS
DAPS7		EQUALS
P50S3		EQUALS
		BNKSUM	17
		
		BANK	20
DAPS6		EQUALS
DAPS1		EQUALS
DAPS2		EQUALS
MANUSTUF	EQUALS
R36CM		EQUALS
VAC5LOC		EQUALS
		BNKSUM	20
		
		BANK	21
DAPS3		EQUALS
MYSUBS		EQUALS
KALCMON3	EQUALS
		BNKSUM	21

# MODULE 4 CONTAINS BANKS 22 THROUGH 27

		BANK	22
RTBCODES	EQUALS
RTBCODE1	EQUALS
DAPS8		EQUALS
APOPERI		EQUALS
P40S5		EQUALS
KALCMON2	EQUALS
KALCMON1	EQUALS
CSIPROG3	EQUALS
		BNKSUM	22

## Page 31

		BANK	23
P20S2		EQUALS
INFLIGHT	EQUALS
COMGEOM1	EQUALS
POWFLITE	EQUALS
POWFLIT1	EQUALS
RENDGUID	EQUALS
POWFLIT2	EQUALS
R30LOC		EQUALS
P11FOUR		EQUALS
CSIPROG4	EQUALS
		BNKSUM	23
		
		BANK	24
LOADDAP		EQUALS
P40S		EQUALS
CSIPROG7	EQUALS
		BNKSUM	24
		
		BANK	25
REENTRY		EQUALS
CDHTAG1		EQUALS
		BNKSUM	25
		
		BANK	26
INTPRET1	EQUALS
REENTRY1	EQUALS
P60S		EQUALS
P60S1		EQUALS
P60S2		EQUALS
P60S3		EQUALS
PLANTIN		EQUALS			# LUNAR ROT
EPHEM		EQUALS
P05P06		EQUALS
26P50S		EQUALS
		BNKSUM	26
		
		BANK	27
TOF-FF		EQUALS
TOF-FF1		EQUALS
MANUVER		EQUALS
MANUVER1	EQUALS

## Page 32

VECPT		EQUALS
UPDATE1		EQUALS
UPDATE2		EQUALS
R22S1		EQUALS
P60S5		EQUALS
P40S2		EQUALS
		BNKSUM	27

# MODULE 5 CONTAINS BANKS 30 THROUGH 35

		BANK	30
IMUSUPER	EQUALS
LOWSUPER	EQUALS
FCSTART		EQUALS			# STANDARD LOCATION FOR THIS. (FOR EXTVB)
LOPC		EQUALS
P20S1		EQUALS
P20S6		EQUALS
P40S3		EQUALS
R35A		EQUALS
		BNKSUM	30
		
		BANK	31
R35		EQUALS
RT23		EQUALS
P30S1A		EQUALS
R34		EQUALS
CDHTAG2		EQUALS
CSIPROG9	EQUALS
R31		EQUALS
P22S		EQUALS
RTE3		EQUALS
		BNKSUM	31
		
		BANK	32
MSGSCAN1	EQUALS
RTE		EQUALS
DELRSPL1	EQUALS
IMUCAL3		EQUALS
		BNKSUM	32
		
		BANK	33
TESTLEAD	EQUALS

## Page 33

IMUCAL		EQUALS
		BNKSUM	33
		
		BANK	34
P11ONE		EQUALS
P20S3		EQUALS
P20S4		EQUALS
RTECON		EQUALS
		BNKSUM	34
		
		BANK	35
RTECON1		EQUALS
CSI/CDH		EQUALS
P30S1		EQUALS
P30S		EQUALS
P17S1		EQUALS
MEASINC3	EQUALS
INTINIT2	EQUALS
		BNKSUM	35
		
# MODULE 6 CONTAINS BANKS 36 THROUGH 43

		BANK	36
MEASINC		EQUALS
MEASINC1	EQUALS
P17S		EQUALS
RTE1		EQUALS
		BNKSUM	36
		
		BANK	37
P20S		EQUALS
BODYATT		EQUALS
RENDEZ		EQUALS
SERVICES	EQUALS
P11TWO		EQUALS
CDHTAG3		EQUALS
		BNKSUM	37
		
		BANK	40
PINSUPER	EQUALS

## Page 34

SELFSUPR	EQUALS
PINBALL1	EQUALS
R36CM1		EQUALS
		BNKSUM	40
		
		BANK	41
PINBALL2	EQUALS
R36LM		EQUALS
		BNKSUM	41
		
		BANK	42
SBAND		EQUALS	
PINBALL3	EQUALS
EXTVBS		EQUALS
R36LM1		EQUALS
		BNKSUM	42
		
		BANK	43
SELFCHEC	EQUALS
EXTVERBS	EQUALS
		BNKSUM	43
		
HI6ZEROS	EQUALS	ZEROVECS		# ZERO VECTOR ALWAYS IN HIGH MEMORY
LO6ZEROS	EQUALS	ZEROVEC			# ZERO VECTOR ALWAYS IN LOW MEMORY
HIDPHALF	EQUALS	UNITX
LODPHALF	EQUALS	XUNIT
HIDP1/4		EQUALS	DP1/4TH	
LODP1/4		EQUALS	D1/4			# 2DEC .25
HIUNITX		EQUALS	UNITX
HIUNITY		EQUALS	UNITY
HIUNITZ		EQUALS	UNITZ
LOUNITX		EQUALS	XUNIT			# 2DEC .5
LOUNITY		EQUALS	YUNIT			# 2DEC 0
LOUNITZ		EQUALS	ZUNIT			# 2DEC 0
3/4LOWDP	EQUALS	3/4			# 2DEC 3.0 B-2

		SBANK=	LOWSUPER

# ROPE SPECIFIC ASSIGNS OBVIATING NEED TO CHECK COMPUTER FLAG IN DETVRUZVING INTEGRATION AREA ENTRIES

OTHPREC		EQUALS	LEMPREC
ATOPOTH		EQUALS	ATOPLEM
ATOPTHIS	EQUALS	ATOPCSM
MOONTHIS	EQUALS	CMOONFLG

## Page 35

MOONOTH		EQUALS	LMOONFLG
MOVATHIS	EQUALS	MOVEACSM
STATEST		EQUALS	V83CALL			# * TEMPORARY
THISPREC	EQUALS	CSMPREC
THISAXIS	=	UNITX
ERASID		EQUALS	LOW10			# DOWNLINK ERASABLE DUMP ID
DELAYNUM	EQUALS	THREE

#****************************************************************************************************************

# THE FOLLOWING ECADRS ARE DEFINED TO FACILITATE EBANK SWITCHING.  THEY ALSO MAKE IT EASIER FOR
# ERASABLE CONTROL TO REARRANGE ERASABLE MEMORY WITHOUT DISRUPTING THE PROGRAMS WHICH SET EBANKS.
# PRIOR TO ROPE RELEASE FIXED MEMORY CAN BE SAVED BY SETTING EACH EBXXXX =EBANKX (X=4,5,6,7).  EBANKX OF COURSE
# WILL BE THE BANK WHERE THE ERASABLES REFERENCED IN EBXXXX WILL BE STORED.

		BANK	7
		EBANK=	MARKDOWN
EBMARKDO	ECADR	MARKDOWN
		EBANK=	MRKBUF1
EBMRKBUF	ECADR	MRKBUF1

		BANK	24
		EBANK=	DVCNTR
EBDVCNTR	ECADR	DVCNTR
		EBANK=	P40TMP
EBP40TMP	ECADR	P40TMP

		BANK	34
		EBANK=	DVCNTR
EBDVCNT		ECADR	DVCNTR
		EBANK=	QPLACES
EBQPLACE	ECADR	QPLACES

		BANK	37
		EBANK=	RN1
EBRN1		ECADR	RN1

#****************************************************************************************************************

## Page 36
## This page contains only assembler-generated messages, and no source code.
