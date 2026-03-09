      ************************************************************************
      *  GSF001AX                     *
      *                    GAS MASTER INPUT                                  *
      *                   EXPANDED RRC IDENT
      *
      * LRECL = 2120
      * BLKSIZE: DISK = 23320
      *          TAPE = 31800
      *
      ******************************************************************
      * Y2K CONVERSION - REFORMAT DATE FIELDS                   RWS
      * UNUSED DATA ELEMENTS GD-LEASE-FUEL, GD-TRANS-LINE,
      * GD-PROC-PLANT AND GD-FLARED WERE DELETED TO MAKE SPACE
      * FOR EXPANDED DATES.
      *********************************************************
       FD  GAS-MAST-IN-1
           BLOCK CONTAINS 0 RECORDS
           LABEL RECORDS ARE STANDARD
           RECORD CONTAINS 2120
           RECORDING MODE IS F.
       01  FLD-REC.
           03  REC-CODE                        PIC 9.
           03  FLD-CODE.
               05  DIST.
                   07  DIST-NO                 PIC 99.
                   07  DIST-SFX                PIC X.
               05  PERM-FLD-ID                 PIC 9(8).
               05  FLD-ID  REDEFINES PERM-FLD-ID.
                   07  FLD-NAM                 PIC 9(5).
                   07  FLD-RES                 PIC 999.
           03  NEXT-FLD    REDEFINES FLD-CODE  PIC X(11).
           03  FILLER                          PIC X(19).
           03  FLD-NAME                        PIC X(32).
           03  COUNTY                          PIC 9(18).
           03  COUNTIES REDEFINES COUNTY OCCURS 6 TIMES
                                               PIC 999.
           03  DISC-DATE                       PIC 9(8).
           03  D-DATE  REDEFINES DISC-DATE.
               05  DISC-DATE-CCYY              PIC 9(4).
               05  DISC-DATE-CCYY-REDF REDEFINES DISC-DATE-CCYY.
                   07  CENT                    PIC 99.
                   07  YEAR                    PIC 99.
               05  MONTH                       PIC 99.
               05  DA                          PIC 99.
           03  TYPE-F                          PIC X.
           03  CLASS                           PIC X.
           03  ALLO-CD                         PIC X.
           03  SPOCE                           PIC 9(8).
           03  SPACING REDEFINES SPOCE.
               05  LINE-SP                     PIC 9(4).
               05  WELL-SP                     PIC 9(4).
           03  NET-ALLO                        PIC 9.
           03  BAL-RULE                        PIC 9.
           03  XMT-FACT                        PIC 9.
           03  PRINT-AS-IS                     PIC 9.
           03  COL-HEAD                        PIC X.
           03  T-CODE                          PIC X(12).
           03  TEST-CODE   REDEFINES T-CODE OCCURS 12 TIMES
                                               PIC X.
           03  CUMU-PROD                       PIC 9(12).
           03  CUMU-COND-PROD                  PIC 9(10).
           03  UNIT-ACRES                      PIC 9(4).
           03  UNIT-TOL                        PIC 999.
           03  ALLOCTION                       PIC 9(15).
           03  CASING                          PIC X(21).
           03  DIAGONAL.
               05  DIAG-X                      PIC X.
               05  DIAG-INFO                   PIC X(20).
           03  FG-DEPTH                        PIC 9(5).
           03  WELLS                           PIC 9(4).
           03  ALLOW-CALC                      PIC 9(8).
           03  TOL                             PIC 999.
           03  ALLOW-DESIRED                   PIC 9(8).
           03  TOTAL-FORECAST                  PIC 9(8).
           03  OFFSHORE                        PIC 9.
           03  FLD-TRANS                       PIC 9.
           03  EX-BAL                          PIC 9.
           03  EX-GOR                          PIC 9.
           03  PENDING-SPEC-LMT-ALLOW          PIC 9.
           03  CUMU-PROD-PRIOR-70              PIC 9(12).
           03  CUMU-PROD-ERROR-SW              PIC X.
           03  FILLER                          PIC X(45).
           03  LINE-INFO   OCCURS 4 TIMES      PIC X(66).
           03  FILLER                          PIC X(16).
           03  FLD-MONTH   OCCURS 14 TIMES.
               05  FLD-DATE                    PIC 9(6).
               05  FLD-DATE-REDF REDEFINES FLD-DATE.
                   07  FLD-DATE-CCYY           PIC 9(4).
                   07  FLD-DATE-CCYY-REDF REDEFINES FLD-DATE-CCYY.
                       09  F-CENT              PIC 99.
                       09  F-YEAR              PIC 99.
                   07  F-MONTH                 PIC 99.
               05  F-CHANGE                    PIC 9.
               05  PER-WELL-CD                 PIC 99.
               05  PER-WELL                    PIC S9(7).
               05  AC-CD                       PIC 99.
               05  ACRG-FACT                   PIC S9(8).
               05  OTHER-CD                    PIC 99.
               05  OTHER-FACT                  PIC S9(4).
               05  SW-SPLIT                    PIC SV999       COMP-3.
               05  SPLIT-DATE                  PIC 99.
               05  SPECIAL-LMT-ALLOW           PIC 9.
               05  SW-EXC-206-CODE             PIC 9.
               05  SW-EXC-8609-LIMIT           PIC 99.
               05  FILLER                      PIC X(43).
           03  FILLER                          PIC X(390).
      *
       01  WELL-REC.
           03  W-REC-CODE                      PIC 9.
           03  WELL-CODE.
               05  OP-CODE.
                   07  W-FLD-CODE.
                       09  W-DISTR.
                           11  W-DIST-NO       PIC 99.
                           11  W-DIST-SFX      PIC X.
                       09  W-PERM-FLD-ID       PIC 9(8).
                       09  W-FLD-ID REDEFINES W-PERM-FLD-ID.
                           11  W-FLD-NAM       PIC 9(5).
                           11  W-FLD-RES       PIC 999.
                   07  OPER-ID                 PIC 9(6).
               05  WELL-ID                     PIC 9(6).
           03  NEXT-WELL REDEFINES WELL-CODE   PIC X(23).
           03  FILLER                          PIC 9.
           03  WELL-NO.
               05  TRACT-NO                    PIC X.
               05  WELL-NR                     PIC XXX.
               05  WELL-SFX.
                   07  SFX-1                   PIC X.
                   07  SFX-2                   PIC X.
           03  LSE-NAME                        PIC X(32).
           03  CO-CODE                         PIC 999.
           03  W-TYPE                          PIC X.
           03  GAS-GATHER-OLD                  PIC X(5).
           03  GAS-GATHER-NEW.
               05  G-GATH                      PIC X(5).
               05  FULL-S                      PIC X.
               05  GAS-SPLIT                   PIC X.
           03  GASGATH2I                       PIC X(5).
           03  GASGATH3I                       PIC X(5).
           03  LIQ-GATHER-OLD                  PIC X(5).
           03  LIQ-GATHER-NEW.
               05  L-GATH                      PIC X(5).
               05  LIQ-SPLIT                   PIC X.
           03  WELL-INFO                       PIC X(22).
           03  BATCH-NR                        PIC X.
           03  EXC-14B                         PIC X.
           03  W14B-DATE                       PIC 9(8).
           03  W14B-DATE-REDF REDEFINES W14B-DATE.
               05  W14B-CCYY                   PIC 9(4).
               05  W14B-CCYY-REDF REDEFINES W14B-CCYY.
                   07  W14B-CC                 PIC 99.
                   07  W14B-YR                 PIC 99.
               05  W14B-MO                     PIC 99.
               05  W14B-DAY                    PIC 99.
           03  CMP-DATE                        PIC 9(8).
           03  CMP-DATE-REDF REDEFINES CMP-DATE.
               05  CMP-DATE-CCYY               PIC 9(4).
               05  CMP-DATE-CCYY-REDF REDEFINES CMP-DATE-CCYY.
                   07  CMP-DATE-CC             PIC 99.
                   07  CMP-DATE-YY             PIC 99.
               05  CMP-DATE-MM                 PIC 99.
               05  CMP-DATE-DD                 PIC 99.
           03  W-DEPTH                         PIC 9(5).
           03  UP-PERF                         PIC 9(5).
           03  LO-PERF                         PIC 9(5).
           03  COMMCD                          PIC 9.
           03  COMM                            PIC 9(4).
           03  COMN-DTE                        PIC 9(8).
           03  COMN-DTE-REDF REDEFINES COMN-DTE.
               05  COMN-CCYY                   PIC 9(4).
               05  COMN-CCYY-REDF REDEFINES COMN-CCYY.
                   07  COMN-CC                 PIC 99.
                   07  COMN-YR                 PIC 99.
               05  COMN-M                      PIC 99.
               05  COMN-DAY                    PIC 99.
           03  DPT-CODE                        PIC X.
           03  BHP-CODE                        PIC X.
           03  SIP-CODE                        PIC X.
           03  G-4-CODE                        PIC X.
           03  WL-TSTX                         PIC X.
           03  G-10-DUE                        PIC 99.
           03  DTE-L-UTL                       PIC 9(8).
           03  DTE-L-UTL-REDF REDEFINES DTE-L-UTL.
               05  DTE-L-UTL-CCYY              PIC 9(4).
               05  DTE-L-UTL-CCYY-REDF REDEFINES DTE-L-UTL-CCYY.
                   07  DTE-L-UTL-CC            PIC 99.
                   07  DTE-L-UTL-YY            PIC 99.
               05  DTE-L-UTL-MM                PIC 99.
               05  DTE-L-UTL-DD                PIC 99.
           03  WL-PA-CD                        PIC 9.
           03  P-A-DATE                        PIC 9(8).
           03  P-A-DATE-REDF REDEFINES P-A-DATE.
               05  P-A-DATE-CCYY               PIC 9(4).
               05  P-A-DATE-CCYY-REDF REDEFINES P-A-DATE-CCYY.
                   07  P-A-DATE-CC             PIC 99.
                   07  P-A-DATE-YY             PIC 99.
               05  P-A-DATE-MM                 PIC 99.
               05  P-A-DATE-DD                 PIC 99.
           03  SP-ALLOW                        PIC 9(7).
           03  SP-AL-CODE                      PIC X.
           03  LIQ-ALLOW                       PIC 9(5).
           03  LIQ-ALLOW-CODE                  PIC 9.
           03  FORM-LACKING                    PIC 9.
           03  OFF-SHORE                       PIC 9.
           03  WL-TOP-PER                      PIC 999V99.
           03  ROYALTY-CODE                    PIC 9.
           03  PRIOR-RINU                      PIC S9(9)   COMP-3.
           03  PRIOR-RINU-DATE                 PIC 9(6).
           03  PRIOR-RINU-DATE-REDF REDEFINES PRIOR-RINU-DATE.
               05  PRIOR-RINU-CCYY             PIC 9(4).
               05  PRIOR-RINU-CCYY-REDF REDEFINES PRIOR-RINU-CCYY.
                   07  PRIOR-RINU-CENT         PIC 9(2).
                   07  PRIOR-RINU-YEAR         PIC 9(2).
               05  PRIOR-RINU-MONTH            PIC 9(2).
           03  RINU                            PIC S9(9)   COMP-3.
           03  RINU-DATE                       PIC 9(6).
           03  RINU-DATE-REDF REDEFINES RINU-DATE.
               05  RINU-CCYY                   PIC 9(4).
               05  RINU-CCYY-REDF REDEFINES RINU-CCYY.
                   07  RINU-CENT               PIC 9(2).
                   07  RINU-YEAR               PIC 9(2).
               05  RINU-MONTH                  PIC 9(2).
           03  EXC-14B2-TYPE                   PIC X.
           03  FILLER                          PIC X.
           03  G-1-DATE                        PIC 9(8).
           03  G-1-DATE-REDF REDEFINES G-1-DATE.
               05  G-1-DATE-CCYY               PIC 9(4).
               05  G-1-DATE-CCYY-REDF REDEFINES G-1-DATE-CCYY.
                   07  G-1-DATE-CENT           PIC 99.
                   07  G-1-DATE-YEAR           PIC 99.
               05  G-1-DATE-MONTH              PIC 99.
               05  G-1-DATE-DAY                PIC 99.
           03  OPEN-FLO                        PIC S9(7)   COMP-3.
           03  SLOPE                           PIC S9V9999 COMP-3.
           03  SLOPED REDEFINES SLOPE          PIC S9(5)   COMP-3.
           03  RATIO                           PIC S9(5)   COMP-3.
           03  G-GRAV                          PIC SV999   COMP-3.
           03  G-GRAVED REDEFINES G-GRAV       PIC S999    COMP-3.
           03  O-GRAV                          PIC S99V9   COMP-3.
           03  O-GRAVED REDEFINES O-GRAV       PIC S999    COMP-3.
           03  BGS                             PIC S9(9)   COMP-3.
           03  BLS                             PIC S9(9)   COMP-3.
           03  PRIOR-6                         PIC S9(9)   COMP-3.
           03  PCU                             PIC S9(7)   COMP-3.
           03  CURR-BAL                        PIC S9(9)   COMP-3.
           03  CANCEL-G                        PIC S9(7)   COMP-3.
           03  G-STATUS                        PIC S9(9)   COMP-3.
           03  L-STATUS                        PIC S9(7)   COMP-3.
           03  LMT-ALLOW                       PIC S9(7)   COMP-3.
           03  SI-AMT                          PIC S9(9)   COMP-3.
           03  SI-CODE                         PIC 9.
           03  EXCEPTION-TO-PROD-LIMIT-CODE    PIC 9.
           03  EXCEPTION-TO-PROD-LIMIT         PIC S9(7)   COMP-3.
           03  EXC-14B2-APP-NO                 PIC 9(6)    COMP-3.
           03  MONTHLY-WELL OCCURS 14 TIMES.
               05  W-DATE                      PIC 9(6).
               05  W-DATE-REDF REDEFINES W-DATE.
                   07  W-DATE-CCYY             PIC 9(4).
                   07  W-DATE-CCYY-REDF REDEFINES W-DATE-CCYY.
                       09  W-CC                PIC 99.
                       09  W-YR                PIC 99.
                   07  W-MO                    PIC 99.
               05  NAME-CHANGE-CODE            PIC 9.
               05  FORM-REC-CODE               PIC 9.
               05  BAL-CODE                    PIC 9.
               05  EXC-206-CODE                PIC 9.
               05  RED-RATE-CODE               PIC 9.
               05  TSF-CODE                    PIC 9.
               05  NO-SUPP                     PIC 9.
               05  LACK                        PIC 9.
               05  OLD-OP-CODE                 PIC 9(6).
               05  W-TYPE-MO                   PIC X.
               05  AL-CODE                     PIC X.
               05  WRD-ALLOW                   PIC X(8).
               05  ON-SHUT-LST                 PIC X.
               05  NO-LMT-ALLOW-SW             PIC 9.
               05  ALLOW                       PIC S9(7)   COMP-3.
               05  GAS-PRD                     PIC S9(7)   COMP-3.
               05  INJ-CREDIT                  PIC S9(7)   COMP-3.
               05  INJ-CODE                    PIC 9.
               05  W-LIQ-ALLOW                 PIC S9(5)   COMP-3.
               05  LSE-LIQ                     PIC S9(5)   COMP-3.
               05  PLT-LIQ                     PIC S9(5)   COMP-3.
               05  LIQ-DISI                    PIC S9(5)   COMP-3.
               05  LIQ-DISCDI                  PIC 9.
               05  OTH-DISI                    PIC S9(5)   COMP-3.
               05  OTH-DISCDI                  PIC 9.
               05  MO-G4                       PIC S9(7)   COMP-3.
               05  MO-G2                       PIC S9(5)   COMP-3.
               05  MO-BHP                      PIC S9(5)   COMP-3.
               05  OTHER-PRESI                 PIC S9(5)   COMP-3.
               05  MO-ACRE                     PIC S9(4)V9(3) COMP-3.
               05  MO-ACRE-FT                  PIC S9(6)V9    COMP-3.
               05  TRAN-ALLOW                  PIC S9(7)   COMP-3.
               05  OPEN-COND                   PIC S9(5)   COMP-3.
               05  CLOSE-COND                  PIC S9(5)   COMP-3.
               05  MO-LEASE-PERCENT-RESERVE    PIC S9(3)V9(4) COMP-3.
               05  PER-CENT-RED-RATE           PIC S9(7)   COMP-3.
               05  MO-TOP-SCH-ALLOW            PIC S9(7)   COMP-3.
               05  MO-LMT-ALLOW                PIC S9(7)   COMP-3.
               05  MO-HIGHEST-DAILY-PROD-LMT   PIC S9(7)   COMP-3.
               05  EXC-8609-LIMIT              PIC 9(2).
               05  SWR38-ACRES-CODE            PIC X.
           03  FILLER                          PIC X(180).
