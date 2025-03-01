#!/usr/bin/env python3
'''
License:    The author, Ron Burkey, declares this program to be in the Public
            Domain, and may be used or modified in any way desired.
Filename:   INITIALI.py
Purpose:    This is part of the port of the original XPL source code for 
            HAL/S-FC into Python.
Contact:    The Virtual AGC Project (www.ibiblio.org/apollo).
History:    2023-08-25 RSB  Began porting from INITIALI.xpl.
'''

from xplBuiltins import *  # Built-in functions
import g  # Get global variables.
from CHARTIME import CHARTIME
from CHARDATE import CHARDATE
from PRINTDAT import PRINT_DATE_AND_TIME
from ERRORS import ERRORS
from GETSUBSE import GET_SUBSET
from UNSPEC import UNSPEC
from SETTLIMI import SET_T_LIMIT
from ORDEROK import ORDER_OK
from SOURCECO import SOURCE_COMPARE
from STREAM import STREAM
from SCAN import SCAN
from SRNUPDAT import SRN_UPDATE
from HALINCL.CERRDECL import CLASS_BI
# from HALINCL.SPACELIB import g.RECORD_USED

'''
*************************************************************************
 PROCEDURE NAME:  INITIALIZATION                                         
 MEMBER NAME:     INITIALI                                               
 LOCAL DECLARATIONS:                                                     
       AGAIN(4)          LABEL              PRO               FIXED      
       CON               FIXED              SORT1       ARRAY BIT(16)    
       ENDMFID           LABEL              SORT2       ARRAY BIT(16)    
       EQUALS            CHARACTER          STORAGE_INCREMENT FIXED      
       LOGHEAD           CHARACTER          STORAGE_MASK      FIXED      
       NO_CORE           LABEL              SUBHEAD           CHARACTER  
       NPVALS            FIXED              TYPE2             FIXED      
       NUM1_OPT          BIT(16)            TYPE2_TYPE(12)    BIT(8)     
       NUM2_OPT          BIT(16)            VALS              FIXED      
 EXTERNAL VARIABLES REFERENCED:                                          
       ATOM#_LIM                            LIT_NDX                      
       ATOMS                                LIT_PG                       
       BLOCK_SRN_DATA                       MACRO_TEXTS                  
       CLASS_B                              MODF                         
       CLASS_BI                             MOVEABLE                     
       CLASS_M                              NSY                          
       CONST_ATOMS                          NT                           
       CONST_DW                             NUM_DWNS                     
       CONTROL                              OPTIONS_CODE                 
       CROSS_REF                            OUTER_REF_TABLE              
       CSECT_LENGTHS                        PAGE                         
       DATE_OF_COMPILATION                  SRN_BLOCK_RECORD             
       DOUBLE                               STMT_NUM                     
       DOUBLE_SPACE                         SUBHEADING                   
       DOWN_INFO                            SYM_TAB                      
       DW_AD                                TIME_OF_COMPILATION          
       DW                                   TOKEN                        
       EJECT_PAGE                           TRUE                         
       FALSE                                UNMOVEABLE                   
       FL_NO                                VMEM_MAX_PAGE                
       IC_SIZE                              VMEMREC                      
       INCLUDE_LIST_HEAD                    VOCAB                        
       INPUT_DEV                            X1                           
       LINK_SORT                            X4                           
       LIT_BUF_SIZE                         X70                          
       LIT_CHAR_AD                          X8                           
 EXTERNAL VARIABLES CHANGED:                                             
       ADDR_FIXED_LIMIT                     LRECL                        
       ADDR_FIXER                           MACRO_TEXT_LIM               
       ADDR_PRESENT                         NEXT                         
       ADDR_ROUNDER                         NEXT_ATOM#                   
       C                                    NT_PLUS_1                    
       CARD_COUNT                           ONE_BYTE                     
       CARD_TYPE                            OUTER_REF_LIM                
       CASE_LEVEL                           PAD1                         
       COMM                                 PAD2                         
       COMMENT_COUNT                        PARTIAL_PARSE                
       CUR_IC_BLK                           PROCMARK                     
       CURRENT_CARD                         S                            
       DATA_REMOTE                          SAVE_CARD                    
       FIRST_CARD                           SDL_OPTION                   
       FOR_ATOMS                            SIMULATING                   
       FOR_DW                               SP                           
       HMAT_OPT                             SREF_OPTION                  
       I                                    SRN_PRESENT                  
       IC_LIM                               STACK_DUMP_PTR               
       IC_MAX                               STATE                        
       IC_ORG                               STMT_PTR                     
       INDENT_INCR                          SYSIN_COMPRESSED             
       INPUT_REC                            SYTSIZE                      
       J                                    TABLE_ADDR                   
       K                                    TEMP1                        
       LAST                                 TEXT_LIMIT                   
       LAST_SPACE                           TPL_FLAG                     
       LINE_LIM                             TPL_LRECL                    
       LINE_MAX                             VMEM_PAD_ADDR                
       LISTING2_COUNT                       VMEM_PAD_PAGE                
       LISTING2                             VOCAB_INDEX                  
       LIT_CHAR_SIZE                        XREF_LIM                     
 EXTERNAL PROCEDURES CALLED:                                             
       CHARDATE                             ORDER_OK                     
       CHARTIME                             PAD                          
       EMIT_ARRAYNESS                       PRINT_DATE_AND_TIME          
       ERRORS                               SCAN                         
       ERROR                                SET_T_LIMIT                  
       GET_CELL                             SOURCE_COMPARE               
       GET_SUBSET                           SRN_UPDATE                   
       LEFT_PAD                             STREAM                       
       MIN                                  UNSPEC                       
       NEXT_RECORD                          VMEM_INIT                    
'''

#           INITIALIZATION         


def INITIALIZATION():
    # INITIALIZATION() is called only once, and therefore couldn't possibly
    # need persistent locals.

    SUBHEAD = 'STMT                                   ' + \
              '               SOURCE                                                  CURRENT S' + \
              'COPE'
    
    EQUALS = ' = '
    TYPE2_TYPE = (
        0,  # TITLE 
        1,  # LINECT 
        1,  # PAGES 
        1,  # SYMBOLS 
        1,  # MACROSIZE 
        1,  # LITSTRINGS 
        1,  # COMPUNIT 
        1,  # XREFSIZE 
        0,  # CARDTYPE 
        1,  # LABELSIZE 
        1,  # DSR 
        1,  # BLOCKSUM 
        0)  # MFID FOR PASS; OLDTPL FOR BFS 
    
    STORAGE_INCREMENT = 0
    STORAGE_MASK = 0
    LOGHEAD = 'STMT                                      ' + \
             '                            SOURCE                                              ' + \
             '                    REVISION'
    TMP = 0
    if g.pfs:
        NUM1_OPT = 19
        SORT1 = (8, 5, 0, 13, 19, 2, 1, 15, 17, 14, 10, 16, 9, 11, 6, 7, 18, 3, 4, 12)
    else:
        NUM1_OPT = 20
        SORT1 = (8, 5, 0, 13, 20, 2, 1, 15, 17, 18, 14, 10, 16, 9, 11, 6, 7, 19, 3, 4, 12)
    NUM2_OPT = 12
    SORT2 = (11, 8, 6, 10, 9, 1, 5, 4, 12, 2, 3, 0, 7)
    
    # INITIALIZE g.DATA_REMOTE FLAG                                   
    g.DATA_REMOTE = g.FALSE;
    #---------------------------------------------------------------
    STORAGE_INCREMENT = MONITOR(32);
    STORAGE_MASK = -STORAGE_INCREMENT & 0xFFFFFF
    '''
    The following code relates to determining and printing out the compiler
    options which have been supplied originally by JCL, but for us by 
    command-line options.  The available options are described by the "HAL/S-FC
    User's Manual" (chapter 5), while the organization of these in IBM 
    System/360 system memory (as we would need it to work with the following
    code) is described in the "HAL/S-FC and HAL/S-360 Compiler System Program 
    Description" (IR-182-1) around p. 696. In neither sources is there an 
    explanation of how the options specifically relate to the bit-flags in
    the 32-bit variable OPTIONS_WORD, so whatever g.I know about that has been
    gleaned from looking at how the source code processes that word.
        Flag          Pass         Keyword (abbreviation)
        ----          ----         ----------------------
        0x40000000    1            REGOPT (R) for BFS
        0x10000000    3            DEBUG
        0x08000000    3            DLIST
        0x04000000    1            MICROCODE (MC)
        0x02000000    1            REGOPT (R) for PFS
        0x01000000    ?            STATISTICS
        0x00800000    1            SDL (NONE)
        0x00400000    4            DECK (D)
        0x00200000    1            LFXI (NONE)
        0x00100000    1            ADDRS (A)
        0x00080000    1            SRN (NONE)
        0x00040000    1            HALMAT (HM)
        0x00020000    1            CODE_LISTING_REQUESTED
        0x00010000    1            g.PARTIAL_PARSE
        0x00008000    3,4          SDF_SUMMARY, TABLST (TL)
        0x00004000    1            EXTRA_LISTING
        0x00002000    1            SREF (SR)
        0x00001000    3,4          TABDMP (TBD)
        0x00000800    1            g.SIMULATING
        0x00000400    1            Z_LINKAGE ... perhaps ZCON (Z)
        0x00000200    ?            TRACE
        0x00000080    3            HIGHOPT (HO)
        0x00000040    1,2,4        NO_VM_OPT, ?, BRIEF
        0x00000020    4            ALL
        0x00000010    1            TEMPLATE (TP)
        0x00000008    2,3          TRACE
        0x00000004    1            LIST (L)
        0x00000002    1            g.LISTING2 (L2)
        ?                          DUMP (DP)
        ?                          LSTALL (LA)
        ?                          PARSE (P)
        ?                          SCAL (SC) for BFS only
        ?                          TABLES (TBL)
        ?                          VARSYM (VS)
    '''
    
    g.OPTIONS_CODE(g.pOPTIONS_CODE)
    CON = g.pCON
    PRO = g.pPRO
    TYPE2 = g.pDESC
    VALS = g.pVALS
    NPVALS = []
    
    g.C[0] = VALS[TYPE2.index("TITLE")]
    if LENGTH(g.C[0]) == 0:
        g.C[0] = 'T H E  V I R T U A L  A G C  P R O J E C T'
    g.J = LENGTH(g.C[0])
    g.J = ((61 - g.J) // 2) + g.J
    g.C[0] = LEFT_PAD(g.C[0], g.J)
    g.C[0] = PAD(g.C[0], 61)  # g.C CONTAINS CENTERED TITLE 
    g.TIME_OF_COMPILATION(TIME())
    g.S = CHARTIME(g.TIME_OF_COMPILATION())
    g.DATE_OF_COMPILATION(DATE())
    g.S = CHARDATE(g.DATE_OF_COMPILATION()) + g.X4 + g.S
    OUTPUT(1, 'H  HAL/S ' + STRING(MONITOR(23)) + g.C[0] + g.X4 + g.S)
    PRINT_DATE_AND_TIME('   HAL/S COMPILER PHASE 1 -- VERSION' + \
                        ' OF ', g.DATE_OF_GENERATION, g.TIME_OF_GENERATION)
    g.DOUBLE_SPACE()
    PRINT_DATE_AND_TIME ('TODAY IS ', DATE(), TIME())
    OUTPUT(0, g.X1)
    
    g.C[0] = g.PARM_FIELD
    g.I = 0
    g.S = ' PARM FIELD: '
    g.K = LENGTH(g.C[0])
    while g.I < g.K:
        g.J = MIN(g.K - g.I, 119)  # DON'T EXCEED LINE WIDTH OF PRINTER 
        OUTPUT(0, g.S + SUBSTR(g.C[0], g.I, g.J))  # PRINT ALL OR PART 
        g.I = g.I + g.J
        g.S = SUBSTR(g.X70, 0, LENGTH(g.S))
    g.DOUBLE_SPACE()
    OUTPUT(0, ' COMPLETE LIST OF COMPILE-TIME OPTIONS IN EFFECT')
    g.DOUBLE_SPACE()
    OUTPUT(0, '       *** TYPE 1 OPTIONS ***')
    OUTPUT(0, g.X1)
    # PRINT THE TYPE 1 OPTIONS USING THE ORDER IN SORT1 ARRAY.
    # SINCE QUASI & TRACE ARE 360 ONLY, DO NOT PRINT.  PRINT LFXI HERE  
    # EVEN THOUGH IT IS DEFINED AS A "NONPRINTABLE" OPTION IN COMPOPT.  
    for g.I in range(0, NUM1_OPT + 1):
        # MAKE SURE NOT QUASI OR TRACE
        if (SORT1[g.I] != 17) & (SORT1[g.I] != 3):
            if SORT1[g.I] == 2:  # PRINT LFXI HERE
                if (g.OPTIONS_CODE() & 0x00200000) != 0:
                    OUTPUT(0, g.X8 + '  LFXI')
                else:
                    OUTPUT(0, g.X8 + 'NOLFXI')
            if SUBSTR(STRING(CON[SORT1[g.I]]), 0, 2) == 'NO':
                OUTPUT(0, g.X8 + STRING(CON[SORT1[g.I]]))
            else:
                OUTPUT(0, g.X8 + '  ' + STRING(CON[SORT1[g.I]]))
    g.DOUBLE_SPACE()
    OUTPUT(0, '       *** TYPE 2 OPTIONS ***')
    OUTPUT(0, g.X1)
    g.I = 0
    
    #********************************************
    # THE FOLLOWING BLOCKS OF CODE WERE EXCLUDED 
    # DUE TO COMPILER FEATURE DIFFERENCES. PASS  
    # SYSTEM IMPLEMENTS MFID OPTION. BFS SYSTEM  
    # IMPLEMENTS OLDTPL OPTION.                  
    #********************************************
    # PRINT THE TYPE 2 OPTIONS USING THE ORDER IN SORT2 ARRAY
    if g.pfs:
        for g.I in range(0, NUM2_OPT + 1):
            g.C[0] = LEFT_PAD(STRING(TYPE2[SORT2[g.I]]), 15);
            if TYPE2_TYPE[SORT2[g.I]]:
                g.S = VALS[SORT2[g.I]];  # DECIMAL VALUE
            else:
                g.S = STRING(VALS[SORT2[g.I]]);  # DESCRIPTOR
            if STRING(TYPE2[SORT2[g.I]]) == 'MFID':
                OUTPUT(0, g.C[0] + EQUALS + g.S);
                if LENGTH(g.S) > 0:
                    VALS[SORT2[g.I]] = 0;
                    for g.J in range(0, LENGTH(g.S)):
                        if BYTE(g.S, g.J) < BYTE('0') or BYTE(g.S, g.J) > BYTE('9'):
                            ERRORS (CLASS_BI, 103, g.X1 + g.S);
                            VALS[SORT2[g.I]] = 0;
                            break
                        else:
                            VALS[SORT2[g.I]] = VALS[SORT2[g.I]] * 10;
                            # FOLLOWING TO AVOID 'USED ALL ACCUMULATORS'
                            TMP = VALS[SORT2[g.I]];
                            VALS[SORT2[g.I]] = TMP + (BYTE(g.S, g.J) & 0x0F);
            else:
                OUTPUT(0, g.C[0] + EQUALS + str(g.S));
    else:
        #***********************************
        # MFID'S ARE NOT IMPLEMENTED IN BFS 
        #***********************************
        for g.I in range(0, NUM2_OPT + 1):
            g.C[0] = LEFT_PAD(STRING(TYPE2[SORT2[g.I]]), 15);
            if TYPE2_TYPE[SORT2[g.I]]:
                g.S = VALS[SORT2[g.I]];  # DECIMAL VALUE
            else:
                g.S = STRING(VALS[SORT2[g.I]]);  # DESCRIPTER
            if SORT2[g.I] != 12: 
                OUTPUT(0, g.C[0] + EQUALS + g.S);
    g.LISTING2 = (g.OPTIONS_CODE() & 0x02) != 0;
    g.SREF_OPTION = (g.OPTIONS_CODE() & 0x2000) != 0;
    g.PARTIAL_PARSE = (g.OPTIONS_CODE() & 0x010000) != 0;
    g.LISTING2_COUNT = VALS[1]
    g.LINE_MAX = VALS[1]
    g.LINE_LIM = VALS[1];
    g.SIMULATING = (g.OPTIONS_CODE() & 0x800) != 0;
    if (g.OPTIONS_CODE() & 0x10) == 0x10:
        g.TPL_FLAG = 0;
    g.SRN_PRESENT = (g.OPTIONS_CODE() & 0x80000) != 0;
    g.SDL_OPTION = (g.OPTIONS_CODE() & 0x800000) != 0;
    if g.SDL_OPTION:
        g.SRN_PRESENT = g.TRUE;
    g.ADDR_PRESENT = (g.OPTIONS_CODE() & 0x100000) != 0;
    if g.SRN_PRESENT:
        g.PAD1 = SUBSTR(g.X70, 0, 11);
        g.PAD2 = SUBSTR(g.X70, 0, 15);
        g.C[0] = '   SRN ';
    else:
        g.PAD1 = g.X4;
        g.PAD2 = g.X8;
        g.C[0] = '';
    if (g.OPTIONS_CODE() & 0x00040000) != 0:
        g.HMAT_OPT = g.TRUE;
    OUTPUT(0, g.X1);
    if GET_SUBSET('$$SUBSET', 0x1):
        OUTPUT(1, '0 *** NO LANGUAGE SUBSET IN EFFECT ***');
    OUTPUT(1, g.SUBHEADING + g.C[0] + LOGHEAD);
    g.EJECT_PAGE();
    OUTPUT(1, g.SUBHEADING + g.C[0] + SUBHEAD);
    g.INDENT_INCR = 2; 
    g.CASE_LEVEL = -1;
    g.CARD_COUNT = -1;
    g.INCLUDE_LIST_HEAD(-1);
    g.COMMENT_COUNT = -1;
    g.LAST = -1;
    g.NEXT = -1;
    g.STMT_PTR = -1;
    g.STACK_DUMP_PTR = -1;
    g.LAST_SPACE = 2;
    g.ONE_BYTE = '?';
    g.STMT_NUM(1);
    g.PROCMARK = 1;
    g.FL_NO(1);
    g.NT_PLUS_1 = g.NT + 1;
    g.IC_ORG = 0;
    g.IC_MAX = 0;
    g.CUR_IC_BLK = 0;
    g.IC_LIM = g.IC_SIZE;  # UPPER LIMIT OF TABLE  
    MONITOR(4, 3, g.IC_SIZE * 8);
    g.SYTSIZE = VALS[3];
    g.MACRO_TEXT_LIM = VALS[4];
    g.LIT_CHAR_SIZE = VALS[5];
    g.XREF_LIM = VALS[7];
    g.OUTER_REF_LIM = VALS[11];
    '''
    g.J = (g.FREELIMIT + 512) & STORAGE_MASK;  # BOUNDARY NEAR TOP OF CORE 
    g.TEMP1 = (g.J - (13000 + 2 * 1680 + 3 * 3458)) & STORAGE_MASK;  # TO ALLOW ROOM FOR BUFFERS
    if g.TEMP1 - 512 <= g.FREEPOINT:
        COMPACTIFY();
    # MONITOR(7, ADDR(g.TEMP1), g.J - g.TEMP1);
    g.FREELIMIT = g.TEMP1 - 512;
    # INITIALIZE VMEM PAGING AND ALLOCATE SPACE FOR IN-CORE PAGES
    '''
    '''
    ... lots of stuff just deleted here that I hope pertains to
        (unnecessary) virtual memory ...
    '''
    g.CARD_TYPE[BYTE('E')] = 1;
    g.CARD_TYPE[BYTE('M')] = 2;
    g.CARD_TYPE[BYTE('S')] = 3;
    g.CARD_TYPE[BYTE('C')] = 4;
    g.CARD_TYPE[BYTE('D')] = 5;
    g.CARD_TYPE[BYTE(g.X1)] = 2;
    g.C[0] = STRING(VALS[8]);  # PICK UP STRING (IF ANY) 
    if LENGTH(g.C[0]) > 0: 
        for g.I in range(0, LENGTH(g.C[0]) - 1, 2):
            g.J = BYTE(g.C[0], g.I);
            g.K = BYTE(g.C[0], g.I + 1);
            if g.CARD_TYPE[g.J] == 0:
                g.CARD_TYPE[g.J] = g.CARD_TYPE[g.K];
    for g.I in range(1, g.NSY + 1):
        g.K = g.VOCAB_INDEX[g.I];
        g.J = g.K & 0xFF;
        g.C[0] = SUBSTR(g.VOCAB[g.J], SHR(g.K, 8) & 0xFFFF, SHR(g.K, 24));
        g.VOCAB_INDEX[g.I] = UNSPEC(g.C[0]);
    g.CURRENT_CARD = INPUT(g.INPUT_DEV);
    g.LRECL = LENGTH(g.CURRENT_CARD) - 1;
    g.TEXT_LIMIT[0] = SET_T_LIMIT(g.LRECL);
    g.FIRST_CARD = g.TRUE;
    if not g.pfs:  # BFS
        g.TEXT_LIMIT[1] = g.TEXT_LIMIT[0];
    if BYTE(g.CURRENT_CARD) == 0x00:
        # COMPRESSED SOURCE 
        g.SYSIN_COMPRESSED = g.TRUE;
        g.INPUT_REC[0] = g.CURRENT_CARD[:];
        NEXT_RECORD();  # GET FIRST REAL RECORD 
    while not ORDER_OK(BYTE('C')):
        ERROR(CLASS_M, 2);
        NEXT_RECORD();
    if LENGTH(g.CURRENT_CARD) > 88:
        g.CURRENT_CARD = SUBSTR(g.CURRENT_CARD, 0, 88);
    g.CARD_COUNT = g.CARD_COUNT + 1;
    g.SAVE_CARD = g.CURRENT_CARD[:];
    SOURCE_COMPARE();
    STREAM();
    SCAN();
    if g.CONTROL[4]:
        OUTPUT(0, 'SCANNER: ' + str(g.TOKEN));
    SRN_UPDATE();
    # INITIALIZE THE PARSE STACK 
    g.STATE = 1;  # START-STATE  
    # g.SP = 0xFFFFFFFF;
    g.SP = -1
    return;
