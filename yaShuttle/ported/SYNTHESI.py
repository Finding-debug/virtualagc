#!/usr/bin/env python3
'''
License:    The author, Ron Burkey, declares this program to be in the Public
            Domain, and may be used or modified in any way desired.
Filename:   RECOVER.py
Purpose:    This is part of the port of the original XPL source code for 
            HAL/S-FC into Python. 
Contact:    The Virtual AGC Project (www.ibiblio.org/apollo).
History:    2023-09-12 RSB  Began porting from XPL
'''

from xplBuiltins import *
import g
import HALINCL.COMMON as h
import HALINCL.CERRDECL as d
from ADDANDSU import ADD_AND_SUBTRACT
from ARITHLIT import ARITH_LITERAL
from COMPRESS import COMPRESS_OUTER_REF
from EMITSMRK import EMIT_SMRK
from ERROR    import ERROR
from GETICQ   import GET_ICQ
from GETLITER import GET_LITERAL
from HALMATOU import HALMAT_OUT
from HALMATPI import HALMAT_PIP
from HALMATPO import HALMAT_POP
from HALMATTU import HALMAT_TUPLE
from KILLNAME import KILL_NAME
from MATCHSIM import MATCH_SIMPLES
from OUTPUTWR import OUTPUT_WRITER
from PROCESS2 import PROCESS_CHECK
from SETUPVAC import SETUP_VAC
from SETXREFR import SET_XREF_RORS
from STACKDUM import STACK_DUMP
from UNARRAY2 import UNARRAYED_SCALAR
from HALINCL.ENTERLAY import ENTER_LAYOUT
from HALINCL.SAVELITE import SAVE_LITERAL

'''
 /***************************************************************************/
 /* PROCEDURE NAME:  SYNTHESIZE                                             */
 /* MEMBER NAME:     SYNTHESI                                               */
 /* INPUT PARAMETERS:                                                       */
 /*       PRODUCTION_NUMBER FIXED                                           */
 /* LOCAL DECLARATIONS:                                                     */
 /*       ALSO_SCALAR       LABEL              INLINE_ENTRY      LABEL      */
 /*       ARITH_LITS        LABEL              INLINE_NAME       CHARACTER  */
 /*       ARRAY_SPEC        LABEL              INLINE_SCOPE      LABEL      */
 /*       ASSIGN_ARG        LABEL              IO_CONTROL        LABEL      */
 /*       ASSIGNING         LABEL              IO_EMIT           LABEL      */
 /*       CHANGED_STMT_NUM  BIT(1)                                          */
 /*       CASE_HEAD         LABEL              LABEL_INCORP      LABEL      */
 /*       CHAR_LITS         LABEL              MAKE_ATTRIBUTES   LABEL      */
 /*       CHECK_ARRAY_SPEC  LABEL              MATRICES_MAY_GO_RIGHT  LABEL */
 /*       CHECK_DECLS       LABEL              MATRICES_TAKEN_CARE_OF  LABEL*/
 /*       CHECK_READ        LABEL              MODE_CHECK        LABEL      */
 /*       CLOSE_IF          LABEL              MOST_IDS          LABEL      */
 /*       CLOSE_IT          LABEL              NEW_SCOPE         LABEL      */
 /*       CLOSE_SCOPE       LABEL              NEXT_ARG          LABEL      */
 /*       COMBINE_SCALARS_AND_VECTORS  LABEL   NO_ATTR_STRUCT    LABEL      */
 /*       CROSS_PRODUCTS    LABEL              NON_EVENT         LABEL      */
 /*       DECL_STAT         LABEL              OK_LABELS         LABEL      */
 /*       DEFAULT_SHAPER    LABEL              ON_ERROR_ACTION   LABEL      */
 /*       DIV_FAIL          LABEL              OUTERMOST_BLOCK   LABEL      */
 /*       DO_BIT_CAT        LABEL              POWER_FAIL        LABEL      */
 /*       DO_BIT_CONST      LABEL              PROC_FUNC_HEAD    LABEL      */
 /*       DO_BIT_CONSTANT_END  LABEL           REGULAR_EXP       LABEL      */
 /*       DO_BIT_FACTOR     LABEL              REPEATING         LABEL      */
 /*       DO_CHAR_CAT       LABEL              SCALAR_SHAPER     LABEL      */
 /*       DO_CONSTANT       LABEL              SCHED_PRIO        LABEL      */
 /*       DO_DISCRETE       LABEL              SCHEDULE_AT       LABEL      */
 /*       DO_DONE           LABEL              SCHEDULE_EMIT     LABEL      */
 /*       DO_FLOWSET        LABEL              SCHEDULE_EVERY    LABEL      */
 /*       DO_INIT_CONST_HEAD  LABEL            SET_ARITH_SHAPERS LABEL      */
 /*       DO_LIT_BIT_FACTOR LABEL              SET_AUTSTAT       LABEL      */
 /*       DO_QUALIFIED_ATTRIBUTE  LABEL        SET_CASE          LABEL      */
 /*       DOT_PRODUCTS      LABEL              SET_INIT          LABEL      */
 /*       DOT_PRODUCTS_LOOP LABEL              SHARP_EXP         LABEL      */
 /*       DUPLICATE_BLOCK   LABEL              SIGNAL_EMIT       LABEL      */
 /*       EMIT_CASE         LABEL              SIMPLE_EXP        LABEL      */
 /*       EMIT_IF           LABEL              SIMPLE_SUBS       LABEL      */
 /*       EMIT_IO_ARG       LABEL              SPEC_TYPE         LABEL      */
 /*       EMIT_IO_HEAD      LABEL              SPEC_VAR          LABEL      */
 /*       EMIT_NULL         LABEL              SS_CHEX           LABEL      */
 /*       EMIT_REL          LABEL              SS_FIXUP          LABEL      */
 /*       EMIT_WHILE        LABEL              STRUC_IDS         LABEL      */
 /*       END_ASSIGN        LABEL              STRUCT_GOING_DOWN LABEL      */
 /*       END_REPEAT_INIT   LABEL              STRUCT_GOING_UP   LABEL      */
 /*       ENDING_DONE       LABEL              SUB_START         LABEL      */
 /*       EXITTING          LABEL              T_FOUND           LABEL      */
 /*       FINISH_EXP        LABEL              TEMPL_INITIAL_CHECK  LABEL   */
 /*       FIX_AUTSTAT       LABEL              TERM_LIST         LABEL      */
 /*       FIX_NOLAB         LABEL              UNQ_TEST1         LABEL      */
 /*       FIX_NULL          LABEL              UNQ_TEST2         LABEL      */
 /*       FUNC_HEADER       LABEL              UP_PRIO           LABEL      */
 /*       FUNC_IDS          LABEL              UPDATE_CHECK      LABEL      */
 /*       H1                BIT(16)            UPDATE_HEAD       LABEL      */
 /*       H2                BIT(16)            UPDATE_NAME       CHARACTER  */
 /*       INCORPORATE_ATTR  LABEL              WAIT_TIME         LABEL      */
 /*       INIT_ELEMENT      LABEL              WHILE_KEY         LABEL      */
 /*       INIT_MACRO        LABEL              YES_EVENT         LABEL      */
 /*       INLINE_DEFS       LABEL                                           */
 /* EXTERNAL VARIABLES REFERENCED:                                          */
 /*       #PRODUCE_NAME                        MAX_SCOPE#                   */
 /*       ACCESS_FLAG                          MISC_NAME_FLAG               */
 /*       ALDENSE_FLAGS                        MPP1                         */
 /*       ALIGNED_FLAG                         MTX_NDX                      */
 /*       ANY_TYPE                             N_DIM_LIM                    */
 /*       ARRAY_DIM_LIM                        NAME_FLAG                    */
 /*       ARRAY_FLAG                           NDECSY                       */
 /*       ARRAY_SUB_COUNT                      NEST_LIM                     */
 /*       ASSIGN_CONTEXT                       NEXT_ATOM#                   */
 /*       ASSIGN_TYPE                          NO_LOOK_AHEAD_DONE           */
 /*       ATTR_BEGIN_FLAG                      NONHAL_FLAG                  */
 /*       AUTO_FLAG                            NOSPACE                      */
 /*       AUTSTAT_FLAGS                        NUM_EL_MAX                   */
 /*       BIT_LENGTH_LIM                       PAGE_THROWN                  */
 /*       BIT_NDX                              PARM_CONTEXT                 */
 /*       BIT_TYPE                             PARM_FLAGS                   */
 /*       CASE_LEVEL_LIM                       PARSE_STACK                  */
 /*       CHAR_LENGTH_LIM                      PC_STMT_TYPE_BASE            */
 /*       CHAR_NDX                             PCARGBITS                    */
 /*       CHAR_TYPE                            PCARGTYPE                    */
 /*       CLASS_AA                             PCCOPY_INDEX                 */
 /*       CLASS_AV                             PERIOD                       */
 /*       CLASS_B                              PRIMARY                      */
 /*       CLASS_BN                             PROC_LABEL                   */
 /*       CLASS_BT                             PROC_MODE                    */
 /*       CLASS_C                              PROG_LABEL                   */
 /*       CLASS_D                              PROG_MODE                    */
 /*       CLASS_DA                             READ_ACCESS_FLAG             */
 /*       CLASS_DC                             REENTRANT_FLAG               */
 /*       CLASS_DD                             REMOTE                       */
 /*       CLASS_DI                             REMOTE_FLAG                  */
 /*       CLASS_DL                             REPL_ARG_CLASS               */
 /*       CLASS_DN                             REPLACE_TEXT_PTR             */
 /*       CLASS_DQ                             RIGID_FLAG                   */
 /*       CLASS_DS                             SBIT_NDX                     */
 /*       CLASS_DT                             SCALAR_TYPE                  */
 /*       CLASS_DU                             SCLR_NDX                     */
 /*       CLASS_E                              SD_FLAGS                     */
 /*       CLASS_EA                             SINGLE_FLAG                  */
 /*       CLASS_EB                             SP                           */
 /*       CLASS_EC                             STAB_STACKTOP                */
 /*       CLASS_ED                             START_POINT                  */
 /*       CLASS_EL                             STATIC_FLAG                  */
 /*       CLASS_EM                             STMT_END_PTR                 */
 /*       CLASS_EN                             STMT_LABEL                   */
 /*       CLASS_EO                             STMT_NUM                     */
 /*       CLASS_EV                             STRUCTURE_SUB_COUNT          */
 /*       CLASS_FD                             SUB_COUNT                    */
 /*       CLASS_FS                             SYM_ADDR                     */
 /*       CLASS_FT                             SYM_ARRAY                    */
 /*       CLASS_GB                             SYM_CLASS                    */
 /*       CLASS_GC                             SYM_FLAGS                    */
 /*       CLASS_GE                             SYM_LENGTH                   */
 /*       CLASS_GL                             SYM_LINK1                    */
 /*       CLASS_GV                             SYM_LINK2                    */
 /*       CLASS_IR                             SYM_LOCK#                    */
 /*       CLASS_IS                             SYM_NAME                     */
 /*       CLASS_LB                             SYM_NEST                     */
 /*       CLASS_LS                             SYM_PTR                      */
 /*       CLASS_P                              SYM_SCOPE                    */
 /*       CLASS_PC                             SYM_TYPE                     */
 /*       CLASS_PE                             SYT_ADDR                     */
 /*       CLASS_PF                             SYT_ARRAY                    */
 /*       CLASS_PL                             SYT_CLASS                    */
 /*       CLASS_PP                             SYT_FLAGS                    */
 /*       CLASS_PS                             SYT_HASHSIZE                 */
 /*       CLASS_PT                             SYT_LINK1                    */
 /*       CLASS_QS                             SYT_LINK2                    */
 /*       CLASS_QX                             SYT_LOCK#                    */
 /*       CLASS_RT                             SYT_MAX                      */
 /*       CLASS_RU                             SYT_NAME                     */
 /*       CLASS_SP                             SYT_NEST                     */
 /*       CLASS_SV                             SYT_PTR                      */
 /*       CLASS_T                              SYT_SCOPE                    */
 /*       CLASS_TC                             SYT_TYPE                     */
 /*       CLASS_TD                             TASK_LABEL                   */
 /*       CLASS_UI                             TASK_MODE                    */
 /*       CLASS_UP                             TEMP_TYPE                    */
 /*       CLASS_UT                             TEMPL_NAME                   */
 /*       CLASS_VA                             TEMPLATE_CLASS               */
 /*       CLASS_VC                             TEMPORARY_FLAG               */
 /*       CLASS_VE                             TEMPORARY_IMPLIED            */
 /*       CLASS_XM                             TOKEN                        */
 /*       CLASS_XR                             TPL_FLAG                     */
 /*       CLASS_XS                             TRUE                         */
 /*       CMPL_MODE                            UNSPEC_LABEL                 */
 /*       COMPOOL_LABEL                        UPDATE_MODE                  */
 /*       COMSUB_END                           VAR_CLASS                    */
 /*       CONSTANT_FLAG                        VAR_LENGTH                   */
 /*       CONTROL                              VEC_LENGTH_LIM               */
 /*       CROSS_TOKEN                          VEC_NDX                      */
 /*       CROSS                                VEC_TYPE                     */
 /*       CURLBLK                              XAFOR                        */
 /*       DECL_STMT_TYPE                       XAST                         */
 /*       DECLARE_CONTEXT                      XBAND                        */
 /*       DEF_BIT_LENGTH                       XBCAT                        */
 /*       DEF_CHAR_LENGTH                      XBEQU                        */
 /*       DEF_MAT_LENGTH                       XBNOT                        */
 /*       DEF_VEC_LENGTH                       XBOR                         */
 /*       DEFAULT_ATTR                         XBRA                         */
 /*       DEFAULT_TYPE                         XBTRU                        */
 /*       DEFINED_LABEL                        XCANC                        */
 /*       DENSE_FLAG                           XCAND                        */
 /*       DEVICE_LIMIT                         XCCAT                        */
 /*       DO_LEVEL_LIM                         XCDEF                        */
 /*       DO_STMT#                             XCEQU                        */
 /*       DO_TOKEN                             XCFOR                        */
 /*       DOT_TOKEN                            XCLBL                        */
 /*       DOT                                  XCLOS                        */
 /*       DOUBLE_FLAG                          XCNOT                        */
 /*       DUMMY_FLAG                           XCO_N                        */
 /*       DUPL_FLAG                            XCOR                         */
 /*       DW_AD                                XCTST                        */
 /*       ENDSCOPE_FLAG                        XDCAS                        */
 /*       EQUATE_TYPE                          XDFOR                        */
 /*       EVENT_TYPE                           XDSMP                        */
 /*       EVIL_FLAG                            XDSUB                        */
 /*       EXCLUSIVE_FLAG                       XDTST                        */
 /*       EXPONENT                             XECAS                        */
 /*       EXPRESSION_CONTEXT                   XEDCL                        */
 /*       EXT_ARRAY                            XEFOR                        */
 /*       EXTENT                               XEINT                        */
 /*       EXTERNAL_FLAG                        XERON                        */
 /*       FACTOR                               XERSE                        */
 /*       FACTOR_LIM                           XESMP                        */
 /*       FACTORED_IC_FND                      XETST                        */
 /*       FACTORED_IC_PTR                      XEXTN                        */
 /*       FALSE                                XFBRA                        */
 /*       FCN_LV                               XFDEF                        */
 /*       FCN_MODE                             XFILE                        */
 /*       FIRST_FREE                           XICLS                        */
 /*       FIRST_STMT                           XIDEF                        */
 /*       FL_NO                                XIEQU                        */
 /*       FUNC_CLASS                           XIFHD                        */
 /*       FUNC_MODE                            XIMD                         */
 /*       HALMAT_CRAP                          XINL                         */
 /*       HOST_BIT_LENGTH_LIM                  XLBL                         */
 /*       IF_TOKEN                             XLIT                         */
 /*       ILL_EQUATE_ATTR                      XMDEF                        */
 /*       ILL_INIT_ATTR                        XMEQU                        */
 /*       ILL_MINOR_STRUC                      XMINV                        */
 /*       ILL_NAME_ATTR                        XMNEG                        */
 /*       ILL_TEMPL_ATTR                       XMSDV                        */
 /*       ILL_TEMPORARY_ATTR                   XMTRA                        */
 /*       ILL_TERM_ATTR                        XNASN                        */
 /*       IMP_DECL                             XNEQU                        */
 /*       IMPL_T_FLAG                          XPDEF                        */
 /*       INACTIVE_FLAG                        XPMAR                        */
 /*       INCLUDED_REMOTE                      XPMHD                        */
 /*       IND_CALL_LAB                         XPMIN                        */
 /*       IND_LINK                             XPRIO                        */
 /*       INDENT_INCR                          XREAD                        */
 /*       INIT_CONST                           XREF_ASSIGN                  */
 /*       INIT_FLAG                            XREF_REF                     */
 /*       INLINE_FLAG                          XRTRN                        */
 /*       INLINE_INDENT                        XSCHD                        */
 /*       INLINE_MODE                          XSEQU                        */
 /*       INPUT_PARM                           XSET                         */
 /*       INT_NDX                              XSEXP                        */
 /*       INT_TYPE                             XSFST                        */
 /*       LABEL_CLASS                          XSGNL                        */
 /*       LABEL_DEFINITION                     XSIEX                        */
 /*       LABEL_FLAG                           XSPEX                        */
 /*       LAST_POPp                            XSYT                         */
 /*       LATCHED_FLAG                         XTDCL                        */
 /*       LIST_EXP_LIM                         XTDEF                        */
 /*       LIT_PG                               XTEQU                        */
 /*       LITERAL1                             XTERM                        */
 /*       LITERAL2                             XTNT                         */
 /*       LITFILE                              XTSUB                        */
 /*       LIT1                                 XUDEF                        */
 /*       LIT2                                 XVAC                         */
 /*       LOCK_FLAG                            XVEQU                        */
 /*       LOCK_LIM                             XWAIT                        */
 /*       MAC_TXT                              XXASN                        */
 /*       MACRO_TEXT                           XXPT                         */
 /*       MAJ_STRUC                            XXREC                        */
 /*       MAT_DIM_LIM                          XXXAR                        */
 /*       MAT_TYPE                             XXXND                        */
 /*       MAX_PARAMETER                        XXXST                        */
 /* EXTERNAL VARIABLES CHANGED:                                             */
 /*       ACCESS_FOUND                         MAIN_SCOPE                   */
 /*       ALT_PCARG#                           MAT_LENGTH                   */
 /*       ARRAYNESS_FLAG                       MATRIX_COUNT                 */
 /*       ASSIGN_ARG_LIST                      MATRIX_PASSED                */
 /*       ATOM#_FAULT                          MATRIXP                      */
 /*       ATTR_FOUND                           MAXNEST                      */
 /*       ATTR_INDENT                          MP                           */
 /*       ATTR_LOC                             N_DIM                        */
 /*       ATTR_MASK                            NAME_BIT                     */
 /*       ATTRIBUTES                           NAME_HASH                    */
 /*       BEGINP                               NAME_IMPLIED                 */
 /*       BI_FUNC_FLAG                         NAME_PSEUDOS                 */
 /*       BIT_LENGTH                           NAMING                       */
 /*       BLOCK_MODE                           NEST                         */
 /*       BLOCK_SYTREF                         NEST_LEVEL                   */
 /*       BUILDING_TEMPLATE                    NEST_STACK                   */
 /*       CLOSE_BCD                            NEXT_SUB                     */
 /*       COMPILING                            NONHAL                       */
 /*       C                                    NUM_ELEMENTS                 */
 /*       CASE_LEVEL                           NUM_FL_NO                    */
 /*       CASE_STACK                           NUM_STACKS                   */
 /*       CHAR_LENGTH                          ON_ERROR_PTR                 */
 /*       CLASS                                OUTER_REF_INDEX              */
 /*       COMM                                 OUTER_REF_PTR                */
 /*       CONTEXT                              PARMS_PRESENT                */
 /*       CROSS_COUNT                          PARMS_WATCH                  */
 /*       CSECT_LENGTHS                        PCARG#                       */
 /*       CURRENT_SCOPE                        PCARGOFF                     */
 /*       DATA_REMOTE                          PP                           */
 /*       DELAY_CONTEXT_CHECK                  PPTEMP                       */
 /*       DO_CHAIN                             PROCMARK                     */
 /*       DO_INIT                              PROCMARK_STACK               */
 /*       DO_INX                               PSEUDO_FORM                  */
 /*       DO_LEVEL                             PSEUDO_LENGTH                */
 /*       DO_LOC                               PSEUDO_TYPE                  */
 /*       DOT_COUNT                            PTR                          */
 /*       ELSE_FLAG                                                         */
 /*       ELSEIF_PTR                           PTR_TOP                      */
 /*       END_FLAG                                                          */
 /*       EXPONENT_LEVEL                       REF_ID_LOC                   */
 /*       EXT_P                                REFER_LOC                    */
 /*       EXTERNAL_MODE                        REGULAR_PROCMARK             */
 /*       EXTERNALIZE                          REL_OP                       */
 /*       FACTOR_FOUND                         S                            */
 /*       FACTORED_TYPE                        S_ARRAY                      */
 /*       FACTORING                            SAVE_ARRAYNESS_FLAG          */
 /*       FCN_ARG                              SAVE_INDENT_LEVEL            */
 /*       FCN_LOC                              SAVE_SCOPE                   */
 /*       FIXF                                 SCALAR_COUNT                 */
 /*       FIXL                                 SCALARP                      */
 /*       FIXV                                 SCOPE#                       */
 /*       GRAMMAR_FLAGS                        SCOPE#_STACK                 */
 /*       HALMAT_OK                            SIMULATING                   */
 /*       IC_FND                               SRN                          */
 /*       IC_PTR                               SRN_COUNT_MARK               */
 /*       ID_LOC                               SRN_COUNT                    */
 /*       INDENT_STACK                         SRN_FLAG                     */
 /*       IODEV                                SRN_MARK                     */
 /*       I                                    STAB_MARK                    */
 /*       IC_FORM                              STAB_STACK                   */
 /*       IC_FOUND                             STAB2_MARK                   */
 /*       IC_LEN                               STAB2_STACKTOP               */
 /*       IC_LINE                              STACK_PTR                    */
 /*       IC_LOC                               STARRED_DIMS                 */
 /*       IC_PTR1                              STMT_PTR                     */
 /*       IC_TYPE                              STMT_TYPE                    */
 /*       IC_VAL                               STRUC_DIM                    */
 /*       IF_FLAG                                                           */
 /*       IMPLICIT_T                           STRUC_PTR                    */
 /*       IMPLIED_UPDATE_LABEL                 STRUC_SIZE                   */
 /*       INCL_SRN                             SUB_END_PTR                  */
 /*       INCL_SRN_MARK                        SUB_SEEN                     */
 /*       INDENT_LEVEL                         SUBSCRIPT_LEVEL              */
 /*       INFORMATION                          SYM_TAB                      */
 /*       INIT_EMISSION                        TEMP1                        */
 /*       INLINE_INDENT_RESET                  TEMP2                        */
 /*       INLINE_LABEL                         TEMP3                        */
 /*       INLINE_LEVEL                         TEMP                         */
 /*       INLINE_STMT_RESET                    TEMP_SYN                     */
 /*       INX                                  TERMP                        */
 /*       J                                    TOKEN_FLAGS                  */
 /*       K                                    TPL_REMOTE                   */
 /*       LOCK#                                TPL_VERSION                  */
 /*       L                                    TYPE                         */
 /*       LABEL_COUNT                          UPDATE_BLOCK_LEVEL           */
 /*       LAST_WRITE                           VAL_P                        */
 /*       LINE_MAX                             VAR                          */
 /*       LOC_P                                VEC_LENGTH                   */
 /*       MAC_NUM                              VECTOR_COUNT                 */
 /*       MACRO_ARG_COUNT                      VECTORP                      */
 /*       MACRO_TEXTS                                                       */
 /* EXTERNAL PROCEDURES CALLED:                                             */
 /*       ADD_AND_SUBTRACT                     ICQ_ARRAY#                   */
 /*       ARITH_LITERAL                        ICQ_TERM#                    */
 /*       ARITH_SHAPER_SUB                     IORS                         */
 /*       ARITH_TO_CHAR                        KILL_NAME                    */
 /*       ASSOCIATE                            LABEL_MATCH                  */
 /*       ATTACH_SUBSCRIPT                     LIT_RESULT_TYPE              */
 /*       BIT_LITERAL                          MAKE_FIXED_LIT               */
 /*       BLOCK_SUMMARY                        MATCH_ARITH                  */
 /*       CALL_SCAN                            MATCH_SIMPLES                */
 /*       CHAR_LITERAL                         MATRIX_COMPARE               */
 /*       CHECK_ARRAYNESS                      MULTIPLY_SYNTHESIZE          */
 /*       CHECK_ASSIGN_CONTEXT                 NAME_ARRAYNESS               */
 /*       CHECK_CONFLICTS                      NAME_COMPARE                 */
 /*       CHECK_CONSISTENCY                    OUTPUT_WRITER                */
 /*       CHECK_EVENT_CONFLICTS                PREC_SCALE                   */
 /*       CHECK_EVENT_EXP                      PROCESS_CHECK                */
 /*       CHECK_IMPLICIT_T                     PUSH_FCN_STACK               */
 /*       CHECK_NAMING                         PUSH_INDIRECT                */
 /*       CHECK_STRUC_CONFLICTS                READ_ALL_TYPE                */
 /*       COMPRESS_OUTER_REF                   RESET_ARRAYNESS              */
 /*       COPINESS                             SAVE_ARRAYNESS               */
 /*       DESCORE                              SAVE_LITERAL                 */
 /*       DISCONNECT                           SET_BI_XREF                  */
 /*       EMIT_ARRAYNESS                       SET_BLOCK_SRN                */
 /*       EMIT_EXTERNAL                        SET_LABEL_TYPE               */
 /*       EMIT_PUSH_DO                         SET_OUTER_REF                */
 /*       EMIT_SMRK                            SET_SYT_ENTRIES              */
 /*       EMIT_SUBSCRIPT                       SET_XREF                     */
 /*       END_ANY_FCN                          SET_XREF_RORS                */
 /*       END_SUBBIT_FCN                       SETUP_CALL_ARG               */
 /*       ENTER                                SETUP_NO_ARG_FCN             */
 /*       ENTER_LAYOUT                         SETUP_VAC                    */
 /*       ERROR                                SRN_UPDATE                   */
 /*       ERROR_SUB                            STAB_HDR                     */
 /*       GET_ICQ                              STAB_LAB                     */
 /*       GET_LITERAL                          STAB_VAR                     */
 /*       HALMAT_BACKUP                        STACK_DUMP                   */
 /*       HALMAT_FIX_PIPp                      START_NORMAL_FCN             */
 /*       HALMAT_FIX_PIPTAGS                   STRUCTURE_COMPARE            */
 /*       HALMAT_FIX_POPTAG                    TIE_XREF                     */
 /*       HALMAT_INIT_CONST                    UNARRAYED_INTEGER            */
 /*       HALMAT_OUT                           UNARRAYED_SCALAR             */
 /*       HALMAT_PIP                           UNARRAYED_SIMPLE             */
 /*       HALMAT_POP                           UNBRANCHABLE                 */
 /*       HALMAT_TUPLE                         VECTOR_COMPARE               */
 /*       HASH                                                              */
 /* CALLED BY:                                                              */
 /*       COMPILATION_LOOP                                                  */
 /***************************************************************************/
'''

#                  THE SYNTHESIS ALGORITHM FOR HAL


class cSYNTHESIZE:

    def __init__(self):
        self.INLINE_NAME = '$FUNCTION'
        self.UPDATE_NAME = '$UPDATE'
        self.H1 = 0
        self.H2 = 0
        self.PREV_LIVES_REMOTE = 0
        self.PREV_POINTS = 0
        self.PREV_REMOTE = 0
        self.NAME_SET = 0
        self.REMOTE_SET = 0
        self.CURRENT_LIVES_REMOTE = 0
        self.CHANGED_STMT_NUM = 0
        self.ELSE_TOKEN = 0


lSYNTHESIZE = cSYNTHESIZE()


def SYNTHESIZE(PRODUCTION_NUMBER):
    l = lSYNTHESIZE  # Local variables.
    
    if True:
        # This is just to simplify debugging of SCAN. Bypass in production.
        return
    
    def SET_INIT(A, B, C, D, E):
        # Local Q doesn't need to be persistent
        g.IC_LINE = g.IC_LINE + 1;
        if g.IC_LINE > g.NUM_EL_MAX:
            ERROR(d.CLASS_BT, 7);
        Q = GET_ICQ(g.IC_LINE);
        g.IC_VAL[Q] = E;
        g.IC_LOC[Q] = A;
        g.IC_LEN[Q] = C;
        g.IC_FORM[Q] = B;
        g.IC_TYPE[Q] = D;
    
    '''
    THIS PROCEDURE IS RESPONSIBLE FOR THE SEMANTICS (CODE SYNTHESIS), IF
    ANY, OF THE SKELETON COMPILER.  ITS ARGUMENT IS THE NUMBER OF THE
    PRODUCTION WHICH WILL BE APPLIED IN THE PENDING REDUCTION.  THE GLOBAL
    VARIABLES g.MP AND g.SP POINT TO THE BOUNDS IN THE STACKS OF THE RIGHT PART
    OF THIS PRODUCTION.
    '''
    
    if g.CONTROL[8]:
        OUTPUT(0, '->->->->->->PRODUCTION NUMBER ' + str(PRODUCTION_NUMBER))
    if SHR(g.pPRODUCE_NAME[PRODUCTION_NUMBER], 12):
        ERROR(d.CLASS_XS, 2, '#' + PRODUCTION_NUMBER);
    
    # THIS CODE CHECKS TO SEE IF THE PREVIOUS STATEMENT WAS AN
    # IF-THEN OR ELSE AND IF THE CURRENT STATEMENT IS NOT A SIMPLE DO.
    # IF TRUE, THE PREVIOUS STATEMENT IS PRINTED AND EXEUCTION CONTINUES.
    if (g.IF_FLAG or g.ELSE_FLAG) and (PRODUCTION_NUMBER != 144):
        g.SQUEEZING = g.FALSE;
        l.CHANGED_STMT_NUM = g.FALSE;
        if g.IF_FLAG:
            g.STMT_NUM(g.STMT_NUM() - 1);
            l.CHANGED_STMT_NUM = g.TRUE;
        g.SAVE_SRN2 = g.SRN[2][:];
        g.SRN[2] = g.SAVE_SRN1[:];
        g.SAVE_SRN_COUNT2 = g.SRN_COUNT[2];
        g.SRN_COUNT[2] = g.SAVE_SRN_COUNT1;
        g.IF_FLAG = g.FALSE
        g.ELSE_FLAG = g.FALSE;  # MUST BE BEFORE OUTPUTWR CALL
        OUTPUT_WRITER(SAVE1, g.SAVE2);
        g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
        if l.CHANGED_STMT_NUM:
            g.STMT_NUM(g.STMT_NUM() + 1);
        if g.STMT_PTR > -1:
            g.LAST_WRITE = g.SAVE2 + 1;
        g.SRN[2] = g.SAVE_SRN2[:];
        g.SRN_COUNT[2] = g.SAVE_SRN_COUNT2;
    
    # THIS CODE IS USED TO ALIGN THE ELSE STATEMENTS CORRECTLY.
    # IF THE CURRENT STATEMENT IS NOT AN ELSE OR A DO, MOVE_ELSE=TRUE.
    if (PRODUCTION_NUMBER != 140) and (PRODUCTION_NUMBER != 54) and \
            (PRODUCTION_NUMBER != 40):
        g.MOVE_ELSE = g.TRUE;
    if (g.SAVE_DO_LEVEL != -1) and (PRODUCTION_NUMBER != 167):
        g.IFDO_FLAG[g.SAVE_DO_LEVEL] = g.FALSE;
        g.SAVE_DO_LEVEL = -1;
    
    '''
    The case statement below, which comprises essentially the remainder of the
    procedure, contains large amounts of spaghetti code in which there are 
    GO TO's within cases that jump inside of other cases.  For the most part,
    with only a few exceptions, that's handled by rearranging the cases so
    that cases with internal target labels are positioned somewhere below
    the cases that have GO TO's targeting them.  That makes it relatively 
    easy to cause those GO TO's to essentially fall into their targets.
    
    Each of the cases for the DO CASE is specified by a condition like
    PRODUCTION_NUMBER == x, however, manual entry and maintenance of those
    PRODUCTION_NUMBERs (at least originally) was error prone and nightmarish.
    I hope they're all correct now.  However, I've accompanied them by comments
    of the form 
        # reference 10*PRODUCTION_NUMBER
    and those reference numbers will remain constant (at their initial values)
    even if the underlying PRODUCTION_NUMBERs need to be corrected somehow;
    thus the reference numbers potentially provide more-stable ways of 
    referring to the cases than the actual PRODUCTION_NUMBERs do.  I've made
    the reference numbers initially 10*PRODUCTION_NUMBER to provide room to
    insert new numbers in between in case missing cases are discovered, without
    having to change the existing reference numbers any.  Again, I think that's
    unlikely, because I eventually automated creation of the
    PRODUCTION_NUMBERS in this code (see productionNumbers.py) to eliminate
    the human error I was introducing when I input or corrected them manually.
    Given that there are ~460 cases, there was a lot of potential for error
    before I automated it.
    
    The general layout of the DO CASE, after rearrangement of the cases, 
    is that we have 3 basic groupings of cases:
    
        1. Cases with *no* labels that are targets of GO TO's (or for which the
           GO TO's to the label are within the case itself), and with no 
           GO TO's targeting any cases *above* them.  This group also contains
           reference 110, which is contained within its own while-loop because
           of the large number of internal GO TO's it has.
        2. Cases with labels that are targets of GO TO's of *above* them but 
           with no GO TO's targeting any cases *above* them.
        3. The cases (references 3110 and 3210) that have GO TO's targeting
           each other are enclosed together in their only mini while-loop.
    
    Within each of the groupings, I've tried to keep the cases sorted 
    more-or-less by PRODUCTION_NUMBER (or reference number), but in the 
    second grouping, that wasn't always possible.
    '''
    goto_COMBINE_SCALARS_AND_VECTORS = False
    goto_CROSS_PRODUCTS = False
    goto_FIX_NOLAB = False
    goto_CLOSE_SCOPE = False
    goto_ARITH_LITS = False
    goto_EXITTING = False
    goto_REPEATING = False
    goto_INLINE_SCOPE = False
    goto_LABEL_INCORP = False
    goto_IO_EMIT = False
    goto_UPDATE_CHECK = False
    goto_WAIT_TIME = False
    goto_UP_PRIO = False
    goto_SCHEDULE_EMIT = False
    goto_NON_EVENT = False
    goto_YES_EVENT = False
    goto_DO_BIT_CAT = False
    goto_DO_BIT_FACTOR = False
    goto_DO_LIT_BIT_FACTOR = False
    goto_EMIT_REL = False
    goto_DO_CHAR_CAT = False
    goto_ASSIGNING = False
    goto_END_ASSIGN = False
    goto_CLOSE_IF = False
    goto_EMIT_IF = False
    goto_DO_DONE = False
    goto_EMIT_WHILE = False
    goto_SET_CASE = False
    goto_EMIT_CASE = False
    goto_CASE_HEAD = False
    goto_EMIT_NULL = False
    goto_WHILE_KEY = False
    goto_DO_FLOWSET = False
    goto_DO_DISCRETE = False
    goto_ON_ERROR_ACTION = False
    goto_SIGNAL_EMIT = False
    goto_ASSIGN_ARG = False
    goto_FIX_NULL = False
    goto_STRUC_IDS = False
    goto_MOST_IDS = False
    goto_FUNC_IDS = False
    goto_SS_CHEX = False
    goto_SS_FIXUP = False
    goto_SUB_START = False
    goto_SHARP_EXP = False
    goto_DO_BIT_CONSTANT_END = False
    goto_DO_BIT_CONST = False
    goto_CHAR_LITS = False
    goto_IO_CONTROL = False
    goto_CHECK_READ = False
    goto_EMIT_IO_ARG = False
    goto_EMIT_IO_HEAD = False
    goto_CHECK_DECLS = False
    goto_PROC_FUNC_HEAD = False
    goto_NEW_SCOPE = False
    goto_INLINE_ENTRY = False
    goto_INLINE_DEFS = False
    goto_OUTERMOST_BLOCK = False
    goto_DUPLICATE_BLOCK = False
    goto_UPDATE_HEAD = False
    goto_FUNC_HEADER = False
    goto_INIT_MACRO = False
    goto_NEXT_ARG = False
    goto_DECL_STAT = False
    goto_STRUCT_GOING_UP = False
    goto_STRUCT_GOING_DOWN = False
    goto_NO_ATTR_STRUCT = False
    goto_SPEC_VAR = False
    goto_CHECK_ARRAY_SPEC = False
    goto_MAKE_ATTRIBUTES = False
    goto_ARRAY_SPEC = False
    goto_INCORPORATE_ATTR = False
    goto_SPEC_TYPE = False
    goto_SET_AUTSTAT = False
    goto_DO_QUALIFIED_ATTRIBUTE = False
    goto_DO_INIT_CONST_HEAD = False
    goto_INIT_ELEMENT = False
    goto_END_REPEAT_INIT = False
    goto_DO_CONSTANT = False
    goto_CLOSE_IT = False
    goto_TERM_LIST = False
    goto_SCHEDULE_AT = False
    goto_SCHED_PRIO = False
    goto_SCHEDULE_EVERY = False
    goto_DEFAULT_SHAPER = False
    goto_DOT_PRODUCTS_LOOP = False
    goto_SIMPLE_SUBS = False
    
    # DO CASE PRODUCTION_NUMBER;
    if PRODUCTION_NUMBER == 0:  # reference 0
        pass
    elif PRODUCTION_NUMBER == 1:  # reference 10
        # <COMPILATION>::= <COMPILE LIST> _|_
        if g.MP > 0:
            ERROR(d.CLASS_P, 1);
            STACK_DUMP();
        elif g.BLOCK_MODE[0] == 0: 
            ERROR(d.CLASS_PP, 4);
        HALMAT_POP(XXREC, 0, 0, 1);
        g.ATOMp_FAULT = -1;
        HALMAT_OUT();
        FILE(LITFILE, CURLBLK, LIT1(0));
        g.COMPILING = 0x80;
        g.STMT_PTR = g.STMT_PTR - 1;
    elif PRODUCTION_NUMBER == 2:  # reference 20
        # <COMPILE LIST>::=<BLOCK DEFINITION>
        pass;
    elif PRODUCTION_NUMBER == 3:  # reference 30
        # <COMPILE LIST>::= <COMPILE LIST> <BLOCK DEFINITION>
        pass;
    elif PRODUCTION_NUMBER == 4:  # reference 40
        #  <ARITH EXP> ::= <TERM>
        pass;
    elif PRODUCTION_NUMBER == 5:  # reference 50
        #  <ARITH EXP> ::= + <TERM>
        # JUST ABSORB '+' SIGN, IE, RESET INDIRECT STACK
        g.PTR[g.MP] = g.PTR[g.SP] ;
        g.NOSPACE();
    elif PRODUCTION_NUMBER == 6:  # reference 60
        #  <ARITH EXP> ::= -1 <TERM>
        if ARITH_LITERAL(g.SP, 0):
            INLINE(0x58, 1, 0, g.DW_AD);  # L   1,DW_AD
            INLINE(0x97, 8, 0, 1, 0);  # XI  0(1),X'80'
            g.LOC_P[g.PTR[g.SP]] = SAVE_LITERAL(1, g.DW_AD);
        else:
            g.TEMP = g.PSEUDO_TYPE_P[g.PTR[g.SP]];
            HALMAT_TUPLE(g.XMNEG[g.TEMP - g.MAT_TYPE], 0, g.SP, 0, 0);
            SETUP_VAC(g.SP, g.TEMP, g.PSEUDO_LENGTH[g.PTR[g.SP]]);
        g.NOSPACE();
        g.PTR[g.MP] = g.PTR[g.SP];
    elif PRODUCTION_NUMBER == 7:  # reference 70
        #  <ARITH EXP> ::= <ARITH EXP> + <TERM>
        ADD_AND_SUBTRACT(0);
    elif PRODUCTION_NUMBER == 8:  # reference 80
        #  <ARITH EXP> ::= <ARITH EXP> -1 <TERM>
        ADD_AND_SUBTRACT(1);
    elif PRODUCTION_NUMBER == 9:  # reference 90
        #  <TERM> ::= <PRODUCT>
        pass;
    elif PRODUCTION_NUMBER == 10:  # reference 100
        #  <TERM> ::= <PRODUCT> / <TERM>
        al = ARITH_LITERAL(g.MP, g.SP)
        goto_DIV_FAIL = False
        if al:
            if MONITOR(9, 4):
                ERROR(d.CLASS_VA, 4);
                goto_DIV_FAIL = True;
            else:
                g.LOC_P[g.PTR[g.MP]] = SAVE_LITERAL(1, g.DW_AD);
                g.PSEUDO_TYPE_P[g.PTR[g.MP]] = g.SCALAR_TYPE;
        if goto_DIV_FAIL or not al:
            goto_DIV_FAIL = False
            if g.PSEUDO_TYPE_P[g.PTR[g.SP]] < g.SCALAR_TYPE:
                ERROR(d.CLASS_E, 1);
            g.PTR[0] = 0;
            g.PSEUDO_TYPE[0] = g.SCALAR_TYPE;
            MATCH_SIMPLES(0, g.SP);
            if g.PSEUDO_TYPE_P[g.PTR[g.MP]] >= g.SCALAR_TYPE: 
                MATCH_SIMPLES(0, g.MP);
            g.TEMP = g.PSEUDO_TYPE_P[g.PTR[g.MP]];
            HALMAT_TUPLE(g.XMSDV[g.TEMP - g.MAT_TYPE], 0, g.MP, g.SP, 0);
            SETUP_VAC(g.MP, g.TEMP);
        g.PTR_TOP = g.PTR[g.MP];
    
    # reference 110 is treated specially, since it has several GO TO's
    # to internal labels.
    while goto_COMBINE_SCALARS_AND_VECTORS or goto_CROSS_PRODUCTS or \
            goto_DOT_PRODUCTS_LOOP or \
            PRODUCTION_NUMBER == 11:  # reference 110
        #  <PRODUCT> ::= <FACTOR>
        if not (goto_COMBINE_SCALARS_AND_VECTORS or goto_CROSS_PRODUCTS or \
                goto_DOT_PRODUCTS_LOOP):
            PRODUCTION_NUMBER = -1
            g.CROSS_COUNT = 0
            g.DOT_COUNT = 0
            g.SCALAR_COUNT = 0
            g.VECTOR_COUNT = 0
            g.MATRIX_COUNT = 0;
            g.TERMP = g.SP + 1;
            while g.TERMP > 0:
                g.TERMP = g.TERMP - 1;
                if g.PARSE_STACK[g.TERMP] == g.CROSS_TOKEN:
                    g.CROSS_COUNT = g.CROSS_COUNT + 1;
                    g.FIXV[g.TERMP] = g.CROSS;
                elif g.PARSE_STACK[g.TERMP] == g.DOT_TOKEN:
                    g.DOT_COUNT = g.DOT_COUNT + 1;
                    g.FIXV[g.TERMP] = g.DOT;
                elif g.PARSE_STACK[g.TERMP] == g.FACTOR:
                    c = 0x0F & g.PSEUDO_TYPE_P[g.PTR[g.TERMP]]
                    # DO CASE 0x0F & PSEUDO_TYPE_P[PTR[TERMP]];
                    if c == 0:  # 0 IS DUMMY
                        pass
                    elif c == 1:  # 1 IS BIT
                        pass
                    elif c == 2:  # 2 IS CHAR
                        pass
                    elif c == 3:
                        g.MATRIX_COUNT = g.MATRIX_COUNT + 1;
                        g.FIXV[g.TERMP] = g.MAT_TYPE;
                    elif c == 4:
                        g.VECTOR_COUNT = g.VECTOR_COUNT + 1;
                        g.FIXV[g.TERMP] = g.VEC_TYPE;
                    elif c in (5, 6):  # TYPE 6 IS INTEGER
                        g.SCALAR_COUNT = g.SCALAR_COUNT + 1;
                        g.FIXV[g.TERMP] = g.SCALAR_TYPE;
                else:
                    g.MP = g.TERMP + 1;  # IT WAS DECREMENTED AT START OF LOOP
                    g.TERMP = 0;  # GET OUT OF LOOP
            g.TERMP = g.MP;
            
            if g.TERMP == g.SP: 
                return;
            
            #  MULTIPLY ALL SCALARS, PLACE RESULT AT SCALARP
            g.SCALARP = 0;
            g.PP = g.TERMP - 1;
            while g.SCALAR_COUNT > 0:
                g.PP = g.PP + 1;
                if g.FIXV[g.PP] == g.SCALAR_TYPE:
                    g.SCALAR_COUNT = g.SCALAR_COUNT - 1;
                    if g.SCALARP == 0: 
                        g.SCALARP = g.PP;
                    else:
                        MULTIPLY_SYNTHESIZE(g.SCALARP, g.PP, g.SCALARP, 0);
            
            # PRODUCTS WITHOUT VECTORS HANDLED HERE
            if g.VECTOR_COUNT == 0:
                if g.CROSS_COUNT + g.DOT_COUNT > 0:
                    ERROR(d.CLASS_E, 4);
                    g.PTR_TOP = g.PTR[g.MP];
                    return;
                if g.MATRIX_COUNT == 0:
                    g.PTR_TOP = g.PTR[g.MP];
                    return;
                #  MULTIPLY MATRIX PRODUCTS
                g.MATRIXP = 0;
                g.PP = g.TERMP - 1;
                while g.MATRIX_COUNT > 0:
                    g.PP = g.PP + 1;
                    if g.FIXV[g.PP] == g.MAT_TYPE:
                        g.MATRIX_COUNT = g.MATRIX_COUNT - 1;
                        if MATRIXP == 0: 
                            g.MATRIXP = g.PP;
                        else: 
                            MULTIPLY_SYNTHESIZE(MATRIXP, g.PP, MATRIXP, 8);
                if g.SCALARP != 0: 
                    MULTIPLY_SYNTHESIZE(MATRIXP, g.SCALARP, g.TERMP, 2);
                g.PTR_TOP = g.PTR[g.MP];
                return;
        
            # PRODUCTS WITH VECTORS TAKE UP THE REST OF THIS REDUCTION
            
            #  FIRST MATRICES ARE PULLED INTO VECTORS
            if g.MATRIX_COUNT == 0: 
                goto_MATRICES_TAKEN_CARE_OF = True
            else:
                g.BEGINP = g.TERMP;
                goto_MATRICES_MAY_GO_RIGHT = True
                while MATRICES_MAY_GO_RIGHT:
                    goto_MATRICES_MAY_GO_RIGHT = False
                    g.MATRIX_PASSED = 0;
                    for g.PP in range(BEGINP, g.SP + 1):
                        if g.FIXV[g.PP] == g.MAT_TYPE: 
                            g.MATRIX_PASSED = MATRIX_PASSED + 1; 
                        elif g.FIXV[g.PP] == g.DOT or g.FIXV[g.PP] == g.CROSS: 
                            g.MATRIX_PASSED = 0; 
                        elif g.FIXV[g.PP] == g.VEC_TYPE:
                            #  THIS ILLEGAL SYNTAX WILL BE CAUGHT ELSEWHERE
                            g.PPTEMP = g.PP;
                            while MATRIX_PASSED > 0:
                                PPTEMPg.TEMPPTEMP - 1;
                                if g.FIXV[PPTEMP] == g.MAT_TYPE:
                                    g.MATRIX_PASSED = MATRIX_PASSED - 1;
                                    MULTIPLY_SYNTHESIZE(PPTEMP, g.PP, g.PP, 7);
                            for PPTEMP in range(g.PP + 1, g.SP + 1):
                                if g.FIXV[PPTEMP] == g.MAT_TYPE:
                                    MULTIPLY_SYNTHESIZE(g.PP, PPTEMP, g.PP, 6); 
                                if g.FIXV[PPTEMP] == g.VEC_TYPE: 
                                    g.PP = PPTEMP;  
                                elif g.FIXV[PPTEMP] == g.DOT or g.FIXV[PPTEMP] == g.CROSS:
                                    g.BEGINP = PPTEMP + 1;
                                    goto_MATRICES_MAY_GO_RIGHT = True
                                    continue
        
        if not (goto_CROSS_PRODUCTS or goto_DOT_PRODUCTS_LOOP):
            goto_MATRICES_TAKEN_CARE_OF = False
            # PRODUCTS WITHOUT DOT OR CROSS COME NEXT
            if (g.DOT_COUNT + g.CROSS_COUNT) > 0: 
                goto_CROSS_PRODUCTS = True
                continue
            else:
                if g.VECTOR_COUNT > 2:
                    ERROR(d.CLASS_EO, 1);
                    g.PTR_TOP = g.PTR[g.MP];
                    return;
                for g.PP in range(g.MP, g.SP + 1):
                   if g.FIXV[g.PP] == g.VEC_TYPE:
                        g.VECTORP = g.PP;
                        g.PP = g.SP + 1;
                goto_COMBINE_SCALARS_AND_VECTORS = False
                if g.SCALARP != 0:
                    MULTIPLY_SYNTHESIZE(g.VECTORP, g.SCALARP, g.TERMP, 1);  
                elif g.VECTORP != g.MP:
                    #   THIS BLOCK OF CODE PUTS THE INDIRECT STACK INFORMATION FOR THE
                    #   ENTIRE PRODUCT IN THE FIRST OF THE INDIRECT STACK ENTRIES ALOTTED
                    #   TO THE ENTIRE PRODUCT, IN CASE THE FINAL MULTIPLY DOESN'T DO SO
                    g.PTR_TOP = g.PTR[g.MP];
                    g.INX[g.PTR_TOP] = g.INX[g.PTR[g.VECTORP]];
                    g.LOC_P[g.PTR_TOP] = g.LOC_P[g.PTR[g.VECTORP]];
                    g.VAL_P[g.PTR_TOP] = g.VAL_P[g.PTR[g.VECTORP]];
                    g.PSEUDO_TYPE_P[g.PTR_TOP] = g.PSEUDO_TYPE_P[g.PTR[g.VECTORP]];
                    g.PSEUDO_FORM[g.PTR_TOP] = g.PSEUDO_FORM[g.PTR[g.VECTORP]];
                    g.PSEUDO_LENGTH[g.PTR_TOP] = g.PSEUDO_LENGTH[g.PTR[g.VECTORP]];
                if g.VECTOR_COUNT == 1:
                    g.PTR_TOP = g.PTR[g.MP];
                    return;
                #  VECTOR_COUNT SHOULD BE 2 HERE
                for g.PP in range(g.VECTORP + 1, g.SP + 1):
                    if g.FIXV[g.PP] == g.VEC_TYPE:
                        MULTIPLY_SYNTHESIZE(g.TERMP, g.PP, g.TERMP, 5);
                        g.PTR_TOP = g.PTR[g.MP];
                        return;
        
        if not goto_DOT_PRODUCTS_LOOP:
            goto_CROSS_PRODUCTS = False
            while g.CROSS_COUNT > 0:
                g.VECTORP = 0;
                for g.PP in range(g.MP, 1 + g.SP):
                    if g.FIXV[g.PP] == g.VEC_TYPE: 
                        g.VECTORP = g.PP;
                    elif g.FIXV[g.PP] == g.DOT: 
                        g.VECTORP = 0;
                    elif g.FIXV[g.PP] == g.CROSS:
                        if g.VECTORP == 0:
                            ERROR(d.CLASS_EC, 3);
                            g.PTR_TOP = g.PTR[g.MP];
                            return;
                        else:
                            for PPTEMP in range(g.PP + 1, 1 + g.SP):
                                if g.FIXV[PPTEMP] == g.VEC_TYPE:
                                    MULTIPLY_SYNTHESIZE(g.VECTORP, PPTEMP, g.VECTORP, 4);
                                    g.FIXV[g.PP] = 0;
                                    g.CROSS_COUNT = g.CROSS_COUNT - 1;
                                    g.FIXV[PPTEMP] = 0;
                                    g.VECTOR_COUNT = g.VECTOR_COUNT - 1;
                                    goto_CROSS_PRODUCTS = True;
                                    break
                            if goto_CROSS_PRODUCTS:
                                break
                        ERROR(d.CLASS_EC, 2);
                        g.PTR_TOP = g.PTR[g.MP];
                        return;
                if goto_CROSS_PRODUCTS:
                    break;
            if goto_CROSS_PRODUCTS:
                continue
            
            if g.DOT_COUNT > 0: 
                # GO TO DOT_PRODUCTS;
                # Fortunately, we need no goto_XXXX; it can just fall through.
                pass
            else:
                if g.VECTOR_COUNT > 1:
                    ERROR(d.CLASS_EO, 2);
                    g.PTR_TOP = g.PTR[g.MP];
                    return;
                # IF YOU GET TO THIS GOTO, VECTOR_COUNT HAD BETTER BE 1
                goto_COMBINE_SCALARS_AND_VECTORS = True
                continue
            
            # DOT_PRODUCTS:
            g.BEGINP = g.TERMP;
        goto_DOT_PRODUCTS_LOOP = False
        while g.DOT_COUNT > 0:
            g.VECTORP = 0;
            for g.PP in range(BEGINP, 1 + g.SP):
                if g.FIXV[g.PP] == g.VEC_TYPE: 
                    g.VECTORP = g.PP;
                if g.FIXV[g.PP] == g.DOT:
                    if g.VECTORP == 0:
                        ERROR(d.CLASS_ED, 2);
                        g.PTR_TOP = g.PTR[g.MP];
                        return;
                    else:
                        for PPTEMP in range(g.PP + 1, 1 + g.SP):
                            if g.FIXV[PPTEMP] == g.VEC_TYPE:
                                MULTIPLY_SYNTHESIZE(g.VECTORP, PPTEMP, g.VECTORP, 3);
                                if g.SCALARP == 0: 
                                    g.SCALARP = g.VECTORP; 
                                else:
                                    MULTIPLY_SYNTHESIZE(g.SCALARP, g.VECTORP, g.SCALARP, 0);
                                g.BEGINP = PPTEMP + 1;
                                g.DOT_COUNT = g.DOT_COUNT - 1;
                                g.FIXV[g.VECTORP] = 0;
                                g.FIXV[PPTEMP] = 0;
                                g.VECTOR_COUNT = g.VECTOR_COUNT - 2;
                                goto_DOT_PRODUCTS_LOOP = True
                                break
                        if goto_DOT_PRODUCTS_LOOP:
                            break
                    ERROR(d.CLASS_ED, 1);
                    g.PTR_TOP = g.PTR[g.MP];
                    return;
            if goto_DOT_PRODUCTS_LOOP:
                break
        if goto_DOT_PRODUCTS_LOOP:
            continue
        if g.VECTOR_COUNT > 0:
            ERROR(d.CLASS_EO, 3);
            g.PTR_TOP = g.PTR[g.MP];
            return;
        # VECTOR_COUNT MUST BE 0 HERE
        if g.SCALARP == g.MP:
            g.PTR_TOP = g.PTR[g.MP];
            return;
        #   KLUDGE TO USE CODE IN ANOTHER SECTION OF THIS CASE
        g.VECTORP = g.SCALARP;
        g.VECTOR_COUNT = 1;
        g.SCALARP = 0;
        goto_COMBINE_SCALARS_AND_VECTORS = True
        continue
        
    if PRODUCTION_NUMBER == 12:  # reference 120
        #  <PRODUCT> ::= <FACTOR> * <PRODUCT>
        pass
    elif PRODUCTION_NUMBER == 13:  # reference 130
        #  <PRODUCT> ::= <FACTOR> . <PRODUCT>
        pass
    elif PRODUCTION_NUMBER == 14:  # reference 140
        #  <PRODUCT> ::= <FACTOR> <PRODUCT>
        pass
    elif PRODUCTION_NUMBER == 15:  # reference 150
        # <FACTOR> ::= <PRIMARY>
        if g.PARSE_STACK[g.MP - 1] != g.EXPONENT: 
            if g.FIXF[g.MP] > 0:
                SET_XREF_RORS(g.MP);
    elif PRODUCTION_NUMBER == 16:  # reference 160
        #  <FACTOR>  ::=  <PRIMARY>  <**>  <FACTOR>
        g.I = g.PTR[g.SP];
        if g.FIXF[g.MP] > 0: 
            SET_XREF_RORS(g.MP);
        g.EXPONENT_LEVEL = g.EXPONENT_LEVEL - 1;
        g.TEMP = g.PSEUDO_TYPE_P[g.PTR[g.MP]];
        # DO CASE TEMP-MAT_TYPE;
        goto_T_FOUND = False
        tmt = g.TEMP - g.MAT_TYPE
        if tmt == 0:
            #  MATRIX
            g.TEMP2 = g.PSEUDO_LENGTH[g.PTR[g.MP]];
            if (g.PSEUDO_FORM[I] == XSYT)or(g.PSEUDO_FORM[I] == XXPT):
                if g.VAR[g.SP] == 'T': 
                    HALMAT_TUPLE(XMTRA, 0, g.MP, 0, 0);
                    SETUP_VAC(g.MP, g.TEMP, SHL(TEMP2, 8) | SHR(TEMP2, 8));
                    if IMPLICIT_T:
                        g.SYT_FLAGS(g.LOC_P[I], g.SYT_FLAGS(g.LOC_P[I]) | IMPL_T_FLAG);
                        g.IMPLICIT_T = g.FALSE;
                    goto_T_FOUND = True;
            if not goto_T_FOUND:
                if g.PSEUDO_TYPE_P[I] != INT_TYPE | g.PSEUDO_FORM[I] != XLIT:
                    ERROR(d.CLASS_E, 2);
                if (TEMP2 & 0xFF) != SHR(TEMP2, 8): 
                    ERROR(d.CLASS_EM, 4);
                HALMAT_TUPLE(XMINV, 0, g.MP, g.SP, 0);
                SETUP_VAC(g.MP, g.TEMP);
        elif tmt == 1:
            #  VECTOR
            ERROR(d.CLASS_EV, 4);
            g.TEMP2 = XSEXP;
            # Rather than implement the GO TO FINISH_EXP, I've just duplicated
            # the code that's at FINISH_EXP.
            # GO TO FINISH_EXP;
            HALMAT_TUPLE(TEMP2, 0, g.MP, g.SP, 0);
            SETUP_VAC(g.MP, g.PSEUDO_TYPE_P[g.PTR[g.MP]]);
        elif tmt in (2, 3):
            #  2 - SCALAR
            #  3 - INTEGER
            # SIMPLE_EXP:
            goto_POWER_FAIL = False
            al = ARITH_LITERAL(g.MP, g.SP, g.TRUE)
            if al:
                if MONITOR(9, 5):
                    ERROR(d.CLASS_VA, 5);
                    goto_POWER_FAIL = True
                else:
                    g.LOC_P[g.PTR[g.MP]] = SAVE_LITERAL(1, g.DW_AD);
                    g.TEMP = LIT_RESULT_TYPE(g.MP, g.SP);
                    if g.TEMP == INT_TYPE: 
                        if MAKE_FIXED_LIT(g.LOC_P[I]) < 0:
                            g.TEMP = g.SCALAR_TYPE;
                    g.PSEUDO_TYPE_P[g.PTR[g.MP]] = g.TEMP;
            if goto_POWER_FAIL or not al:  # was else: 
                goto_POWER_FAIL = False
                g.TEMP2 = XSPEX(g.TEMP - g.SCALAR_TYPE);
                if g.PSEUDO_TYPE_P[I] < g.SCALAR_TYPE: 
                    ERROR(d.CLASS_E, 3);
                goto_REGULAR_EXP = False
                firstTry = True
                while firstTry or goto_REGULAR_EXP:
                    firstTry = False
                    if g.PSEUDO_TYPE_P[I] != INT_TYPE or goto_REGULAR_EXP:
                        if not goto_REGULAR_EXP:
                            g.TEMP2 = XSEXP;
                        goto_REGULAR_EXP = False
                        g.PTR = 0;
                        g.PSEUDO_TYPE = g.SCALAR_TYPE;
                        MATCH_SIMPLES(g.MP, 0);
                    elif g.PSEUDO_FORM[I] != XLIT:
                       g.TEMP2 = XSIEX;
                       goto_REGULAR_EXP = True
                       continue
                    else:
                       g.TEMP = MAKE_FIXED_LIT(g.LOC_P[I]);
                       if g.TEMP < 0: 
                           g.TEMP2 = XSIEX;
                           goto_REGULAR_EXP = True
                           continue
                # FINISH_EXP:
                HALMAT_TUPLE(TEMP2, 0, g.MP, g.SP, 0);
                SETUP_VAC(g.MP, g.PSEUDO_TYPE_P[g.PTR[g.MP]]);
        # End of CASE TEMP-MAT_TYPE
        if not goto_T_FOUND:
            if g.FIXF[g.SP] > 0: 
                SET_XREF_RORS(g.SP);
        goto_T_FOUND = False
        g.PTR_TOP = g.PTR[g.MP];
    elif PRODUCTION_NUMBER == 17:  # reference 170
        #  <**>  ::=  **
        g.EXPONENT_LEVEL = g.EXPONENT_LEVEL + 1;
    elif PRODUCTION_NUMBER == 18:  # reference 180
        #  <PRE PRIMARY>  ::=  (  <ARITH EXP>  )
        g.VAR[g.MP] = g.VAR[g.MPP1];
        g.PTR[g.MP] = g.PTR[g.MPP1];
    # reference 190 has been relocated.
    elif PRODUCTION_NUMBER == 20:  # reference 200
        #  <PRE PRIMARY> ::= <COMPOUND NUMBER>
        g.TEMP = g.SCALAR_TYPE;
        goto_ARITH_LITS = True
    elif PRODUCTION_NUMBER == 21:  # reference 210
        #  <ARITH FUNC HEAD>  ::=  <ARITH FUNC>
        START_NORMAL_FCN;
    elif PRODUCTION_NUMBER == 22:  # reference 220
        #  <ARITH FUNC HEAD>  ::=  <ARITH CONV> <SUBSCRIPT>
        g.NOSPACE();
        g.TEMP, NEXT_SUB = g.PTR[g.SP];
        g.PTR_TOP, g.PTR[g.MP] = g.TEMP;
        if g.INX[g.TEMP] == 0: 
            goto_DEFAULT_SHAPER = True
        else:
            if (g.PSEUDO_LENGTH[g.TEMP] >= 0) or (g.VAL_P[g.TEMP] >= 0): 
                ERROR(d.CLASS_QS, 1);
            # DO CASE FIXL[MP];
            fm = g.FIXL[g.MP]
            if fm == 0:
                #  MATRIX
                if g.INX[g.TEMP] != 2: 
                    ERROR(d.CLASS_QS, 2);
                    goto_DEFAULT_SHAPER = True
                else:
                    g.TEMP_SYN = ARITH_SHAPER_SUB(MAT_DIM_LIM);
                    g.TEMP1 = ARITH_SHAPER_SUB(MAT_DIM_LIM);
                    g.PSEUDO_LENGTH[g.TEMP] = SHL(TEMP_SYN, 8) | TEMP1;
                    g.INX[g.TEMP] = TEMP_SYN * TEMP1;
            elif fm == 1:
                #  VECTOR
                if g.INX[g.TEMP] != 1: 
                    ERROR(d.CLASS_QS, 3);
                    goto_DEFAULT_SHAPER = True
                else:
                    g.TEMP_SYN = ARITH_SHAPER_SUB(VEC_LENGTH_LIM);
                    g.PSEUDO_LENGTH[g.TEMP], g.INX[g.TEMP] = TEMP_SYN;
            elif fm in (2, 3):
                #  2 - SCALAR
                #  3 - INTEGER
                # SCALAR_SHAPER:
                if (g.INX[g.TEMP] < 1) or (g.INX[g.TEMP] > N_DIM_LIM):
                    ERROR(d.CLASS_QS, 4);
                    goto_DEFAULT_SHAPER = True
                else:
                    g.TEMP_SYN = 1;
                    for TEMP1 in range(1, 1 + g.INX[g.TEMP]):
                        g.PTR_TOP = g.PTR_TOP + 1;  # OLD STACKS BEING REINSTATED
                        g.LOC_P[g.PTR_TOP] = ARITH_SHAPER_SUB(ARRAY_DIM_LIM);
                        g.TEMP_SYN = g.LOC_P[g.PTR_TOP] * TEMP_SYN;
                    # IF THE TOTAL NUMBER OF ELEMENTS BEING CREATED
                    # WITH A SHAPING FUNCTION IS GREATER THAN 32767
                    # OR LESS THAN 1 THEN GENERATE A QS8 ERROR
                    if (TEMP_SYN > ARRAY_DIM_LIM) or (TEMP_SYN < 1):  # ""
                        ERROR(d.CLASS_QS, 8);
                    g.PSEUDO_LENGTH[g.TEMP] = TEMP_SYN;
        if goto_DEFAULT_SHAPER:
            goto_DEFAULT_SHAPER = False
            # DO CASE FIXL[MP];
            fm = g.FIXL[g.MP]
            if fm == 0:
                #  MATRIX
                g.PSEUDO_LENGTH[g.PTR_TOP] = DEF_MAT_LENGTH;
                g.TEMP = DEF_MAT_LENGTH & 0xFF;
                g.INX[g.PTR_TOP] = g.TEMP * g.TEMP;
            elif fm == 1:
                #  VECTOR
                g.PSEUDO_LENGTH[g.PTR_TOP], g.INX[g.PTR_TOP] = DEF_VEC_LENGTH;
            elif fm == 2:
                #  SCALAR
                g.INX[g.PTR_TOP] = 0;
            elif fm == 3:
                #  INTEGER
                g.INX[g.PTR_TOP] = 0;
        # SET_ARITH_SHAPERS:
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = g.FIXL[g.MP] + g.MAT_TYPE;
        if PUSH_FCN_STACK(2): 
            g.FCN_LOC[g.FCN_LV] = g.FIXL[g.MP];
            SAVE_ARRAYNESS();
            HALMAT_POP(XSFST, 0, XCO_N, g.FCN_LV);
            g.VAL_P[g.PTR_TOP] = LAST_POPp;
    elif PRODUCTION_NUMBER == 23:  # reference 230
        #  <ARITH CONV>  ::=  INTEGER
        g.FIXL[g.MP] = 3;
        SET_BI_XREF(INT_NDX);
    elif PRODUCTION_NUMBER == 24:  # reference 240
        #  <ARITH CONV>  ::=  SCALAR
        g.FIXL[g.MP] = 2;
        SET_BI_XREF(SCLR_NDX);
    elif PRODUCTION_NUMBER == 25:  # reference 250
        #  <ARITH CONV>  ::=  VECTOR
        g.FIXL[g.MP] = 1;
        SET_BI_XREF(VEC_NDX);
    elif PRODUCTION_NUMBER == 26:  # reference 260
        #  <ARITH CONV>  ::=  MATRIX
        g.FIXL[g.MP] = 0;
        SET_BI_XREF(MTX_NDX);
    elif PRODUCTION_NUMBER == 27:  # reference 270
        #  <PRIMARY> ::= <ARITH VAR>
        pass;
    elif PRODUCTION_NUMBER == 28:  # reference 280
        # <PRE PRIMARY>  ::=  <ARITH FUNC HEAD> ( <CALL LIST> )
        END_ANY_FCN();
    elif PRODUCTION_NUMBER == 29:  # reference 290
        #  <PRIMARY>  ::=  <MODIFIED ARITH FUNC>
        SETUP_NO_ARG_FCN(TEMP_SYN);
    # reference 300 has been relocated.
    elif PRODUCTION_NUMBER == 31:  # reference 310
        #  <PRIMARY> ::= <PRE PRIMARY>
        g.FIXF[g.MP] = 0;
    elif PRODUCTION_NUMBER == 32:  # reference 320
        #  <PRIMARY> ::= <PRE PRIMARY> <QUALIFIER>
        PREC_SCALE(g.SP, g.PSEUDO_TYPE_P[g.PTR[g.MP]]);
        g.PTR_TOP = g.PTR[g.MP];
        g.FIXF[g.MP] = 0;
    elif PRODUCTION_NUMBER == 33:  # reference 330
        #  <OTHER STATEMENT>  ::=  <ON PHRASE> <STATEMENT>
        HALMAT_POP(XLBL, 1, XCO_N, 0);
        HALMAT_PIP(g.FIXL[g.MP], XINL, 0, 0);
        g.INDENT_LEVEL = g.INDENT_LEVEL - g.INDENT_INCR;
        UNBRANCHABLE(g.SP, 7);
        g.FIXF[g.MP] = 0;
    elif PRODUCTION_NUMBER == 34:  # reference 340
        #  <OTHER STATEMENT> ::= <IF STATEMENT>
        g.FIXF[g.MP] = 0;
    # reference 350 has been relocated.
    elif PRODUCTION_NUMBER == 36:  # reference 360
        #  <STATEMENT> ::= <BASIC STATEMENT>
        CHECK_IMPLICIT_T();
        OUTPUT_WRITER(g.LAST_WRITE, STMT_END_PTR);
        # ONLY SET LAST_WRITE TO 0 WHEN STATEMENT STACK
        # COMPLETELY PRINTED.
        if STMT_END_PTR > -1:
            g.LAST_WRITE = STMT_END_PTR + 1;
        else:
            g.LAST_WRITE = 0;
        EMIT_SMRK();
    elif PRODUCTION_NUMBER == 37:  # reference 370
        #  <STATEMENT>  ::=  <OTHER STATEMENT>
        pass;
    elif PRODUCTION_NUMBER == 38:  # reference 380
        #  <ANY STATEMENT>  ::= <STATEMENT>
        g.PTR[g.MP] = 1;
    elif PRODUCTION_NUMBER == 39:  # reference 390
        # <ANY STATEMENT>::= <BLOCK DEFINITION>
        g.PTR[g.MP] = g.BLOCK_MODE[g.NEST + 1] = UPDATE_MODE;  # WHAT BLOCK WAS
    elif PRODUCTION_NUMBER == 40:  # reference 400
        #  <BASIC STATEMENT>  ::= <LABEL DEFINITION> <BASIC STATEMENT>
        goto_LABEL_INCORP = True
    elif PRODUCTION_NUMBER == 41:  # reference 410
        # <BASIC STATEMENT>::=<ASSIGNMENT>
        g.XSET(0x4);
        g.PTR_TOP = g.PTR_TOP - g.INX[g.PTR[g.MP]];
        if NAME_PSEUDOS: NAME_ARRAYNESS(g.MP);
        HALMAT_FIX_PIPp(LAST_POPp, g.INX[g.PTR[g.MP]]);
        EMIT_ARRAYNESS();
        goto_FIX_NOLAB = True
    # reference 420 has been relocated.
    elif PRODUCTION_NUMBER == 43:  # reference 430
        #  <BASIC STATEMENT>  ::=  EXIT  <LABEL>  ;
        SET_XREF(g.FIXL[g.MPP1], XREF_REF);
        goto_EXITTING = True
    # reference 440 has been relocated.
    elif PRODUCTION_NUMBER == 45:  # reference 450
        #  <BASIC STATEMENT>  ::=  REPEAT  <LABEL>  ;
        SET_XREF(g.FIXL[g.MPP1], XREF_REF);
        goto_REPEATING = True
    elif PRODUCTION_NUMBER == 46:  # reference 460
        #  <BASIC STATEMENT>  ::=  GO TO  <LABEL>  ;
        g.I = g.FIXL[g.MP + 2];
        SET_XREF(I, XREF_REF);
        if g.SYT_LINK1(I) < 0: 
            if g.DO_LEVEL < (-g.SYT_LINK1(I)): 
                ERROR(d.CLASS_GL, 3);
        elif g.SYT_LINK1(I) == 0: 
            g.SYT_LINK1(I, g.STMT_NUM());
        g.XSET(0x1001);
        if VAR_LENGTH(I) > 3: 
            ERROR(d.CLASS_GL, VAR_LENGTH(I));
        elif VAR_LENGTH(I) == 0: 
            g.VAR_LENGTH(I, 3);
        HALMAT_POP(XBRA, 1, 0, 0);
        HALMAT_PIP(I, XSYT, 0, 0);
        goto_FIX_NOLAB = True
    # reference 470 has been relocated.
    elif PRODUCTION_NUMBER == 48:  # reference 480
        # <BASIC STATEMENT>::= <CALL KEY> ;
        END_ANY_FCN();
    elif PRODUCTION_NUMBER == 49:  # reference 490
        # <BASIC STATEMENT>::= <CALL KEY> (<CALL LIST>) ;
        END_ANY_FCN();
    elif PRODUCTION_NUMBER == 50:  # reference 500
        # <BASIC STATEMENT>::=<CALL KEY><ASSIGN>(<CALL ASSIGN LIST>);
        END_ANY_FCN();
    elif PRODUCTION_NUMBER == 51:  # reference 510
        # <BASIC STATEMENT>::=<CALL KEY>(<CALL LIST>)<ASSIGN>(<CALL ASSIGN LIST>);
        END_ANY_FCN();
    elif PRODUCTION_NUMBER == 52:  # reference 520
        # <BASIC STATEMENT>::= RETURN ;
        if SYT_CLASS(g.BLOCK_SYTREF[g.NEST]) == FUNC_CLASS: 
            ERROR(d.CLASS_PF, 1);
        elif g.BLOCK_MODE[g.NEST] == UPDATE_MODE: 
            ERROR(d.CLASS_UP, 2);
        HALMAT_POP(XRTRN, 0, 0, 0);
        g.XSET(0x7);
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 53:  # reference 530
        # <BASIC STATEMENT>::= RETURN <EXPRESSION> ;
        g.XSET(0x7);
        g.TEMP = 0;
        if KILL_NAME(g.MPP1): 
            ERROR(d.CLASS_PF, 9);
        if CHECK_ARRAYNESS: 
            ERROR(d.CLASS_PF, 3);
        if g.BLOCK_MODE[g.NEST] == UPDATE_MODE: 
            ERROR(d.CLASS_UP, 2);
        elif SYT_CLASS(g.BLOCK_SYTREF[g.NEST]) != FUNC_CLASS:
            ERROR(d.CLASS_PF, 2);
        else:
            g.PTR = 0;
            g.LOC_P = g.BLOCK_SYTREF[g.NEST];
            g.PSEUDO_LENGTH[0] = VAR_LENGTH(LOC_P);
            g.TEMP = g.SYT_TYPE(g.BLOCK_SYTREF[g.NEST]);
            if (SHL(1, g.PSEUDO_TYPE_P[g.PTR[g.MPP1]]) & ASSIGN_TYPE(g.TEMP)) == 0:
                ERROR(d.CLASS_PF, 4);
        # DO CASE TEMP;
        if g.TEMP in (0, 1, 2):
            pass
        elif g.TEMP == 3:
            MATRIX_COMPARE(0, g.MPP1, d.CLASS_PF, 5);
        elif g.TEMP == 4:
            VECTOR_COMPARE(0, g.MPP1, d.CLASS_PF, 6);
        elif g.TEMP in (5, 6, 7, 8, 9):
            pass
        elif g.TEMP == 10:
            STRUCTURE_COMPARE(VAR_LENGTH(LOC_P), g.FIXL[g.MPP1], d.CLASS_PF, 7);
        elif g.TEMP == 11:
            pass;
        HALMAT_TUPLE(XRTRN, 0, g.MPP1, 0, 0);
        HALMAT_FIX_PIPTAGS(NEXT_ATOMp - 1, g.PSEUDO_TYPE_P[g.PTR[g.MPP1]], 0);
        g.PTR_TOP = g.PTR[g.MPP1] - 1;
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 54:  # reference 540
        # <BASIC STATEMENT>::= <DO GROUP HEAD> <ENDING> ;
        g.XSET(0x8);
        g.INDENT_LEVEL = g.INDENT_LEVEL - g.INDENT_INCR;
        g.NEST_LEVEL = NEST_LEVEL - 1;
        # DO CASE DO_INX[DO_LEVEL]&0x7F;
        didl = g.DO_INX[g.DO_LEVEL] & 0x7F
        if didl == 0:
            # SIMPLE DO
            g.TEMP = XESMP;
        elif didl == 1:
            # DO FOR
            g.TEMP = XEFOR;
        elif didl == 2:
            # DO CASE
            HALMAT_FIX_POPTAG(g.FIXV[g.MP], 1);
            g.TEMP = XECAS;
            g.INFORMATION = '';
            g.CASE_LEVEL = CASE_LEVEL - 1;
        elif didl == 3:
            # DO WHILE
            g.TEMP = XETST;
        # End of CASE DO_INX...
        HALMAT_POP(g.TEMP, 1, 0, 0);
        HALMAT_PIP(g.DO_LOC[g.DO_LEVEL], XINL, 0, 0);
        g.I = 0;
        while g.SYT_LINK2(I) > 0:
            g.J = g.SYT_LINK2(I);
            if g.SYT_LINK1(J) < 0: 
                if g.DO_LEVEL == (-g.SYT_LINK1(J)): 
                    g.SYT_LINK1(J, -(DO_LEVEL_LIM + 1));
                    g.SYT_LINK2(I, g.SYT_LINK2(J));
            g.I = J;
        if g.DO_LOC[0] == 0: 
            g.I = g.DO_CHAIN[g.DO_LEVEL];
            while I > 0:
                g.CLOSE_BCD = SYT_NAME(I);
                DISCONNECT(I);
                g.I = g.SYT_LINK1(I);
            g.DO_LEVEL = g.DO_LEVEL - 1;
        else:
            g.DO_LOC[0] = g.DO_LOC[0] - 1;
        goto_FIX_NOLAB = True
    # reference 550 has been relocated.
    elif PRODUCTION_NUMBER == 56:  # reference 560
        # <BASIC STATEMENT>::= <READ PHRASE> ;
        goto_IO_EMIT = True
    elif PRODUCTION_NUMBER == 57:  # reference 570
        # <BASIC STATEMENT>::= <WRITE KEY> ;
        goto_IO_EMIT = True
    elif PRODUCTION_NUMBER == 58:  # reference 580
    # <BASIC STATEMENT>::= <WRITE PHRASE> ;
        goto_IO_EMIT = True
    elif PRODUCTION_NUMBER == 59:  # reference 590
        # <BASIC STATEMENT>::= <FILE EXP> = <EXPRESSION> ;
        HALMAT_TUPLE(XFILE, 0, g.MP, g.SP - 1, g.FIXV[g.MP]);
        HALMAT_FIX_PIPTAGS(NEXT_ATOMp - 1, g.PSEUDO_TYPE_P[g.PTR[g.SP - 1]], 1);
        if KILL_NAME(g.SP - 1): 
            ERROR(d.CLASS_T, 5);
        EMIT_ARRAYNESS();
        g.PTR_TOP = g.PTR[g.MP] - 1;
        g.XSET(0x800);
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 60:  # reference 600
        # <BASIC STATEMENT>::= <VARIABLE> = <FILE EXP> ;
        HALMAT_TUPLE(XFILE, 0, g.SP - 1, g.MP, g.FIXV[g.SP - 1]);
        l.H1 = g.VAL_P[g.PTR[g.MP]];
        if SHR(l.H1, 7): 
            ERROR(d.CLASS_T, 4);
        if SHR(l.H1, 4): 
            ERROR(d.CLASS_T, 7);
        if (l.H1 & 0x6) == 0x2: 
            ERROR(d.CLASS_T, 8);
        HALMAT_FIX_PIPTAGS(NEXT_ATOMp - 1, g.PSEUDO_TYPE_P[g.PTR[g.MP]], 0);
        if KILL_NAME(g.MP): 
            ERROR(d.CLASS_T, 5);
        CHECK_ARRAYNESS();  # DR 173
        g.PTR_TOP = g.PTR[g.MP] - 1;
        goto_FIX_NOLAB = True
    # reference 610 has been relocated.
    # reference 620 has been relocated.
    elif PRODUCTION_NUMBER == 63:  # reference 630
        #  <BASIC STATEMENT> ::=  <WAIT KEY> UNTIL <ARITH EXP> ;
        g.TEMP = 2;
        if UNARRAYED_SCALAR(g.SP - 1): 
            ERROR(d.CLASS_RT, 6, 'WAIT UNTIL');
        goto_WAIT_TIME = True;
    elif PRODUCTION_NUMBER == 64:  # reference 640
        # <BASIC STATEMENT>::= <WAIT KEY> FOR <BIT EXP> ;
        g.TEMP = 3;
        if CHECK_EVENT_EXP(g.SP - 1): ERROR(d.CLASS_RT, 6, 'WAIT FOR');
        goto_WAIT_TIME = True
    elif PRODUCTION_NUMBER == 65:  # reference 650
        # <BASIC STATEMENT>::= <TERMINATOR> ;
        g.XSET(0xA);
        HALMAT_POP(g.FIXL[g.MP], 0, 0, 0);
        goto_UPDATE_CHECK = True
    elif PRODUCTION_NUMBER == 66:  # reference 660
        # <BASIC STATEMENT>::= <TERMINATOR> <TERMINATE LIST>;
        g.XSET(0xA);
        HALMAT_POP(g.FIXL[g.MP], g.EXT_P[g.PTR[g.MPP1]], 0, 1);
        for l.H1 in range(g.PTR[g.MPP1], 1 + g.EXT_P[g.PTR[g.MPP1]] + g.PTR[g.MPP1] - 1):
            HALMAT_PIP(g.LOC_P[l.H1], g.PSEUDO_FORM[l.H1], 0, 0);
        g.PTR_TOP = g.PTR[g.MPP1] - 1;
        goto_UPDATE_CHECK = True
    # "reference 670" has been relocated.
    elif PRODUCTION_NUMBER == 68:  # reference 680
        #  <BASIC STATEMENT>  ::=  UPDATE PRIORITY  <LABEL VAR>  TO  <ARITH EXP>;
        SET_XREF_RORS(g.MP + 2, 0xC000);
        PROCESS_CHECK(g.MP + 2);
        g.TEMP = g.MP + 2;
        g.PTR_TOP = g.PTR[g.TEMP] - 1;
        goto_UP_PRIO = True
    # reference 690 has been relocated.
    elif PRODUCTION_NUMBER == 70:  # reference 700
        # <BASIC STATEMENT>::=<SCHEDULE PHRASE><SCHEDULE CONTROL>;
        goto_SCHEDULE_EMIT = True;
    elif PRODUCTION_NUMBER == 71:  # reference 710
        #  <BASIC  STATEMENT>  ::=  <SIGNAL CLAUSE>  ;
        g.XSET(0xD);
        HALMAT_TUPLE(XSGNL, 0, g.MP, 0, g.INX[g.PTR[g.MP]]);
        g.PTR_TOP = g.PTR[g.MP] - 1;
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 72:  # reference 720
        #  <BASIC STATEMENT>  ::=  SEND ERROR <SUBSCRIPT>  ;
        ERROR_SUB(2);
        HALMAT_TUPLE(XERSE, 0, g.MP + 2, 0, 0, g.FIXV[g.MP] & 0x3F);
        SET_OUTER_REF(g.FIXV[g.MP], 0x0000);
        g.PTR_TOP = g.PTR[g.MP + 2] - 1;
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 73:  # reference 730
        #  <BASIC STATEMENT>  ::=  <ON CLAUSE>  ;
        HALMAT_TUPLE(XERON, 0, g.MP, 0, g.FIXL[g.MP], g.FIXV[g.MP] & 0x3F);
        g.PTR_TOP = g.PTR[g.MP] - 1;
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 74:  # reference 740
        #  <BASIC STATEMENT>  ::=  <ON CLAUSE> AND <SIGNAL CLAUSE> ;
        HALMAT_TUPLE(XERON, 0, g.MP, g.MP + 2, g.FIXL[g.MP], g.FIXV[g.MP] & 0x3F, 0, 0, g.INX[g.PTR[g.MP + 2]]);
        g.PTR_TOP = g.PTR[g.MP] - 1;
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 75:  # reference 750
        #  <BASIC STATEMENT>  ::=  OFF ERROR <SUBSCRIPT>  ;
        ERROR_SUB(0);
        HALMAT_TUPLE(XERON, 0, g.MP + 2, 0, 3, g.FIXV[g.MP] & 0x3F);
        g.PTR_TOP = g.PTR[g.MP + 2] - 1;
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 76:  # reference 760
        #  <BASIC STATEMENT>  ::=  <% MACRO NAME> ;
        HALMAT_POP(XPMHD, 0, 0, g.FIXL[g.MP]);
        HALMAT_POP(XPMIN, 0, 0, g.FIXL[g.MP]);
        XSET (PC_STMT_TYPE_BASE + g.FIXL[g.MP]);
        if PCARGp(g.FIXL[g.MP]) != 0:
            if ALT_PCARGp(g.FIXL[g.MP]) != 0:
                ERROR(d.CLASS_XM, 2, g.VAR[g.MP]);
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 77:  # reference 770
        #  <BASIC STATEMENT>  ::=  <% MACRO HEAD> <% MACRO ARG> ) ;
        if PCARGp != 0:
            if ALT_PCARGp != 0:
                ERROR(d.CLASS_XM, 2, g.VAR[g.MP]);
        HALMAT_TUPLE(XPMAR, 0, g.MPP1, 0, 0, g.PSEUDO_TYPE_P[g.PTR[g.MPP1]]);
        g.PTR_TOP = g.PTR[g.MPP1] - 1;
        g.DELAY_CONTEXT_CHECK = g.FALSE;
        HALMAT_POP(XPMIN, 0, 0, g.FIXL[g.MP]);
        g.ASSIGN_ARG_LIST = g.FALSE;  # RESTORE LOCK GROUP CHECKING
        
        # RESET PCARGOFF HERE SO THAT IT CAN BE USED
        # TO DETERMINE WHETHER PERCENT MACRO ARGUMENT
        # PROCESSING IS HAPPENING.
        g.PCARGOFF[0] = 0;
        goto_FIX_NOLAB = True
    elif PRODUCTION_NUMBER == 78:  # reference 780
        #  <% MACRO HEAD>  ::=  <% MACRO NAME> (
        if g.FIXL[g.MP] == 0: 
            g.ALT_PCARGp[0] = 0
            g.PCARGp[0] = 0
            g.PCARGOFF[0] = 0;
        else:
            g.PCARGp[0] = g.PCARGp[g.FIXL[g.MP]];
            g.PCARGOFF[0] = g.PCARGOFF[g.FIXL[g.MP]];
            
            # CHECK PCARGBITS OF THE %MACRO ARGUMENT TO
            # SEE IF IT REQUIRES NAME CONTEXT CHECKING.
            # IF SO, SET NAMING FLAG.
            if ((g.PCARGBITS[PCARGOFF] & 0x80) != 0):
                g.NAMING = g.TRUE;
            
            g.ALT_PCARG[0] = g.ALT_PCARGp[g.FIXL[g.MP]];
        XSET (PC_STMT_TYPE_BASE + g.FIXL[g.MP]);
        HALMAT_POP(XPMHD, 0, 0, g.FIXL[g.MP]);
        g.DELAY_CONTEXT_CHECK = g.TRUE;
        if g.FIXL[g.MP] == PCCOPY_INDEX:
            g.ASSIGN_ARG_LIST = g.TRUE;  # INHIBIT LOCK CHECK IN ASSOCIATE
    elif PRODUCTION_NUMBER == 79:  # reference 790
        #  <% MACRO HEAD>  ::=  <% MACRO HEAD> <% MACRO ARG> ,
        HALMAT_TUPLE(XPMAR, 0, g.MPP1, 0, 0, g.PSEUDO_TYPE_P[g.PTR[g.MPP1]]);
        g.PTR_TOP = g.PTR[g.MPP1] - 1;
    elif PRODUCTION_NUMBER == 80:  # reference 800
        #  <% MACRO ARG>  ::=  <NAME VAR>
        if PCARGOFF > 0:
            if PCARGp == 0: 
                g.PCARGOFF = 0;
            else:
                g.TEMP = g.PCARGBITS[PCARGOFF];
                if (g.TEMP & 0x1) == 0: 
                    ERROR(d.CLASS_XM, 5);
                else:
                    l.H1 = g.PSEUDO_TYPE_P[g.PTR[g.MP]];
                    if l.H1 > 0x40: 
                        l.H1 = (l.H1 & 0xF) + 10;
                    elif TEMP_SYN == 0: 
                        l.H1 = l.H1 + 20;
                    if (SHL(1, l.H1) & g.PCARGTYPE[PCARGOFF]) == 0:
                        ERROR(d.CLASS_XM, 4);  # ILLEGAL TYPE
                    if g.EXT_P[g.PTR[g.MP]] > 0: 
                        if SHR(g.TEMP, 6):
                            ERROR(d.CLASS_XM, 10);  # NO NAME COPINESS
                    RESET_ARRAYNESS();
                    if CHECK_ARRAYNESS: 
                        if SHR(g.TEMP, 5):
                            ERROR(d.CLASS_XM, 7);  # NO ARRAYNESS
                    if SHR(g.TEMP, 4): 
                        if TEMP_SYN != 2: 
                            g.TEMP_SYN = 3;
                    if SHR(g.TEMP, 7): 
                        CHECK_NAMING(TEMP_SYN, g.MP);
                    else:
                        if SHR(g.TEMP, 4): 
                            CHECK_ASSIGN_CONTEXT(g.MP);
                        else:
                            SET_XREF_RORS(g.MP);
                        if g.FIXV[g.MP] > 0: 
                            l.H2 = g.FIXV[g.MP];
                        else:
                            l.H2 = g.FIXL[g.MP];
                        if (g.SYT_FLAGS(l.H2) & (TEMPORARY_FLAG)) != 0:
                            if SHR(g.TEMP, 8): 
                                ERROR(d.CLASS_XM, 8);
                        l.H2 = g.VAL_P[g.PTR[g.MP]];
                        # NO SUBSCRIPTS ARE ALLOWED ON THE SOURCE OF %NAMEBIAS
                        if PCARGOFF == 2:
                            if SHR(g.TEMP, 2):
                                if SHR(l.H2, 5): 
                                    ERROR(d.CLASS_XM, 9);
                        elif SHR(g.TEMP, 2):
                            if SHR(l.H2, 4): 
                                ERROR(d.CLASS_XM, 9);
                g.PCARGOFF = PCARGOFF + 1;
                
                # CHECK PCARGBITS OF THE %MACRO ARGUMENT TO
                # SEE IF IT REQUIRES NAME CONTEXT CHECKING.
                # IF SO, SET NAMING FLAG.
                if ((g.PCARGBITS[PCARGOFF] & 0x80) != 0):
                   g.NAMING = g.TRUE;
                
            g.PCARGp[0] = g.PCARGp[0] - 1;
            g.ALT_PCARGp[0] = g.ALT_PCARGp[0] - 1;
    elif PRODUCTION_NUMBER == 81:  # reference 810
        #  <% MACRO ARG>  ::=  <CONSTANT>
        if PCARGOFF > 0: 
            if PCARGp == 0: 
                g.PCARGOFF = 0;
            elif (g.PCARGBITS[PCARGOFF] & 0x8) == 0: 
                ERROR(d.CLASS_XM, 3);
            # LITERALS ILLEGAL
            elif (SHL(1, g.PSEUDO_TYPE_P[g.PTR[g.MP]]) & g.PCARGTYPE[PCARGOFF]) == 0:
                ERROR(d.CLASS_XM, 4);  #  TYPE ILLEGAL
            g.PCARGOFF = PCARGOFF + 1;
        g.PCARGp[0] = g.PCARGp[0] - 1;
        g.ALT_PCARGp[0] = g.ALT_PCARGp[0] - 1;
    # reference 820 has been relocated.
    # reference 830 has been relocated.
    elif PRODUCTION_NUMBER == 84:  # reference 840
        #  <BIT PRIM>  ::=  <EVENT VAR>
        SET_XREF_RORS(g.MP);
        g.INX[g.PTR[g.MP]] = REFER_LOC > 0;
        goto_YES_EVENT = True
    elif PRODUCTION_NUMBER == 85:  # reference 850
        #  <BIT PRIM>  ::=  <BIT CONST>
        goto_NON_EVENT = True
    elif PRODUCTION_NUMBER == 86:  # reference 860
        #  <BIT PRIM>  ::=  (  <BIT EXP>  )
        g.PTR[g.MP] = g.PTR[g.MPP1];
    elif PRODUCTION_NUMBER == 87:  # reference 870
        #  <BIT PRIM>  ::=  <MODIFIED BIT FUNC>
        SETUP_NO_ARG_FCN();
        goto_NON_EVENT = True
    elif PRODUCTION_NUMBER == 88:  # reference 880
        #  <BIT PRIM>  ::=  <BIT INLINE DEF> <BLOCK BODY> <CLOSING>  ;
        goto_INLINE_SCOPE = True
    elif PRODUCTION_NUMBER == 89:  # reference 890
        #  <BIT PRIM>  ::=  <SUBBIT HEAD>  <EXPRESSION>  )
        END_SUBBIT_FCN;
        SET_BI_XREF(SBIT_NDX);
        goto_NON_EVENT = True
    elif PRODUCTION_NUMBER == 90:  # reference 900
        #  <BIT PRIM>  ::=  <BIT FUNC HEAD>  (  <CALL LIST>  )
        END_ANY_FCN();
        goto_NON_EVENT = True
    elif PRODUCTION_NUMBER == 91:  # reference 910
        #  <BIT FUNC HEAD>  ::= <BIT FUNC>
        if START_NORMAL_FCN: 
            ASSOCIATE();
    elif PRODUCTION_NUMBER == 92:  # reference 920
        #  <BIT FUNC HEAD>  ::=  BIT  <SUB OR QUALIFIER>
        g.NOSPACE();
        g.PTR[g.MP] = g.PTR[g.SP];
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = BIT_TYPE;
        g.VAR[g.MP] = 'BIT CONVERSION FUNCTION';
        if PUSH_FCN_STACK(3): 
            g.FCN_LOC[g.FCN_LV] = 1;
        SET_BI_XREF(BIT_NDX);
    elif PRODUCTION_NUMBER == 93:  # reference 930
        #  <BIT CAT> ::= <BIT PRIM>
        pass;
    # reference 940 relocated.
    elif PRODUCTION_NUMBER == 95:  # reference 950
        # <BIT CAT> ::= <NOT> <BIT PRIM>
        if BIT_LITERAL(g.SP, 0): 
            g.TEMP = g.PSEUDO_LENGTH[g.PTR[g.SP]];
            g.TEMP2 = SHL(g.FIXV[g.SP], HOST_BIT_LENGTH_LIM - g.TEMP);
            g.TEMP2 = not TEMP2;
            g.TEMP2 = SHR(TEMP2, HOST_BIT_LENGTH_LIM - g.TEMP);
            g.LOC_P[g.PTR[g.SP]] = SAVE_LITERAL(2, TEMP2, g.TEMP);
        else:
            HALMAT_TUPLE(XBNOT, 0, g.SP, 0, g.INX[g.PTR[g.SP]]);
            SETUP_VAC(g.SP, BIT_TYPE);
        g.INX[g.PTR[g.SP]] = g.INX[g.PTR[g.SP]] & 1;
        g.PTR[g.MP] = g.PTR[g.SP];
    elif PRODUCTION_NUMBER == 96:  # reference 960
        # <BIT CAT> ::= <BIT CAT> <CAT> <NOT> <BIT PRIM>
        HALMAT_TUPLE(XBNOT, 0, g.SP, 0, 0);
        SETUP_VAC(g.SP, BIT_TYPE);
        goto_DO_BIT_CAT = True;
    elif PRODUCTION_NUMBER == 97:  # reference 970
        #  <BIT FACTOR> ::= <BIT CAT>
        pass;
    # reference 980 has been relocated.
    elif PRODUCTION_NUMBER == 99:  # reference 990
        #  <BIT EXP> ::= <BIT FACTOR>
        pass;
    elif PRODUCTION_NUMBER == 100:  # reference 1000
        #   <BIT EXP> ::= <BIT EXP> <OR> <BIT FACTOR>
        if BIT_LITERAL(g.MP, g.SP): 
            g.TEMP = g.FIXV[g.MP] | g.FIXV[g.SP];
            goto_DO_LIT_BIT_FACTOR = True
        else:
            g.TEMP = XBOR;
            goto_DO_BIT_FACTOR = True
    elif PRODUCTION_NUMBER == 101:  # reference 1010
        #  <RELATIONAL OP> ::= =
        g.REL_OP = 0 ;
    elif PRODUCTION_NUMBER == 102:  # reference 1020
        # <RELATIONAL OP> ::= <NOT> =
        g.REL_OP = 1 ;
    elif PRODUCTION_NUMBER == 103:  # reference 1030
        #  <RELATIONAL OP> ::= <
        g.REL_OP = 2 ;
    elif PRODUCTION_NUMBER == 104:  # reference 1040
        #  <RELATIONAL OP> ::= >
        g.REL_OP = 3 ;
    elif PRODUCTION_NUMBER == 105:  # reference 1050
        # <RELATIONAL OP> ::= <  =
        g.NOSPACE();
        g.REL_OP = 4 ;
    elif PRODUCTION_NUMBER == 106:  # reference 1060
        # <RELATIONAL OP> ::= >  =
        g.NOSPACE();
        g.REL_OP = 5 ;
    elif PRODUCTION_NUMBER == 107:  # reference 1070
        # <RELATIONAL OP> ::= <NOT> <
        g.REL_OP = 5 ;
    elif PRODUCTION_NUMBER == 108:  # reference 1080
        # <RELATIONAL OP> ::= <NOT> >
        g.REL_OP = 4 ;
    # reference 1090 relocated.
    elif PRODUCTION_NUMBER == 110:  # reference 1100
        # <COMPARISON> ::= <CHAR EXP> <RELATIONAL OP> <CHAR EXP>
        g.TEMP = XCEQU(REL_OP);
        g.VAR[g.MP] = '';
        goto_EMIT_REL = True;
    elif PRODUCTION_NUMBER == 111:  # reference 1110
        # <COMAPRISON> ::= <BIT CAT> <RELATIONAL OP> <BIT CAT>
        g.TEMP = XBEQU(REL_OP);
        g.VAR[g.MP] = 'BIT';
        goto_EMIT_REL = True;
    elif PRODUCTION_NUMBER == 112:  # reference 1120
        #  <COMPARISON>  ::=  <STRUCTURE EXP> <RELATIONAL OP> <STRUCTURE EXP>
        g.TEMP = XTEQU(REL_OP);
        g.VAR[g.MP] = 'STRUCTURE';
        STRUCTURE_COMPARE(g.FIXL[g.MP], g.FIXL[g.SP], d.CLASS_C, 3);
        goto_EMIT_REL = True;
    elif PRODUCTION_NUMBER == 113:  # reference 1130
        #  <COMPARISON>  ::=  <NAME EXP>  <RELATIONAL OP>  <NAME EXP>
        NAME_COMPARE(g.MP, g.SP, d.CLASS_C, 4);
        g.TEMP = XNEQU(REL_OP);
        g.VAR[g.MP] = 'NAME';
        if COPINESS(g.MP, g.SP): 
            ERROR(d.CLASS_EA, 1, g.VAR[g.SP]);
        NAME_ARRAYNESS(g.SP);
        goto_EMIT_REL = True;
    elif PRODUCTION_NUMBER == 114:  # reference 1140
        #  <RELATIONAL FACTOR>  ::=  <REL PRIM>
        pass;
    elif PRODUCTION_NUMBER == 115:  # reference 1150
        # <RELATIONAL FACTOR> ::= <RELATIONAL FACTOR> <AND> <REL PRIM>
        HALMAT_TUPLE(XCAND, XCO_N, g.MP, g.SP, 0);
        SETUP_VAC(g.MP, 0);
        g.PTR_TOP = g.PTR[g.MP];
    elif PRODUCTION_NUMBER == 116:  # reference 1160
        # <RELATIONAL EXP> ::= <RELATIONAL FACTOR>
        pass;
    elif PRODUCTION_NUMBER == 117:  # reference 1170
        # <RELATIONAL EXP> ::= < RELATIONAL EXP> <OR> < RELATIONAL FACTOR>
        HALMAT_TUPLE(XCOR, XCO_N, g.MP, g.SP, 0);
        SETUP_VAC(g.MP, 0);
        g.PTR_TOP = g.PTR[g.MP];
    elif PRODUCTION_NUMBER == 118:  # reference 1180
        # <REL PRIM> ::= (1 <RELATIONAL EXP> )
        g.PTR[g.MP] = g.PTR[g.MPP1] ;  # MOVE INDIRECT STACKS
    elif PRODUCTION_NUMBER == 119:  # reference 1190
        # <REL PRIM> ::= <NOT> (1 <RELATIONAL EXP> )
        HALMAT_TUPLE(XCNOT, XCO_N, g.MP + 2, 0, 0);
        g.PTR[g.MP] = g.PTR[g.MP + 2];
        SETUP_VAC(g.MP, 0);
    elif PRODUCTION_NUMBER == 120:  # reference 1200
        # <REL PRIM> ::=  <COMPARISON>
        if REL_OP > 1:
            if LENGTH(g.VAR[g.MP]) > 0: 
                ERROR(d.CLASS_C, 1, g.VAR[g.MP]);
            elif CHECK_ARRAYNESS: 
                ERROR(d.CLASS_C, 2);
            CHECK_ARRAYNESS();
        SETUP_VAC(g.MP, 0);
        g.PTR_TOP = g.PTR[g.MP];
        EMIT_ARRAYNESS();
    elif PRODUCTION_NUMBER == 121:  # reference 1210
        #  <CHAR PRIM> ::= <CHAR VAR>
        SET_XREF_RORS(g.MP);  # SET XREF FLAG TO SUBSCR OR REF
    elif PRODUCTION_NUMBER == 122:  # reference 1220
        #  <CHAR PRIM>  ::=  <CHAR CONST>
        pass;
    elif PRODUCTION_NUMBER == 123:  # reference 1230
        #  <CHAR PRIM>  ::=  <MODIFIED CHAR FUNC>
        SETUP_NO_ARG_FCN();
    elif PRODUCTION_NUMBER == 124:  # reference 1240
        #  <CHAR PRIM>  ::=  <CHAR INLINE DEF> <BLOCK BODY> <CLOSING>  ;
        goto_INLINE_SCOPE = True
    elif PRODUCTION_NUMBER == 125:  # reference 1250
        #  <CHAR PRIM>  ::=  <CHAR FUNC HEAD>  (  <CALL LIST>  )
        END_ANY_FCN();
    elif PRODUCTION_NUMBER == 126:  # reference 1260
        #  <CHAR PRIM>  ::=  (  <CHAR EXP>  )
        g.PTR[g.MP] = g.PTR[g.MPP1];
    elif PRODUCTION_NUMBER == 127:  # reference 1270
        #  <CHAR FUNC HEAD>  ::=  <CHAR FUNC>
        if START_NORMAL_FCN: 
            ASSOCIATE();
    elif PRODUCTION_NUMBER == 128:  # reference 1280
        #  <CHAR FUNC HEAD>  ::=  CHARACTER  <SUB OR QUALIFIER>
        g.NOSPACE();
        g.PTR[g.MP] = g.PTR[g.SP];
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = CHAR_TYPE;
        g.VAR[g.MP] = 'CHARACTER CONVERSION FUNCTION';
        if PUSH_FCN_STACK(3): 
            g.FCN_LOC[g.FCN_LV] = 0;
        SET_BI_XREF(CHAR_NDX);
    elif PRODUCTION_NUMBER == 129:  # reference 1290
        #  <SUB OR QUALIFIER>  ::=  <SUBSCRIPT>
        g.TEMP = g.PTR[g.MP];
        g.LOC_P[g.TEMP] = 0;
        if g.PSEUDO_FORM[g.TEMP] != 0: 
            g.PSEUDO_FORM[g.TEMP] = 0;
            ERROR(d.CLASS_QS, 9);
        if g.INX[g.TEMP] > 0: 
           if (g.PSEUDO_LENGTH[g.TEMP] >= 0) or (g.VAL_P[g.TEMP] >= 0):
               ERROR(d.CLASS_QS, 1);
           if g.INX[g.TEMP] != 1:
               g.INX[g.TEMP] = 1;
               ERROR(d.CLASS_QS, 10);
    elif PRODUCTION_NUMBER == 130:  # reference 1300
        #  <SUB OR QUALIFIER>  ::=  <BIT QUALIFIER>
        g.INX[g.PTR[g.MP]] = 0;
    elif PRODUCTION_NUMBER == 131:  # reference 1310
        #  <CHAR EXP> ::= <CHAR PRIM>
        pass;
    # reference 1320 relocated.
    elif PRODUCTION_NUMBER == 133:  # reference 1330
        # <CHAR EXP> ::= <CHAR EXP> <CAT> <ARITH EXP>
        ARITH_TO_CHAR(g.SP) ;
        goto_DO_CHAR_CAT = True ;
    elif PRODUCTION_NUMBER == 134:  # reference 1340
        #  <CHAR EXP>  ::=  <ARITH EXP>  <CAT>  <ARITH EXP>
        ARITH_TO_CHAR(g.SP);
        ARITH_TO_CHAR(g.MP);
        goto_DO_CHAR_CAT = True;
    elif PRODUCTION_NUMBER == 135:  # reference 1350
        # <CHAR EXP> ::= <ARITH EXP> <CAT> <CHAR PRIM>
        ARITH_TO_CHAR(g.MP) ;
        goto_DO_CHAR_CAT = True ;
    # reference 1360 has been relocated.
    elif PRODUCTION_NUMBER == 137:  # reference 1370
        # <ASSIGNMENT>::=<VARIABLE>,<ASSIGNMENT>
        HALMAT_PIP(g.LOC_P[g.PTR[g.MP]], g.PSEUDO_FORM[g.PTR[g.MP]], 0, 0);
        g.INX[g.PTR[g.SP]] = g.INX[g.PTR[g.SP]] + 1;
        if NAME_PSEUDOS: 
            NAME_COMPARE(g.MP, g.SP, d.CLASS_AV, 5, 0);
            if COPINESS(g.MP, g.SP) > 0: 
                ERROR(d.CLASS_AA, 2, g.VAR[g.MP]);
            goto_END_ASSIGN = True
        else:
            goto_ASSIGNING = True
    # reference 1380 relocated.
    elif PRODUCTION_NUMBER == 139:  # reference 1390
        # <IF STATEMENT>::=<TRUE PART> <STATEMENT>
        UNBRANCHABLE(g.SP, 5);
        goto_CLOSE_IF = True
    elif PRODUCTION_NUMBER == 140:  # reference 1400
        # <TRUE PART>::=<IF CLAUSE><BASIC STATEMENT> ELSE
        UNBRANCHABLE(g.MPP1, 4);
        CHECK_IMPLICIT_T();
        g.ELSEIF_PTR = g.STACK_PTR[g.SP];
        # MOVE ELSEIF_PTR TO FIRST PRINTABLE REPLACE MACRO TOKEN-111342
        g.I = ELSEIF_PTR;
        while (I > 0) and ((g.GRAMMAR_FLAGS[I - 1] & MACRO_ARG_FLAG) != 0):
           g.I = I - 1;
           if ((g.GRAMMAR_FLAGS[I] & PRINT_FLAG) != 0):
                g.ELSEIF_PTR = I;
        if ELSEIF_PTR > 0:
            if STMT_END_PTR > -1:
                g.SQUEEZING = g.FALSE;
                OUTPUT_WRITER(g.LAST_WRITE, ELSEIF_PTR - 1);
                g.LAST_WRITE = ELSEIF_PTR;
        # ALIGN ELSE CORRECTLY.
        if g.MOVE_ELSE:
            g.INDENT_LEVEL = g.INDENT_LEVEL - g.INDENT_INCR;
        g.MOVE_ELSE = g.TRUE;
        EMIT_SMRK();
        SRN_UPDATE();
        # PUT THE ELSE ON THE SAME LINE AS THE DO.
        g.ELSE_FLAG = g.TRUE;
        # DETERMINES IF ELSE WAS ALREADY PRINTED IN REPLACE MACRO-11342
        if (g.GRAMMAR_FLAGS[ELSEIF_PTR] & PRINT_FLAG) == 0:
            g.ELSE_FLAG = g.FALSE;
        if NO_LOOK_AHEAD_DONE: 
            CALL_SCAN();
        if TOKEN != IF_TOKEN: 
            #  PRINT ELSE STATEMENTS ON SAME LINE AS A
            # SIMPLE DO.  IF ELSE_FLAG IS FALSE, THEN THE ELSE STATEMENT
            # WAS ALREADY PRINTED.
            if not g.ELSE_FLAG:
                g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
            else:
                # DO NOT OUTPUT_WRITER.  SAVE VALUES
                # THAT ARE NEEDED WHEN OUTPUT_WRITER WILL BE CALLED.
                g.SAVE_SRN1 = g.SRN[2][:];
                g.SAVE_SRN_COUNT1 = g.SRN_COUNT[2];
                g.SAVE1 = ELSEIF_PTR;
                g.SAVE2 = g.STACK_PTR[g.SP];
        else:
            # IF ELSE_FLAG IS FALSE, THEN THE ELSE STATEMENT
            # WAS ALREADY PRINTED FROM PRINT_COMMENT AND INDENT_LEVEL
            # SHOULD BE SET TO INDENT THE LINE FOLLOWING THE COMMENT
            # OR DIRECTIVE.
            if not g.ELSE_FLAG:
                g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
            g.ELSE_FLAG = g.FALSE;
            g.LAST_WRITE = ELSEIF_PTR;
        HALMAT_POP(XBRA, 1, 0, 1);
        HALMAT_PIP(g.FL_NO(), XINL, 0, 0);
        HALMAT_POP(XLBL, 1, XCO_N, 0);
        HALMAT_PIP(g.FIXV[g.MP], XINL, 0, 0);
        g.FIXV[g.MP] = g.FL_NO();
        g.XSET(0x100);
        g.FL_NO(g.FL_NO() + 1);
    # reference 1410 relocated.
    elif PRODUCTION_NUMBER == 142:  # reference 1420
        #  <IF CLAUSE>  ::=  <IF> <BIT EXP> THEN
        HALMAT_TUPLE(XBTRU, 0, g.MPP1, 0, 0);
        if g.PSEUDO_LENGTH[g.PTR[g.MPP1]] > 1: 
            ERROR(d.CLASS_GB, 1, 'IF');
        g.TEMP = LAST_POPp;
        EMIT_ARRAYNESS();
        goto_EMIT_IF = True
    elif PRODUCTION_NUMBER == 143:  # reference 1430
        #  <IF>  ::=  IF
        g.XSET(0x5);
        g.FIXL[g.MP] = g.INDENT_LEVEL;
        HALMAT_POP(XIFHD, 0, XCO_N, 0);
    # reference 1440 relocated
    elif PRODUCTION_NUMBER == 145:  # reference 1450
        # <DO GROUP HEAD>::= DO <FOR LIST> ;
        g.XSET(0x13);
        HALMAT_FIX_POPTAG(g.FIXV[g.MPP1], g.PTR[g.MPP1]);
        goto_DO_DONE = True
    # reference 1460 relocated
    elif PRODUCTION_NUMBER == 147:  # reference 1470
        # <DO GROUP HEAD>::= DO <WHILE CLAUSE> ;
        g.XSET(0x12);
        g.FIXL[g.MPP1] = 0;
        g.TEMP = g.PTR[g.MPP1];
        HALMAT_POP(XCTST, 1, 0, g.INX[g.TEMP]);
        goto_EMIT_WHILE = True
    # reference 1480 relocated
    # reference 1490 relocated
    # reference 1500 relocated
    elif PRODUCTION_NUMBER == 151:  # reference 1510
        #  <DO GROUP HEAD>  ::=  <DO GROUP HEAD>  <TEMPORARY STMT>
        if (g.DO_INX[g.DO_LEVEL] & 0x7F) == 2: 
            ERROR(d.CLASS_D, 10);
        elif g.FIXV[g.MP]:
            ERROR(d.CLASS_D, 7);
            g.FIXV[g.MP] = 0;
        goto_EMIT_NULL = True;
    elif PRODUCTION_NUMBER == 152:  # reference 1520
        #  <CASE ELSE>  ::=  DO CASE <ARITH EXP> ; ELSE
        g.FIXL[g.MP] = 1;
        goto_CASE_HEAD = True
    # reference 1530 relocated.
    elif PRODUCTION_NUMBER == 154:  # reference 1540
        # <WHILE KEY>::= UNTIL
        g.TEMP = 1;
        goto_WHILE_KEY = True
    # reference 1550 relocated.
    elif PRODUCTION_NUMBER == 156:  # reference 1560
        # <WHILE CLAUSE>::= <WHILE KEY> <RELATIONAL EXP>
        goto_DO_FLOWSET = True
    elif PRODUCTION_NUMBER == 157:  # reference 1570
        # <FOR LIST>::= <FOR KEY>  <ARITH EXP><ITERATION CONTROL>
        if UNARRAYED_SIMPLE(g.SP - 1): 
            ERROR(d.CLASS_GC, 3);
        HALMAT_POP(XDFOR, TEMP2 + 3, XCO_N, 0);
        EMIT_PUSH_DO(1, 5, g.PSEUDO_TYPE_P[g.PTR[g.SP]] == INT_TYPE, g.MP - 2, g.FIXL[g.MP]);
        g.TEMP = g.PTR[g.MP];
        while g.TEMP <= g.PTR_TOP:
            HALMAT_PIP(g.LOC_P[g.TEMP], g.PSEUDO_FORM[g.TEMP], 0, 0);
            g.TEMP = g.TEMP + 1;
        g.FIXV[g.MP] = LAST_POPp;
        g.PTR_TOP = g.PTR[g.MP] - 1;
        g.PTR[g.MP] = TEMP2 | g.FIXF[g.MP];  ''' RECORD DO TYPE AND WHETHER
                                         LOOP VAR IS TEMPORARY '''
    elif PRODUCTION_NUMBER == 158:  # reference 1580
        # <FOR LIST> = <FOR KEY>  <ITERATION BODY>
        HALMAT_FIX_POPTAG(g.FIXV[g.SP], 1);
        g.PTR_TOP = g.PTR[g.MP] - 1;
        g.PTR[g.MP] = g.FIXF[g.MP];  # RECORD WHETHER LOOP VAR IS TEMPORARY
    elif PRODUCTION_NUMBER == 159:  # reference 1590
        # <ITERATION BODY>::= <ARITH EXP>
        g.TEMP = g.PTR[g.MP - 1];  # <FOR KEY> PTR
        HALMAT_POP(XDFOR, 2, XCO_N, 0);
        EMIT_PUSH_DO(1, 5, 0, g.MP - 3, g.FIXL[g.MP - 1]);
        HALMAT_PIP(g.LOC_P[g.TEMP], g.PSEUDO_FORM[g.TEMP], 0, 0);
        g.FIXV[g.MP - 1] = LAST_POPp;  # IN <FOR KEY> STACK ENTRY
        goto_DO_DISCRETE = True
    # reference 1600 relocated.
    elif PRODUCTION_NUMBER == 161:  # reference 1610
        # <ITERATION CONTROL>::= TO <ARITH EXP>
        if UNARRAYED_SIMPLE(g.MPP1): ERROR(d.CLASS_GC, 3);
        g.PTR[g.MP] = g.PTR[g.MPP1];
        g.TEMP2 = 1;
    elif PRODUCTION_NUMBER == 162:  # reference 1620
        # <ITERATION CONTROL>::= TO <ARITH EXP> BY <ARITH EXP>
        g.TEMP2 = UNARRAYED_SIMPLE(g.SP);
        if UNARRAYED_SIMPLE(g.MPP1) or TEMP2:
            ERROR(d.CLASS_GC, 3);
        g.PTR[g.MP] = g.PTR[g.MPP1];
        g.TEMP2 = 2;
    elif PRODUCTION_NUMBER == 163:  # reference 1630
        # <FOR KEY>::= FOR <ARITH VAR> =
        CHECK_ASSIGN_CONTEXT(g.MPP1);
        if UNARRAYED_SIMPLE(g.MPP1): 
            ERROR(d.CLASS_GV, 1);
        g.PTR[g.MP] = g.PTR[g.MPP1];
        g.FIXL[g.MP], g.FIXF[g.MP] = 0;  # NO DO CHAIN EXISTS
    elif PRODUCTION_NUMBER == 164:  # reference 1640
        #  <FOR KEY>  ::=  FOR TEMPORARY  <IDENTIFIER>  =
        g.ID_LOC = g.FIXL[g.MP + 2];
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.LOC_P[g.PTR_TOP] = ID_LOC;
        g.PSEUDO_FORM[g.PTR_TOP] = XSYT;
        g.PSEUDO_TYPE_P[g.PTR_TOP] = INT_TYPE
        g.SYT_TYPE(ID_LOC, INT_TYPE);
        g.TEMP = DEFAULT_ATTR & SD_FLAGS;
        g.SYT_FLAGS(ID_LOC, g.SYT_FLAGS(ID_LOC) | g.TEMP);
        g.FIXL[g.MP] = ID_LOC
        g.DO_CHAIN = ID_LOC;
        g.FIXF[g.MP] = 8;  # DO CHAIN EXISTS FOR CURRENT DO
        g.CONTEXT = 0;
        g.FACTORING = g.TRUE;
        if g.SIMULATING: 
            STAB_VAR(g.MP);
        SET_XREF(ID_LOC, XREF_ASSIGN);
    elif PRODUCTION_NUMBER == 165:  # reference 1650
        # <ENDING>::= END
        # ON END STATEMENT, REPLACE THE CURRENT SCOPE WITH
        # THE STATEMENT NUMBER OF THE DO.  SET A FLAG HERE TO BE USED
        # IN OUTPUT_WRITER IF THE END ISN'T IN A NON-EXPANDED
        # REPLACE MACRO.
        if ((g.GRAMMAR_FLAGS[g.STACK_PTR[g.SP]] & PRINT_FLAG) != 0):
            g.END_FLAG = g.TRUE;
        # USED TO ALIGN ELSE CORRECTLY
        if (g.DO_INX[g.DO_LEVEL] == 0) and g.IFDO_FLAG[g.DO_LEVEL]:
            g.MOVE_ELSE = g.FALSE;
        g.SAVE_DO_LEVEL = g.DO_LEVEL;
    elif PRODUCTION_NUMBER == 166:  # reference 1660
        # <ENDING>::= END <LABEL>
        # ON END STATEMENT, REPLACE THE CURRENT SCOPE WITH
        # THE STATEMENT NUMBER OF THE DO.  SET A FLAG HERE TO BE USED
        # IN OUTPUT_WRITER IF THE END ISN'T IN A NON-EXPANDED
        # REPLACE MACRO.
        if ((g.GRAMMAR_FLAGS[g.STACK_PTR[g.SP]] and PRINT_FLAG) != 0):
            g.END_FLAG = g.TRUE;
        # USED TO ALIGN ELSE CORRECTLY
        if (g.DO_INX[g.DO_LEVEL] == 0) and g.IFDO_FLAG[g.DO_LEVEL]:
            g.MOVE_ELSE = g.FALSE;
        g.SAVE_DO_LEVEL = g.DO_LEVEL;
        g.TEMP = g.MP - 1;
        while g.PARSE_STACK[g.TEMP] == LABEL_DEFINITION:
            g.TEMP = g.TEMP - 1;
        g.TEMP = g.TEMP - 1;
        # Note that ENDING_DONE is entirely local to this case.
        goto_ENDING_DONE = False
        while g.PARSE_STACK[g.TEMP] == LABEL_DEFINITION:
            if g.FIXL[g.TEMP] == g.FIXL[g.SP]:
                # CREATE AN ASSIGN XREF ENTRY FOR A LABEL THAT
                # IS USED ON AN END STATEMENT SO THE "NOT
                # REFERENCED" MESSAGE WILL NOT BE PRINTED IN
                # THE CROSS REFERENCE TABLE. THIS XREF ENTRY
                # WILL BE REMOVED IN SYT_DUMP SO IT DOES NOT
                # SHOW UP IN THE SDF.
                SET_XREF(g.FIXL[g.SP], XREF_ASSIGN);
                goto_ENDING_DONE = True
                break
            g.TEMP = g.TEMP - 1;
        if not goto_ENDING_DONE:
            ERROR(d.CLASS_GL, 1);
        goto_ENDING_DONE = False
    elif PRODUCTION_NUMBER == 167:  # reference 1670
        # <ENDING>::= <LABEL DEFINITION> <ENDING>
        # USED TO ALIGN ELSE CORRECTLY
        if (g.DO_INX[g.DO_LEVEL] == 0) and g.IFDO_FLAG[g.DO_LEVEL]:
            g.MOVE_ELSE = g.FALSE;
        g.SAVE_DO_LEVEL = g.DO_LEVEL;
        SET_LABEL_TYPE(g.FIXL[g.MP], g.STMT_LABEL);
    elif PRODUCTION_NUMBER == 168:  # reference 1680
        #    <ON PHRASE>  ::= ON ERROR  <SUBSCRIPT>
        ERROR_SUB(1);
        HALMAT_POP(XERON, 2, 0, 0);
        HALMAT_PIP(g.LOC_P[g.PTR[g.MP + 2]], XIMD, g.FIXV[g.MP] & 0x3F, 0);
        HALMAT_PIP(g.FL_NO(), XINL, 0, 0);
        g.FIXL[g.MP] = g.FL_NO();
        g.FL_NO(g.FL_NO() + 1);
        g.PTR_TOP = g.PTR[g.SP] - 1;
        if g.INX[g.PTR[g.SP]] == 0:
            g.SUB_END_PTR = g.STACK_PTR[g.MP] + 1;  # NULL SUBSCRIPT
        OUTPUT_WRITER(g.LAST_WRITE, SUB_END_PTR);
        g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
        EMIT_SMRK();
        g.XSET(0x400);
    # reference 1690 relocated.
    elif PRODUCTION_NUMBER == 170:  # reference 1700
        #  <ON CLAUSE>  ::=  ON ERROR <SUBSCRIPT> IGNORE
        g.FIXL[g.MP] = 2;
        goto_ON_ERROR_ACTION = True
    # reference 1710 relocated.
    elif PRODUCTION_NUMBER == 172:  # reference 1720
        #  <SIGNAL CLAUSE>  ::=  RESET <EVENT VAR>
        g.TEMP = 2;
        goto_SIGNAL_EMIT = True
    elif PRODUCTION_NUMBER == 173:  # reference 1730
        #  <SIGNAL CLAUSE>  ::= SIGNAL <EVENT VAR>
        g.TEMP = 0;
        goto_SIGNAL_EMIT = True
    elif PRODUCTION_NUMBER == 174:  # reference 1740
        #  <FILE EXP>  ::=  <FILE HEAD>  ,  <ARITH EXP>  )
        if g.FIXV[g.MP] > DEVICE_LIMIT:
            ERROR(d.CLASS_TD, 1, '' + DEVICE_LIMIT);
            g.FIXV[g.MP] = 0;
        if UNARRAYED_INTEGER(g.SP - 1): 
            ERROR(d.CLASS_TD, 2);
        RESET_ARRAYNESS();
        g.PTR[g.MP] = g.PTR[g.SP - 1];
        if UPDATE_BLOCK_LEVEL > 0: 
            ERROR(d.CLASS_UT, 1);
        g.XSET(0x10);
    elif PRODUCTION_NUMBER == 175:  # reference 1750
        #  <FILE HEAD>  ::=  FILE  (  <NUMBER>
        g.FIXV[g.MP] = g.FIXV[g.MP + 2];
        if INLINE_LEVEL > 0: 
            ERROR(d.CLASS_PP, 5);
        SAVE_ARRAYNESS();
    elif PRODUCTION_NUMBER == 176:  # reference 1760
        #  <CALL KEY>  ::=  CALL  <LABEL VAR>
        g.I = g.FIXL[g.MPP1];
        if g.SYT_TYPE(I) == PROC_LABEL: 
            if g.SYT_LINK1(I) < 0:
                if g.DO_LEVEL < (-g.SYT_LINK1(I)): 
                    ERROR(d.CLASS_PL, 8, g.VAR[g.MPP1]);
        if g.SYT_LINK1(I) == 0: 
            g.SYT_LINK1(I, g.STMT_NUM());
        while g.SYT_TYPE(I) == IND_CALL_LAB:
            g.I = SYT_PTR(I);
        if g.SYT_TYPE(I) != PROC_LABEL: 
            ERROR(d.CLASS_DT, 3, g.VAR[g.MPP1]);
        if CHECK_ARRAYNESS: 
            ERROR(d.CLASS_PL, 7, g.VAR[g.MPP1]);
        if (g.SYT_FLAGS(I) & ACCESS_FLAG) != 0:
            ERROR(d.CLASS_PS, 6, g.VAR[g.MPP1]);
        g.XSET(0x2);
        g.FCN_ARG = 0;
        g.PTR[g.MP] = g.PTR[g.MPP1];
        SET_XREF_RORS(g.SP, 0x6000);
        if INLINE_LEVEL > 0: 
            ERROR(d.CLASS_PP, 7);
    elif PRODUCTION_NUMBER == 177:  # reference 1770
        #  <CALL LIST> ::= <LIST EXP>
        SETUP_CALL_ARG();
    elif PRODUCTION_NUMBER == 178:  # reference 1780
        #  <CALL LIST> ::= <CALL LIST> , <LIST EXP>
        SETUP_CALL_ARG();
    # reference 1790 relocated.
    elif PRODUCTION_NUMBER == 180:  # reference 1800
        #  <CALL ASSIGN LIST> ::= <CALL ASSIGN LIST> , <VARIABLE>
        goto_ASSIGN_ARG = True
    elif PRODUCTION_NUMBER == 181:  # reference 1810
        #  <EXPRESSION> ::= <ARITH EXP>
        g.EXT_P[g.PTR[g.MP]] = 0;
        # if THE DECLARED VALUE IS A DOUBLE CONSTANT SCALAR OR
        # INTEGER,: SET LIT1 EQUAL TO 5.
        if (TYPE == g.SCALAR_TYPE) or (FACTORED_TYPE == g.SCALAR_TYPE) or \
                (TYPE == INT_TYPE) or (FACTORED_TYPE == INT_TYPE) or \
                ((TYPE == 0) and (FACTORED_TYPE == 0)):
            if ((ATTRIBUTES & DOUBLE_FLAG) != 0) and \
                    ((g.FIXV[g.MP - 1] & CONSTANT_FLAG) != 0):
                LIT1(GET_LITERAL(g.LOC_P[g.PTR[g.MP]]), 5);
    elif PRODUCTION_NUMBER == 182:  # reference 1820
        #  <EXPRESSION> ::= <BIT EXP>
        g.EXT_P[g.PTR[g.MP]] = 0;
    elif PRODUCTION_NUMBER == 183:  # reference 1830
        #  <EXPRESSION> ::= <CHAR EXP>
        g.EXT_P[g.PTR[g.MP]] = 0;
    elif PRODUCTION_NUMBER == 184:  # reference 1840
        #  <EXPRESSION>  ::=  <STRUCTURE EXP>
        g.EXT_P[g.PTR[g.MP]] = 0;
    elif PRODUCTION_NUMBER == 185:  # reference 1850
        #  <EXPRESSION>  ::=  <NAME EXP>
        pass;
    elif PRODUCTION_NUMBER == 186:  # reference 1860
        #  <STRUCTURE EXP>  ::=  <STRUCTURE VAR>
        SET_XREF_RORS(g.MP);
    elif PRODUCTION_NUMBER == 187:  # reference 1870
        #  <STRUCTURE EXP>  ::=  <MODIFIED STRUCT FUNC>
        SETUP_NO_ARG_FCN();
    elif PRODUCTION_NUMBER == 188:  # reference 1880
        #  <STRUCTURE EXP>  ::=  <STRUC INLINE DEF> <BLOCK BODY> <CLOSING> ;
        goto_INLINE_SCOPE = True
    elif PRODUCTION_NUMBER == 189:  # reference 1890
        #  <STRUCTURE EXP>  ::=  <STRUCT FUNC HEAD>  (  <CALL LIST>  )
        END_ANY_FCN();
    elif PRODUCTION_NUMBER == 190:  # reference 1900
        #  <STRUCT FUNC HEAD>  ::=  <STRUCT FUNC>
        if START_NORMAL_FCN: 
            ASSOCIATE();
    elif PRODUCTION_NUMBER == 191:  # reference 1910
        # <LIST EXP> ::= <EXPRESSION>
        if g.FCN_MODE[g.FCN_LV] != 1: 
            g.INX[g.PTR[g.MP]] = 0;
    elif PRODUCTION_NUMBER == 192:  # reference 1920
        #  <LIST EXP>  ::=  <ARITH EXP>  #  <EXPRESSION>
        if g.FCN_MODE[g.FCN_LV] == 2: 
            if g.PSEUDO_FORM[g.PTR[g.MP]] != XLIT: 
                g.TEMP = 0;
            else:
                g.TEMP = MAKE_FIXED_LIT(g.LOC_P[g.PTR[g.MP]]);
            if (g.TEMP < 1) or (g.TEMP > LIST_EXP_LIM): 
                g.TEMP = 1;
                ERROR(d.CLASS_EL, 2);
            g.INX[g.PTR[g.MP]] = g.TEMP;
        else:
            ERROR(d.CLASS_EL, 1);
            if g.FCN_MODE[g.FCN_LV] != 1: 
                g.INX[g.PTR[g.MP]] = 1;
            else:
                g.INX[g.PTR[g.MP]] = g.INX[g.PTR[g.SP]];
        g.TEMP = g.PTR[g.SP];
        g.PTR_TOP = g.PTR[g.MP];
        g.LOC_P[g.PTR_TOP] = g.LOC_P[g.TEMP];
        g.PSEUDO_FORM[g.PTR_TOP] = g.PSEUDO_FORM[g.TEMP];
        g.PSEUDO_TYPE_P[g.PTR_TOP] = g.PSEUDO_TYPE_P[g.TEMP];
        g.PSEUDO_LENGTH[g.PTR_TOP] = g.PSEUDO_LENGTH[g.TEMP];
    elif PRODUCTION_NUMBER == 193:  # reference 1930
        #  <VARIABLE> ::= <ARITH VAR>
        if not DELAY_CONTEXT_CHECK: 
            CHECK_ASSIGN_CONTEXT(g.MP);
    elif PRODUCTION_NUMBER == 194:  # reference 1940
        #  <VARIABLE> ::= <STRUCTURE VAR>
        if not DELAY_CONTEXT_CHECK: 
            CHECK_ASSIGN_CONTEXT(g.MP);
    elif PRODUCTION_NUMBER == 195:  # reference 1950
        #  <VARIABLE> ::= <BIT VAR>
        if not DELAY_CONTEXT_CHECK: 
            CHECK_ASSIGN_CONTEXT(g.MP);
    elif PRODUCTION_NUMBER == 196:  # reference 1960
        #  <VARIABLE  ::=  <EVENT VAR>
        if CONTEXT > 0: 
            if not NAME_PSEUDOS: g.PSEUDO_TYPE_P[g.PTR[g.MP]] = BIT_TYPE;
        if not DELAY_CONTEXT_CHECK: 
            CHECK_ASSIGN_CONTEXT(g.MP);
        g.PSEUDO_LENGTH[g.PTR[g.MP]] = 1;
    elif PRODUCTION_NUMBER == 197:  # reference 1970
        #  <VARIABLE>  ::=  <SUBBIT HEAD>  <VARIABLE>  )
        if CONTEXT == 0:
            if SHR(g.VAL_P[g.PTR[g.MPP1]], 7): 
                ERROR(d.CLASS_QX, 7);
            g.TEMP = 1;
        else:
            g.TEMP = 0;
        END_SUBBIT_FCN(g.TEMP);
        SET_BI_XREF(SBIT_NDX);
        g.VAL_P[g.PTR[g.MP]] = g.VAL_P[g.PTR[g.MPP1]] | 0x80;
    elif PRODUCTION_NUMBER == 198:  # reference 1980
        #  <VARIABLE> ::= <CHAR VAR>
        if not DELAY_CONTEXT_CHECK: CHECK_ASSIGN_CONTEXT(g.MP);
    elif PRODUCTION_NUMBER == 199:  # reference 1990
        #  <VARIABLE>  ::=  <NAME KEY>  (  <NAME VAR>  )
        if TEMP_SYN != 2: 
            if CONTEXT == 0: 
                g.TEMP_SYN = 3;
        CHECK_NAMING(TEMP_SYN, g.MP + 2);
        g.DELAY_CONTEXT_CHECK = g.FALSE;
    elif PRODUCTION_NUMBER == 200:  # reference 2000
        #  <NAME VAR>  ::=  <VARIABLE>
        l.H1 = g.VAL_P[g.PTR[g.MP]];
        g.ARRAYNESS_FLAG = 0;
        if SHR(l.H1, 11): 
            ERROR(d.CLASS_EN, 1);
        g.VAL_P[g.PTR[g.MP]] = l.H1 | 0x800;
        if SHR(l.H1, 7): 
            ERROR(d.CLASS_EN, 2);
        if (l.H1 & 0x880) != 0: 
            g.TEMP_SYN = 2;
        else:
            g.TEMP_SYN = 1;
    elif PRODUCTION_NUMBER == 201:  # reference 2010
        #  <NAME VAR>  ::=  <LABEL VAR>
        l.H1 = g.SYT_TYPE(g.FIXL[g.MP]);
        if l.H1 == TASK_LABEL or l.H1 == PROG_LABEL: 
            pass  # GO TO OK_LABELS;
        elif g.VAR[g.MP - 2] == 'NAME':
            ERROR(d.CLASS_EN, 4, g.VAR[g.MP]);
        # OK_LABELS:
        g.TEMP_SYN = 0;
    elif PRODUCTION_NUMBER == 202:  # reference 2020
        #  <NAME VAR>  ::=  <MODIFIED ARITH FUNC>
        g.TEMP_SYN = 0;
    elif PRODUCTION_NUMBER == 203:  # reference 2030
        #  <NAME VAR>  ::=  <MODIFIED BIT FUNC>
        g.TEMP_SYN = 0;
    elif PRODUCTION_NUMBER == 204:  # reference 2040
        #  <NAME VAR>  ::=  <MODIFIED CHAR FUNC>
        g.TEMP_SYN = 0;
    elif PRODUCTION_NUMBER == 205:  # reference 2050
        #  <NAME VAR>  ::=  <MODIFIED STRUCT FUNC>
        g.TEMP_SYN = 0;
    elif PRODUCTION_NUMBER == 206:  # reference 2060
        #  <NAME EXP>  ::=  <NAME KEY>  (  <NAME VAR>  )
        CHECK_NAMING(TEMP_SYN, g.MP + 2);
        g.DELAY_CONTEXT_CHECK = g.FALSE;
    # reference 2070 relocated
    elif PRODUCTION_NUMBER == 208:  # reference 2080
        #  <NAME EXP>  ::=  <NAME KEY> ( NULL )
        g.NAMING = g.FALSE;
        g.DELAY_CONTEXT_CHECK = g.FALSE;
        goto_FIX_NULL = True
    elif PRODUCTION_NUMBER == 209:  # reference 2090
        #  <NAME KEY>  ::=  NAME
        g.NAMING = g.TRUE
        g.NAME_PSEUDOS = g.TRUE;
        g.DELAY_CONTEXT_CHECK = g.TRUE;
        g.ARRAYNESS_FLAG = 0;
    elif PRODUCTION_NUMBER == 210:  # reference 2100
        #  <LABEL VAR>  ::=  <PREFIX>  <LABEL>  <SUBSCRIPT>
        goto_FUNC_IDS = True;
    elif PRODUCTION_NUMBER == 211:  # reference 2110
        #  <MODIFIED ARITH FUNC>  ::=  <PREFIX>  <NO ARG ARITH FUNC> <SUBSCRIPT>
        goto_FUNC_IDS = True;
    elif PRODUCTION_NUMBER == 212:  # reference 2120
        #  <MODIFIED BIT FUNC>  ::=  <PREFIX>  <NO ARG BIT FUNC>  <SUBSCRIPT>
        goto_FUNC_IDS = True;
    elif PRODUCTION_NUMBER == 213:  # reference 2130
        #  <MODIFIED CHAR FUNC>  ::=  <PREFIX> <NO ARG CHAR FUNC>  <SUBSCRIPT>
        goto_FUNC_IDS = True;
    # reference 2140 relocated
    elif PRODUCTION_NUMBER == 215:  # reference 2150
        #  <STRUCTURE VAR>  ::=  <QUAL STRUCT>  <SUBSCRIPT>
        l.H1 = g.PTR[g.MP];
        goto_STRUC_IDS = True
    elif PRODUCTION_NUMBER == 216:  # reference 2160
        #  <ARITH VAR>  ::=  <PREFIX>  <ARITH ID>  <SUBSCRIPT>
        goto_MOST_IDS = True
    elif PRODUCTION_NUMBER == 217:  # reference 2170
        #  <CHAR VAR>  ::=  <PREFIX>  <CHAR ID>  <SUBSCRIPT>
        goto_MOST_IDS = True
    elif PRODUCTION_NUMBER == 218:  # reference 2180
        #  <BIT VAR>  ::=  <PREFIX>  <BIT ID>  <SUBSCRIPT>
        goto_MOST_IDS = True
    # reference 2190 relocated.
    elif PRODUCTION_NUMBER == 220:  # reference 2200
        #  <QUAL STRUCT>  ::=  <STRUCTURE ID>
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.PSEUDO_TYPE_P[g.PTR_TOP] = MAJ_STRUC;
        g.EXT_P[g.PTR_TOP] = g.STACK_PTR[g.SP];
        if g.FIXV[g.MP] == 0: 
            g.FIXV[g.MP] = g.FIXL[g.MP];
            g.FIXL[g.MP] = VAR_LENGTH(g.FIXL[g.MP]);
            SET_XREF(g.FIXL[g.MP], XREF_REF);
        g.LOC_P[g.PTR_TOP] = g.FIXV[g.MP];
        g.INX[g.PTR_TOP] = 0;
        g.VAL_P[g.PTR_TOP] = SHL(NAMING, 8);
        g.PSEUDO_FORM[g.PTR_TOP] = XSYT;
    elif PRODUCTION_NUMBER == 221:  # reference 2210
        #  <QUAL STRUCT>  ::=  <QUAL STRUCT>  .  <STRUCTURE ID>
        g.TEMP = VAR_LENGTH(g.FIXL[g.SP]);
        if g.TEMP > 0: 
            PUSH_INDIRECT(1);
            g.LOC_P[g.PTR_TOP] = g.FIXL[g.SP];
            g.INX[g.PTR_TOP - 1] = 1;
            g.INX[g.PTR_TOP] = 0;
            SET_XREF(g.TEMP, XREF_REF);
            g.FIXL[g.MP] = g.TEMP;
        else:
            g.FIXL[g.MP] = g.FIXL[g.SP];
        g.VAR[g.MP] = g.VAR[g.MP] + PERIOD + g.VAR[g.SP];
        g.TOKEN_FLAGS[g.STACK_PTR[g.MPP1]] = g.TOKEN_FLAGS[g.STACK_PTR[g.MPP1]] | 0x20;
        g.TOKEN_FLAGS[g.EXT_P[g.PTR[g.MP]]] = g.TOKEN_FLAGS[g.EXT_P[g.PTR[g.MP]]] | 0x20;
        g.EXT_P[g.PTR[g.MP]] = g.STACK_PTR[g.SP];
    elif PRODUCTION_NUMBER == 222:  # reference 2220
        #  <PREFIX>  ::=  <EMPTY>
        DO;
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.VAL_P[g.PTR_TOP] = SHL(NAMING, 8);
        g.INX[g.PTR_TOP] = 0;
        g.FIXL[g.MP], g.FIXV[g.MP] = 0;
        END;
    elif PRODUCTION_NUMBER == 223:  # reference 2230
        #  <PREFIX>  ::=  <QUAL STRUCT>  .
        g.TOKEN_FLAGS[g.STACK_PTR[g.SP]] = g.TOKEN_FLAGS[g.STACK_PTR[g.SP]] | 0x20;
    elif PRODUCTION_NUMBER == 224:  # reference 2240
        # <SUBBIT HEAD>::= <SUBBIT KEY> <SUBSCRIPT>(
        g.PTR[g.MP], g.TEMP = g.PTR[g.MPP1];
        g.LOC_P[g.TEMP] = 0;
        if g.INX[g.TEMP] > 0: 
            if g.PSEUDO_LENGTH[g.TEMP] >= 0 | g.VAL_P[g.TEMP] >= 0: 
                ERROR(d.CLASS_QS, 12);
            if g.PSEUDO_FORM[g.TEMP] != 0: 
                ERROR(d.CLASS_QS, 13);
            if g.INX[g.TEMP] != 1: 
                g.INX[g.TEMP] = 1;
                ERROR(d.CLASS_QS, 11);
    elif PRODUCTION_NUMBER == 225:  # reference 2250
        # <SUBBIT KEY> ::= SUBBIT
        g.NAMING = g.FALSE;
        g.VAR[g.MP] = 'SUBBIT PSEUDO-VARIABLE';
    elif PRODUCTION_NUMBER == 226:  # reference 2260
        #  <SUBSCRIPT> ::= <SUB HEAD> )
        g.SUB_END_PTR = g.STMT_PTR;
        if SUB_SEEN == 0: 
            ERROR(d.CLASS_SP, 6);
        goto_SS_CHEX = True
    elif PRODUCTION_NUMBER == 227:  # reference 2270
        #  <SUBSCRIPT>  ::=  <QUALIFIER>
        g.SUB_END_PTR = g.STMT_PTR;
        g.SUB_COUNT = 0;
        g.FIXL[g.MP] = 0;
        g.STRUCTURE_SUB_COUNT = 0;
        g.ARRAY_SUB_COUNT(0);
    # reference 2280 relocated.
    elif PRODUCTION_NUMBER == 229:  # reference 2290
        # <SUBSCRIPT> ::= <$> <ARITH VAR>
        g.SUB_END_PTR = g.STMT_PTR;
        IORS(g.SP);
        SET_XREF_RORS(g.MPP1);
        goto_SIMPLE_SUBS = True;
    elif PRODUCTION_NUMBER == 230:  # reference 2300
        #  <SUBSCRIPT>  ::=  <EMPTY>
        g.FIXL[g.MP] = 0;
        goto_SS_FIXUP = True
    # reference 2310 relocated
    elif PRODUCTION_NUMBER == 232:  # reference 2320
        #  <SUB START>  ::=  <$>  (  @  <PREC SPEC>  ,
        g.PSEUDO_FORM[g.PTR[g.MP]] = g.PTR[g.MP + 3];
        goto_SUB_START = True
    elif PRODUCTION_NUMBER == 233:  # reference 2330
        #  <SUB START> ::= <SUB HEAD> ;
        if STRUCTURE_SUB_COUNT >= 0: 
            ERROR(d.CLASS_SP, 1);
        if SUB_SEEN: 
            g.STRUCTURE_SUB_COUNT = SUB_COUNT;
        else:
            ERROR(d.CLASS_SP, 4);
        g.SUB_SEEN = 1;
    elif PRODUCTION_NUMBER == 234:  # reference 2340
        #  <SUB START> ::= <SUB HEAD> :
        if STRUCTURE_SUB_COUNT == -1: 
            g.STRUCTURE_SUB_COUNT = 0;
        if g.ARRAY_SUB_COUNT() >= 0: 
            ERROR(d.CLASS_SP, 2);
        if SUB_SEEN: 
            g.ARRAY_SUB_COUNT(SUB_COUNT - STRUCTURE_SUB_COUNT);
        else:
            ERROR(d.CLASS_SP, 3);
        g.SUB_SEEN = 1;
    elif PRODUCTION_NUMBER == 235:  # reference 2350
        #  <SUB START> ::= <SUB HEAD> ,
        if SUB_SEEN: 
            pass;
        else:
            ERROR(d.CLASS_SP, 5);
        g.SUB_SEEN = 0;
    elif PRODUCTION_NUMBER == 236:  # reference 2360
        #  <SUB HEAD> ::= <SUB START>
        if SUB_SEEN: SUB_SEEN = 2;
    elif PRODUCTION_NUMBER == 237:  # reference 2370
        #  <SUB HEAD> ::= <SUB START> <SUB>
        g.SUB_SEEN = 1;
        g.SUB_COUNT = SUB_COUNT + 1 ;
    elif PRODUCTION_NUMBER == 238:  # reference 2380
        #  <SUB> ::= <SUB EXP>
        g.INX[g.PTR[g.MP]] = 1;
    elif PRODUCTION_NUMBER == 239:  # reference 2390
        # <SUB> ::= *
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.INX[g.PTR[g.MP]] = 0;
        g.PSEUDO_FORM[g.PTR[g.MP]] = XAST;
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = 0;
        g.VAL_P[g.PTR[g.MP]] = 0;
        g.LOC_P[g.PTR[g.MP]] = 0;
    elif PRODUCTION_NUMBER == 240:  # reference 2400
        # <SUB> ::= <SUB RUN HEAD><SYB EXP>
        g.INX[g.PTR[g.MP]] = 2;
        g.INX[g.PTR[g.SP]] = 2;
    elif PRODUCTION_NUMBER == 241:  # reference 2410
        # <SUB> ::= <ARITH EXP> AT <SUB EXP>
        IORS(g.MP);
        g.INX[g.PTR[g.MP]] = 3;
        g.INX[g.PTR[g.SP]] = 3;
        g.VAL_P[g.PTR[g.MP]] = 0;
        g.PTR[g.MPP1] = g.PTR[g.SP];
    elif PRODUCTION_NUMBER == 242:  # reference 2420
        # <SUB RUN HEAD> ::= <SUB EXP> TO
        pass;
    elif PRODUCTION_NUMBER == 243:  # reference 2430
        # <SUB EXP> ::= <ARITH EXP>
        IORS(g.MP);
        g.VAL_P[g.PTR[g.MP]] = 0;
    elif PRODUCTION_NUMBER == 244:  # reference 2440
        # <SUB EXP> ::= <# EXPRESSION>
        if g.FIXL[g.MP] == 1: 
            g.PTR[g.MP] = PUSH_INDIRECT(1);
            g.PSEUDO_FORM[g.PTR[g.MP]] = 0;  #  MUSNT FALL IN LIT OR VAC
            g.PSEUDO_TYPE_P[g.PTR[g.MP]] = INT_TYPE;
        g.VAL_P[g.PTR[g.MP]] = g.FIXL[g.MP];
    elif PRODUCTION_NUMBER == 245:  # reference 2450
        #  <# EXPRESSION>  ::=  #
        g.FIXL[g.MP] = 1;
    # reference 2460 relocated
    elif PRODUCTION_NUMBER == 247:  # reference 2470
        # <# EXPRESSION> ::= <# EXPRESSION> -1 <TERM>
        g.TEMP = 1;
        goto_SHARP_EXP = True
    elif PRODUCTION_NUMBER == 248:  # reference 2480
        # <=1> ::= =
        if ARRAYNESS_FLAG: SAVE_ARRAYNESS();
        g.ARRAYNESS_FLAG = 0;
    # reference 2490 relocated.
    elif PRODUCTION_NUMBER == 250:  # reference 2500
        # <AND> ::= &
        pass
    elif PRODUCTION_NUMBER == 251:  # reference 2510
        # <AND> ::= AND
        pass
    elif PRODUCTION_NUMBER == 252:  # reference 2520
        # <OR> ::= |
        pass
    elif PRODUCTION_NUMBER == 253:  # reference 2530
        # <OR> ::= OR
        pass
    elif PRODUCTION_NUMBER == 254:  # reference 2540
        # <NOT> ::= not 
        pass
    elif PRODUCTION_NUMBER == 255:  # reference 2550
        # <NOT> ::= NOT
        pass
    elif PRODUCTION_NUMBER == 256:  # reference 2560
        # <CAT> ::= +
        pass
    elif PRODUCTION_NUMBER == 257:  # reference 2570
        # <CAT> ::= CAT
        pass
    elif PRODUCTION_NUMBER == 258:  # reference 2580
        #  <QUALIFIER>  ::=  <$>  (  @  <PREC SPEC>  )
        g.PSEUDO_FORM[g.PTR[g.MP]] = g.PTR[g.MP + 3];
        goto_SS_CHEX = True;
    elif PRODUCTION_NUMBER == 259:  # reference 2590
        #  <QUALIFIER> ::= <$> ( <SCALE HEAD> <ARITH EXP> )
        g.PSEUDO_FORM[g.PTR[g.MP]] = 0xF0;
        g.INX[g.PTR[g.SP - 1]] = g.PTR[g.SP - 2];
        goto_SS_CHEX = True;
    elif PRODUCTION_NUMBER == 260:  # reference 2600
        # <QUALIFIER>::=<$>(@<PREC SPEC>,<SCALE HEAD><ARITH EXP>)
        g.PSEUDO_FORM[g.PTR[g.MP]] = 0xF0 | g.PTR[g.MP + 3];
        g.INX[g.PTR[g.SP - 1]] = g.PTR[g.SP - 2];
        goto_SS_CHEX = True;
    elif PRODUCTION_NUMBER == 261:  # reference 2610
        #  <SCALE HEAD>  ::=  @
        g.PTR[g.MP] = 0;
    elif PRODUCTION_NUMBER == 262:  # reference 2620
        #  <SCALE HEAD> ::=  @ @
        g.PTR[g.MP] = 1;
    # reference 2630 relocated.
    elif PRODUCTION_NUMBER == 264:  # reference 2640
        #  <RADIX> ::= HEX
        g.TEMP3 = 4;
    elif PRODUCTION_NUMBER == 265:  # reference 2650
        #  <RADIX> ::= OCT
        g.TEMP3 = 3;
    elif PRODUCTION_NUMBER == 266:  # reference 2660
        #  <RADIX> ::= BIN
        g.TEMP3 = 1;
    elif PRODUCTION_NUMBER == 267:  # reference 2670
        # <RADIX> ::= DEC
        g.TEMP3 = 0;
    elif PRODUCTION_NUMBER == 268:  # reference 2680
        #  <BIT CONST HEAD> ::= <RADIX>
        g.FIXL[g.MP] = 1;
    elif PRODUCTION_NUMBER == 269:  # reference 2690
        #  <BIT CONST HEAD>  ::=  <RADIX>  (  <NUMBER>  )
        g.TOKEN_FLAGS[g.STACK_PTR[g.SP]] = g.TOKEN_FLAGS[g.STACK_PTR[g.SP]] | 0x20;
        if g.FIXV[g.MP + 2] == 0:
            ERROR(d.CLASS_LB, 8);
            g.FIXL[g.MP] = 1;
        else:
            g.FIXL[g.MP] = g.FIXV[g.MP + 2];
    # reference 2700 relocated.
    # reference 2170 relocated.
    elif PRODUCTION_NUMBER == 272:  # reference 2720
        # <BIT CONST> ::= FALSE
        g.TEMP_SYN = 0;
        goto_DO_BIT_CONST = True
    elif PRODUCTION_NUMBER == 273:  # reference 2730
        # <BIT CONST> ::= ON
        g.TEMP_SYN = 1;
        goto_DO_BIT_CONST = True
    elif PRODUCTION_NUMBER == 274:  # reference 2740
        # <BIT CONST> ::= OFF
        g.TEMP_SYN = 0;
        goto_DO_BIT_CONST = True
    # reference 2750 relocated
    elif PRODUCTION_NUMBER == 276:  # reference 2760
        #  <CHAR CONST>  ::=  CHAR  (  <NUMBER>  )  <CHAR STRING>
        g.TOKEN_FLAGS[g.STACK_PTR[g.SP - 1]] = g.TOKEN_FLAGS[g.STACK_PTR[g.SP - 1]] | 0x20;
        g.VAR[g.MP] = g.VAR[g.SP];
        g.TEMP = g.FIXV[g.MP + 2];
        if g.TEMP < 1: 
            ERROR(d.CLASS_LS, 2);
        else:
            while g.TEMP > 1:
                g.TEMP = g.TEMP - 1;
                g.TEMP2 = CHAR_LENGTH_LIM - LENGTH(g.VAR[g.MP]);
                if TEMP2 < g.FIXV[g.SP]: 
                    g.TEMP = 0;
                    ERROR(d.CLASS_LS, 1);
                    g.S = SUBSTR(g.VAR[g.SP], 0, TEMP2);
                    g.VAR[g.MP] = g.VAR[g.MP] + S;
                else:
                    g.VAR[g.MP] = g.VAR[g.MP] + g.VAR[g.SP];
        goto_CHAR_LITS = True
    # reference 2770 relocated
    elif PRODUCTION_NUMBER == 278:  # reference 2780
        #  <IO CONTROL>  ::=  TAB  (  <ARITH EXP>  )
        g.TEMP = 1;
        goto_IO_CONTROL = True
    elif PRODUCTION_NUMBER == 279:  # reference 2790
        #  <IO CONTROL>  ::=  COLUMN  (  <ARITH EXP>  )
        g.TEMP = 2;
        goto_IO_CONTROL = True
    elif PRODUCTION_NUMBER == 280:  # reference 2800
        #  <IO CONTROL>  ::=  LINE  (  <ARITH EXP>  )
        g.TEMP = 4;
        goto_IO_CONTROL = True
    elif PRODUCTION_NUMBER == 281:  # reference 2810
        #  <IO CONTROL>  ::=  PAGE  (  <ARITH EXP>  )
        g.TEMP = 5;
        goto_IO_CONTROL = True
    # reference 2820 relocated
    elif PRODUCTION_NUMBER == 283:  # reference 2830
        #  <READ PHRASE>  ::=  <READ PHRASE>  ,  <READ ARG>
        goto_CHECK_READ = True
    elif PRODUCTION_NUMBER == 284:  # reference 2840
        #  <WRITE PHRASE>  ::=  <WRITE KEY>  <WRITE ARG>
        pass;
    elif PRODUCTION_NUMBER == 285:  # reference 2850
        #  <WRITE PHRASE>  ::=  <WRITE PHRASE>  ,  <WRITE ARG>
        pass;
    # reference 2860 relocated
    elif PRODUCTION_NUMBER == 287:  # reference 2870
        #  <READ ARG>  ::=  <IO CONTROL>
        goto_EMIT_IO_ARG = True
    elif PRODUCTION_NUMBER == 288:  # reference 2880
        #  <WRITE ARG>  ::=  <EXPRESSION>
        g.TEMP = 0;
        goto_EMIT_IO_ARG = True
    elif PRODUCTION_NUMBER == 289:  # reference 2890
        #  <WRITE ARG>  ::=  <IO CONTROL>
        goto_EMIT_IO_ARG = True
    # reference 2900 relocated
    elif PRODUCTION_NUMBER == 291:  # reference 2910
        #  <READ KEY>  ::=  READALL  (  <NUMBER>  )
        g.TEMP = 1;
        goto_EMIT_IO_HEAD = True
    elif PRODUCTION_NUMBER == 292:  # reference 2920
        #  <WRITE KEY>  ::=  WRITE  (  <NUMBER>  )
        g.TEMP = 2;
        goto_EMIT_IO_HEAD = True
    # reference 2930 has been relocated.
    elif PRODUCTION_NUMBER == 294:  # reference 2940
        #  <BLOCK BODY>  ::= <EMPTY>
        HALMAT_POP(XEDCL, 0, XCO_N, 0);
        goto_CHECK_DECLS = True
    if goto_CHECK_DECLS or PRODUCTION_NUMBER == 295:  # reference 2950
        #  <BLOCK BODY>  ::=  <DECLARE GROUP>
        if not goto_CHECK_DECLS:
            HALMAT_POP(XEDCL, 0, XCO_N, 1);
        goto_CHECK_DECLS = False
        g.I = g.BLOCK_MODE[g.NEST];
        if (I == FUNC_MODE) or (I == PROC_MODE): 
            g.J = g.BLOCK_SYTREF[g.NEST];  # PROC FUNC NAME
            if SYT_PTR(J) != 0: 
                g.J = SYT_PTR(J);  # POINT TO FIRST ARG
                while (g.SYT_FLAGS(J) & PARM_FLAGS) != 0:
                    if (g.SYT_FLAGS(J) & IMP_DECL) != 0:
                        # UNDECLARED PARAMETER
                        ERROR(d.CLASS_DU, 2, SYT_NAME(J));
                        g.PARMS_PRESENT = 0;
                        g.SYT_TYPE(J, DEFAULT_TYPE);
                        g.SYT_FLAGS(J, g.SYT_FLAGS(J) | DEFAULT_ATTR);
                    g.J = J + 1;  # NEXT PARAMETER
                if (EXTERNAL_MODE > 0) and (EXTERNAL_MODE < CMPL_MODE):
                    while J <= g.NDECSY():
                        if SYT_CLASS(J) < REPL_ARG_CLASS:
                            ERROR(d.CLASS_DU, 3, SYT_NAME(J));
                            g.SYT_FLAGS(J, g.SYT_FLAGS(J) | DUMMY_FLAG);
                    g.J = J + 1;
                END;
        if EXTERNALIZE: 
            g.EXTERNALIZE = 4;
        g.PTR[g.MP] = 0;
    elif PRODUCTION_NUMBER == 296:  # reference 2960
        #  <BLOCK BODY>  ::=  <BLOCK BODY>  <ANY STATEMENT>
        g.PTR[g.MP] = 1;
    # reference 2970 relocated
    elif PRODUCTION_NUMBER == 298:  # reference 2980
        #  <ARITH INLINE DEF>  ::=  FUNCTION  ;
        g.TYPE = DEFAULT_TYPE;
        g.ATTRIBUTES = DEFAULT_ATTR & SD_FLAGS;
        g.TEMP = 0;
        g.INLINE_DEFS = True
    elif PRODUCTION_NUMBER == 299:  # reference 2990
        #  <BIT INLINE DEF>  ::=  FUNCTION <BIT SPEC>  ;
        g.TEMP = BIT_LENGTH;
        goto_INLINE_DEFS = True
    elif PRODUCTION_NUMBER == 300:  # reference 3000
        #  <CHAR INLINE DEF>  ::=  FUNCTION <CHAR SPEC>  ;
        if CHAR_LENGTH < 0:
            ERROR(d.CLASS_DS, 3);
            g.TEMP = DEF_CHAR_LENGTH;
        else:
            g.TEMP = CHAR_LENGTH;
        goto_INLINE_DEFS = True
    elif PRODUCTION_NUMBER == 301:  # reference 3010
        #  <STRUC INLINE DEF>  ::=  FUNCTION <STRUCT SPEC>  ;
        if STRUC_DIM != 0: 
            ERROR(d.CLASS_DD, 12);
            g.STRUC_DIM = 0;
        g.TEMP = STRUC_PTR;
        g.TYPE = MAJ_STRUC;
        goto_INLINE_DEFS = True
    elif PRODUCTION_NUMBER == 302:  # reference 3020
        #  <BLOCK STMT>  ::=  <BLOCK STMT TOP>  ;
        OUTPUT_WRITER();
        if PARMS_PRESENT <= 0: 
            if EXTERNALIZE: EXTERNALIZE = 4;
        g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
        if TPL_REMOTE:
            if EXTERNAL_MODE > 0 and g.NEST == 1 and g.BLOCK_MODE[g.NEST] == CMPL_MODE:
                g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | REMOTE_FLAG);
            else:
                ERROR(d.CLASS_PS, 13);
        g.TPL_REMOTE = g.FALSE;
        EMIT_SMRK();
    elif PRODUCTION_NUMBER == 303:  # reference 3030
        #  <BLOCK STMT TOP> ::= <BLOCK STMT TOP> ACCESS
        if g.BLOCK_MODE[g.NEST] > PROG_MODE:
            ERROR(d.CLASS_PS, 3);
        elif g.NEST != 1: 
            ERROR(d.CLASS_PS, 4);
        elif (g.SYT_FLAGS(g.FIXL[g.MP]) & ACCESS_FLAG) != 0: 
            ERROR(d.CLASS_PS, 10);
        else:
            g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | ACCESS_FLAG);
            g.ACCESS_FOUND = g.TRUE;
    elif PRODUCTION_NUMBER == 304:  # reference 3040
        #  <BLOCK STMT TOP>  ::= <BLOCK STMT TOP> RIGID
        if g.BLOCK_MODE[g.NEST] != CMPL_MODE: 
            ERROR(d.CLASS_PS, 12);
        elif (g.SYT_FLAGS(g.FIXL[g.MP]) and RIGID_FLAG) != 0: 
            ERROR(d.CLASS_PS, 11);
        else:
            g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | RIGID_FLAG);
    elif PRODUCTION_NUMBER == 305:  # reference 3050
        #  <BLOCK STMT TOP>  ::=  <BLOCK STMT HEAD>
        pass;
    elif PRODUCTION_NUMBER == 306:  # reference 3060
        #  <BLOCK STMT TOP>  ::=  <BLOCK STMT HEAD>  EXCLUSIVE
        if g.BLOCK_MODE[g.NEST] > FUNC_MODE: 
            ERROR(d.CLASS_PS, 2, 'EXCLUSIVE');
        g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | EXCLUSIVE_FLAG);
    elif PRODUCTION_NUMBER == 307:  # reference 3070
        #  <BLOCK STMT TOP>  ::=  <BLOCK STMT HEAD>  REENTRANT
        if g.BLOCK_MODE[g.NEST] > FUNC_MODE: 
            ERROR(d.CLASS_PS, 2, 'REENTRANT');
        g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | REENTRANT_FLAG);
    elif PRODUCTION_NUMBER == 308:  # reference 3080
        #  <LABEL DEFINITION>  ::=  <LABEL>  :
        if g.NEST == 0: 
            g.EXTERNAL_MODE = 0;
        HALMAT_POP(g.XLBL, 1, g.XCO_N, 0);
        HALMAT_PIP(g.FIXL[g.MP], g.XSYT, 0, 0);
        g.TEMP = g.FIXL[g.MP];
        if g.SYT_TYPE(g.TEMP) != g.IND_CALL_LAB: 
            if g.SYT_LINK1(g.TEMP) > 0: 
                if g.DO_LEVEL > 0:
                    if g.DO_STMTp[g.DO_LEVEL] > g.SYT_LINK1(g.TEMP):
                        if g.SYT_TYPE(g.TEMP) == g.STMT_LABEL: 
                            ERROR(d.CLASS_GL, 2);
                        else:
                            ERROR(d.CLASS_PL, 10);
            if g.SYT_LINK1(g.TEMP) >= 0: 
                g.SYT_LINK1(g.TEMP, -g.DO_LEVEL);
                g.SYT_LINK2(g.TEMP, g.SYT_LINK2(0));
                g.SYT_LINK2(0, g.TEMP);
        g.LABEL_COUNT = g.LABEL_COUNT + 1;
        if g.SIMULATING: 
            STAB_LAB(g.FIXL[g.MP]);
        g.GRAMMAR_FLAGS[g.STACK_PTR[g.MP]] = \
            g.GRAMMAR_FLAGS[g.STACK_PTR[g.MP]] | g.LABEL_FLAG;
        # IF THE XREF ENTRY IS FOR THE LABEL'S DEFINITION (FLAG=0),
        # THEN CHECK THE STATEMENT NUMBER.  IF IT IS NOT EQUAL TO CURRENT
        # STATEMENT NUMBER, CHANGE IT TO THE CURRENT STATEMENT NUMBER.
        if (SHR(g.XREF(g.SYT_XREF(g.FIXL[g.MP])), 13) & 7) == 0:
            if (g.XREF(g.SYT_XREF(g.FIXL[g.MP])) & g.XREF_MASK) != g.STMT_NUM():
                g.XREF(g.SYT_XREF(g.FIXL[g.MP]), \
                    (g.XREF(g.SYT_XREF(g.FIXL[g.MP])) & 0xFFFFE000) | g.STMT_NUM());
        if g.SYT_TYPE(g.FIXL[g.MP]) == g.STMT_LABEL:
            g.NO_NEW_XREF = g.TRUE;
            SET_XREF(g.FIXL[g.MP], 0);
    elif PRODUCTION_NUMBER == 309:  # reference 3090
        #  <LABEL EXTERNAL>  ::=  <LABEL DEFINITION>
        pass;
    elif PRODUCTION_NUMBER == 310:  # reference 3100
        #  <LABEL EXTERNAL>  ::=  <LABEL DEFINITION>  EXTERNAL
        if g.NEST > 0: 
            ERROR(d.CLASS_PE, 1);
        else:
            g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | EXTERNAL_FLAG);
            g.EXTERNAL_MODE = 1;  # JUST A FLAG FOR NOW
            if g.BLOCK_MODE[0] > 0: 
                ERROR(d.CLASS_PE, 2);
            if g.SIMULATING:
                g.STAB2_STACKTOP = STAB2_STACKTOP - 1;
                g.SIMULATING = 2;
    # reference 3110 relocated
    elif PRODUCTION_NUMBER == 312:  # reference 3120
        #  <BLOCK STMT HEAD>  ::=  <LABEL EXTERNAL>  COMPOOL
        g.TEMP = XCDEF;
        g.TEMP2 = CMPL_MODE;
        g.PARMS_PRESENT = 1;  #  FIX SO ALL DECLARES EMITTED IN CMPL TEMPLATE
        SET_LABEL_TYPE(g.FIXL[g.MP], COMPOOL_LABEL);
        # THIS IS A COMPOOL COMPILATION
        # CHECK IF #D OPTION IS ON.   EMIT FATAL ERROR IF ITS.
        # TURN OFF DATA REMOTE TO ALLOW FOR FUTURE DOWNGRADE OF
        # THE ERROR
        # PART 1. ALSO CHECK IF COMPOOL IS NOT
        #         EXTERNAL BEFORE EMITTING THE XR2 ERROR.
        if DATA_REMOTE and (EXTERNAL_MODE == 0):
            ERROR(d.CLASS_XR, 2);
            g.DATA_REMOTE = g.FALSE;
        if EXTERNAL_MODE > 0: 
            if g.NEST == 0: 
                g.EXTERNAL_MODE = TEMP2;
            goto_NEW_SCOPE = True
        else:
            goto_OUTERMOST_BLOCK = True
    elif PRODUCTION_NUMBER == 313:  # reference 3130
        #  <BLOCK STMT HEAD>  ::=  <LABEL DEFINITION>  TASK
        g.TEMP = XTDEF;
        g.TEMP2 = TASK_MODE;
        SET_LABEL_TYPE(g.FIXL[g.MP], TASK_LABEL);
        g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | LATCHED_FLAG);
        if g.NEST == 1:
            if g.BLOCK_MODE[1] == PROG_MODE: 
                if g.DO_LEVEL > 1: 
                    ERROR(d.CLASS_PT, 2);
                goto_NEW_SCOPE = True
        if not goto_NEW_SCOPE:
            ERROR(d.CLASS_PT, 1);
            if g.NEST == 0: 
                goto_DUPLICATE_BLOCK = True
            else:
                goto_NEW_SCOPE = True
    # reference 3140 relocated
    elif PRODUCTION_NUMBER == 315:  # reference 3150
        #  <BLOCK STMT HEAD>  ::=  UPDATE
        g.VAR[g.MPP1] = g.VAR[g.MP];
        g.IMPLIED_UPDATE_LABEL = IMPLIED_UPDATE_LABEL + 1;
        g.VAR[g.MP] = l.UPDATE_NAME + IMPLIED_UPDATE_LABEL;
        g.NAME_HASH = HASH(g.VAR[g.MP], SYT_HASHSIZE);
        g.I = ENTER(g.VAR[g.MP], LABEL_CLASS);
        g.FIXL[g.MP] = I;
        g.SYT_TYPE(I, UNSPEC_LABEL);
        g.SYT_FLAGS(I, g.SYT_FLAGS(I) | DEFINED_LABEL);
        g.VAR_LENGTH(I, 2);
        if g.SIMULATING: 
            STAB_LAB(g.FIXL[g.MP]);
        goto_UPDATE_HEAD = True
    # reference 3160 relocated
    elif PRODUCTION_NUMBER == 317:  # reference 3170
        #  <BLOCK STMT HEAD>  ::=  <FUNCTION NAME>  <FUNC STMT BODY>
        goto_FUNC_HEADER = True
    elif PRODUCTION_NUMBER == 318:  # reference 3180
        #  <BLOCK STMT HEAD>  ::=  <PROCEDURE NAME>
        g.PARMS_WATCH = g.FALSE;
        if MAIN_SCOPE == g.SCOPEp: 
            g.COMSUB_END(g.FIXL[g.MP]);
    elif PRODUCTION_NUMBER == 319:  # reference 3190
        #  <BLOCK STMT HEAD>  ::=  <PROCEDURE NAME>  <PROC STMT BODY>
        pass;
    elif PRODUCTION_NUMBER == 320:  # reference 3200
        #  <FUNCTION NAME>  ::=  <LABEL EXTERNAL>  FUNCTION
        g.ID_LOC = g.FIXL[g.MP];
        g.FACTORING = g.FALSE;
        if SYT_CLASS(ID_LOC) != FUNC_CLASS:
            if SYT_CLASS(ID_LOC) != LABEL_CLASS or g.SYT_TYPE(ID_LOC) != UNSPEC_LABEL:
                ERROR(d.CLASS_PL, 4);
            else:
                g.SYT_CLASS(ID_LOC, FUNC_CLASS);
                g.SYT_TYPE(ID_LOC, 0);
        g.TEMP = XFDEF;
        g.TEMP2 = FUNC_MODE;
        goto_PROC_FUNC_HEAD = True
    # reference 3210 relocated
    elif PRODUCTION_NUMBER == 322:  # reference 3220
        #  <FUNC STMT BODY>  ::=  <PARAMETER LIST>
        pass;
    elif PRODUCTION_NUMBER == 323:  # reference 3230
        #  <FUNC STMT BODY>  ::=  <TYPE SPEC>
        pass;
    elif PRODUCTION_NUMBER == 324:  # reference 3240
        #  <FUNC STMT BODY>  ::=  <PARAMETER LIST>  <TYPE SPEC>
        pass;
    elif PRODUCTION_NUMBER == 325:  # reference 3250
        #  <PROC STMT BODY>  ::=  <PARAMETER LIST>
        pass;
    elif PRODUCTION_NUMBER == 326:  # reference 3260
        #  <PROC STMT BODY>  ::=  <ASSIGN LIST>
        pass;
    elif PRODUCTION_NUMBER == 327:  # reference 3270
        #  <PROC STMT BODY>  ::=  <PARAMETER LIST>  < ASSIGN LIST>
        pass;
    elif PRODUCTION_NUMBER == 328:  # reference 3280
        #  <PARAMETER LIST>  ::=  <PARAMETER HEAD>  <IDENTIFIER>  )
        g.PARMS_PRESENT = PARMS_PRESENT + 1;
    elif PRODUCTION_NUMBER == 329:  # reference 3290
        #  <PARAMETER HEAD>  ::=  (
        pass;
    elif PRODUCTION_NUMBER == 330:  # reference 3300
        #  <PARAMETER HEAD>  ::=  <PARAMETER HEAD>  <IDENTIFIER>  ,
        g.PARMS_PRESENT = PARMS_PRESENT + 1;
    elif PRODUCTION_NUMBER == 331:  # reference 3310
        #  <ASSIGN LIST>  ::=  <ASSIGN>  <PARAMETER LIST>
        pase;
    elif PRODUCTION_NUMBER == 332:  # reference 3320
        #  <ASSIGN>  ::=  ASSIGN
        if CONTEXT == PARM_CONTEXT: 
            g.CONTEXT = ASSIGN_CONTEXT;
        else:
            g.ASSIGN_ARG_LIST = g.TRUE;
    elif PRODUCTION_NUMBER == 333:  # reference 3330
        #  <DECLARE ELEMENT>  ::=  <DECLARE STATEMENT>
        g.STMT_TYPE = DECL_STMT_TYPE;
        if g.SIMULATING: 
            STAB_HDR();
        EMIT_SMRK(1);
    # reference 3340 relocated.
    elif PRODUCTION_NUMBER == 335:  # reference 3350
        #  <DECLARE ELEMENT>  ::=  <STRUCTURE STMT>
        g.SYT_ADDR(REF_ID_LOC, STRUC_SIZE);
        g.REF_ID_LOC = 0;
        g.STMT_TYPE = STRUC_STMT_TYPE;
        if g.SIMULATING: 
            STAB_HDR();
        goto_EMIT_NULL = True;
    elif PRODUCTION_NUMBER == 336:  # reference 3360
        #  <DECLARE ELEMENT>  ::=  EQUATE  EXTERNAL  <IDENTIFIER>  TO <VARIABLE>  ;
        g.I = g.FIXL[g.MP + 2];  # EQUATE NAME
        g.J = g.SP - 1;
        if SYT_CLASS(g.FIXL[J]) == TEMPLATE_CLASS:
            g.J = g.FIXV[J];  # ROOT PTR SAVED IN FIXV FOR STRUCS
        else:
            g.J = g.FIXL[J];  # SYT PTR IN FIXL FOR OTHERS
        g.SYT_PTR(I, J);  # POINT AT REFERENCED ITEM
        if (g.SYT_FLAGS(g.BLOCK_SYTREF[g.NEST]) & EXTERNAL_FLAG) != 0:
            g.SYT_FLAGS(I, g.SYT_FLAGS(I) | DUMMY_FLAG);  # IGNORE IN TEMPLATES
        if SYT_SCOPE(I) != SYT_SCOPE(J):
            ERROR(d.CLASS_DU, 7, g.VAR[g.SP - 1]);
        if g.SYT_TYPE(J) > MAJ_STRUC:
            ERROR(d.CLASS_DU, 8, g.VAR[g.SP - 1]);
        if (g.SYT_FLAGS(J) & ILL_EQUATE_ATTR) != 0:
            ERROR(d.CLASS_DU, 9, g.VAR[g.SP - 1]);
        if (g.SYT_FLAGS(J) & AUTO_FLAG) != 0:
            if (g.SYT_FLAGS(g.BLOCK_SYTREF[g.NEST]) & REENTRANT_FLAG) != 0:
                ERROR(d.CLASS_DU, 13, g.VAR[g.SP - 1]);
        g.TEMP = g.PTR[g.SP - 1];
        if (g.VAL_P[g.TEMP] & 0x40) != 0:
            ERROR(d.CLASS_DU, 10, g.VAR[g.SP - 1]);  # PREC MODIFIER
        if (g.VAL_P[g.TEMP] & 0x80) != 0:
            ERROR(d.CLASS_DU, 11, g.VAR[g.MP + 2]);  # SUBBIT
        if KILL_NAME(g.SP - 1):
            ERROR(d.CLASS_DU, 14, g.VAR[g.MP + 2]);  # NAME(.)
        else:
            RESET_ARRAYNESS();
        if (g.VAL_P[g.TEMP] & 0x20) != 0:
            HALMAT_FIX_PIPTAGS(g.INX[g.TEMP], 0, 1);
        DELAY_CONTEXT_CHECK, NAMING = g.FALSE;
        if SYT_PTR(J) < 0:
            ERROR(d.CLASS_DU, 12, g.VAR[g.SP - 1]);
        HALMAT_POP(XEINT, 2, 0, g.PSEUDO_TYPE_P[g.TEMP]);
        HALMAT_PIP(g.FIXL[g.MP + 2], XSYT, 0, 0);
        HALMAT_PIP(g.LOC_P[g.TEMP], g.PSEUDO_FORM[g.TEMP], 0, 0);
        CHECK_ARRAYNESS();
        g.PTR_TOP = g.PTR[g.SP - 1] - 1;
        g.STMT_TYPE = EQUATE_TYPE;
        if g.SIMULATING: 
            STAB_HDR();
        goto_EMIT_NULL = True;
    elif PRODUCTION_NUMBER == 337:  # reference 3370
        #  <REPLACE STMT>  ::=  REPLACE  <REPLACE HEAD>  BY  <TEXT>
        g.CONTEXT = 0;
        g.MAC_NUM = g.FIXL[g.MPP1];
        g.SYT_ADDR(MAC_NUM, START_POINT);
        g.VAR_LENGTH(MAC_NUM, MACRO_ARG_COUNT);
        g.EXTENT(MAC_NUM, REPLACE_TEXT_PTR);
        g.MACRO_ARG_COUNT = 0;
    # reference 3380 relocated.
    elif PRODUCTION_NUMBER == 339:  # reference 3390
        #  <REPLACE HEAD>  ::=  <IDENTIFIER>  (  <ARG LIST>  )
        g.NOSPACE();
        goto_INIT_MACRO = True
    # reference 3400 relocated
    elif PRODUCTION_NUMBER == 341:  # reference 3410
        #  <ARG LIST>  ::=  <ARG LIST>  ,  <IDENTIFIER>
        goto_NEXT_ARG = True
    elif PRODUCTION_NUMBER == 342:  # reference 3420
        #  <TEMPORARY STMT>  ::=  TEMPORARY  <DECLARE BODY>  ;
        if g.SIMULATING: 
            g.STMT_TYPE = TEMP_TYPE;
        STAB_HDR();
        goto_DECL_STAT = True
    # reference 3430 relocated
    elif PRODUCTION_NUMBER == 344:  # reference 3440
        #  <DECLARE BODY>  ::=  <DECLARATION LIST>
        pass;
    elif PRODUCTION_NUMBER == 345:  # reference 3450
        #  <DECLARE BODY>  ::=  <ATTRIBUTES> , <DECLARATION LIST>
        # Regarding this implementation of the , see the comments in g.py for the 
        # TYPE variable et al.
        g.FACTORED_TYPE = 0
        g.FACTORED_BIT_LENGTH = 0
        g.FACTORED_CHAR_LENGTH = 0
        g.FACTORED_MAT_LENGTH = 0
        g.FACTORED_VEC_LENGTH = 0
        g.FACTORED_ATTRIBUTES = 0
        g.FACTORED_ATTRIBUTES2 = 0
        g.FACTORED_ATTR_MASK = 0
        g.FACTORED_STRUC_PTR = 0
        g.FACTORED_STRUC_DIM = 0
        g.FACTORED_CLASS = 0
        g.FACTORED_NONHAL = 0
        g.FACTORED_LOCKp = 0
        g.FACTORED_IC_PTR = 0
        g.FACTORED_IC_FND = 0
        g.FACTORED_N_DIM = 0
        g.FACTORED_S_ARRAY = [0] * (N_DIM_LIM + 1)
        g.FACTOR_FOUND = g.FALSE;
    elif PRODUCTION_NUMBER == 346:  # reference 3460
        #  <DECLARATION LIST>  ::=  <DECLARATION>
        g.SAVE_INDENT_LEVEL = g.INDENT_LEVEL;
        g.ATTR_FOUND = g.FALSE;
        g.LAST_WRITE = 0;
    elif PRODUCTION_NUMBER == 347:  # reference 3470
        #  <DECLARATION LIST>  ::=  <DCL LIST ,>   <DECLARATION>
        pass;
    elif PRODUCTION_NUMBER == 348:  # reference 3480
        #  <DCL LIST ,>  ::=  <DECLARATION LIST>  ,
        if ATTR_FOUND:
            if ATTR_LOC >= 0:
                if ATTR_LOC != 0:
                    OUTPUT_WRITER(g.LAST_WRITE, ATTR_LOC - 1);
                    if g.INDENT_LEVEL == SAVE_INDENT_LEVEL:
                        g.INDENT_LEVEL = g.INDENT_LEVEL + ATTR_INDENT;
                OUTPUT_WRITER(ATTR_LOC, g.STMT_PTR);
                g.LAST_WRITE = 0;
        else:
            g.ATTR_FOUND = g.TRUE;
            if (g.GRAMMAR_FLAGS[1] & ATTR_BEGIN_FLAG) != 0:
                # <ARRAY, TYPE, & ATTR> FACTORED
                OUTPUT_WRITER(0, g.STACK_PTR[g.MP] - 1);
                g.LAST_WRITE = g.STACK_PTR[g.MP];
                g.INDENT_LEVEL = g.INDENT_LEVEL + ATTR_INDENT + g.INDENT_INCR;
                if ATTR_LOC >= 0:
                    OUTPUT_WRITER(g.STACK_PTR[g.MP], g.STMT_PTR);
                    g.LAST_WRITE = 0;
            else:
                if ATTR_LOC >= 0:
                    OUTPUT_WRITER();
                    g.LAST_WRITE = 0;
                    g.INDENT_LEVEL = g.INDENT_LEVEL + ATTR_INDENT;
        if INIT_EMISSION: 
            g.INIT_EMISSION = g.FALSE;
            EMIT_SMRK(0);
    elif PRODUCTION_NUMBER == 349:  # reference 3490
        #  <DECLARE GROUP>  ::=  <DECLARE ELEMENT>
        pass;
    elif PRODUCTION_NUMBER == 350:  # reference 3500
        #  <DECLARE GROUP>  ::=  <DECLARE GROUP>  <DECLARE ELEMENT>
        pass;
    elif PRODUCTION_NUMBER == 351:  # reference 3510
        #  <STRUCTURE STMT>  ::=  STRUCTURE <STRUCT STMT HEAD> <STRUCT STMT TAIL>
        g.FIXV[g.SP] = 0;
        g.FIXL[g.MP] = g.FIXL[g.MPP1];
        g.FIXV[g.MP] = g.FIXV[g.MPP1];
        g.FIXL[g.MPP1] = g.FIXL[g.SP];
        g.FACTORING = g.TRUE;
        goto_STRUCT_GOING_UP = True
    # reference 3520 relocated
    elif PRODUCTION_NUMBER == 353:  # reference 3530
        #  <STRUCT STMT HEAD>  ::=  <IDENTIFIER> <MINOR ATTR LIST> : <LEVEL>
        goto_NO_ATTR_STRUCT = True
    # reference 3540 was relocated
    elif PRODUCTION_NUMBER == 355:  # reference 3550
        #  <STRUCT STMT TAIL>  ::=  <DECLARATION>  ;
        pass;
    elif PRODUCTION_NUMBER == 356:  # reference 3560
        # <STRUCT SPEC> ::= <STRUCT TEMPLATE> <STRUCT SPEC BODY>
        g.STRUC_PTR = g.FIXL[g.MP];
        if g.SYT_TYPE(STRUC_PTR) != TEMPL_NAME:
            g.SYT_FLAGS(STRUC_PTR, g.SYT_FLAGS(STRUC_PTR) | EVIL_FLAG);
        SET_XREF(STRUC_PTR, XREF_REF);
        g.NOSPACE();
    elif PRODUCTION_NUMBER == 357:  # reference 3570
        # <STRUCT SPEC BODY> ::= - STRUCTURE
        g.NOSPACE();
    elif PRODUCTION_NUMBER == 358:  # reference 3580
        # <STRUCT SPEC BODY> ::= <STRUCT SPEC HEAD> <LITERAL EXP OR*> )
        g.CONTEXT = DECLARE_CONTEXT;
        g.I = g.FIXV[g.MPP1];
        if not ((I > 1) and (I <= ARRAY_DIM_LIM) or (I == -1)):
            ERROR(d.CLASS_DD, 11);
            g.STRUC_DIM = 2;  # A DEFAULT
        else:
            g.STRUC_DIM = I;
    elif PRODUCTION_NUMBER == 359:  # reference 3590
        # <STRUCT SPEC HEAD> ::= - STRUCTURE (
        g.NOSPACE();
        g.TOKEN_FLAGS[g.STACK_PTR[g.MPP1]] = g.TOKEN_FLAGS[g.STACK_PTR[g.MPP1]] | 0x20;
    elif PRODUCTION_NUMBER == 360:  # reference 3600
        #  <DECLARATION>  ::=  <NAME ID>
        if not BUILDING_TEMPLATE:
            if NAME_IMPLIED: 
                g.ATTR_LOC = g.STACK_PTR[g.MP];
            else:
                g.ATTR_LOC = -1;
            goto_SPEC_VAR = True
    # reference 3610 relocated.
    elif PRODUCTION_NUMBER == 362:  # reference 3620
        #  <NAME ID>   ::=  <IDENTIFIER>
        g.ID_LOC = g.FIXL[g.MP];
    elif PRODUCTION_NUMBER == 363:  # reference 3630
        #  <NAME ID>  ::=  <IDENTIFIER> NAME
        # REMOVED DN2 ERROR
        g.NAME_IMPLIED = g.TRUE;
        g.ID_LOC = g.FIXL[g.MP];
    elif PRODUCTION_NUMBER == 364:  # reference 3640
        # <ATTRIBUTES> ::= <ARRAY SPEC> <TYPE & MINOR ATTR>
        goto_CHECK_ARRAY_SPEC = True
    # reference 3650 relocated
    # reference 3660 relocated
    elif PRODUCTION_NUMBER == 367:  # reference 3670
        #  <ARRAY SPEC> ::= <ARRAY HEAD> <LITERAL EXP OR *> )
        g.CONTEXT = DECLARE_CONTEXT;
        goto_CHECK_ARRAY_SPEC = True
    elif PRODUCTION_NUMBER == 368:  # reference 3680
        #  <ARRAY SPEC>  ::=  FUNCTION
        g.CLASS = 2;
    elif PRODUCTION_NUMBER == 369:  # reference 3690
        #  <ARRAY SPEC>  ::=  PROCEDURE
        g.TYPE = PROC_LABEL;
        g.CLASS = 1;
    elif PRODUCTION_NUMBER == 370:  # reference 3700
        #  <ARRAY SPEC>  ::= PROGRAM
        g.TYPE = PROG_LABEL;
        g.CLASS = 1;
    elif PRODUCTION_NUMBER == 371:  # reference 3710
        #  <ARRAY SPEC>  ::=  TASK
        g.TYPE = TASK_LABEL;
        g.CLASS = 1;
    elif PRODUCTION_NUMBER == 372:  # reference 3720
        #  <ARRAY HEAD> ::= ARRAY (
        g.STARRED_DIMS = 0
        g.N_DIM = 0;
        for I in range(0, 1 + N_DIM_LIM):
            g.S_ARRAY[I] = 0;
        g.FIXL[g.SP], g.FIXV[g.SP] = ARRAY_FLAG;
        goto_INCORPORATE_ATTR = True;
    # reference 3730 relocated
    elif PRODUCTION_NUMBER == 374:  # reference 3740
        #  <TYPE & MINOR ATTR> ::= <TYPE SPEC>
        goto_SPEC_TYPE = True
    # reference 3750 relocated
    elif PRODUCTION_NUMBER == 376:  # reference 3760
        #  <TYPE & MINOR ATTR> ::= <MINOR ATTR LIST>
        pass;
    elif PRODUCTION_NUMBER == 377:  # reference 3770
        #  <TYPE SPEC> ::= <STRUCT SPEC>
        g.TYPE = MAJ_STRUC;
    elif PRODUCTION_NUMBER == 378:  # reference 3780
        #  <TYPE SPEC>  ::=  <BIT SPEC>
        pass;
    elif PRODUCTION_NUMBER == 379:  # reference 3790
        #  <TYPE SPEC>  ::=  <CHAR SPEC>
        pass;
    elif PRODUCTION_NUMBER == 380:  # reference 3800
        #  <TYPE SPEC>  ::=  <ARITH SPEC>
        pass;
    elif PRODUCTION_NUMBER == 381:  # reference 3810
        #  <TYPE SPEC>  ::=  EVENT
        g.TYPE = EVENT_TYPE;
    elif PRODUCTION_NUMBER == 382:  # reference 3820
        #  <BIT SPEC>  ::=  BOOLEAN
        g.TYPE = BIT_TYPE;
        g.BIT_LENGTH = 1;  # BOOLEAN
    elif PRODUCTION_NUMBER == 383:  # reference 3830
        #  <BIT SPEC>  ::=  BIT  (  <LITERAL EXP OR *>  )
        g.NOSPACE();
        g.CONTEXT = DECLARE_CONTEXT;
        g.J = g.FIXV[g.MP + 2];
        g.K = DEF_BIT_LENGTH;
        if J == -1: 
            ERROR(d.CLASS_DS, 4);  # "*" ILLEGAL
        elif (J <= 0) | (J > BIT_LENGTH_LIM):
            ERROR(d.CLASS_DS, 1);
        else:
            g.K = J;
        g.TYPE = BIT_TYPE;
        g.BIT_LENGTH = K;
    elif PRODUCTION_NUMBER == 384:  # reference 3840
        #  <CHAR SPEC>  ::=  CHARACTER  (  <LITERAL EXP OR *>  )
        g.NOSPACE();
        g.CONTEXT = DECLARE_CONTEXT;
        g.J = g.FIXV[g.MP + 2];
        g.K = DEF_CHAR_LENGTH;
        if J == -1: 
            g.K = J;
        elif (J <= 0) or (J > CHAR_LENGTH_LIM):
            ERROR(d.CLASS_DS, 2);
        else:
            g.K = J;
        g.CHAR_LENGTH = K;
        g.TYPE = CHAR_TYPE;
    elif PRODUCTION_NUMBER == 385:  # reference 3850
        #  <ARITH SPEC>  ::=  <PREC SPEC>
        g.ATTR_MASK = ATTR_MASK | g.FIXL[g.MP];
        g.ATTRIBUTES = ATTRIBUTES | g.FIXV[g.MP];
    elif PRODUCTION_NUMBER == 386:  # reference 3860
        #  <ARITH SPEC>  ::=  <SQ DQ NAME>
        pass;
    elif PRODUCTION_NUMBER == 387:  # reference 3870
        #  <ARITH SPEC>  ::=  <SQ DQ NAME>  <PREC SPEC>
        g.ATTR_MASK = ATTR_MASK | g.FIXL[g.SP];
        g.ATTRIBUTES = ATTRIBUTES | g.FIXV[g.SP];
    elif PRODUCTION_NUMBER == 388:  # reference 3880
        #  <SQ DQ NAME> ::= <DOUBLY QUAL NAME HEAD> <LITERAL EXP OR *> )
        g.CONTEXT = DECLARE_CONTEXT;
        g.I = g.FIXV[g.MPP1];  # VALUE
        g.TYPE = g.FIXL[g.MP];
        if TYPE == g.VEC_TYPE:
            if I == -1:
                ERROR(d.CLASS_DD, 7);
                g.I = 3;
            elif (I <= 1) or (I > VEC_LENGTH_LIM):
                ERROR(d.CLASS_DD, 5);
                g.I = 3;
            g.VEC_LENGTH = I;
        else:  # MATRIX
           if I == -1:
               ERROR(d.CLASS_DD, 9);
               g.I = 3;
           elif (I <= 1) or (I > MAT_DIM_LIM):
               ERROR(d.CLASS_DD, 4);
               g.I = 3;
           g.MAT_LENGTH = SHL(g.FIXV[g.MP], 8) + (I & 0xFF);
    elif PRODUCTION_NUMBER == 389:  # reference 3890
        #  <SQ DQ NAME> ::= INTEGER
        g.TYPE = INT_TYPE;
    elif PRODUCTION_NUMBER == 390:  # reference 3900
        #  <SQ DQ NAME> ::= SCALAR
        g.TYPE = g.SCALAR_TYPE;
    elif PRODUCTION_NUMBER == 391:  # reference 3910
        #  <SQ DQ NAME> ::= VECTOR
        g.TYPE = g.VEC_TYPE;
        g.VEC_LENGTH = DEF_VEC_LENGTH;
    elif PRODUCTION_NUMBER == 392:  # reference 3920
        #  <SQ DQ NAME> ::= MATRIX
        g.TYPE = g.MAT_TYPE;
        g.MAT_LENGTH = DEF_MAT_LENGTH;
    elif PRODUCTION_NUMBER == 393:  # reference 3930
        #  <DOUBLY QUAL NAME HEAD> ::= VECTOR (
        g.NOSPACE();
        g.FIXL[g.MP] = g.VEC_TYPE;
    elif PRODUCTION_NUMBER == 394:  # reference 3940
        #  <DOUBLY QUAL NAME HEAD>  ::=  MATRIX  (  <LITERAL EXP OR *>  ,
        g.NOSPACE();
        g.FIXL[g.MP] = g.MAT_TYPE;
        g.I = g.FIXV[g.MP + 2];
        g.FIXV[g.MP] = 3;  # DEFAULT IF BAD SPEC FOLLOWS
        if I == -1: 
            ERROR(d.CLASS_DD, 9);
        elif (I <= 1) or (I > MAT_DIM_LIM):
            ERROR(d.CLASS_DD, 4);
        else:
            g.FIXV[g.MP] = I;
    elif PRODUCTION_NUMBER == 395:  # reference 3950
        #  <LITERAL EXP OR *> ::= <ARITH EXP>
        g.PTR_TOP = g.PTR[g.MP] - 1;
        CHECK_ARRAYNESS();
        CHECK_IMPLICIT_T();
        if g.PSEUDO_FORM[g.PTR[g.SP]] != XLIT:
            ERROR(d.CLASS_VE, 1);
            g.TEMP = 0;
        else:
            g.TEMP = MAKE_FIXED_LIT(g.LOC_P[g.PTR[g.SP]]);
            if g.TEMP == -1:
                g.TEMP = 0;
        g.FIXV[g.SP] = g.TEMP;
    elif PRODUCTION_NUMBER == 396:  # reference 3960
        #  <LITERAL EXP OR *> ::= *
        g.FIXV[g.SP] = -1;
    elif PRODUCTION_NUMBER == 397:  # reference 3970
        #  <PREC_SPEC> ::= SINGLE
        g.FIXL[g.MP] = SD_FLAGS;
        g.FIXV[g.MP] = SINGLE_FLAG;
        g.PTR[g.MP] = 1;
    elif PRODUCTION_NUMBER == 398:  # reference 3980
        #  <PREC SPEC> ::= DOUBLE
        g.FIXL[g.MP] = SD_FLAGS;
        g.FIXV[g.MP] = DOUBLE_FLAG;
        g.PTR[g.MP] = 2;
    elif PRODUCTION_NUMBER == 399:  # reference 3990
        #  <MINOR ATTR LIST> ::= <MINOR ATTRIBUTE>
        goto_INCORPORATE_ATTR = True
    # reference 4000 relocated
    # reference 4010 relocated
    elif PRODUCTION_NUMBER == 402:  # reference 4020
        #  <MINOR ATTRIBUTE> ::= AUTOMATIC
        g.I = AUTO_FLAG;
        goto_SET_AUTSTAT = True
    elif PRODUCTION_NUMBER == 403:  # reference 4030
        #  <MINOR ATTRIBUTE> ::= DENSE
        if (TYPE == 0) and (BUILDING_TEMPLATE and (TYPE == BIT_TYPE) and \
                          ((ATTRIBUTES & ARRAY_FLAG) == 0) and \
                          (not NAME_IMPLIED)):
            g.FIXL[g.MP] = ALDENSE_FLAGS;
            g.FIXV[g.MP] = DENSE_FLAG;
    elif PRODUCTION_NUMBER == 404:  # reference 4040
        #  <MINOR ATTRIBUTE> ::= ALIGNED
        g.FIXL[g.MP] = ALDENSE_FLAGS;
        g.FIXV[g.MP] = ALIGNED_FLAG;
    elif PRODUCTION_NUMBER == 405:  # reference 4050
        #  <MINOR ATTRIBUTE> ::= ACCESS
        if g.BLOCK_MODE[g.NEST] == CMPL_MODE:
            g.FIXL[g.MP] = ACCESS_FLAG;
            g.FIXV[g.MP] = ACCESS_FLAG;
            g.ACCESS_FOUND = g.TRUE;
        else:
            ERROR(d.CLASS_DC, 5);
    elif PRODUCTION_NUMBER == 406:  # reference 4060
        #  <MINOR ATTRIBUTE>  ::=  LOCK ( <LITERAL EXP OR *> )
        g.CONTEXT = DECLARE_CONTEXT;
        g.LOCKp = g.FIXV[g.MP + 2];
        if g.LOCKp < 0: 
            g.LOCKp = 0xFF;
        elif LOCKp < 1 or LOCKp > LOCK_LIM:
            ERROR(d.CLASS_DL, 3);
            g.LOCKp = 0xFF;
        g.FIXL[g.MP], g.FIXV[g.MP] = LOCK_FLAG;
    elif PRODUCTION_NUMBER == 407:  # reference 4070
        #  <MINOR ATTRIBUTE>  ::=  REMOTE
        g.FIXL[g.MP], g.FIXV[g.MP] = REMOTE_FLAG;
    elif PRODUCTION_NUMBER == 408:  # reference 4080
        #  <MINOR ATTRIBUTE> ::= RIGID
        g.FIXL[g.MP], g.FIXV[g.MP] = RIGID_FLAG;
    # reference 4090 relocated
    elif PRODUCTION_NUMBER == 410:  # reference 4100
        #  <MINOR ATTRIBUTE> ::= <INIT/CONST HEAD> * )
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = 1;  # INDICATE "*" PRESENT
        goto_DO_QUALIFIED_ATTRIBUTE = True
    elif PRODUCTION_NUMBER == 411:  # reference 4110
        #  <MINOR ATTRIBUTE> ::= LATCHED
        g.FIXL[g.MP] = LATCHED_FLAG;
        g.FIXV[g.MP] = LATCHED_FLAG;
    elif PRODUCTION_NUMBER == 412:  # reference 4120
        #  <MINOR ATTRIBUTE>  ::=  NONHAL  (  <LEVEL>  )
        g.NONHAL = g.FIXV[g.MP + 2];
        #   DISCONNECT SYT_FLAGS FROM NONHAL; SET
        #   NONHAL IN SYT_FLAGS2 ARRAY.
        g.FIXL[g.MP] = NONHAL_FLAG;
        g.SYT_FLAGS2(ID_LOC, g.SYT_FLAGS2(ID_LOC) | NONHAL_FLAG);
        g.ATTRIBUTES2 = ATTRIBUTES2 | NONHAL_FLAG;
    # reference 4130 relocated
    elif PRODUCTION_NUMBER == 414:  # reference 4140
        #  <INIT/CONST HEAD> ::= CONSTANT (
        g.FIXL[g.MP] = INIT_CONST;
        g.FIXV[g.MP] = CONSTANT_FLAG;
        goto_DO_INIT_CONST_HEAD = True
    elif PRODUCTION_NUMBER == 415:  # reference 4150
        #  <INIT/CONST HEAD>  ::=  <INIT/CONST HEAD>  <REPEATED CONSTANT>  ,
        pass;
    elif PRODUCTION_NUMBER == 416:  # reference 4160
        #  <REPEATED CONSTANT>  ::=  <EXPRESSION>
        g.TEMP_SYN = 0;
        goto_INIT_ELEMENT = True
    elif PRODUCTION_NUMBER == 417:  # reference 4170
        #  <REPEATED CONSTANT>  ::=  <REPEAT HEAD>  <VARIABLE>
        g.TEMP_SYN = 1;
        goto_INIT_ELEMENT = True
    # reference 4180 relocated
    elif PRODUCTION_NUMBER == 419:  # reference 4190
        # <REPEATED CONSTANT>  ::=  <NESTED REPEAT HEAD>  <REPEATED CONSTANT>  )
        goto_END_REPEAT_INIT = True
    elif PRODUCTION_NUMBER == 420:  # reference 4200
        #  <REPEATED CONSTANT>  ::=  <REPEAT HEAD>
        g.IC_LINE = g.IC_LINE - 1;
        g.NUM_STACKS = NUM_STACKS - 1;
        g.NUM_FL_NO = NUM_FL_NO - 1;
        g.NUM_ELEMENTS = NUM_ELEMENTS + g.INX[g.PTR[g.MP]];
        g.PTR_TOP = g.PTR[g.MP] - 1;
    elif PRODUCTION_NUMBER == 421:  # reference 4210
        #  <REPEAT HEAD>  ::=  <ARITH EXP>  #
        CHECK_ARRAYNESS();
        if g.PSEUDO_FORM[g.PTR[g.MP]] != XLIT: 
            g.TEMP_SYN = 0;
        else:
            g.TEMP_SYN = MAKE_FIXED_LIT(g.LOC_P[g.PTR[g.MP]]);
        if TEMP_SYN < 1: 
            ERROR(d.CLASS_DI, 1);
            g.TEMP_SYN = 0;
        if TEMP_SYN > g.NUM_EL_MAX: 
            g.TEMP_SYN = g.NUM_EL_MAX;
        g.INX[g.PTR[g.MP]] = TEMP_SYN;
        g.FIXV[g.MP] = NUM_ELEMENTS;
        g.NUM_FL_NO = NUM_FL_NO + 1;
        SET_INIT(TEMP_SYN, 1, 0, 0, NUM_FL_NO);
        g.FIXL[g.MP] = g.IC_LINE;
        g.NUM_STACKS = NUM_STACKS + 1;
    elif PRODUCTION_NUMBER == 422:  # reference 4220
        #  <NESTED REPEAT HEAD>  ::=  <REPEAT HEAD>  (
        pass;
    elif PRODUCTION_NUMBER == 423:  # reference 4230
        #  <NESTED REPEAT HEAD>  ::=  <NESTED REPEAT HEAD>  <REPEATED CONSTANT>  ,
        pass;
    # reference 4240 relocated
    elif PRODUCTION_NUMBER == 425:  # reference 4250
        #  <CONSTANT>  ::=  <COMPOUND NUMBER>
        g.TEMP_SYN = g.SCALAR_TYPE;
        goto_DO_CONSTANT = True
    elif PRODUCTION_NUMBER == 426:  # reference 4260
        #  <CONSTANT>  ::=  <BIT CONST>
        pass;
    elif PRODUCTION_NUMBER == 427:  # reference 4270
        #  <CONSTANT>  ::=  <CHAR CONST>
        pass;
    elif PRODUCTION_NUMBER == 428:  # reference 4280
        #  <NUMBER> ::= <SIMPLE NUMBER>
        pass
    elif PRODUCTION_NUMBER == 429:  # reference 4290
        #  <NUMBER> ::= <LEVEL>
        pass
    # reference 4300 relocated
    elif PRODUCTION_NUMBER == 431:  # reference 4310
        #  <CLOSING> ::= CLOSE <LABEL>
        g.VAR[g.MP] = g.VAR[g.SP];
        goto_CLOSE_IT = True
    elif PRODUCTION_NUMBER == 432:  # reference 4320
        #  <CLOSING> ::= <LABEL DEFINITION> <CLOSING>
        SET_LABEL_TYPE(g.FIXL[g.MP], g.STMT_LABEL);
        g.VAR[g.MP] = g.VAR[g.SP];
    elif PRODUCTION_NUMBER == 433:  # reference 4330
        # <TERMINATOR>::= TERMINATE
        g.FIXL[g.MP] = XTERM;
        g.FIXV[g.MP] = 0xE000;
    elif PRODUCTION_NUMBER == 434:  # reference 4340
        # <TERMINATOR>::= CANCEL
        g.FIXL[g.MP] = XCANC;
        g.FIXV[g.MP] = 0xA000;
    elif PRODUCTION_NUMBER == 435:  # reference 4350
        #  <TERMINATE LIST>  ::=  <LABEL VAR>
        g.EXT_P[g.PTR[g.MP]] = 1;
        goto_TERM_LIST = True
    # reference 4360 relocated
    elif PRODUCTION_NUMBER == 437:  # reference 4370
        # <WAIT KEY>::= WAIT
        g.REFER_LOC = 1;
    elif PRODUCTION_NUMBER == 438:  # reference 4380
        #  <SCHEDULE HEAD>  ::=  SCHEDULE  <LABEL VAR>
        PROCESS_CHECK(g.MPP1);
        if (g.SYT_FLAGS(g.FIXL[g.MPP1]) & ACCESS_FLAG) != 0:
            ERROR(d.CLASS_PS, 5, g.VAR[g.MPP1]);
        SET_XREF_RORS(g.MPP1, 0x6000);
        REFER_LOC, g.PTR[g.MP] = g.PTR[g.MPP1];
        g.INX[REFER_LOC] = 0;
    # reference 4390 relocated
    elif PRODUCTION_NUMBER == 440:  # reference 4400
        # <SCHEDULE HEAD>::= <SCHEDULE HEAD> IN <ARITH EXP>
        g.TEMP = 0x2;
        if UNARRAYED_SCALAR(g.SP): 
            ERROR(d.CLASS_RT, 1, 'IN');
        goto_SCHEDULE_AT = True
    elif PRODUCTION_NUMBER == 441:  # reference 4410
        # <SCHEDULE HEAD>::=<SCHEDULE HEAD> ON <BIT EXP>
        g.TEMP = 0x3;
        if CHECK_EVENT_EXP(g.SP): 
            ERROR(d.CLASS_RT, 3, 'ON');
        goto_SCHEDULE_AT = True
    # reference 4420 relocated
    elif PRODUCTION_NUMBER == 443:  # reference 4430
        # <SCHEDULE PHRASE>::=<SCHEDULE HEAD> PRIORITY (<ARITH EXP>)
        if UNARRAYED_INTEGER(g.SP - 1): 
            goto_SCHED_PRIO = True
        g.INX[REFER_LOC] = g.INX[REFER_LOC] | 0x4;
    elif PRODUCTION_NUMBER == 444:  # reference 4440
        #  <SCHEDULE PHRASE>  ::=  <SCHEDULE PHRASE>  DEPENDENT
        g.INX[REFER_LOC] = g.INX[REFER_LOC] | 0x8;
    elif PRODUCTION_NUMBER == 445:  # reference 4450
        # <SCHEDULE CONTROL>::= <STOPPING>
        pass;
    elif PRODUCTION_NUMBER == 446:  # reference 4460
        # <SCHEDULE CONTROL>::= <TIMING>
        pass;
    elif PRODUCTION_NUMBER == 447:  # reference 4470
        # <SCHEDULE CONTROL>::= <TIMING><STOPPING>
        pass;
    # reference 4480 relocated
    elif PRODUCTION_NUMBER == 449:  # reference 4490
        #  <TIMING>  ::=  <REPEAT> AFTER <ARITH EXP>
        g.TEMP = 0x30;
        goto_SCHEDULE_EVERY = True
    elif PRODUCTION_NUMBER == 450:  # reference 4500
        #  <TIMING>  ::=  <REPEAT>
        g.INX[REFER_LOC] = g.INX[REFER_LOC] | 0x10;
    elif PRODUCTION_NUMBER == 451:  # reference 4510
        #  <REPEAT>  ::=  , REPEAT
        g.CONTEXT = 0;
    elif PRODUCTION_NUMBER == 452:  # reference 4520
        # <STOPPING>::=<WHILE KEY><ARITH EXP>
        if g.FIXL[g.MP] == 0: 
            ERROR(d.CLASS_RT, 2);
        elif UNARRAYED_SCALAR(g.SP): 
            ERROR(d.CLASS_RT, 1, 'UNTIL');
        g.INX[REFER_LOC] = g.INX[REFER_LOC] | 0x40;
    elif PRODUCTION_NUMBER == 453:  # reference 4530
        # <STOPPING>::=<WHILE KEY><BIT EXP>
        DO;
        if CHECK_EVENT_EXP(g.SP): ERROR(d.CLASS_RT, 3, 'WHILE/UNTIL');
        g.TEMP = SHL(g.FIXL[g.MP] + 2, 6);
        g.INX[REFER_LOC] = g.INX[REFER_LOC] | g.TEMP;
        END;
    elif PRODUCTION_NUMBER == 454:  # reference 4540
        pass  #  INSURANCE
    elif PRODUCTION_NUMBER == 455:  # reference 4550
        pass  #  INSURANCE
    elif PRODUCTION_NUMBER == 456:  # reference 4560
        pass  #  INSURANCE
    elif PRODUCTION_NUMBER == 457:  # reference 4570
        pass  #  INSURANCE
    elif PRODUCTION_NUMBER == 458:  # reference 4580
        pass  #  INSURANCE
    
    #----------------------------------------------------------------------
    # The following cases have all been relocated from their original 
    # positions to facilitate fallthrough from GO TO statements with
    # minimal rearrangement of the cases.  These are all cases containing
    # labels which are jump targets.
    
    elif goto_INLINE_SCOPE or PRODUCTION_NUMBER == 30:  # reference 300
        #  <PRIMARY>  ::=  <ARITH INLINE DEF>  <BLOCK BODY>  <CLOSING>  ;
        goto_INLINE_SCOPE = False
        g.TEMP2 = INLINE_LEVEL;
        g.TEMP = XICLS;
        g.GRAMMAR_FLAGS[g.STACK_PTR[g.SP]] = g.GRAMMAR_FLAGS[g.STACK_PTR[g.SP]] | INLINE_FLAG;
        goto_CLOSE_SCOPE = True
    elif goto_WAIT_TIME or PRODUCTION_NUMBER == 62:  # reference 620
        # <BASIC STATEMENT>::= <WAIT KEY><ARITH EXP>;
        if not goto_WAIT_TIME:
            g.TEMP = 1;
            if UNARRAYED_SCALAR(g.SP - 1): 
                ERROR(d.CLASS_RT, 6, 'WAIT');
        goto_WAIT_TIME = False
        g.XSET(0xB);
        HALMAT_TUPLE(XWAIT, 0, g.SP - 1, 0, g.TEMP);
        g.PTR_TOP = g.PTR[g.SP - 1] - 1;
        goto_UPDATE_CHECK = True
    elif goto_UP_PRIO or PRODUCTION_NUMBER == 67:  # reference 670
        # <BASIC STATEMENT>::= UPDATE PRIORITY TO <ARITH EXP>;
        if not goto_UP_PRIO:
            g.PTR_TOP = g.PTR[g.SP - 1] - 1;
            g.TEMP = 0;
        goto_UP_PRIO = False
        g.XSET(0xC);
        if UNARRAYED_INTEGER(g.SP - 1):
            ERROR(d.CLASS_RT, 4, 'UPDATE PRIORITY');
        HALMAT_TUPLE(XPRIO, 0, g.SP - 1, g.TEMP, g.TEMP > 0);
        goto_UPDATE_CHECK = True
    elif goto_SCHEDULE_EMIT or PRODUCTION_NUMBER == 69:  # reference 690
        # <BASIC STATEMENT>::= <SCHEDULE PHRASE>;
        goto_SCHEDULE_EMIT = False
        g.XSET(0x9);
        HALMAT_POP(XSCHD, g.PTR_TOP - REFER_LOC + 1, 0, g.INX[REFER_LOC]);
        while REFER_LOC <= g.PTR_TOP:
            HALMAT_PIP(g.LOC_P[REFER_LOC], g.PSEUDO_FORM[REFER_LOC], 0, 0);
            g.REFER_LOC = REFER_LOC + 1;
        g.PTR_TOP = g.PTR[g.MP] - 1;
        goto_UPDATE_CHECK = True
    if goto_UPDATE_CHECK or PRODUCTION_NUMBER == 61:  # reference 610
        # <BASIC STATEMENT>  ::=  <WAIT KEY>  FOR DEPENDENT ;
        if not goto_UPDATE_CHECK:
            HALMAT_POP(XWAIT, 0, 0, 0);
            g.XSET(0xB);
        goto_UPDATE_CHECK = False
        if UPDATE_BLOCK_LEVEL > 0: 
            ERROR(d.CLASS_RU, 1);
        if INLINE_LEVEL > 0: 
            ERROR(d.CLASS_PP, 6);
        g.REFER_LOC = 0;
        goto_FIX_NOLAB = True
    elif goto_EXITTING or PRODUCTION_NUMBER == 42:  # reference 420
        # <BASIC STATEMENT>::= EXIT ;
        goto_EXITTING = False
        g.TEMP = g.DO_LEVEL;
        while g.TEMP > 1:
            if SHR(g.DO_INX[g.TEMP], 7): 
                ERROR(d.CLASS_GE, 3);
            if LABEL_MATCH: 
                HALMAT_POP(XBRA, 1, 0, 0);
                HALMAT_PIP(g.DO_LOC[g.TEMP], XINL, 0, 0);
                g.TEMP = 1;
            g.TEMP = g.TEMP - 1;
        if g.TEMP == 1: 
            ERROR(d.CLASS_GE, 1);
        g.XSET(0x01);
        goto_FIX_NOLAB = True
    elif goto_REPEATING or PRODUCTION_NUMBER == 44:  # reference 440
        # <BASIC STATEMENT>::= REPEAT ;
        goto_REPEATING = False
        g.TEMP = g.DO_LEVEL;
        while g.TEMP > 1:
            if SHR(g.DO_INX[g.TEMP], 7): 
                ERROR(d.CLASS_GE, 4);
            if g.DO_INX[g.TEMP]: 
                if LABEL_MATCH:
                    HALMAT_POP(XBRA, 1, 0, 0);
                    HALMAT_PIP(g.DO_LOC[g.TEMP] + 1, XINL, 0, 0);
                    g.TEMP = 1;
            g.TEMP = g.TEMP - 1;
        if g.TEMP == 1: 
            ERROR(d.CLASS_GE, 2);
        g.XSET(0x801);
        goto_FIX_NOLAB = True
    elif goto_IO_EMIT or PRODUCTION_NUMBER == 55:  # reference 550
        # <BASIC STATEMENT>::= <READ KEY>;
        goto_IO_EMIT = False
        g.XSET(0x3);
        HALMAT_TUPLE(g.XREAD[g.INX[g.PTR[g.MP]]], 0, g.MP, 0, 0);
        g.PTR_TOP = g.PTR[g.MP] - 1;
        HALMAT_POP(XXXND, 0, 0, 0);
        goto_FIX_NOLAB = True
    if goto_FIX_NOLAB or PRODUCTION_NUMBER == 47:  # reference 470
        # <BASIC STATEMENT>::= ;
        goto_FIX_NOLAB = False
        g.FIXF[g.MP] = 0;
    elif goto_ARITH_LITS or PRODUCTION_NUMBER == 19:  # reference 190
        #  <PRE PRIMARY> ::= <NUMBER>
        if not goto_ARITH_LITS:
            g.TEMP = INT_TYPE;
        goto_ARITH_LITS = False
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.LOC_P[g.PTR[g.MP]] = g.FIXL[g.MP];
        g.PSEUDO_FORM[g.PTR[g.MP]] = XLIT ;
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = g.TEMP;
    elif goto_LABEL_INCORP or PRODUCTION_NUMBER == 35:  # reference 350
        #  <OTHER STATEMENT>  ::= <LABEL DEFINITION> <OTHER STATEMENT>
        goto_LABEL_INCORP = False
        if g.FIXL[g.MP] != g.FIXF[g.SP]: 
            g.SYT_PTR(g.FIXL[g.MP], g.FIXF[g.SP]);
        g.FIXF[g.MP] = g.FIXL[g.MP];
        g.PTR[g.MP] = g.PTR[g.MPP1];
        SET_LABEL_TYPE(g.FIXL[g.MP], g.STMT_LABEL);
    elif goto_NON_EVENT or PRODUCTION_NUMBER == 82:  # reference 820
        #  <BIT PRIM>  ::=  <BIT VAR>
        if not goto_NON_EVENT:
            SET_XREF_RORS(g.MP);
        goto_NON_EVENT = False
        g.INX[g.PTR[g.MP]] = g.FALSE;
    elif goto_YES_EVENT or PRODUCTION_NUMBER == 83:  # reference 830
        #  <BIT PRIM>  ::=  <LABEL VAR>
        if not goto_YES_EVENT:
            SET_XREF_RORS(g.MP, 0x2000);
            g.TEMP = g.PSEUDO_TYPE_P[g.PTR[g.MP]];
            if (g.TEMP == TASK_LABEL) or (g.TEMP == PROG_LABEL):
                pass;
            else:
                ERROR(d.CLASS_RT, 14, g.VAR[g.MP]);
            if REFER_LOC > 0: 
                g.INX[g.PTR[g.MP]] = 1;
            else:
                g.INX[g.PTR[g.MP]] = 2;
        goto_YES_EVENT = False
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = BIT_TYPE;
        g.PSEUDO_LENGTH[g.PTR[g.MP]] = 1;
    elif goto_DO_BIT_CAT or PRODUCTION_NUMBER == 94:  # reference 940
        #  <BIT CAT>  ::=  <BIT CAT>  <CAT>  <BIT PRIM>
        goto_DO_BIT_CAT = False
        g.INX[g.PTR[g.MP]] = g.FALSE;
        g.TEMP = g.PSEUDO_LENGTH[g.PTR[g.MP]] + g.PSEUDO_LENGTH[g.PTR[g.SP]];
        if g.TEMP > BIT_LENGTH_LIM:
            g.TEMP = BIT_LENGTH_LIM;
            ERROR(d.CLASS_EB, 1);
        HALMAT_TUPLE(XBCAT, 0, g.MP, g.SP, 0);
        SETUP_VAC(g.MP, BIT_TYPE, g.TEMP);
        g.PTR_TOP = g.PTR[g.MP];
    elif goto_DO_LIT_BIT_FACTOR or goto_DO_BIT_FACTOR or \
            PRODUCTION_NUMBER == 98:  # reference 980
        #   <BIT FACTOR> ::= <BIT FACTOR> <AND> <BIT CAT>
        if goto_DO_LIT_BIT_FACTOR or \
                (BIT_LITERAL(g.MP, g.SP) and not goto_DO_BIT_FACTOR): 
            if not goto_DO_LIT_BIT_FACTOR:
                g.TEMP = g.FIXV[g.MP] & g.FIXV[g.SP];
            goto_DO_LIT_BIT_FACTOR = False
            if g.PSEUDO_LENGTH[g.PTR[g.MP]] != g.PSEUDO_LENGTH[g.PTR[g.SP]]:
                ERROR(d.CLASS_YE, 100);
            g.TEMP2 = g.PSEUDO_LENGTH[g.PTR[g.MP]];
            if TEMP2 < g.PSEUDO_LENGTH[g.PTR[g.SP]]: 
                g.TEMP2 = g.PSEUDO_LENGTH[g.PTR[g.SP]];
            g.LOC_P[g.PTR[g.MP]] = SAVE_LITERAL(2, g.TEMP, TEMP2);
        else:
            if not goto_DO_BIT_FACTOR:
                g.TEMP = XBAND ;
            goto_DO_BIT_FACTOR = False
            g.TEMP2 = g.INX[g.PTR[g.MP]] & g.INX[g.PTR[g.SP]] & 1;
            HALMAT_TUPLE(g.TEMP, 0, g.MP, g.SP, TEMP2);
            g.INX[g.PTR[g.MP]] = TEMP2;
            g.TEMP = g.PSEUDO_LENGTH[g.PTR[g.MP]];
            if g.TEMP < g.PSEUDO_LENGTH[g.PTR[g.SP]]:
                g.TEMP = g.PSEUDO_LENGTH[g.PTR[g.SP]];
            SETUP_VAC(g.MP, BIT_TYPE, g.TEMP);
        g.PTR_TOP = g.PTR[g.MP];
    elif goto_EMIT_REL or PRODUCTION_NUMBER == 109:  # reference 1090
        #  <COMPARISON> ::= <ARITH EXP> <RELATIONAL OP> <ARITH EXP>
        if not goto_EMIT_REL:
            MATCH_ARITH(g.MP, g.SP);
            # DO CASE PSEUDO_TYPE_P[PTR[MP]]-MAT_TYPE;
            pt = g.PSEUDO_TYPE_P[g.PTR[g.MP]] - g.MAT_TYPE
            if pt == 0:
                g.TEMP = XMEQU(REL_OP);
                g.VAR[g.MP] = 'MATRIX';
            elif pt == 1:
                g.TEMP = XVEQU(REL_OP);
                g.VAR[g.MP] = 'VECTOR';
            elif pt == 2:
                g.TEMP = XSEQU(REL_OP);
                g.VAR[g.MP] = '';
            elif pt == 3:
                g.TEMP = XIEQU(REL_OP);
                g.VAR[g.MP] = '';
        goto_EMIT_REL = False
        HALMAT_TUPLE(g.TEMP, XCO_N, g.MP, g.SP, 0);
    elif goto_DO_CHAR_CAT or PRODUCTION_NUMBER == 132:  # reference 1320
        # <CHAR EXP> ::= <CHAR EXP> <CAT> <CHAR PRIM>
        if CHAR_LITERAL(g.MP, g.SP) and not goto_DO_CHAR_CAT:
            g.TEMP = CHAR_LENGTH_LIM - LENGTH(g.VAR[g.MP]);
            if g.TEMP < LENGTH(g.VAR[g.SP]):
                g.VAR[g.SP] = SUBSTR(g.VAR[g.SP], 0, g.TEMP);
                ERROR(d.CLASS_VC, 1);
            g.VAR[g.MP] = g.VAR[g.MP] + g.VAR[g.SP];
            g.LOC_P[g.PTR[g.MP]] = SAVE_LITERAL(0, g.VAR[g.MP]);
            g.PSEUDO_LENGTH[g.PTR[g.MP]] = LENGTH(g.VAR[g.MP]);
        else:
            goto_DO_CHAR_CAT = False
            HALMAT_TUPLE(XCCAT, 0, g.MP, g.SP, 0);
            SETUP_VAC(g.MP, CHAR_TYPE);
        g.PTR_TOP = g.PTR[g.MP];
    elif goto_ASSIGNING or goto_END_ASSIGN or \
            PRODUCTION_NUMBER == 136:  # reference 1360
        # <ASSIGNMENT>::=<VARIABLE><=1><EXPRESSION>
        if not ASSIGNING and not END_ASSIGN:
            g.INX[g.PTR[g.SP]] = 2;
            if NAME_PSEUDOS: 
                NAME_COMPARE(g.MP, g.SP, d.CLASS_AV, 5);
                HALMAT_TUPLE(XNASN, 0, g.SP, g.MP, 0);
                if COPINESS(g.MP, g.SP) > 2: 
                    ERROR(d.CLASS_AA, 1);
                goto_END_ASSIGN = True
            else:
                if RESET_ARRAYNESS > 2: 
                    ERROR(d.CLASS_AA, 1);
                HALMAT_TUPLE(g.XXASN[g.PSEUDO_TYPE_P[g.PTR[g.SP]]], 0, g.SP, g.MP, 0);
        if not goto_END_ASSIGN:
            goto_ASSIGNING = False
            g.TEMP = g.PSEUDO_TYPE_P[g.PTR[g.SP]];
            if g.TEMP == INT_TYPE: 
                if g.PSEUDO_FORM[g.PTR[g.SP]] == XLIT: 
                    g.TEMP2 = GET_LITERAL(g.LOC_P[g.PTR[g.SP]]);
                    if LIT2(TEMP2) == 0: 
                        g.TEMP = 0;
            if (SHL(1, g.TEMP) & ASSIGN_TYPE(g.PSEUDO_TYPE_P[g.PTR[g.MP]])) == 0:
                ERROR(d.CLASS_AV, 1, g.VAR[g.MP]);
            elif g.TEMP > 0: 
                # DO CASE PSEUDO_TYPE_P[PTR[MP]];
                pt = g.PSEUDO_TYPE_P[g.PTR[g.MP]]
                if pt == 0:
                    pass;
                elif pt == 1:
                    pass;  # BIT
                elif pt == 2:
                    # CHAR*/
                    # CHECK IF THE EXPRESSION BEING ASSIGNED TO A
                    # CHARACTER IS SCALAR AND SHOULD BE IN DOUBLE
                    # PRECISION (DOUBLELIT=TRUE).  IF TRUE, THEN SET
                    # LIT1 EQUAL TO 5.
                    if (g.PSEUDO_TYPE_P[g.PTR[g.SP]] == g.SCALAR_TYPE) & DOUBLELIT:  # "
                        LIT1(GET_LITERAL(g.LOC_P[g.PTR[g.SP]]), 5);
                elif pt == 3:
                    MATRIX_COMPARE(g.MP, g.SP, d.CLASS_AV, 2);  # MATRIX
                elif pt == 4:
                    VECTOR_COMPARE(g.MP, g.SP, d.CLASS_AV, 3);  # VECTOR
                elif pt == 5:
                    pass;  # SCALAR
                elif pt == 6:
                    pass;  # INTEGER
                elif pt in (7, 8):
                    pass
                elif pt == 9:
                    pass;  # EVENT
                elif pt == 10:
                    STRUCTURE_COMPARE(g.FIXL[g.MP], g.FIXL[g.SP], d.CLASS_AV, 4);  # STRUC
                elif pt == 11:
                    pass;
        goto_END_ASSIGN = False
        g.DOUBLELIT = g.FALSE;
        g.FIXV[g.MP] = g.FIXV[g.SP];
        g.PTR[g.MP] = g.PTR[g.SP];
    elif goto_CLOSE_IF or PRODUCTION_NUMBER == 138:  # reference 1380
        # <IF STATEMENT>::= <IF CLAUSE> <STATEMENT>
        if not goto_CLOSE_IF:
            UNBRANCHABLE(g.SP, 4);
        goto_CLOSE_IF = False
        g.INDENT_LEVEL = g.FIXL[g.MP];
        HALMAT_POP(XLBL, 1, XCO_N, 1);
        HALMAT_PIP(g.FIXV[g.MP], XINL, 0, 0);
    elif goto_EMIT_IF or PRODUCTION_NUMBER == 141:  # reference 1410
        # <IF CLAUSE>  ::=  <IF> <RELATIONAL EXP> THEN
        if not goto_EMIT_IF:
            g.TEMP = g.LOC_P[g.PTR[g.MPP1]];
        goto_EMIT_IF = False
        HALMAT_POP(XFBRA, 2, XCO_N, 0);
        HALMAT_PIP(g.FL_NO(), XINL, 0, 0);
        HALMAT_PIP(g.TEMP, XVAC, 0, 0);
        g.PTR_TOP = g.PTR[g.MPP1] - 1;
        g.FIXV[g.MP] = g.FL_NO();
        g.FL_NO(g.FL_NO() + 1);
        # PRINT IF-THEN STATEMENTS ON SAME LINE AS A
        # SIMPLE DO.  DO NOT OUTPUT_WRITER.  SAVE VALUES THAT
        # ARE NEEDED WHEN OUTPUT_WRITER WILL BE CALLED.
        g.IF_FLAG = g.TRUE;
        # DETERMINES IF IF-THEN WAS ALREADY PRINTED IN REPLACE MACRO-11342
        if (g.GRAMMAR_FLAGS[g.LAST_WRITE] & PRINT_FLAG) == 0:
            g.IF_FLAG = g.FALSE;
            for I in range((g.LAST_WRITE + 1), 1 + g.STACK_PTR[g.SP]):
                if (g.GRAMMAR_FLAGS[I] & PRINT_FLAG) != 0:
                    g.IF_FLAG = g.TRUE;
        if not g.IF_FLAG and (g.STMT_STACK[g.LAST_WRITE] != l.ELSE_TOKEN):
            g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
        else:
            g.SAVE_SRN1 = g.SRN[2][:];
            g.SAVE_SRN_COUNT1 = g.SRN_COUNT[2];
            g.SAVE1 = g.LAST_WRITE;
            g.SAVE2 = g.STACK_PTR[g.SP];
        EMIT_SMRK();
        g.XSET(0x200);
    elif goto_EMIT_WHILE or PRODUCTION_NUMBER == 146:  # reference 1460
        # <DO GROUP HEAD>::= DO <FOR LIST> <WHILE CLAUSE> ;
        if not goto_EMIT_WHILE:
            g.XSET(0x13);
            g.TEMP = g.PTR[g.SP - 1];
            HALMAT_FIX_POPTAG(g.FIXV[g.MPP1], SHL(g.INX[g.TEMP], 4) | g.PTR[g.MPP1]);
            HALMAT_POP(XCFOR, 1, 0, g.INX[g.TEMP]);
        goto_EMIT_WHILE = False
        HALMAT_PIP(g.LOC_P[g.TEMP], g.PSEUDO_FORM[g.TEMP], 0, 0);
        g.PTR_TOP = g.TEMP - 1;
        goto_DO_DONE = True
    if goto_DO_DONE or PRODUCTION_NUMBER == 144:  # reference 1440
        # <DO GROUP HEAD>::= DO ;
        if not goto_DO_DONE:
            g.XSET(0x11);
            g.FIXL[g.MPP1] = 0;
            HALMAT_POP(XDSMP, 1, 0, 0);
            EMIT_PUSH_DO(0, 1, 0, g.MP - 1);
        goto_DO_DONE = False
        g.FIXV[g.MP] = 0;
        CHECK_IMPLICIT_T();
        # PRINT IF-THEN/ELSE STATEMENTS ON SAME LINE AS A
        # SIMPLE DO.  IF AN IF-THEN OR ELSE WAS THE PREVIOUS STATEMENT
        # PRINT THE DO ON THE SAME LINE USING SRN & STATEMENT NUMBER
        # FROM IF-THEN OR ELSE.
        if (g.IF_FLAG | g.ELSE_FLAG) and (PRODUCTION_NUMBER == 144):
            g.SQUEEZING = g.FALSE;
            g.SAVE_SRN2 = g.SRN[2][:];
            g.SRN[2] = g.SAVE_SRN1[:];
            g.SAVE_SRN_COUNT2 = g.SRN_COUNT[2];
            g.SRN_COUNT[2] = g.SAVE_SRN_COUNT1;
            if g.IF_FLAG:
                g.STMT_NUM(g.STMT_NUM() - 1);
            OUTPUT_WRITER(SAVE1, g.STMT_PTR);
            if g.IF_FLAG:
                g.STMT_NUM(g.STMT_NUM() + 1);
            g.IF_FLAG = g.FALSE
            g.ELSE_FLAG = g.FALSE;
            g.IFDO_FLAG[g.DO_LEVEL] = g.TRUE;
            g.SRN[2] = g.SAVE_SRN2[:];
            g.SRN_COUNT[2] = g.SAVE_SRN_COUNT2;
        else:
            g.IF_FLAG = g.FALSE
            g.ELSE_FLAG = g.FALSE;
            OUTPUT_WRITER(g.LAST_WRITE, g.STMT_PTR);
        if g.FIXL[g.MPP1] > 0:
            HALMAT_POP(XTDCL, 1, 0, 0);
            HALMAT_PIP(g.FIXL[g.MPP1], XSYT, 0, 0);
        EMIT_SMRK();
        g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
        g.NEST_LEVEL = NEST_LEVEL + 1;
    elif goto_CASE_HEAD or PRODUCTION_NUMBER == 148:  # reference 1480
        # <DO GROUP HEAD>::= DO CASE  <ARITH EXP> ;
        if not goto_CASE_HEAD:
            g.FIXV[g.MP], g.FIXL[g.MP] = 0;
        goto_CASE_HEAD = False
        g.XSET(0x14);
        g.TEMP2 = g.PTR[g.MP + 2];
        if UNARRAYED_INTEGER(g.MP + 2): 
            ERROR(d.CLASS_GC, 1);
        HALMAT_POP(XDCAS, 2, 0, g.FIXL[g.MP]);
        EMIT_PUSH_DO(2, 4, 0, g.MP - 1);
        HALMAT_PIP(g.LOC_P[TEMP2], g.PSEUDO_FORM[TEMP2], 0, 0);
        g.PTR_TOP = TEMP2 - 1;
        CHECK_IMPLICIT_T();
        if g.FIXL[g.MP]: 
            OUTPUT_WRITER(g.LAST_WRITE, g.STACK_PTR[g.SP] - 1);
            g.LAST_WRITE = g.STACK_PTR[g.SP];
            g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
            EMIT_SMRK();
            SRN_UPDATE();
            g.XSET(0x100);
            OUTPUT_WRITER(g.LAST_WRITE, g.LAST_WRITE);
            g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
        else:
            if STMT_END_PTR > -1:
                OUTPUT_WRITER(g.LAST_WRITE, g.STACK_PTR[g.SP]);
            EMIT_SMRK();
            g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
            goto_SET_CASE = True;
    if goto_SET_CASE or PRODUCTION_NUMBER == 149:  # reference 1490
        #  <DO GROUP HEAD>  ::=  <CASE ELSE>  <STATEMENT>
        if not goto_SET_CASE:
            UNBRANCHABLE(g.SP, 6);
            g.FIXV[g.MP] = 0;
            g.INDENT_LEVEL = g.INDENT_LEVEL - g.INDENT_INCR;
        goto_SET_CASE = False
        g.CASE_LEVEL = CASE_LEVEL + 1;
        if CASE_LEVEL <= CASE_LEVEL_LIM:
            g.CASE_STACK[CASE_LEVEL] = 0;
        g.NEST_LEVEL = NEST_LEVEL + 1;
        goto_EMIT_CASE = True
    if goto_EMIT_CASE or PRODUCTION_NUMBER == 150:  # reference 1500
        # <DO GROUP HEAD>::= <DO GROUP HEAD> <ANY STATEMENT>
        if not goto_EMIT_CASE:
            g.FIXV[g.MP] = 1;
        if goto_EMIT_CASE or (g.DO_INX[g.DO_LEVEL] & 0x7F) == 2: 
            if goto_EMIT_CASE or g.PTR[g.SP]:
                goto_EMIT_CASE = False
                g.INFORMATION = INFORMATION + 'CASE ';
                if CASE_LEVEL <= CASE_LEVEL_LIM:
                    g.CASE_STACK[CASE_LEVEL] = g.CASE_STACK[CASE_LEVEL] + 1;
                g.TEMP = 0;
                while (g.TEMP < CASE_LEVEL) & (g.TEMP < CASE_LEVEL_LIM):
                    g.INFORMATION = INFORMATION + g.CASE_STACK[g.TEMP] + PERIOD;
                    g.TEMP = g.TEMP + 1;
                g.INFORMATION = INFORMATION + g.CASE_STACK[g.TEMP];
                HALMAT_POP(XCLBL, 2, XCO_N, 0);
                HALMAT_PIP(g.DO_LOC[g.DO_LEVEL], XINL, 0, 0);
                HALMAT_PIP(g.FL_NO(), XINL, 0, 0);
                g.FL_NO(g.FL_NO() + 2);
                g.FIXV[g.MP] = LAST_POPp;
    elif goto_WHILE_KEY or PRODUCTION_NUMBER == 153:  # reference 1530
        # <WHILE KEY>::= WHILE
        if not goto_WHILE_KEY:
            g.TEMP = 0;
        goto_WHILE_KEY = False
        if g.PARSE_STACK[g.MP - 1] == DO_TOKEN:
            HALMAT_POP(XDTST, 1, XCO_N, g.TEMP);
            EMIT_PUSH_DO(3, 3, 0, g.MP - 2);
        g.FIXL[g.MP] = g.TEMP;
    elif goto_DO_FLOWSET or PRODUCTION_NUMBER == 155:  # reference 1550
        # <WHILE CLAUSE>::=<WHILE KEY> <BIT EXP>
        if not goto_DO_FLOWSET:
            if CHECK_ARRAYNESS: 
                ERROR(d.CLASS_GC, 2);
            if g.PSEUDO_LENGTH[g.PTR[g.SP]] > 1: 
                ERROR(d.CLASS_GB, 1, 'WHILE/UNTIL');
            HALMAT_TUPLE(XBTRU, 0, g.SP, 0, 0);
            SETUP_VAC(g.SP, BIT_TYPE);
        goto_DO_FLOWSET = False
        g.INX[g.PTR[g.SP]] = g.FIXL[g.MP];
        g.PTR[g.MP] = g.PTR[g.SP];
    if goto_DO_DISCRETE or PRODUCTION_NUMBER == 160:  # reference 1600
        # <ITERATION BODY>::= <ITERATION BODY>,<ARITH EXP>
        goto_DO_DISCRETE = False
        if UNARRAYED_SIMPLE(g.SP): 
            ERROR(d.CLASS_GC, 3);
        g.PTR_TOP = g.PTR[g.SP] - 1;
        HALMAT_TUPLE(XAFOR, XCO_N, g.SP, 0, 0);
        g.FL_NO(g.FL_NO() + 1);
        g.FIXV[g.MP] = LAST_POPp;
    elif goto_ON_ERROR_ACTION or PRODUCTION_NUMBER == 169:  # reference 1690
        #  <ON CLAUSE>  ::=  ON ERROR <SUBSCRIPT>  SYSTEM
        if not goto_ON_ERROR_ACTION:
            g.FIXL[g.MP] = 1;
        goto_ON_ERROR_ACTION = False
        ERROR_SUB(1);
        g.PTR[g.MP], g.PTR_TOP = g.PTR[g.MP + 2];
    elif goto_SIGNAL_EMIT or PRODUCTION_NUMBER == 171:  # reference 1710
        #  <SIGNAL CLAUSE>  ::=  SET <EVENT VAR>
        if not goto_SIGNAL_EMIT:
            g.TEMP = 1;
        goto_SIGNAL_EMIT = False
        if INLINE_LEVEL > 0: 
            ERROR(d.CLASS_PP, 6);
        if g.TEMP > 0: 
            if (g.SYT_FLAGS(g.FIXL[g.MPP1]) & LATCHED_FLAG) == 0:
                ERROR(d.CLASS_RT, 10);
        SET_XREF_RORS(g.MPP1, 0, XREF_ASSIGN);
        if CHECK_ARRAYNESS: 
            ERROR(d.CLASS_RT, 8);
        if g.SIMULATING: 
            STAB_VAR(g.MPP1);
        g.PTR[g.MP] = g.PTR[g.MPP1];
        g.INX[g.PTR[g.MP]] = g.TEMP;
    elif goto_ASSIGN_ARG or PRODUCTION_NUMBER == 179:  # reference 1790
        #  <CALL ASSIGN LIST> ::= <VARIABLE>
        if INLINE_LEVEL == 0 or goto_ASSIGN_ARG:
            goto_ASSIGN_ARG = False
            g.FCN_ARG = g.FCN_ARG + 1;
            HALMAT_TUPLE(XXXAR, XCO_N, g.SP, 0, 0);
            HALMAT_FIX_PIPTAGS(NEXT_ATOMp - 1, g.PSEUDO_TYPE_P[g.PTR[g.SP]] | \
                               SHL(NAME_PSEUDOS, 7), 1);
            if NAME_PSEUDOS: 
                KILL_NAME(g.SP);
                if g.EXT_P[g.PTR[g.SP]] != 0: 
                    ERROR(d.CLASS_FD, 7);
            CHECK_ARRAYNESS();
            l.H1 = g.VAL_P[g.PTR[g.SP]];
            if SHR(l.H1, 7): 
                ERROR(d.CLASS_FS, 1);
            if SHR(l.H1, 4): 
                ERROR(d.CLASS_SV, 1, g.VAR[g.SP]);
            if (l.H1 & 0x6) == 0x2: 
                ERROR(d.CLASS_FS, 2, g.VAR[g.SP]);
            g.PTR_TOP = g.PTR[g.SP] - 1;
    elif goto_FIX_NULL or PRODUCTION_NUMBER == 207:  # reference 2070
        #  <NAME EXP>  ::=  NULL
        goto_FIX_NULL = False
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.LOC_P[g.PTR_TOP] = 0;
        g.PSEUDO_FORM[g.PTR_TOP] = XIMD;
        g.NAME_PSEUDOS = g.TRUE;
        g.EXT_P[g.PTR_TOP] = 0;
        g.VAL_P[g.PTR_TOP] = 0x500;
    elif goto_FUNC_IDS or PRODUCTION_NUMBER == 214:  # reference 2140
        #  <MODIFIED STRUCT FUNC> ::= <PREFIX> <NO ARG STRUCT FUNC> <SUBSCRIPT>
        goto_FUNC_IDS = False
        if g.FIXL[g.MPP1] > SYT_MAX: 
            if g.FIXL[g.SP]: 
                ERROR(d.CLASS_FT, 8, g.VAR[g.MPP1]);
            g.TEMP_SYN = g.PSEUDO_FORM[g.PTR[g.SP]];
            g.PTR_TOP = g.PTR[g.MP];
            g.FIXL[g.MP] = g.FIXL[g.MPP1];
            g.VAR[g.MP] = g.VAR[g.MPP1];
        else:
            g.FIXL[g.SP] = g.FIXL[g.SP] | 2;
            goto.MOST_IDS = True
    if goto_MOST_IDS or goto_STRUC_IDS or \
            PRODUCTION_NUMBER == 219:  # reference 2190
        #  <EVENT VAR>  ::=  <PREFIX>  (EVENT ID>  <SUBSCRIPT>
        if not goto_STRUC_IDS:
            goto_MOST_IDS = False
            l.H1 = g.PTR[g.MP];
            g.PSEUDO_TYPE_P[l.H1] = g.SYT_TYPE(g.FIXL[g.MPP1]);
            g.PSEUDO_LENGTH[l.H1] = VAR_LENGTH(g.FIXL[g.MPP1]);
            if g.FIXV[g.MP] == 0: 
                g.STACK_PTR[g.MP] = g.STACK_PTR[g.MPP1];
                g.VAR[g.MP] = g.VAR[g.MPP1];
                if g.FIXV[g.MPP1] == 0: 
                    g.LOC_P[l.H1] = g.FIXL[g.MPP1];
                else:
                    g.FIXV[g.MP], g.LOC_P[l.H1] = g.FIXV[g.MPP1];
                g.PSEUDO_FORM[l.H1] = XSYT;
            else:
                g.VAR[g.MP] = g.VAR[g.MP] + PERIOD + g.VAR[g.MPP1];
                g.TOKEN_FLAGS[g.EXT_P[l.H1]] = g.TOKEN_FLAGS[g.EXT_P[l.H1]] | 0x20;
                g.I = g.FIXL[g.MPP1];
                goto_UNQ_TEST1 = True
                while goto_UNQ_TEST1:
                    goto_UNQ_TEST1 = False
                    while I > 0:
                        g.I = g.SYT_LINK2(I);
                    g.I = -I;
                    if I == 0: 
                        ERROR (d.CLASS_IS, 2, g.VAR[g.MPP1]);
                        break  # GO TO UNQ_TEST2;
                    if I != g.FIXL[g.MP]: 
                        goto_UNQ_TEST1 = True
                        continue
            # UNQ_TEST2:
            g.FIXL[g.MP] = g.FIXL[g.MPP1];
            g.EXT_P[l.H1] = g.STACK_PTR[g.MPP1];
        goto_STRUC_IDS = False
        g.NAME_BIT = SHR(g.VAL_P[l.H1], 1) & 0x80;
        g.TEMP_SYN = g.INX[l.H1];
        g.TEMP3 = g.LOC_P[l.H1];
        if ATTACH_SUBSCRIPT: 
            HALMAT_TUPLE(XTSUB, 0, g.MP, 0, MAJ_STRUC | NAME_BIT);
            g.INX[l.H1] = NEXT_ATOMp - 1;
            HALMAT_FIX_PIPp(LAST_POPp, EMIT_SUBSCRIPT(0x8));
            SETUP_VAC(g.MP, g.PSEUDO_TYPE_P[l.H1]);
            g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x20;
        g.PTR_TOP = l.H1;  # BASH DOWN STACKS
        if g.FIXV[g.MP] > 0:
            HALMAT_TUPLE(XEXTN, 0, g.MP, 0, 0);
            g.TEMP = l.H1;
            if (g.SYT_FLAGS(TEMP3) & NAME_FLAG) != 0:
                g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x4000;
            l.H2 = g.FALSE;
            
            l.PRl.PREV_LIVES_REMOTE = (g.SYT_FLAGS(TEMP3) & REMOTE_FLAG) != 0;
            l.PREV_POINTS = (g.SYT_FLAGS(TEMP3) & NAME_FLAG) != 0;
            l.PREV_REMOTE = l.PREV_LIVES_REMOTE;
            
            while TEMP_SYN != 0:
                g.TEMP = g.TEMP + 1;
                g.TEMP3 = g.LOC_P[g.TEMP];
                HALMAT_PIP(TEMP3, XSYT, 0, 0);
                l.H2 = l.H2 | (g.SYT_FLAGS(TEMP3) & NAME_FLAG) != 0;
                
                # KEEP TRACK OF THE REMOTENESS -----------------
                # OF THE NODE BEING PROCESSED
                l.PREV_REMOTE = ((g.SYT_FLAGS(TEMP3) & NAME_FLAG) > 0);
                l.REMOTE_SET = ((g.SYT_FLAGS(TEMP3) & REMOTE_FLAG) > 0);
                if (l.REMOTE_SET and not l.PREV_REMOTE) \
                        or (l.PREV_POINTS and l.PREV_REMOTE) \
                        or (l.PREV_LIVES_REMOTE and not l.PREV_POINTS):
                    l.CURRENT_LIVES_REMOTE = g.TRUE;
                else:
                    l.CURRENT_LIVES_REMOTE = g.FALSE;
                l.PREV_LIVES_REMOTE = l.CURRENT_LIVES_REMOTE;
                l.PREV_POINTS = l.PREV_REMOTE;
                l.PREV_REMOTE = l.REMOTE_SET;
                
                g.TEMP_SYN = g.INX[g.TEMP];
            if l.H2: 
                g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x4000;
            
            # SET FLAG IN VAL_P TO INDICATE
            # THAT TERMINAL LIVES REMOTE
            if (l.PREV_POINTS and l.PREV_REMOTE) \
                    or (PREV_LIVES_REMOTE and not  l.PREV_POINTS):
                g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x8000;
            
            g.PTR_TOP = g.TEMP;  # WAIT - DONT LOSE EXTN TILL XREF DONE
            if VAR_LENGTH(TEMP3) == g.FIXL[g.MP]:
                if g.TEMP == l.H1: 
                    g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x4;
                g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x1000;
                HALMAT_FIX_PIPTAGS(NEXT_ATOMp - 1, 0, 1);
                if (g.SYT_FLAGS(TEMP3) & NAME_FLAG) != 0:
                    g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x200;
            HALMAT_PIP(g.FIXL[g.MP], XSYT, 0, 1);
            l.H2 = (l.H2 or (g.SYT_FLAGS(g.FIXL[g.MP]) & NAME_FLAG) != 0);
            HALMAT_FIX_PIPp(LAST_POPp, g.TEMP - l.H1 + 2);
            HALMAT_FIX_POPTAG(LAST_POPp, l.H2);
            g.LOC_P[l.H1], l.H2 = LAST_POPp;
            g.PSEUDO_FORM[l.H1] = XXPT;
        else:
            l.H2 = -1;
        if g.PSEUDO_FORM[INX] > 0: 
            if g.FIXL[g.SP] >= 2:
                if DELAY_CONTEXT_CHECK: 
                    ERROR(d.CLASS_EN, 14);
                    g.PSEUDO_FORM[INX] = 0;
                else:
                    g.TEMP_SYN = g.SP;
                # THIS ASSUMES THAT PTR[SP] AND THE INDIRECT STACKS
                # ARE NOT OVERWRITTEN UNTIL AFTER REACHING THE
                # <PRIMARY>::=<MODIFIED ARITH FUNC> PRODUCTION,
                # WHEN THAT PARSING ROUTE IS TAKEN
            else:
                PREC_SCALE(g.SP, g.PSEUDO_TYPE_P[l.H1]);
            if g.PSEUDO_FORM[INX] > 0: 
                g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x40;
        elif IND_LINK > 0: 
            HALMAT_TUPLE(XDSUB, 0, g.MP, 0, g.PSEUDO_TYPE_P[l.H1] | NAME_BIT);
            g.INX[l.H1] = NEXT_ATOMp - 1;
            g.VAL_P[l.H1] = g.VAL_P[l.H1] | 0x20;
            HALMAT_FIX_PIPp(LAST_POPp, EMIT_SUBSCRIPT(0x0));
            SETUP_VAC(g.MP, g.PSEUDO_TYPE_P[l.H1]);
        g.FIXF[g.MP] = g.PTR_TOP;  # RECORD WHERE TOP IS IN CASE CHANGED
        ASSOCIATE()(l.H2);
    elif goto_SIMPLE_SUBS or PRODUCTION_NUMBER == 228:  # reference 2280
        # <SUBSCRIPT> ::= <$> <NUMBER>
        if not goto_SIMPLE_SUBS:
            g.SUB_END_PTR = g.STMT_PTR;
            g.PTR[g.SP] = PUSH_INDIRECT(1);
            g.LOC_P[g.PTR[g.SP]] = g.FIXV[g.SP];
            g.PSEUDO_FORM[g.PTR[g.SP]] = XIMD;
            g.PSEUDO_TYPE_P[g.PTR[g.SP]] = INT_TYPE;
        goto_SIMPLE_SUBS = False
        g.INX[g.PTR[g.SP]] = 1;
        g.VAL_P[g.PTR[g.SP]] = 0;
        g.SUB_COUNT = 1;
        g.ARRAY_SUB_COUNT(-1);
        g.STRUCTURE_SUB_COUNT = -1;
        goto_SS_CHEX = True
    elif goto_SUB_START or PRODUCTION_NUMBER == 231:  # reference 2310
        #  <SUB START>  ::=  <$> (
        goto_SUB_START = False
        g.SUB_COUNT = 0;
        g.STRUCTURE_SUB_COUNT = -1;
        g.ARRAY_SUB_COUNT(-1);
        g.SUB_SEEN = 0;
    elif goto_SHARP_EXP or PRODUCTION_NUMBER == 246:  # reference 2460
        # <# EXPRESSION> ::= <# EXPRESSION> + <TERM>
        if not goto_SHARP_EXP:
            g.TEMP = 0;
        goto_SHARP_EXP = False
        IORS(g.SP);
        if g.FIXL[g.MP] == 1: 
            g.FIXL[g.MP] = g.TEMP + 2;
            g.PTR[g.MP] = g.PTR[g.SP];
        else:
            if g.FIXL[g.MP] == 3: 
                g.TEMP = 1 - g.TEMP;
            ADD_AND_SUBTRACT(g.TEMP);
    elif goto_SS_FIXUP or PRODUCTION_NUMBER == 249:  # reference 2490
        # <$> ::= $
        if not goto_SS_FIXUP:
            g.FIXL[g.MP] = 1;
        goto_SS_FIXUP = False
        g.TEMP = g.FIXF[g.MP - 1];
        if g.TEMP > 0:
            HALMAT_POP(XXXST, 1, XCO_N, g.TEMP + g.FCN_LV - 1);
            HALMAT_PIP(g.FIXL[g.MP - 1], XSYT, 0, 0);
        g.NAMING = g.FALSE;
        if SUBSCRIPT_LEVEL == 0:
            if ARRAYNESS_FLAG: SAVE_ARRAYNESS();
            g.SAVE_ARRAYNESS_FLAG = ARRAYNESS_FLAG;
            g.ARRAYNESS_FLAG = 0;
        g.SUBSCRIPT_LEVEL = SUBSCRIPT_LEVEL + g.FIXL[g.MP];
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.PSEUDO_FORM[g.PTR_TOP] = 0;
        g.LOC_P[g.PTR_TOP], g.INX[g.PTR_TOP] = 0;
    if goto_SS_CHEX or PRODUCTION_NUMBER == 263:  # reference 2630
        # <BIT QUALIFIER> ::= <$(> @ <RADIX> )
        if not goto_SS_CHEX:
            if TEMP3 == 0: 
                g.TEMP3 = 2;
            g.PSEUDO_FORM[g.PTR[g.MP]] = TEMP3;
        goto_SS_CHEX = False
        if SUBSCRIPT_LEVEL > 0:
            g.SUBSCRIPT_LEVEL = SUBSCRIPT_LEVEL - 1;
    elif goto_DO_BIT_CONST or PRODUCTION_NUMBER == 271:  # reference 2710
        # <BIT CONST> ::= TRUE
        if not goto_DO_BIT_CONST:
            g.TEMP_SYN = 1;
        goto_DO_BIT_CONST = False
        g.I = 1;
        goto_DO_BIT_CONSTANT_END = True;
    if goto_DO_BIT_CONSTANT_END or PRODUCTION_NUMBER == 270:  # reference 2700
        #  <BIT CONST> ::= <BIT CONST HEAD> <CHAR STRING>
        if not goto_DO_BIT_CONSTANT_END:
            g.S = g.VAR[g.SP];
            g.I = 1;
            g.K = LENGTH(S);
            g.L = g.FIXL[g.MP];
            g.TEMP_SYN = 0;  #  START WITH VALUE CALC. = O
            # DO CASE TEMP3;
            if TEMP3 == 0:
                g.C[0] = 'D';
                if L != 1:
                    ERROR(d.CLASS_LB, 2);
                    g.L = 1;
                g.TEMP2 = 0;  #  INDICATE START FROM 1ST CHAR
                if SUBSTR(S, TEMP2) > '2147483647':
                    ERROR(d.CLASS_LB, 1);
                    goto_DO_BIT_CONSTANT_END = True
                else:
                    for g.TEMP in range(TEMP2, 1 + LENGTH(S) - 1):  #  CHECK FOR CHAR 1 TO 9
                        l.H1 = BYTE(S, g.TEMP);
                        if not ((l.H1 >= BYTE('0')) & (l.H1 <= BYTE('9'))): 
                            ERROR(d.CLASS_LB, 4);
                            g.TEMP_SYN = 0;
                            goto_DO_BIT_CONSTANT_END = True
                            break
                        else:
                            g.TEMP_SYN = TEMP_SYN * 10;  #  ADD IN NEXT DIGIT
                            g.TEMP_SYN = TEMP_SYN + (l.H1 & 0x0F);
                    #  END OF DO FOR
                    if not goto_DO_BIT_CONSTANT_END:
                        g.I = 1;
                        while SHR(TEMP_SYN, I) != 0:
                            g.I = I + 1;
                        goto_DO_BIT_CONSTANT_END = True
                #  END OF CASE 0
            elif TEMP3 == 1:
                # CASE 1, BIN
                g.C[0] = 'B';
                for g.TEMP in range(0, 1 + LENGTH(S) - 1):  #  CHECK FOR '0' OR '1'
                   l.H1 = BYTE(S, g.TEMP);
                   if not ((l.H1 == BYTE('0')) or (l.H1 == BYTE('1'))):
                       ERROR(d.CLASS_LB, 5);
                       g.TEMP_SYN = 0;
                       goto_DO_BIT_CONSTANT_END = True
                   else:
                       g.TEMP_SYN = SHL(TEMP_SYN, 1);  #  ADDIN NEXT VALUE
                       g.TEMP_SYN = TEMP_SYN | (l.H1 & 0x0F);
                #  END OF CASE 1
            elif TEMP3 == 2:
                # CASE 2, NO RADIX BASE 2 AT MOMENT
                pass;
            elif TEMP3 == 3:
                # CASE 3, OCT
                g.C[0] = 'O';
                for g.TEMP in range(0, 1 + LENGTH(S) - 1):  #  CHECK FOR OCTAL CHARACTERS
                    l.H1 = BYTE(S, g.TEMP);
                    if not ((l.H1 >= BYTE('0')) and (l.H1 <= BYTE('7'))):
                        ERROR(d.CLASS_LB, 6);
                        g.TEMP_SYN = 0;
                        goto_DO_BIT_CONSTANT_END = True
                    else:
                        g.TEMP_SYN = SHL(TEMP_SYN, 3);  #  ADD IN NEXT VALUE
                        g.TEMP_SYN = TEMP_SYN | (l.H1 & 0x0F);
                #  END OF CASE 3
            elif TEMP3 == 4:
                # CASE 4, HEX
                g.C[0] = 'H';
                for g.TEMP in range(0, 1 + LENGTH(S) - 1):  #  CHECK FOR HEXADECIMAL CHARACTERS
                    l.H1 = BYTE(S, g.TEMP);
                    if not ((l.H1 >= BYTE('0')) and (l.H1 <= BYTE('9'))):
                        if not ((l.H1 >= BYTE('A')) and (l.H1 <= BYTE('F'))):
                            ERROR(d.CLASS_LB, 7);
                            g.TEMP_SYN = 0;
                            goto_DO_BIT_CONSTANT_END = True
                        else:
                            g.TEMP_SYN = SHL(TEMP_SYN, 4);  #  GET NEW VAL WITH NUM.DIG.
                            g.TEMP_SYN = TEMP_SYN + 9 + (l.H1 & 0x0F);
                    else:
                       g.TEMP_SYN = SHL(TEMP_SYN, 4);  #  ADD IN NUM. VALUE
                       g.TEMP_SYN = TEMP_SYN + (l.H1 & 0x0F);
                # END OF CASE 4
            #  END OF DO CASE
            #  INCORPORATE REPETITION FACTOR
            if not goto_DO_BIT_CONSTANT_END:
                g.TEMP2 = TEMP_SYN;
                g.J = TEMP3 * K;
                for g.TEMP in range(2, 1 + L):
                    g.TEMP_SYN = SHL(TEMP_SYN, J) | TEMP2;
                g.I = J * L;
                if I > BIT_LENGTH_LIM: 
                    if I - TEMP3 < BIT_LENGTH_LIM:
                        l.H1 = BYTE(S);
                        if l.H1 >= BYTE('A') and l.H1 <= BYTE('F'): 
                            l.H1 = l.H1 + 9;
                        l.H1 = l.H1 & 0x0F;
                        if SHR(l.H1, BIT_LENGTH_LIM + TEMP3 - I) != 0:
                            ERROR(d.CLASS_LB, 1);
                    else:
                        ERROR(d.CLASS_LB, 1);
                    g.I = BIT_LENGTH_LIM;
        goto_DO_BIT_CONSTANT_END = False
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = BIT_TYPE;
        g.PSEUDO_FORM[g.PTR[g.MP]] = XLIT;
        g.PSEUDO_LENGTH[g.PTR[g.MP]] = I;
        g.LOC_P[g.PTR[g.MP]] = SAVE_LITERAL(2, TEMP_SYN, I);
    elif goto_CHAR_LITS or PRODUCTION_NUMBER == 275:  # reference 2750
        #  <CHAR CONST>  ::=  <CHAR STRING>
        goto_CHAR_LITS = False
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.LOC_P[g.PTR[g.MP]] = SAVE_LITERAL(0, g.VAR[g.MP]);
        g.PSEUDO_FORM[g.PTR[g.MP]] = XLIT;
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = CHAR_TYPE;
        g.PSEUDO_LENGTH[g.PTR[g.MP]] = LENGTH(g.VAR[g.MP]);
    elif goto_IO_CONTROL or PRODUCTION_NUMBER == 277:  # reference 2770
        #  <IO CONTROL>  ::=  SKIP  (  <ARITH EXP>  )
        if not goto_IO_CONTROL:
            g.TEMP = 3;
        goto_IO_CONTROL = False
        if UNARRAYED_INTEGER(g.SP - 1): 
            ERROR(d.CLASS_TC, 1);
        g.VAL_P[g.PTR[g.MP]] = 0;
        g.PTR[g.MP] = g.PTR[g.SP - 1];
    elif goto_CHECK_READ or PRODUCTION_NUMBER == 282:  # reference 2820
        #  <READ PHRASE>  ::=  <READ KEY>  <READ ARG>
        goto_CHECK_READ = False
        if g.INX[g.PTR[g.MP]] == 0: 
            if SHR(g.VAL_P[g.PTR[g.SP]], 7): ERROR(d.CLASS_T, 3);
            if g.PSEUDO_TYPE_P[g.PTR[g.SP]] == EVENT_TYPE: ERROR(d.CLASS_T, 2);
        elif g.TEMP > 0: 
            pass;
        elif READ_ALL_TYPE(g.SP): 
            ERROR(d.CLASS_T, 1);
    elif goto_EMIT_IO_ARG or PRODUCTION_NUMBER == 286:  # reference 2860
        #  <READ ARG>  ::=  <VARIABLE>
        if not goto_EMIT_IO_ARG:
            g.TEMP = 0;
        goto_EMIT_IO_ARG = False
        if KILL_NAME(g.MP): 
            ERROR(d.CLASS_T, 5);
        if INLINE_LEVEL > 0: 
            ERROR(d.CLASS_PP, 5);
        HALMAT_TUPLE(XXXAR, XCO_N, g.MP, 0, 0);
        HALMAT_FIX_PIPTAGS(NEXT_ATOMp - 1, g.PSEUDO_TYPE_P[g.PTR[g.MP]], g.TEMP);
        if g.PSEUDO_TYPE_P[g.PTR[g.MP]] == MAJ_STRUC:
            if (g.SYT_FLAGS(VAR_LENGTH(g.FIXV[g.MP])) & MISC_NAME_FLAG) != 0:
                ERROR(d.CLASS_T, 6);
        EMIT_ARRAYNESS();
        g.PTR_TOP = g.PTR[g.MP] - 1;
    elif goto_EMIT_IO_HEAD or PRODUCTION_NUMBER == 290:  # reference 2900
        #  <READ KEY>  ::=  READ  (  <NUMBER>  )
        if not goto_EMIT_IO_HEAD:
            g.TEMP = 0;
        goto_EMIT_IO_HEAD = False
        XSET(SHL(g.TEMP, 11));
        HALMAT_POP(XXXST, 1, XCO_N, 0);
        HALMAT_PIP(g.TEMP, XIMD, 0, 0);
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        if g.FIXV[g.MP + 2] > DEVICE_LIMIT: 
            ERROR(d.CLASS_TD, 1, '' + DEVICE_LIMIT);
            g.LOC_P[g.PTR[g.MP]] = 0;
        else:
            g.LOC_P[g.PTR[g.MP]] = g.FIXV[g.MP + 2];
            g.I = g.IODEV[g.FIXV[g.MP + 2]];
            if (I & 0x28) == 0: 
                if g.TEMP == 2: 
                    if (I & 0x01) == 0: 
                        g.I = I | 0x04;
                    else:
                        g.I = I | 0x02;
                else:
                    g.I = I | 0x01;
                    if (I & 0x04) != 0: 
                        if (I & 0x40) != 0: 
                            g.I = I | 0x80;
                        else:
                            g.I = (I & 0xFB) | 0x02;
            g.IODEV[g.FIXV[g.MP + 2]] = I;
        g.PSEUDO_FORM[g.PTR[g.MP]] = XIMD;
        g.INX[g.PTR[g.MP]] = g.TEMP;
        if UPDATE_BLOCK_LEVEL > 0: 
            ERROR(d.CLASS_UT, 1);
    if goto_CLOSE_SCOPE or PRODUCTION_NUMBER == 293:  # reference 2930
        #  <BLOCK DEFINITION> ::= <BLOCK STMT> <BLOCK BODY> <CLOSING> ;
        if not goto_CLOSE_SCOPE:
            g.TEMP = XCLOS;
            g.TEMP2 = 0;
        goto_CLOSE_SCOPE = False
        HALMAT_POP(g.TEMP, 1, 0, TEMP2);
        HALMAT_PIP(g.BLOCK_SYTREF[g.NEST], XSYT, 0, 0);
        for I in range(0, 1 + g.NDECSY() - REGULAR_PROCMARK):
            g.J = g.NDECSY() - I;
            if (g.SYT_FLAGS(J) & INACTIVE_FLAG) == 0:
                g.CLOSE_BCD = SYT_NAME(J);
                if SYT_CLASS(J) == FUNC_CLASS:
                    if (g.SYT_FLAGS(J) & DEFINED_LABEL) == 0:
                       ERROR(d.CLASS_PL, 1, g.CLOSE_BCD);
                    DISCONNECT(J);
                elif SYT_CLASS(J) == LABEL_CLASS:
                    if (g.SYT_FLAGS(J) & DEFINED_LABEL) == 0:
                        # UNDEFINED CALLABLE LABEL
                        if g.SYT_TYPE(J) == g.STMT_LABEL:
                            DISCONNECT(J);
                            ERROR(d.CLASS_PL, 5, g.CLOSE_BCD);
                        # UNDEFINED OBJECT OF GO TO
                        else:
                            # CALLED/SCHED BUT UNDEFINED PROCS/TASKS
                            if g.NEST == 1:
                                ''' CLOSING PROGRAM -
                                    MAKE UNDEFINED CALLS/SCHEDS
                                    INTO ERRORS '''
                                ERROR(d.CLASS_PL, 6, g.CLOSE_BCD);
                                DISCONNECT(J);
                            else:
                                SET_OUTER_REF(J, 0x6000);
                                g.SYT_NEST(J, g.NEST - 1);
                        # END OF CALLED LABELS
                    # END OF UNDEFINED CALLABLE LABELS
                    elif g.SYT_TYPE(J) == IND_CALL_LAB:
                        g.SYT_NEST(J, g.NEST - 1);
                        g.K = SYT_PTR(J);
                        while g.SYT_TYPE(K) == IND_CALL_LAB:
                            g.K = SYT_PTR(K);
                        if SYT_NEST(K) >= SYT_NEST(J):
                            ''' IND CALL HAS REACHED SAME SCOPE AS
                                DEFINITION OF LABEL. SO LEAVE
                                AS IND CALL AND DISCONNECT FROM SYT '''
                            if SYT_PTR(J) == K:
                                if g.SYT_LINK1(K) < 0:
                                    if g.DO_LEVEL < (-g.SYT_LINK1(K)):
                                        ERROR(d.CLASS_PL, 11, g.CLOSE_BCD);
                            DISCONNECT(J);
                            TIE_XREF(J);
                    # END OF TYPE = IND_CALL_LAB
                    else:
                        DISCONNECT(J);  # NONE OF THE ABOVE
                # END OF LABEL CLASS
                else:
                    DISCONNECT(J);  # ALL OTHER CLASSES
        if g.BLOCK_MODE[g.NEST] == UPDATE_MODE:
            g.UPDATE_BLOCK_LEVEL = UPDATE_BLOCK_LEVEL - 1;
        if LENGTH(g.VAR[g.SP - 1]) > 0:
            if g.VAR[g.SP - 1] != CURRENT_SCOPE:
                ERROR(d.CLASS_PL, 3, CURRENT_SCOPE);
        if REGULAR_PROCMARK > g.NDECSY():  # NO LOCAL NAMES
            g.SYT_PTR(g.FIXL[g.MP], 0);
        if (g.SYT_FLAGS(g.FIXL[g.MP]) & ACCESS_FLAG) != 0:
            if g.BLOCK_MODE[g.NEST] == CMPL_MODE:
                for I in range(g.FIXL[g.MP], 1 + g.NDECSY()):
                    g.SYT_FLAGS(I, g.SYT_FLAGS(I) | READ_ACCESS_FLAG);
        ''' IF THIS IS THE CLOSE OF A COMPOOL INCLUDED REMOTE
            THEN MAKE SURE THAT ALL OF THE ITEMS IN THE COMPOOL
            ARE ALSO FLAGED AS REMOTE - EXCEPT FOR NAME TYPES AND
            STRUCTURE TEMPLATE VARIABLES. '''
        if ((g.SYT_FLAGS(g.FIXL[g.MP]) & EXTERNAL_FLAG) != 0) \
                and ((g.SYT_FLAGS(g.FIXL[g.MP]) & REMOTE_FLAG) != 0):
            if g.BLOCK_MODE[g.NEST] == CMPL_MODE:
                for I in range(g.FIXL[g.MP], 1 + g.NDECSY()):
                    # IF 16-BIT NAME VARIABLE WAS INITIALIZED TO NON-REMOTE VARIABLE IN
                    # A REMOTELY INCLUDED COMPOOL, IT IS NOW INVALID.
                    
                    def TEMPL_INITIAL_CHECK():
                        # IS POINTED TO BY A NAME VARIABLE
                        if (g.SYT_FLAGS(I) & MISC_NAME_FLAG) != 0:
                            if g.SYT_TYPE(I) != TEMPL_NAME:  # NOT A TEMPLATE
                                                          # NON-REMOTE
                                if (g.SYT_FLAGS(I) & REMOTE_FLAG) == 0:
                                    ERROR(d.CLASS_DI, 21);
           
                    TEMPL_INITIAL_CHECK();
                    # INCLUDED_REMOTE MEANS VARIABLE LIVES REMOTE ONLY BECAUSE
                    # IT WAS INCLUDED REMOTE (IT RESIDES IN #P, NOT IN #R)
                    if (SYT_CLASS(I) != TEMPLATE_CLASS): 
                            # NOT A NAME VARIABLE AND NOT INITIALLY DECLARED REMOTE
                            if ((g.SYT_FLAGS(I) & NAME_FLAG) == 0) and \
                                    ((g.SYT_FLAGS(I) & REMOTE_FLAG) == 0):
                                g.SYT_FLAGS(I, g.SYT_FLAGS(I) | REMOTE_FLAG | \
                                                INCLUDED_REMOTE);
                                # FOR NAME VARIABLES, SET THAT THEY NOW LIVE REMOTE
                                if ((g.SYT_FLAGS(I) & NAME_FLAG) != 0):
                                    g.SYT_FLAGS(I, g.SYT_FLAGS(I) | \
                                                    INCLUDED_REMOTE);

        g.SYT_FLAGS(g.NDECSY(), g.SYT_FLAGS(g.NDECSY()) | ENDSCOPE_FLAG);
        g.CURRENT_SCOPE = g.VAR[g.MP];
        if g.PTR[g.MPP1]: 
            # DO CASE EXTERNAL_MODE;
            if EXTERNAL_MODE == 0:
                #  NOT EXTERNAL
                if g.BLOCK_MODE[g.NEST] == CMPL_MODE: ERROR(d.CLASS_PC, 1);
            elif EXTERNAL_MODE == 1:
                #  PROC MODE
                ERROR(d.CLASS_PS, 1);
            elif EXTERNAL_MODE == 2:
                #  FUNC MODE
                ERROR(d.CLASS_PS, 1);
            elif EXTERNAL_MODE == 3:
                #  COMPOOL MODE
                ERROR(d.CLASS_PC, 2);
            elif EXTERNAL_MODE == 4:
                # PROGRAM MODE
                ERROR(d.CLASS_PS, 1);
        OUTPUT_WRITER();
        EMIT_SMRK();
        if g.BLOCK_MODE[g.NEST] == INLINE_MODE: 
            g.INLINE_INDENT_RESET = g.EXT_P[g.PTR[g.MP]];
            g.INDENT_LEVEL = INLINE_INDENT + g.INDENT_INCR;
            g.INLINE_STMT_RESET = g.STMT_NUM();
            g.STMT_NUM(g.INX[g.PTR[g.MP]]);
            g.INX[g.PTR[g.MP]] = 0;
            if g.PSEUDO_TYPE_P[g.PTR[g.MP]] == MAJ_STRUC: 
                g.FIXL[g.MP] = g.PSEUDO_LENGTH[g.PTR[g.MP]];
            RESET_ARRAYNESS();
            g.INLINE_LEVEL = INLINE_LEVEL - 1;
            g.NEST_LEVEL = NEST_LEVEL - 1;
            if INLINE_LEVEL == 0: 
                g.STAB_MARK = 0
                g.STAB2_MARK = 0;
                XSET(g.STAB_STACK[0]);
                g.SRN_FLAG = g.FALSE;
                g.SRN[2] = SRN_MARK[:];
                g.INCL_SRN[2] = INCL_SRN_MARK[:];
                g.SRN_COUNT[2] = SRN_COUNT_MARK;
            g.FIXF[g.MP] = 0;
        else:
            BLOCK_SUMMARY();
            g.OUTER_REF_INDEX = (g.OUTER_REF_PTR_P[g.NEST] & 0x7FFF) - 1;
            g.INDENT_LEVEL = g.INDENT_STACK[g.NEST];
            g.NEST_LEVEL = g.NEST_STACK[g.NEST];
        g.REGULAR_PROCMARK = g.PROCMARK_STACK[g.NEST];
        g.PROCMARK = REGULAR_PROCMARK
        g.SCOPEp = g.SCOPEp_STACK[g.NEST];
        g.I = 0;
        while ON_ERROR_PTR < -SYT_ARRAY(g.BLOCK_SYTREF[g.NEST]):
            if EXT_ARRAY(ON_ERROR_PTR) == 0x3FFF: 
                g.I = I + 0x1001;
            else:
                g.I = I + 1;
            g.ON_ERROR_PTR = ON_ERROR_PTR + 1;
        g.SYT_ARRAY(g.BLOCK_SYTREF[g.NEST], I | 0xE000);
        g.NEST = g.NEST - 1;
        g.DO_INX[g.DO_LEVEL] = g.DO_INX[g.DO_LEVEL] & 0x7F;
        if g.NEST == 0:
            if EXTERNAL_MODE > 0: 
                if g.SIMULATING == 2:
                    g.STMT_TYPE = 0;
                    g.SIMULATING = 1;
                g.EXTERNAL_MODE = 0;
                g.TPL_VERSION = g.BLOCK_SYTREF[g.NEST + 1];
                g.SYT_LOCKp(TPL_VERSION, 0);
            elif g.BLOCK_MODE[0] > 0:
                if EXTERNALIZE == 4: 
                    g.EXTERNALIZE = 2;
                EMIT_EXTERNAL();
    elif goto_INLINE_DEFS or PRODUCTION_NUMBER == 297:  # reference 2970
        #  <ARITH INLINE DEF>  ::=  FUNCTION <ARITH SPEC>  ;
        if not goto_INLINE_DEFS:
            if TYPE == 0: 
                g.TYPE = DEFAULT_TYPE;
            if (ATTRIBUTES & SD_FLAGS) == 0: 
                g.ATTRIBUTES = ATTRIBUTES | (DEFAULT_ATTR & SD_FLAGS);
            if TYPE < g.SCALAR_TYPE: 
                g.TEMP = TYPE(TYPE);
            else:
                g.TEMP = 0;
        goto_INLINE_DEFS = False
        if CONTEXT == EXPRESSION_CONTEXT: 
            ERROR(d.CLASS_PP, 11);
        g.CONTEXT = 0;
        g.GRAMMAR_FLAGS[g.STACK_PTR[g.MP]] = g.GRAMMAR_FLAGS[g.STACK_PTR[g.MP]] | INLINE_FLAG;
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.INLINE_LEVEL = INLINE_LEVEL + 1;
        if INLINE_LEVEL > 1: 
            ERROR(d.CLASS_PP, 10);
        else:
            g.STAB_MARK = STAB_STACKTOP;
            g.STAB2_MARK = STAB2_STACKTOP;
            g.STAB_STACK[0] = STMT_TYPE;
            g.SRN_MARK = g.SRN[2][:];
            g.INCL_SRN_MARK = g.INCL_SRN[2][:];
            g.SRN_COUNT_MARK = g.SRN_COUNT[2];
            g.STMT_TYPE = 0;
        g.INLINE_LABEL = INLINE_LABEL + 1;
        g.VAR[g.MP] = l.INLINE_NAME + INLINE_LABEL;
        g.NAME_HASH = HASH(g.VAR[g.MP], SYT_HASHSIZE);
        g.FIXL[g.MP] = ENTER(g.VAR[g.MP], FUNC_CLASS);
        g.FIXL[g.MP] = I
        if g.SIMULATING: 
            STAB_LAB(I);
        SET_XREF(I, XREF_REF);
        g.SYT_TYPE(I, TYPE);
        g.SYT_FLAGS(I, g.SYT_FLAGS(I) | DEFINED_LABEL | ATTRIBUTES);
        g.VAR_LENGTH(I, g.TEMP);
        HALMAT_POP(XIDEF, 1, 0, INLINE_LEVEL);
        HALMAT_PIP(I, XSYT, 0, 0);
        SETUP_VAC(g.MP, TYPE, g.TEMP);
        g.TEMP2 = INLINE_MODE;
        # See the comments in g.py for TYPE to understand the next few lines
        g.TYPE = 0
        g.BIT_LENGTH = 0
        g.CHAR_LENGTH = 0
        g.MAT_LENGTH = 0
        g.VEC_LENGTH = 0
        g.ATTRIBUTES = 0
        g.ATTRIBUTES2 = 0
        g.ATTR_MASK = 0
        g.STRUC_PTR = 0
        g.STRUC_DIM = 0
        g.CLASS = 0
        g.NONHAL = 0
        g.LOCKp = 0
        g.IC_PTR = 0
        g.IC_FND = 0
        g.N_DIM = 0
        g.S_ARRAY = [0] * (g.N_DIM_LIM + 1)
        # (End of TYPE loop)------------------------------------------------
        SAVE_ARRAYNESS();
        if (SUBSCRIPT_LEVEL | g.EXPONENT_LEVEL) != 0: 
            ERROR(d.CLASS_B, 2);
        goto_INLINE_ENTRY = True
    elif goto_UPDATE_HEAD or PRODUCTION_NUMBER == 314:  # reference 3140
        #  <BLOCK STMT HEAD>  ::=  <LABEL DEFINITION>  UPDATE
        if not goto_UPDATE_HEAD:
            g.VAR_LENGTH(g.FIXL[g.MP], 1);
            HALMAT_BACKUP(LAST_POPp);
        goto_UPDATE_HEAD = False
        if UPDATE_BLOCK_LEVEL > 0: 
            ERROR(d.CLASS_UI, 2);
        g.UPDATE_BLOCK_LEVEL = UPDATE_BLOCK_LEVEL + 1;
        g.TEMP2 = UPDATE_MODE;
        g.TEMP = XUDEF;
        SET_LABEL_TYPE(g.FIXL[g.MP], g.STMT_LABEL);
        if g.NEST == 0: 
            ERROR(d.CLASS_PP, 3, g.VAR[g.MPP1]);
            goto_DUPLICATE_BLOCK = True
        else:
            goto_NEW_SCOPE = True
    elif goto_FUNC_HEADER or PRODUCTION_NUMBER == 316:  # reference 3160
        #  <BLOCK STMT HEAD>  ::=  <FUNCTION NAME>
        goto_FUNC_HEADER = False
        if PARMS_PRESENT == 0:
            g.PARMS_WATCH = g.FALSE;
            if MAIN_SCOPE == g.SCOPEp: 
                g.COMSUB_END(g.FIXL[g.MP]);
        g.FACTORING = g.TRUE;
        g.DO_INIT = g.FALSE;
        if TYPE == 0:
            g.TYPE = DEFAULT_TYPE;
        elif TYPE == EVENT_TYPE:
            ERROR(d.CLASS_FT, 3, SYT_NAME(ID_LOC));
            g.TYPE = DEFAULT_TYPE;
        if (ATTRIBUTES & SD_FLAGS) == 0:
            if (TYPE >= g.MAT_TYPE) and (TYPE <= INT_TYPE):
                g.ATTRIBUTES = ATTRIBUTES | (DEFAULT_ATTR & SD_FLAGS);
        if TYPE == MAJ_STRUC: 
            CHECK_STRUC_CONFLICTS();
        if g.SYT_TYPE(ID_LOC) == 0: 
            SET_SYT_ENTRIES();
        else:
            if g.SYT_TYPE(ID_LOC) != TYPE:
                ERROR(d.CLASS_DT, 1, SYT_NAME(ID_LOC));
            else:  # TYPES MATCH, WHAT ABOUT SIZES
               if TYPE <= g.VEC_TYPE:
                    if TYPE(TYPE) != VAR_LENGTH(ID_LOC):
                        ERROR(d.CLASS_FT, 4, SYT_NAME(ID_LOC));
               elif TYPE == MAJ_STRUC: 
                    if STRUC_PTR != VAR_LENGTH(ID_LOC):
                        ERROR(d.CLASS_FT, 6, SYT_NAME(ID_LOC));
               if (ATTRIBUTES & SD_FLAGS) != 0:
                    if ((g.SYT_FLAGS(ID_LOC) & ATTRIBUTES) & SD_FLAGS) == 0:
                        ERROR(d.CLASS_FT, 7, SYT_NAME(ID_LOC));
            # END OF TYPES MATCH
            # See the comments in g.py for TYPE to understand the next few lines
            g.TYPE = 0
            g.BIT_LENGTH = 0
            g.CHAR_LENGTH = 0
            g.MAT_LENGTH = 0
            g.VEC_LENGTH = 0
            g.ATTRIBUTES = 0
            g.ATTRIBUTES2 = 0
            g.ATTR_MASK = 0
            g.STRUC_PTR = 0
            g.STRUC_DIM = 0
            g.CLASS = 0
            g.NONHAL = 0
            g.LOCKp = 0
            g.IC_PTR = 0
            g.IC_FND = 0
            g.N_DIM = 0
            g.S_ARRAY = [0] * (g.N_DIM_LIM + 1)
            # (End of TYPE loop)------------------------------------------------
    elif goto_EMIT_NULL or PRODUCTION_NUMBER == 334:  # reference 3340
        #  <DECLARE ELEMENT>  ::=  <REPLACE STMT>  ;
        if not goto_EMIT_NULL:
            g.STMT_TYPE = REPLACE_STMT_TYPE;
            if g.SIMULATING: 
                STAB_HDR();
        goto_EMIT_NULL = False
        OUTPUT_WRITER();
        EMIT_SMRK(1);
    elif goto_INIT_MACRO or PRODUCTION_NUMBER == 338:  # reference 3380
        #  <REPLACE HEAD>  ::=  <IDENTIFIER>
        goto_INIT_MACRO = False
        g.CONTEXT = 0;
        g.MACRO_TEXT(g.FIRST_FREE(), 0xEF);  # INITIALIZE TO NULL
    elif goto_NEXT_ARG or PRODUCTION_NUMBER == 340:  # reference 3400
        #  <ARG LIST>  ::=  <IDENTIFIER>
        goto_NEXT_ARG = False
        g.MACRO_ARG_COUNT = MACRO_ARG_COUNT + 1 ;
        if MACRO_ARG_COUNT > MAX_PARAMETER:
            ERROR(d.CLASS_IR, 10);
    elif goto_DECL_STAT or PRODUCTION_NUMBER == 343:  # reference 3430
        #  <DECLARE STATEMENT>  ::=  DECLARE  <DECLARE BODY>  ;
        if not goto_DECL_STAT:
            if PARMS_PRESENT <= 0: 
                g.PARMS_WATCH = g.FALSE;
                if EXTERNALIZE: 
                    g.EXTERNALIZE = 4;
        goto_DECL_STAT = False
        g.FACTORING = g.TRUE;
        if IC_FOUND > 0: 
            g.IC_LINE = g.INX[IC_PTR1];
            g.PTR_TOP = IC_PTR1 - 1;
        g.IC_FOUND = 0;
        if ATTR_LOC > 1: 
            OUTPUT_WRITER(g.LAST_WRITE, ATTR_LOC - 1);
            if not ATTR_FOUND: 
                if (g.GRAMMAR_FLAGS[1] & ATTR_BEGIN_FLAG) != 0:
                    g.INDENT_LEVEL = g.INDENT_LEVEL + ATTR_INDENT + g.INDENT_INCR;
            elif g.INDENT_LEVEL == SAVE_INDENT_LEVEL:
                g.INDENT_LEVEL = g.INDENT_LEVEL + ATTR_INDENT;
            OUTPUT_WRITER(ATTR_LOC, g.STMT_PTR);
        else:
            OUTPUT_WRITER(g.LAST_WRITE, g.STMT_PTR);
        g.INDENT_LEVEL = SAVE_INDENT_LEVEL;
        g.LAST_WRITE, SAVE_INDENT_LEVEL = 0;
    elif goto_NO_ATTR_STRUCT or PRODUCTION_NUMBER == 352:  # reference 3520
        #  <STRUCT STMT HEAD>  ::=  <IDENTIFIER>  :  <LEVEL>
        goto_NO_ATTR_STRUCT = False
        g.BUILDING_TEMPLATE = g.TRUE;
        g.FIXL[g.MPP1] = g.FIXL[g.MP];
        g.ID_LOC = g.FIXL[g.MPP1]
        g.STRUC_SIZE = 0;
        g.REF_ID_LOC = ID_LOC;
        if g.FIXV[g.SP] > 1: 
            ERROR(d.CLASS_DQ, 1);
        g.FIXV[g.MP] = 1;
        g.SYT_CLASS(ID_LOC, TEMPLATE_CLASS);
        g.SYT_TYPE(ID_LOC, TEMPL_NAME);
        if (ATTRIBUTES & ILL_TEMPL_ATTR) != 0 or \
                (ATTRIBUTES2 & NONHAL_FLAG) != 0: 
            ERROR(d.CLASS_DA, 22, SYT_NAME(ID_LOC));
            g.ATTRIBUTES = ATTRIBUTES & ~ILL_TEMPL_ATTR;
            g.ATTRIBUTES2 = ATTRIBUTES2 & ~NONHAL_FLAG;
            g.DO_INIT = g.FALSE;
        if (ATTRIBUTES & ALDENSE_FLAGS) == 0:
            g.ATTRIBUTES = ATTRIBUTES | (DEFAULT_ATTR & ALDENSE_FLAGS);
        g.SYT_FLAGS(ID_LOC, g.SYT_FLAGS(ID_LOC) | ATTRIBUTES);
        HALMAT_INIT_CONST();
        # See the comments in g.py for TYPE to understand the next few lines
        g.TYPE = 0
        g.BIT_LENGTH = 0
        g.CHAR_LENGTH = 0
        g.MAT_LENGTH = 0
        g.VEC_LENGTH = 0
        g.ATTRIBUTES = 0
        g.ATTRIBUTES2 = 0
        g.ATTR_MASK = 0
        g.STRUC_PTR = 0
        g.STRUC_DIM = 0
        g.CLASS = 0
        g.NONHAL = 0
        g.LOCKp = 0
        g.IC_PTR = 0
        g.IC_FND = 0
        g.N_DIM = 0
        g.S_ARRAY = [0] * (g.N_DIM_LIM + 1)
        # (End of TYPE loop)------------------------------------------------
        g.SAVE_INDENT_LEVEL = g.INDENT_LEVEL;
        if g.STACK_PTR[g.SP] > 0:
            OUTPUT_WRITER(0, g.STACK_PTR[g.SP] - 1);
        g.LAST_WRITE = g.STACK_PTR[g.SP];
        g.INDENT_LEVEL = SAVE_INDENT_LEVEL + g.INDENT_INCR;  # IN BY ONE LEVEL
        goto_STRUCT_GOING_DOWN = True
    if goto_STRUCT_GOING_UP or goto_STRUCT_GOING_DOWN or \
            PRODUCTION_NUMBER == 354:  # reference 3540
        #  <STRUCT STMT HEAD> ::= <STRUCT STMT HEAD> <DECLARATION> , <LEVEL>
        if not goto_STRUCT_GOING_DOWN:
            goto_STRUCT_GOING_UP = False
            if (g.SYT_FLAGS(ID_LOC) & DUPL_FLAG) != 0:
                g.SYT_FLAGS(ID_LOC, g.SYT_FLAGS(ID_LOC) & (not DUPL_FLAG));
                g.S = SYT_NAME(ID_LOC);
                g.TEMP_SYN = g.SYT_LINK1(g.FIXL[g.MP]);
                while TEMP_SYN != ID_LOC:
                    if S == SYT_NAME(TEMP_SYN):
                        ERROR(d.CLASS_DQ, 9, S);
                        g.S = '';
                    g.TEMP_SYN = g.SYT_LINK2(TEMP_SYN);
        if goto_STRUCT_GOING_DOWN or g.FIXV[g.SP] > g.FIXV[g.MP]:
            if not goto_STRUCT_GOING_DOWN: 
                if g.FIXV[g.SP] > g.FIXV[g.MP] + 1: 
                    ERROR(d.CLASS_DQ, 2);
                g.FIXV[g.MP] = g.FIXV[g.MP] + 1;
                if (TYPE | CLASS) != 0:
                    ERROR(d.CLASS_DT, 5, SYT_NAME(ID_LOC));  # TYPE NOT LEGAL
                if (ATTRIBUTES & ILL_MINOR_STRUC) != 0 or NAME_IMPLIED or \
                        (ATTRIBUTES2 & NONHAL_FLAG) != 0: 
                    ERROR(d.CLASS_DA, 20, SYT_NAME(ID_LOC));
                    g.ATTRIBUTES = ATTRIBUTES & (not ILL_MINOR_STRUC);
                    g.ATTRIBUTES2 = ATTRIBUTES2 & (not NONHAL_FLAG);
                    g.NAME_IMPLIED = g.FALSE;
                    g.DO_INIT = 0;
                if N_DIM != 0: 
                    ERROR(d.CLASS_DA, 21, SYT_NAME(ID_LOC));
                    g.N_DIM = 0;
                    g.ATTRIBUTES = ATTRIBUTES & (not ARRAY_FLAG);
                g.SYT_CLASS(ID_LOC, TEMPLATE_CLASS);
                g.TYPE = MAJ_STRUC;
                if (ATTRIBUTES & ALDENSE_FLAGS) == 0:
                    g.ATTRIBUTES = ATTRIBUTES | (g.SYT_FLAGS(g.FIXL[g.MP]) & ALDENSE_FLAGS);
                # GIVE ALIGNED/DENSE OF PARENT IF NOT LOCALLY SPECIFIED
                if (ATTRIBUTES & RIGID_FLAG) == 0:
                    g.ATTRIBUTES = ATTRIBUTES | (g.SYT_FLAGS(g.FIXL[g.MP]) & RIGID_FLAG);
                SET_SYT_ENTRIES();
                if g.STACK_PTR[g.SP] > 0:
                    OUTPUT_WRITER(g.LAST_WRITE, g.STACK_PTR[g.SP] - 1);
                g.LAST_WRITE = g.STACK_PTR[g.SP];
                g.INDENT_LEVEL = SAVE_INDENT_LEVEL + (g.FIXV[g.MP] * g.INDENT_INCR);
            goto_STRUCT_GOING_DOWN = False
            PUSH_INDIRECT(1);
            g.LOC_P[g.PTR_TOP] = g.FIXL[g.MP];
            g.SYT_LINK1(g.FIXL[g.MPP1], g.FIXL[g.MPP1] + 1);
            g.FIXL[g.MP] = g.FIXL[g.MPP1];
        else:
            g.TEMP_SYN = g.FIXL[g.MPP1];
            g.FIXL[g.SP] = g.FIXL[g.MP];
            while g.FIXV[g.SP] < g.FIXV[g.MP]:
                g.SYT_LINK2(g.FIXL[g.MPP1], -g.FIXL[g.MP]);
                g.FIXL[g.MPP1] = g.FIXL[g.MP];
                g.FIXL[g.MP] = g.LOC_P[g.PTR_TOP];
                g.PTR_TOP = g.PTR_TOP - 1;
                g.FIXV[g.MP] = g.FIXV[g.MP] - 1;
            if TYPE == 0: 
                g.TYPE = DEFAULT_TYPE;
            elif TYPE == MAJ_STRUC: 
                if not NAME_IMPLIED:
                    if STRUC_PTR == REF_ID_LOC:
                        ERROR(d.CLASS_DT, 6);
                        g.SYT_FLAGS(REF_ID_LOC, g.SYT_FLAGS(REF_ID_LOC) | EVIL_FLAG);
            if CLASS != 0: 
                if NAME_IMPLIED:
                    g.ATTRIBUTES = ATTRIBUTES | DEFINED_LABEL;
                    if TYPE == PROC_LABEL: 
                        ERROR(d.CLASS_DA, 14, SYT_NAME(ID_LOC));
                    elif CLASS == 2: 
                        ERROR(d.CLASS_DA, 13, SYT_NAME(ID_LOC));
                else:
                    ERROR(d.CLASS_DT, 7, SYT_NAME(ID_LOC));
                    g.CLASS = 0;
                    if TYPE > ANY_TYPE: 
                        g.TYPE = DEFAULT_TYPE;
            CHECK_CONSISTENCY();
            if (ATTRIBUTES & ILL_TERM_ATTR(NAME_IMPLIED)) != 0 or \
                    (ATTRIBUTES2 & NONHAL_FLAG) != 0:
                ERROR(d.CLASS_DA, 23, SYT_NAME(ID_LOC));
                #  ILL_NAME_ATTR MUST BE SUBSET OF ILL_TERM_ATTR
                g.ATTRIBUTES = (~ILL_TERM_ATTR(NAME_IMPLIED)) & ATTRIBUTES;
                g.ATTRIBUTES2 = (~NONHAL_FLAG) & ATTRIBUTES2;
                g.DO_INIT = g.FALSE;
            g.SYT_CLASS(ID_LOC, TEMPLATE_CLASS + CLASS);
            if TYPE == MAJ_STRUC: 
                CHECK_STRUC_CONFLICTS();
            elif TYPE == EVENT_TYPE: 
                CHECK_EVENT_CONFLICTS();
            if (ATTRIBUTES & SD_FLAGS) == 0:
                if (TYPE >= g.MAT_TYPE) & (TYPE <= INT_TYPE):
                    g.ATTRIBUTES = ATTRIBUTES | (DEFAULT_ATTR & SD_FLAGS);
            if (ATTRIBUTES & ALDENSE_FLAGS) == 0:
                if (not NAME_IMPLIED) and ((ATTRIBUTES & ARRAY_FLAG) == 0) and \
                        (TYPE == BIT_TYPE):
                    g.ATTRIBUTES = ATTRIBUTES | (g.SYT_FLAGS(g.FIXL[g.SP]) & ALDENSE_FLAGS);
                else:
                    g.ATTRIBUTES = ATTRIBUTES | ALIGNED_FLAG;
            if (ATTRIBUTES & RIGID_FLAG) == 0:
                g.ATTRIBUTES = ATTRIBUTES | (g.SYT_FLAGS(g.FIXL[g.SP]) & RIGID_FLAG);
            if NAME_IMPLIED: 
                g.SYT_FLAGS(REF_ID_LOC, g.SYT_FLAGS(REF_ID_LOC) | MISC_NAME_FLAG);
            SET_SYT_ENTRIES();
            g.STRUC_SIZE = ICQ_TERMp(ID_LOC) * ICQ_ARRAYp(ID_LOC) + STRUC_SIZE;
            g.NAME_IMPLIED = g.FALSE;
            if g.FIXV[g.SP] > 0: 
                g.SYT_LINK2(g.FIXL[g.MPP1], TEMP_SYN + 1);
                if g.STACK_PTR[g.SP] > 0:
                    OUTPUT_WRITER(g.LAST_WRITE, g.STACK_PTR[g.SP] - 1);
                g.LAST_WRITE = g.STACK_PTR[g.SP];
                g.INDENT_LEVEL = SAVE_INDENT_LEVEL + (g.FIXV[g.MP] * g.INDENT_INCR);
            else:
                g.BUILDING_TEMPLATE = g.FALSE;
                OUTPUT_WRITER(g.LAST_WRITE, g.STMT_PTR);
                g.INDENT_LEVEL = SAVE_INDENT_LEVEL;
                g.LAST_WRITE, SAVE_INDENT_LEVEL = 0;
    elif goto_SPEC_VAR or PRODUCTION_NUMBER == 361:  # reference 3610
        #  <DECLARATION>  ::=  <NAME ID>  <ATTRIBUTES>
        if not goto_SPEC_VAR:
            if not BUILDING_TEMPLATE:
                if (g.TOKEN_FLAGS[0] & 7) == 7: 
                    g.ATTR_LOC = 0;
                elif (g.TOKEN_FLAGS[1] & 7) == 7: 
                    g.ATTR_LOC = 1;
                else:
                    g.ATTR_LOC = MAX(0, g.STACK_PTR[g.MP]);
        goto_SPEC_VAR = False
        g.DO_INIT = g.TRUE;
        CHECK_CONFLICTS();
        g.I = g.SYT_FLAGS(ID_LOC);
        if (I & PARM_FLAGS) != 0:
            g.PARMS_PRESENT = PARMS_PRESENT - 1;
            if PARMS_PRESENT == 0 and PARMS_WATCH: 
                g.COMSUB_END(g.NDECSY());
            if (ATTRIBUTES & ILL_INIT_ATTR) != 0: 
                ERROR(d.CLASS_DI, 12, g.VAR[g.MP]);
                g.DO_INIT = g.FALSE;
                g.ATTRIBUTES = ATTRIBUTES & (not ILL_INIT_ATTR);
            if CLASS > 0 & (not NAME_IMPLIED): 
                ERROR(d.CLASS_D, 1, g.VAR[g.MP]);
                NONHAL, CLASS = 0;
                if TYPE > ANY_TYPE: 
                    g.TYPE = DEFAULT_TYPE;
            #  REMOTE NOW OK FOR ASSIGN PARMS & IGNORED FOR INPUT PARMS
            #  SO REMOVE D14 ERROR MESSAGE.
        elif PARMS_WATCH: 
            ERROR(d.CLASS_D, 15);
        if TYPE == EVENT_TYPE: 
            CHECK_EVENT_CONFLICTS();
        goto_MODE_CHECK = False  # Internal to this case only
        goto_FIX_AUTSTAT = False  # Internal to this case only
        nonHAL = False
        firstTry = True
        while firstTry or goto_FIX_AUTSTAT:
            firstTry = False
            if not NAME_IMPLIED:
                if not goto_FIX_AUTSTAT:
                    if NONHAL > 0:
                        if TYPE == PROC_LABEL or CLASS == 2:
                            g.ATTRIBUTES = ATTRIBUTES | EXTERNAL_FLAG | DEFINED_LABEL;
                            g.SYT_ARRAY(ID_LOC, NONHAL | 0xFF00);
                            goto_MODE_CHECK = True
                        else:
                            ERROR(d.CLASS_D, 11, g.VAR[g.MP]);
                            #   DISCONNECT SYT_FLAGS WITH NONHAL
                            #   THIS ALSO DISCONNECTS ATTRIBUTES WITH NONHAL
                            g.SYT_FLAGS2(ID_LOC, g.SYT_FLAGS2(ID_LOC) & (~NONHAL_FLAG));
                            nonHAL = True
                    if nonHAL:
                        pass
                    elif goto_MODE_CHECK or CLASS == 2:
                        goto_MODE_CHECK = False
                        if g.BLOCK_MODE[g.NEST] == CMPL_MODE: 
                            ERROR(d.CLASS_D, 2, g.VAR[g.MP]);
                    elif CLASS == 1:
                        if TYPE == TASK_LABEL:
                            if g.NEST > 1 | g.BLOCK_MODE[1] != PROG_MODE:
                                ERROR(d.CLASS_PT, 1);
                        else:
                            ERROR(d.CLASS_DN, 1, g.VAR[g.MP]);
                            g.CLASS = 0;
                            g.TYPE = DEFAULT_TYPE;
                if not goto_FIX_AUTSTAT and CLASS != 0:
                    if (ATTRIBUTES & ILL_INIT_ATTR) != 0:
                        ERROR(d.CLASS_DI, 13, g.VAR[g.MP]);
                        g.ATTRIBUTES = ATTRIBUTES & (~ILL_INIT_ATTR);
                        g.DO_INIT = g.FALSE;
                    if TEMPORARY_IMPLIED: 
                        ERROR(d.CLASS_D, 8, g.VAR[g.MP]);
                        g.CLASS = 0;
                        if TYPE > ANY_TYPE: 
                            g.TYPE = DEFAULT_TYPE;
                elif not goto_FIX_AUTSTAT and TEMPORARY_IMPLIED: 
                    if (ATTRIBUTES & ILL_TEMPORARY_ATTR) != 0 or \
                            (ATTRIBUTES2 & NONHAL_FLAG) != 0:
                        ERROR(d.CLASS_D, 8, g.VAR[g.MP]);
                        g.ATTRIBUTES = ATTRIBUTES & (not ILL_TEMPORARY_ATTR);
                        g.ATTRIBUTES2 = ATTRIBUTES2 & (not NONHAL_FLAG);
                        g.DO_INIT = g.FALSE;
                else:
                    goto_FIX_AUTSTAT = False
                    if (ATTRIBUTES & ALDENSE_FLAGS) == 0:
                        g.ATTRIBUTES = ATTRIBUTES | (DEFAULT_ATTR & ALDENSE_FLAGS);
                    if g.BLOCK_MODE[g.NEST] != CMPL_MODE:
                        if (I & PARM_FLAGS) == 0:
                            if (ATTRIBUTES & AUTSTAT_FLAGS) == 0:
                                    g.ATTRIBUTES = ATTRIBUTES | (DEFAULT_ATTR & AUTSTAT_FLAGS);
            else: 
                # ADD ILLEGAL TEMP ATTRIBUTE CHECKING FROM ABOVE FOR NAME TEMPS TOO
                if TEMPORARY_IMPLIED: 
                    if CLASS != 0:
                        ERROR(d.CLASS_D, 8, g.VAR[g.MP]);
                        g.CLASS = 0;
                        if TYPE > ANY_TYPE: 
                            g.TYPE = DEFAULT_TYPE;
                    # ONLY DIFFERENCE FOR NAME TEMPS IS THAT REMOTE IS LEGAL
                    elif (((ATTRIBUTES & ILL_TEMPORARY_ATTR) != 0) and \
                            ((ATTRIBUTES & ILL_TEMPORARY_ATTR) != REMOTE_FLAG)) or \
                            (ATTRIBUTES2 & NONHAL_FLAG) != 0:
                        ERROR(d.CLASS_D, 8, g.VAR[g.MP]);
                        g.ATTRIBUTES = ATTRIBUTES & (not ILL_TEMPORARY_ATTR);
                        g.ATTRIBUTES2 = ATTRIBUTES2 & (not NONHAL_FLAG);
                        g.DO_INIT = g.FALSE;
                if (ATTRIBUTES & ILL_NAME_ATTR) != 0 or \
                        (ATTRIBUTES2 & NONHAL_FLAG) != 0:
                    ERROR(d.CLASS_D, 12, g.VAR[g.MP]);
                    g.ATTRIBUTES = ATTRIBUTES & (not ILL_NAME_ATTR);
                    g.ATTRIBUTES2 = ATTRIBUTES2 & (not NONHAL_FLAG);
                if TYPE == PROC_LABEL: 
                    ERROR(d.CLASS_DA, 14, g.VAR[g.MP]);
                elif CLASS == 2: 
                    ERROR(d.CLASS_DA, 13, g.VAR[g.MP]);
                if CLASS > 0: 
                    g.ATTRIBUTES = ATTRIBUTES | DEFINED_LABEL;
                goto_FIX_AUTSTAT = True
                continue
        g.SYT_CLASS(ID_LOC, VAR_CLASS(CLASS));
        if TYPE == MAJ_STRUC: 
            CHECK_STRUC_CONFLICTS();
        if (ATTRIBUTES & SD_FLAGS) == 0: 
            if TYPE >= g.MAT_TYPE & TYPE <= INT_TYPE:
                g.ATTRIBUTES = ATTRIBUTES | (DEFAULT_ATTR & SD_FLAGS);
        SET_SYT_ENTRIES();
        g.NAME_IMPLIED = g.FALSE;
        if TEMPORARY_IMPLIED:
            g.ATTR_INDENT = 10;
            if g.DO_CHAIN[g.DO_LEVEL] == 0:
                g.DO_CHAIN[g.DO_LEVEL] = ID_LOC;
                HALMAT_POP(XTDCL, 1, 0, 0);
                HALMAT_PIP(ID_LOC, XSYT, 0, 0);
            else: 
                g.SYT_LINK1(g.DO_CHAIN[0], ID_LOC);
            g.DO_CHAIN[0] = ID_LOC;
        else:
            g.ATTR_INDENT = 8;
        # SET REMOTE ATTRIBUTE FOR ALL NON-NAME #D DATA WHEN THE
        # DATA_REMOTE DIRECTIVE IS IN EFFECT
        # (MUST NOT BE AUTOMATIC OR A PARAMETER TO BE #D DATA.)
        if DATA_REMOTE: 
            if ((g.SYT_FLAGS(ID_LOC) & NAME_FLAG) == 0) and \
                    ((g.SYT_FLAGS(ID_LOC) & TEMPORARY_FLAG) == 0) and \
                    (g.SYT_TYPE(ID_LOC) != TASK_LABEL) and \
                    (g.SYT_TYPE(ID_LOC) != PROC_LABEL) and \
                    (SYT_CLASS(ID_LOC) != FUNC_CLASS) and \
                    ((g.SYT_FLAGS(g.BLOCK_SYTREF[g.NEST]) & EXTERNAL_FLAG) == 0) and \
                    not (((g.SYT_FLAGS(ID_LOC) & AUTO_FLAG) != 0) and \
                    ((g.SYT_FLAGS(g.BLOCK_SYTREF[g.NEST]) & REENTRANT_FLAG) != 0)) and \
                    ((g.SYT_FLAGS(ID_LOC) & PARM_FLAGS) == 0):
                if (g.SYT_FLAGS(ID_LOC) & REMOTE_FLAG) != 0:
                    ERROR(d.CLASS_XR, 3);
                if g.SYT_TYPE(ID_LOC) == EVENT_TYPE:
                    ERROR(d.CLASS_DA, 9);
                g.SYT_FLAGS(ID_LOC, g.SYT_FLAGS(ID_LOC) | REMOTE_FLAG);
            elif SDL_OPTION and \
                    ((g.SYT_FLAGS(ID_LOC) & NAME_FLAG) == 0) and \
                    ((g.SYT_FLAGS(ID_LOC) & PARM_FLAGS) == 0) and \
                    ((g.SYT_FLAGS(ID_LOC) & REMOTE_FLAG) != 0):
                ERROR(d.CLASS_XR, 5);
        if ((g.SYT_FLAGS(ID_LOC) & NAME_FLAG) == 0) and \
                ((g.SYT_FLAGS(ID_LOC) & INPUT_PARM) != 0) and \
                ((g.SYT_FLAGS(ID_LOC) & REMOTE_FLAG) != 0):
            g.SYT_FLAGS(ID_LOC, g.SYT_FLAGS(ID_LOC) & ~REMOTE_FLAG);
            ERROR(d.CLASS_YD, 100);
    elif goto_CHECK_ARRAY_SPEC or PRODUCTION_NUMBER == 365:  # reference 3650
        #  <ATTRIBUTES> ::= <ARRAY SPEC>
        goto_CHECK_ARRAY_SPEC = False
        if N_DIM > 1:
            if STARRED_DIMS > 0:
                ERROR(d.CLASS_DD, 6);
                for I in range(0, 1 + N_DIM - 1):
                    if g.S_ARRAY[I] == -1:
                        g.S_ARRAY[I] = 2;  # DEFAULT
        goto_MAKE_ATTRIBUTES = True
    if goto_MAKE_ATTRIBUTES or PRODUCTION_NUMBER == 366:  # reference 3660
        #  <ATTRIBUTES> ::= <TYPE & MINOR ATTR>
        goto_MAKE_ATTRIBUTES = False
        g.GRAMMAR_FLAGS[g.STACK_PTR[g.MP]] = \
                        g.GRAMMAR_FLAGS[g.STACK_PTR[g.MP]] | ATTR_BEGIN_FLAG;
        CHECK_CONSISTENCY();
        if FACTORING:
            # See the comments in g.py for TYPE to understand the next few lines
            g.FACTORED_TYPE = g.TYPE
            g.FACTORED_BIT_LENGTH = g.BIT_LENGTH
            g.FACTORED_CHAR_LENGTH = g.CHAR_LENGTH
            g.FACTORED_MAT_LENGTH = g.MAT_LENGTH
            g.FACTORED_VEC_LENGTH = g.VEC_LENGTH
            g.FACTORED_ATTRIBUTES = g.ATTRIBUTES
            g.FACTORED_ATTRIBUTES2 = g.ATTRIBUTES2
            g.FACTORED_ATTR_MASK = g.ATTR_MASK
            g.FACTORED_STRUC_PTR = g.STRUC_PTR
            g.FACTORED_STRUC_DIM = g.STRUC_DIM
            g.FACTORED_CLASS = g.CLASS
            g.FACTORED_NONHAL = g.NONHAL
            g.FACTORED_LOCKp = g.LOCKp
            g.FACTORED_IC_PTR = g.IC_PTR
            g.FACTORED_IC_FND = g.IC_FND
            g.FACTORED_N_DIM = g.N_DIM
            g.FACTORED_S_ARRAY = g.S_ARRAY
            g.TYPE = 0
            g.BIT_LENGTH = 0
            g.CHAR_LENGTH = 0
            g.MAT_LENGTH = 0
            g.VEC_LENGTH = 0
            g.ATTRIBUTES = 0
            g.ATTRIBUTES2 = 0
            g.ATTR_MASK = 0
            g.STRUC_PTR = 0
            g.STRUC_DIM = 0
            g.CLASS = 0
            g.NONHAL = 0
            g.LOCKp = 0
            g.IC_PTR = 0
            g.IC_FND = 0
            g.N_DIM = 0
            g.S_ARRAY = [0] * (g.N_DIM_LIM + 1)
            # (End of TYPE/FACTORED_TYPE loop)----------------------------------
            g.FACTOR_FOUND = g.TRUE;
            if FACTORED_IC_FND:
                g.IC_FOUND = 1;  # FOR HALMAT_INIT_CONST
                g.IC_PTR1 = FACTORED_IC_PTR;
    elif goto_ARRAY_SPEC or PRODUCTION_NUMBER == 373:  # reference 3730
        #  <ARRAY HEAD> ::= <ARRAY HEAD> <LITERAL_EXP OR *> ,
        goto_ARRAY_SPEC = False
        if N_DIM >= N_DIM_LIM:
            ERROR(d.CLASS_DD, 3);
        else:
            g.K = 2;  # A DEFAULT
            g.I = g.FIXV[g.MPP1];
            if not (I > 1 and I <= ARRAY_DIM_LIM and I == -1):
                ERROR(d.CLASS_DD, 1);
            else:
                g.K = I;
            if K == -1: 
                g.STARRED_DIMS = STARRED_DIMS + 1;
            g.S_ARRAY[N_DIM] = K;
            g.N_DIM = N_DIM + 1;
    elif goto_SPEC_TYPE or PRODUCTION_NUMBER == 375:  # reference 3750
        #  <TYPE & MINOR ATTR> ::= <TYPE SPEC> <MINOR ATTR LIST>
        goto_SPEC_TYPE = False
        if CLASS:
            ERROR(d.CLASS_DC, 1);
            g.CLASS = 0;
    elif goto_INCORPORATE_ATTR or PRODUCTION_NUMBER == 400:  # reference 4000
        #  <MINOR ATTR LIST> ::= <MINOR ATTR LIST> <MINOR ATTRIBUTE>
        goto_INCORPORATE_ATTR = False
        if (ATTR_MASK & g.FIXL[g.SP]) != 0:
            ERROR(d.CLASS_DA, 25);
        else:
            g.ATTR_MASK = ATTR_MASK | g.FIXL[g.SP];
            g.ATTRIBUTES = ATTRIBUTES | g.FIXV[g.SP];
    elif goto_SET_AUTSTAT or PRODUCTION_NUMBER == 401:  # reference 4010
        #  <MINOR ATTRIBUTE> ::= STATIC
        if not goto_SET_AUTSTAT:
            g.I = STATIC_FLAG;
        goto_SET_AUTSTAT = False
        if g.BLOCK_MODE[g.NEST] == CMPL_MODE:
            ERROR(d.CLASS_DC, 2);
        else:
            g.FIXL[g.MP] = AUTSTAT_FLAGS;
            g.FIXV[g.MP] = I;
    elif goto_DO_QUALIFIED_ATTRIBUTE or PRODUCTION_NUMBER == 409:  # reference 4090
        #  <MINOR ATTRIBUTE> ::= <INIT/CONST HEAD> <REPEATED CONSTANT> )
        if not goto_DO_QUALIFIED_ATTRIBUTE:
            g.PSEUDO_TYPE_P[g.PTR[g.MP]] = 0;  # NO "*"
        goto_DO_QUALIFIED_ATTRIBUTE = False
        g.BI_FUNC_FLAG = g.FALSE;
        CHECK_IMPLICIT_T();
        g.CONTEXT = DECLARE_CONTEXT;
        if (NUM_ELEMENTS >= g.NUM_EL_MAX) or (NUM_ELEMENTS < 1):
            ERROR(d.CLASS_DI, 2);
        g.LOC_P[g.PTR[g.MP]] = NUM_ELEMENTS;  # SAVE NUMBER OF ELEMENTS TO SET
        g.VAL_P[g.PTR[g.MP]] = NUM_FL_NO;  # SAVE NUMBER OF GVR'S USED
        g.PSEUDO_LENGTH[g.PTR[g.MP]] = NUM_STACKS;  # INDICATE LENGTH OF LIST
        g.IC_PTR = g.PTR[g.MP];  # SAVE PTR TO THIS I/C LIST
        g.IC_FND = g.TRUE;
        if BUILDING_TEMPLATE: 
            g.PTR_TOP = g.PTR[g.MP] - 1;
        # KILL STACKS IF STRUCTURE TEMPLATE
    elif goto_DO_INIT_CONST_HEAD or PRODUCTION_NUMBER == 413:  # reference 4130
        #  <INIT/CONST HEAD> ::= INITIAL (
        if not goto_DO_INIT_CONST_HEAD:
            g.FIXL[g.MP] = INIT_CONST;
            g.FIXV[g.MP] = INIT_FLAG;
        goto_DO_INIT_CONST_HEAD = False
        g.BI_FUNC_FLAG = g.TRUE;
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        NUM_ELEMENTS, NUM_FL_NO = 0;
        g.NUM_STACKS = 1;  #  THIS IS FIRST INDIRECT LOC NEEDED
        g.PSEUDO_FORM[g.PTR[g.MP]] = 0;  #  INDICATE I/C LIST TOP, IE., STRI
        g.INX[g.PTR[g.MP]] = g.IC_LINE;
    elif goto_INIT_ELEMENT or goto_END_REPEAT_INIT or \
            PRODUCTION_NUMBER == 418:  # reference 4180
        #  <REPEATED CONSTANT>  ::=  <REPEAT HEAD>  <CONSTANT>
        if not (goto_INIT_ELEMENT or goto_END_REPEAT_INIT):
            g.TEMP_SYN = 1;
        if not goto_END_REPEAT_INIT:
            goto_INIT_ELEMENT = False
            g.TEMP = g.PTR[g.SP];
            if NAME_PSEUDOS:
                g.NAME_PSEUDOS = g.FALSE;
                g.PSEUDO_TYPE_P[g.TEMP] = g.PSEUDO_TYPE_P[g.TEMP] | 0x80;
                if (g.VAL_P[g.TEMP] & 0x40) != 0: 
                    ERROR(d.CLASS_DI, 14);
                if (g.VAL_P[g.TEMP] & 0x200) != 0: 
                    ERROR(d.CLASS_DI, 16);
                # LOOK FOR THE 0x4000 VAL_P BIT AND EMIT DI16 ERROR.
                # THE VAL_P 0x4000 BIT INDICATES THE PRESENCE OF A
                # NAME VARIABLE SOMEWHERE INSIDE THE STRUCTURE REFER-
                # ENCE LIST. THE PRESENCE OF A NAME VARIABLE INSIDE
                # A NAME() INITIALIZATION IS A DI16 ERROR CONDITION.
                if (g.VAL_P[g.TEMP] & 0x4000) != 0:
                    ERROR(d.CLASS_DI, 16);
                if g.EXT_P[g.TEMP] != 0: 
                    ERROR(d.CLASS_DI, 15);
                if (g.VAL_P[g.TEMP] & 0x400) == 0: 
                    RESET_ARRAYNESS();
                if SYT_CLASS(g.FIXL[g.MP]) == TEMPLATE_CLASS:
                    if (((g.SYT_FLAGS(g.FIXV[g.MP]) & ASSIGN_PARM) > 0) or \
                            (((g.SYT_FLAGS(g.FIXV[g.MP]) & AUTO_FLAG) != 0) and \
                             ((g.SYT_FLAGS(g.BLOCK_SYTREF[g.NEST]) and \
                               REENTRANT_FLAG) != 0))):
                        ERROR(d.CLASS_DI, 3);
                elif (((g.SYT_FLAGS(g.FIXL[g.MP]) & ASSIGN_PARM) > 0) or \
                        (((g.SYT_FLAGS(g.FIXL[g.MP]) & AUTO_FLAG) != 0) and \
                         ((g.SYT_FLAGS(g.BLOCK_SYTREF[g.NEST]) and \
                           REENTRANT_FLAG) != 0))):
                    ERROR(d.CLASS_DI, 3);
            elif g.PSEUDO_FORM[g.TEMP] != XLIT: 
                ERROR(d.CLASS_DI, 3);
            CHECK_ARRAYNESS();
            SET_INIT(g.LOC_P[g.TEMP], 2, g.PSEUDO_FORM[g.TEMP], g.PSEUDO_TYPE_P[g.TEMP], NUM_ELEMENTS);
            g.NUM_ELEMENTS = NUM_ELEMENTS + 1;
            g.NUM_STACKS = NUM_STACKS + 1;
        if TEMP_SYN or goto_END_REPEAT_INIT:
            goto_END_REPEAT_INIT = False
            SET_INIT(0, 3, 0, 0, NUM_FL_NO);
            g.NUM_FL_NO = NUM_FL_NO - 1;
            g.NUM_STACKS = NUM_STACKS + 1;
            g.TEMP_SYN = NUM_ELEMENTS - g.FIXV[g.MP];
            g.IC_LEN[GET_ICQ(g.FIXL[g.MP])] = TEMP_SYN;
            g.NUM_ELEMENTS = g.INX[g.PTR[g.MP]] * TEMP_SYN + g.FIXV[g.MP];
        g.PTR_TOP = g.PTR[g.MP] - 1;
    elif goto_DO_CONSTANT or PRODUCTION_NUMBER == 424:  # reference 4240
        #  <CONSTANT>  ::=  <NUMBER>
        if not goto_DO_CONSTANT:
            g.TEMP_SYN = INT_TYPE;
        goto_DO_CONSTANT = False
        g.PTR[g.MP] = PUSH_INDIRECT(1);
        g.PSEUDO_TYPE_P[g.PTR[g.MP]] = TEMP_SYN;
        g.PSEUDO_FORM[g.PTR[g.MP]] = XLIT;
        g.LOC_P[g.PTR[g.MP]] = g.FIXL[g.MP];
    elif goto_CLOSE_IT or PRODUCTION_NUMBER == 430:  # reference 4300
        #  <CLOSING> ::= CLOSE
        if not goto_CLOSE_IT:
            g.VAR[g.MP] = '';
        goto_CLOSE_IT = False
        g.INDENT_LEVEL = g.INDENT_LEVEL - g.INDENT_INCR;
        g.XSET(0x6);
    elif goto_TERM_LIST or PRODUCTION_NUMBER == 436:  # reference 4360
        #  <TERMINATE LIST>  ::=  <TERMINATE LIST>  ,  <LABEL VAR>
        if not goto_TERM_LIST:
            g.EXT_P[g.PTR[g.MP]] = g.EXT_P[g.PTR[g.MP]] + 1;
        goto_TERM_LIST = False
        SET_XREF_RORS(g.SP, g.FIXV[g.MP - 1]);
        PROCESS_CHECK(g.SP);
    elif goto_SCHEDULE_AT or PRODUCTION_NUMBER == 439:  # reference 4390
        # <SCHEDULE HEAD>::= <SCHEDULE HEAD> AT <ARITH EXP>
        if not goto_SCHEDULE_AT:
            g.TEMP = 0x1;
            if UNARRAYED_SCALAR(g.SP): 
                ERROR(d.CLASS_RT, 1, 'AT');
        goto_SCHEDULE_AT = False
        if g.INX[REFER_LOC] == 0: 
            g.INX[REFER_LOC] = g.TEMP;
        else:
            ERROR(d.CLASS_RT, 5);
            g.PTR_TOP = g.PTR_TOP - 1;
    elif goto_SCHED_PRIO or PRODUCTION_NUMBER == 442:  # reference 4420
        # <SCHEDULE PHRASE>::=<SCHEDULE HEAD>
        goto_SCHED_PRIO = False
        ERROR(d.CLASS_RT, 4, 'SCHEDULE');
    elif goto_SCHEDULE_EVERY or PRODUCTION_NUMBER == 448:  # reference 4480
        #  <TIMING>  ::=  <REPEAT> EVERY <ARITH EXP>
        if not goto_SCHEDULE_EVERY:
            g.TEMP = 0x20;
        goto_SCHEDULE_EVERY = False
        if UNARRAYED_SCALAR(g.SP): 
            ERROR(d.CLASS_RT, 1, 'EVERY/AFTER');
        g.INX[REFER_LOC] = g.INX[REFER_LOC] | g.TEMP;
    
    # references 3110 and 3210 have GOTO's to each other, so we enclose them
    # together in a mini-loop to let them reach each other easily.
    while goto_OUTERMOST_BLOCK or goto_DUPLICATE_BLOCK or \
               goto_PROC_FUNC_HEAD or goto_NEW_SCOPE or goto_INLINE_ENTRY or \
               PRODUCTION_NUMBER == 311 or PRODUCTION_NUMBER == 321:
        if goto_OUTERMOST_BLOCK or goto_DUPLICATE_BLOCK or \
                PRODUCTION_NUMBER == 311:  # reference 3110
            #  <BLOCK STMT HEAD>  ::=  <LABEL EXTERNAL>  PROGRAM
            PRODUCTION_NUMBER = -1
            if not (goto_OUTERMOST_BLOCK or goto_DUPLICATE_BLOCK):
                g.TEMP = XMDEF;
                g.PARMS_PRESENT = 0;
                g.TEMP2 = PROG_MODE;
                SET_LABEL_TYPE(g.FIXL[g.MP], PROG_LABEL);
                g.SYT_FLAGS(g.FIXL[g.MP], g.SYT_FLAGS(g.FIXL[g.MP]) | LATCHED_FLAG);
                if EXTERNAL_MODE > 0:
                    if g.NEST == 0: 
                        g.EXTERNAL_MODE = TEMP2;
                    goto_NEW_SCOPE = True
                    continue
            goto_OUTERMOST_BLOCK = False
            if g.NEST > 0 and not goto_DUPLICATE_BLOCK: 
                ERROR(d.CLASS_PP, 1, g.VAR[g.MPP1]);
            else:
                goto_DUPLICATE_BLOCK = False
                if g.BLOCK_MODE[0] == 0: 
                    g.MAIN_SCOPE = g.MAX_SCOPEp() + 1;  # WHAT SYT_SCOPE WILL BECOME
                    g.FIRST_STMT(g.STMT_NUM());
                    g.BLOCK_MODE[0] = TEMP2;
                    if g.BLOCK_MODE[0] < TASK_MODE: 
                        if TPL_FLAG < 3: 
                            g.EXTERNALIZE = 3;
                    MONITOR(17, DESCORE(g.VAR[g.MP]));
                    EMIT_EXTERNAL();
                else:
                    ERROR(d.CLASS_PP, 2);
            goto_NEW_SCOPE = True
            continue
        if goto_PROC_FUNC_HEAD or goto_NEW_SCOPE or goto_INLINE_ENTRY or \
                PRODUCTION_NUMBER == 321:  # reference 3210
            #  <PROCEDURE NAME>  ::=  <LABEL EXTERNAL>  PROCEDURE
            PRODUCTION_NUMBER = -1
            if not (goto_PROC_FUNC_HEAD or goto_NEW_SCOPE or goto_INLINE_ENTRY):
                g.TEMP2 = PROC_MODE;
                g.TEMP = XPDEF;
                SET_LABEL_TYPE(g.FIXL[g.MP], PROC_LABEL);
            if not (goto_NEW_SCOPE or goto_INLINE_ENTRY):
                goto_PROC_FUNC_HEAD = False
                g.PARMS_PRESENT = 0;
                if INLINE_LEVEL > 0: 
                    ERROR(d.CLASS_PP, 9);
                if EXTERNAL_MODE > 0: 
                    if g.NEST == 0: EXTERNAL_MODE = TEMP2;
                elif g.NEST == 0:
                    g.PARMS_WATCH = g.TRUE;
                    goto_DUPLICATE_BLOCK = True
                    continue
            if not goto_INLINE_ENTRY:
                #  ALL BLOCKS AND TEMPLATES COME HERE
                goto_NEW_SCOPE = False
                SET_BLOCK_SRN(g.FIXL[g.MP]);
                if not PAGE_THROWN:
                    if (g.SYT_FLAGS(g.FIXL[g.MP]) & EXTERNAL_FLAG) == 0:
                        g.LINE_MAX = 0;
                if TEMP2 != UPDATE_MODE:
                    HALMAT_BACKUP(LAST_POPp);
                if not HALMAT_CRAP: 
                    g.HALMAT_OK = EXTERNAL_MODE = 0;
                HALMAT_POP(g.TEMP, 1, 0, 0);
                HALMAT_PIP(g.FIXL[g.MP], XSYT, 0, 0);
            goto_INLINE_ENTRY = False
            g.XSET(0x16);
            g.NEST = g.NEST + 1;
            g.DO_INX[g.DO_LEVEL] = g.DO_INX[g.DO_LEVEL] | 0x80;
            g.BLOCK_MODE[g.NEST] = TEMP2;
            g.BLOCK_SYTREF[g.NEST] = g.FIXL[g.MP];
            SYT_ARRAY(g.BLOCK_SYTREF[g.NEST], -ON_ERROR_PTR);
            if g.NEST > MAXNEST:
                g.MAXNEST = g.NEST;
                if g.NEST >= NEST_LIM:
                    ERROR(d.CLASS_BN, 1);
            g.SCOPEp_STACK[g.NEST] = g.SCOPEp;
            g.SCOPEp = g.MAX_SCOPEp() + 1;
            g.MAX_SCOPEp(g.SCOPEp)
            if (g.SYT_FLAGS(g.FIXL[g.MP]) & EXTERNAL_FLAG) != 0: 
                NEXT_ELEMENT(CSECT_LENGTHS);
                g.CSECT_LENGTHS[g.SCOPEp].PRIMARY = 0x7FFF;  # SET LENGTH TO MAX
                g.CSECT_LENGTHS[g.SCOPEp].REMOTE = 0x7FFF;  # TO TURN OFF PHASE2
                # %COPY CHECKING
            SYT_SCOPE(g.FIXL[g.MP], g.SCOPEp);  # UPDATE BLOCK NAME TO SAME SCOPE
            # AS CONTENTS
            g.PROCMARK_STACK[g.NEST] = PROCMARK;
            g.PROCMARK = g.NDECSY() + 1;
            g.REGULAR_PROCMARK = PROCMARK
            g.SYT_PTR(g.FIXL[g.MP], PROCMARK);
            if g.BLOCK_MODE[g.NEST] == CMPL_MODE:
                g.PROCMARK = 1;  # ALL COMPOOLS IN SAME SCOPE
            g.S = g.CURRENT_SCOPE[:];
            g.CURRENT_SCOPE = g.VAR[g.MP];
            g.SAVE_SCOPE = g.CURRENT_SCOPE[:]
            g.VAR[g.MP] = S;
            g.NEST = g.NEST - 1;
            COMPRESS_OUTER_REF();
            g.NEST = g.NEST + 1;
            g.OUTER_REF_PTR_P[g.NEST] = OUTER_REF_INDEX + 1;
            ENTER_LAYOUT(g.FIXL[g.MP]);
            if g.BLOCK_MODE[g.NEST] == INLINE_MODE: 
                if g.STACK_PTR[g.MP] > 0: 
                    OUTPUT_WRITER(0, g.STACK_PTR[g.MP] - 1);
                g.EXT_P[g.PTR[g.MP]] = g.INDENT_LEVEL;
                g.INX[g.PTR[g.MP]] = g.STMT_NUM();
                EMIT_SMRK(5);
                g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
                OUTPUT_WRITER(g.STACK_PTR[g.MP], g.STACK_PTR[g.SP]);
                g.INDENT_LEVEL = g.INDENT_LEVEL + g.INDENT_INCR;
                g.NEST_LEVEL = NEST_LEVEL + 1;
                EMIT_SMRK();
            else:
                g.INDENT_STACK[g.NEST] = g.INDENT_LEVEL;
                g.NEST_STACK[g.NEST] = NEST_LEVEL;
                g.INDENT_LEVEL, NEST_LEVEL = 0;
    
    # END OF PART_2
    if (g.PREV_STMT_NUM != g.STMT_NUM()):
        g.INCREMENT_DOWN_STMT = g.FALSE;
    g.PREV_STMT_NUM = g.STMT_NUM();

