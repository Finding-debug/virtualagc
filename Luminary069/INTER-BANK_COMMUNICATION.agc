### FILE="Main.annotation"
## Copyright:   Public domain.
## Filename:    INTER-BANK_COMMUNICATION.agc
## Purpose:     The main source file for Luminary revision 069.
##              It is part of the source code for the original release
##              of the flight software for the Lunar Module's (LM) Apollo
##              Guidance Computer (AGC) for Apollo 10. The actual flown
##              version was Luminary 69 revision 2, which included a
##              newer lunar gravity model and only affected module 2.
##              This file is intended to be a faithful transcription, except
##              that the code format has been changed to conform to the
##              requirements of the yaYUL assembler rather than the
##              original YUL assembler.
## Reference:   pp. 993-996
## Assembler:   yaYUL
## Contact:     Ron Burkey <info@sandroid.org>.
## Website:     www.ibiblio.org/apollo/index.html
## Mod history: 2016-12-13 MAS  Created from Luminary 99.
##              2016-12-18 MAS  Updated from comment-proofed Luminary 99 version.
##		2017-01-04 RRB	Updated for Luminary 69.
##		2017-01-28 RSB	Proofed comment text using octopus/prooferComments
##				but no errors found.
##		2017-03-17 RSB	Comment-text fixes identified in diff'ing
##				Luminary 99 vs Comanche 55.
##              2021-05-30 ABS  ISWCALLL -> ISWCALL

## Page 993
#          THE FOLLOWING ROUTINE CAN BE USED TO CALL A SUBROUTINE IN ANOTHER BANK. IN THE BANKCALL VERSION, THE
# CADR OF THE SUBROUTINE IMMEDIATELY FOLLOWS THE TC BANKCALL INSTRUCTION, WITH C(A) AND C(L) PRESERVED.

		BLOCK	02
		COUNT*	$$/BANK
BANKCALL	DXCH	BUF2		# SAVE INCOMING A,L.
		INDEX	Q		# PICK UP CADR.
		CA	0
		INCR	Q		# SO WE RETURN TO THE LOC. AFTER THE CADR.

#           SWCALL IS IDENTICAL TO BANKCALL, EXCEPT THAT THE CADR ARRIVES IN A.

SWCALL		TS	L
		LXCH	FBANK		# SWITCH BANKS, SAVING RETURN.
		MASK	LOW10		# GET SUB-ADDRESS OF CADR.
		XCH	Q		# A,L NOW CONTAINS DP RETURN.
		DXCH	BUF2		# RESTORING INPUTS IF THIS IS A BANKCALL.
		INDEX	Q
		TC	10000		# SETTING Q TO SWRETURN.

SWRETURN	XCH	BUF2 	+1	# COMES HERE TO RETURN TO CALLER. C(A,L)
		XCH	FBANK		# ARE PRESERVED FOR RETURN.
		XCH	BUF2 	+1
		TC	BUF2

#          THE FOLLOWING ROUTINE CAN BE USED AS A UNILATERAL JUMP WITH C(A,L) PRESERVED AND THE CADR IMMEDIATELY
# FOLLOWING THE TC POSTJUMP INSTRUCTION.

POSTJUMP	XCH	Q		# SAVE INCOMING C(A).
		INDEX	A		# GET CADR.
		CA	0

#           BANKJUMP IS THE SAME AS POSTJUMP, EXCEPT THAT THE CADR ARRIVES IN A.

BANKJUMP	TS	FBANK
		MASK	LOW10
		XCH	Q		# RESTORING INPUT C(A) IF THIS WAS A
Q+10000		INDEX	Q		# POSTJUMP.
PRIO12		TCF	10000		# PRIO12 = TCF	10000 = 12000

## Page 994
#           THE FOLLOWING ROUTINE GETS THE RETURN CADR SAVED BY SWCALL OR BANKCALL AND LEAVES IT IN A.

MAKECADR	CAF	LOW10
		MASK	BUF2
		AD	BUF2 	+1
		TC	Q

SUPDACAL	TS	MPTEMP
		XCH	FBANK		# SET FBANK FOR DATA.
		EXTEND
		ROR	SUPERBNK	# SAVE FBANK IN BITS 15-11, AND
		XCH	MPTEMP		#  SUPERBANK IN BITS 7-5.
		MASK	LOW10
		XCH	L		# SAVE REL. ADR. IN BANK, FETCH SUPERBITS.
		INHINT			# BECAUSE RUPT DOES NOT SAVE SUPERBANK.
		EXTEND
		WRITE	SUPERBNK	# SET SUPERBANK FOR DATA.
		INDEX	L
		CA	10000		# PINBALL (FIX MEM DISP) PREVENTS DCA HERE
		XCH	MPTEMP		# SAVE 1ST WD, FETCH OLD FBANK AND SBANK.
		EXTEND
		WRITE	SUPERBNK	# RESTORE SUPERBANK.
		RELINT
		TS	FBANK		# RESTORE FBANK.
		CA	MPTEMP		# RECOVER FIRST WORD OF DATA.
		RETURN			# 24 WDS. DATACALL 516 MU, SUPDACAL 432 MU

## Page 995
#          THE FOLLOWING ROUTINES ARE IDENTICAL TO BANKCALL AND SWCALL EXCEPT THAT THEY ARE USED IN INTERRUPT.

IBNKCALL	DXCH	RUPTREG3	# USES RUPTREG3,4 FOR DP RETURN ADDRESS.
		INDEX	Q
		CAF	0
		INCR	Q

ISWCALL		TS	L
		LXCH	FBANK
		MASK	LOW10
		XCH	Q
		DXCH	RUPTREG3
		INDEX	Q
		TC	10000

ISWRETRN	XCH	RUPTREG4
		XCH	FBANK
		XCH	RUPTREG4
		TC	RUPTREG3

# 2. USPRCADR ACCESSES INTERPRETIVE CODING IN OTHER THAN THE USER'S FBANK.  THE CALLING SEQUENCE IS AS FOLLOWS:
#	L	TC	USPRCADR
#	L+1	CADR	INTPRETX	INTPRETX IS THE INTERPRETIVE CODING
#					RETURN IS TO L+2

USPRCADR	TS	LOC		# SAVE A
		CA	BIT8
		TS	EDOP		# EXIT INSTRUCTION TO EDOP
		CA	BBANK
		TS	BANKSET		# USER'S BBANK TO BANKSET
		INDEX	Q
		CA	0
		TS	FBANK		# INTERPRETIVE BANK TO FBANK
		MASK	LOW10		# YIELDS INTERPRETIVE RELATIVE ADDRESS
		XCH	Q		# INTERPRETIVE ADDRESS TO Q, FETCHING L+1
		XCH	LOC		# L+1 TO LOC, RETRIEVING ORIGINAL A
		TCF	Q+10000

## Page 996
# THERE ARE FOUR POSSIBLE SETTINGS FOR CHANNEL 07.  (CHANNEL 07 CONTAINS THE SUPERBANK SETTING.)
#
#					PSEUDO-FIXED	  OCTAL PSEUDO
# SUPERBANK	SETTING	S-REG. VALUE	BANK NUMBERS	  ADDRESSES
# ----------	-------	------------	 ------------	   ------------
# SUPERBANK 3	  0XX	 2000 - 3777	   30 - 37	 70000 - 107777		(WHERE XX CAN BE ANYTHING AND
#										WILL USUALLY BE SEEN AS 11)
# SUPERBANK 4	  100	 2000 - 3777	   40 - 47	110000 - 127777		(AS FAR AS IT CAN BE SEEN,
#										ONLY BANKS 40-43 WILL EVER BE
#										AND ARE PRESENTLY AVAILABLE)
# SUPERBANK 5	  101	 2000 - 3777	   50 - 57	130000 - 147777		(PRESENTLY NOT AVAILABLE TO
#										THE USER)
# SUPERBANK 6	  110	 2000 - 3777	   60 - 67	150000 - 167777		(PRESENTLY NOT AVAILABLE TO
#										THE USER)
# *** THIS ROUTINE MAY BE CALLED BY ANY PROGRAM LOCATED IN BANKS 00 - 27.  I.E., NO PROGRAM LIVING IN ANY
# SUPERBANK SHOULD USE SUPERSW. ***
#
# SUPERSW MAY BE CALLED IN THIS FASHION:
#	CAF	ABBCON		WHERE   -- ABBCON   BBCON  SOMETHIN  --
#	TCR	SUPERSW		(THE SUPERBNK BITS ARE IN THE BBCON)
#	...	  ...
#	 .	   .
#	 .	   .
# OR IN THIS FASHION:
#	CAF	SUPERSET	WHERE SUPERSET IS ONE OF THE FOUR AVAILABLE
#	TCR	SUPERSW		SUPERBANK BIT CONSTANTS:
#	...	  ...					SUPER011 OCTAL  60
#	 .	   .					SUPER100 OCTAL 100
#	 .	   .					SUPER101 OCTAL 120
#							SUPER110 OCTAL 140

SUPERSW		EXTEND
		WRITE	SUPERBNK	# WRITE BITS 7-6-5 OF THE ACCUMULATOR INTO
					# CHANNEL 07
		TC	Q		# TC TO INSTRUCTION FOLLOWING
					#  TC SUPERSW
		
