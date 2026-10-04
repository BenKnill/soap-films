(* Heavy already loads realanalysis and its transcendental library. *)
needs "Multivariate/realanalysis.ml";;
needs "proofs/snap_algebra.ml";;
prioritize_real();;

(* tanh in an exponential form; no new axiom or external numerical oracle. *)
let soap_tanh = new_definition
 `soap_tanh t = (exp(&2 * t) - &1) / (exp(&2 * t) + &1)`;;
let soap_snap = new_definition
 `soap_snap t = (t - &1) * exp(&2 * t) - (t + &1)`;;

let SOAP_SNAP_EQUATION = prove
 (`!t. t * soap_tanh t = &1 <=> soap_snap t = &0`,
  GEN_TAC THEN REWRITE_TAC[soap_tanh; soap_snap] THEN
  MATCH_MP_TAC SOAP_SNAP_ALGEBRA THEN
  MP_TAC(SPEC `&2 * t` REAL_EXP_POS_LT) THEN REAL_ARITH_TAC);;

(* Kernel-checked Taylor remainder at the two rational endpoints. The same
   exponential appears in the remainder, so linear arithmetic bounds it
   without importing the incompatible legacy Library/calc_real.ml. *)
let SOAP_SNAP_LOWER_SIGN = prove
 (`soap_snap (&11996786402 / &10000000000) < &0`,
  MP_TAC(ISPECL [`24`; `Cx(&23993572804 / &10000000000)`] TAYLOR_CEXP) THEN
  SIMP_TAC[RE_CX; GSYM CX_EXP; GSYM CX_DIV; GSYM CX_SUB;
           COMPLEX_NORM_CX] THEN
  CONV_TAC(ONCE_DEPTH_CONV EXPAND_VSUM_CONV) THEN
  REWRITE_TAC[GSYM CX_POW; GSYM CX_DIV; GSYM CX_ADD;
             GSYM CX_SUB; COMPLEX_NORM_CX; soap_snap] THEN
  CONV_TAC NUM_REDUCE_CONV THEN CONV_TAC REAL_RAT_REDUCE_CONV THEN
  REAL_ARITH_TAC);;

let SOAP_SNAP_UPPER_SIGN = prove
 (`&0 < soap_snap (&11996786403 / &10000000000)`,
  MP_TAC(ISPECL [`24`; `Cx(&23993572806 / &10000000000)`] TAYLOR_CEXP) THEN
  SIMP_TAC[RE_CX; GSYM CX_EXP; GSYM CX_DIV; GSYM CX_SUB;
           COMPLEX_NORM_CX] THEN
  CONV_TAC(ONCE_DEPTH_CONV EXPAND_VSUM_CONV) THEN
  REWRITE_TAC[GSYM CX_POW; GSYM CX_DIV; GSYM CX_ADD;
             GSYM CX_SUB; COMPLEX_NORM_CX; soap_snap] THEN
  CONV_TAC NUM_REDUCE_CONV THEN CONV_TAC REAL_RAT_REDUCE_CONV THEN
  REAL_ARITH_TAC);;

let SOAP_SNAP_CONTINUOUS = prove
 (`!s. soap_snap real_continuous_on s`,
  GEN_TAC THEN GEN_REWRITE_TAC LAND_CONV [GSYM ETA_AX] THEN
  REWRITE_TAC[soap_snap] THEN
  MATCH_MP_TAC REAL_CONTINUOUS_ON_SUB THEN CONJ_TAC THENL
   [MATCH_MP_TAC REAL_CONTINUOUS_ON_MUL THEN CONJ_TAC THENL
     [MATCH_MP_TAC REAL_CONTINUOUS_ON_SUB THEN
      REWRITE_TAC[REAL_CONTINUOUS_ON_ID; REAL_CONTINUOUS_ON_CONST];
      SUBGOAL_THEN `(\x. exp(&2 * x)) = exp o (\x. &2 * x)`
      SUBST1_TAC THENL
       [REWRITE_TAC[o_DEF];
        MATCH_MP_TAC REAL_CONTINUOUS_ON_COMPOSE THEN
        SIMP_TAC[REAL_CONTINUOUS_ON_LMUL; REAL_CONTINUOUS_ON_ID;
                 REAL_CONTINUOUS_ON_EXP]]];
    MATCH_MP_TAC REAL_CONTINUOUS_ON_ADD THEN
    REWRITE_TAC[REAL_CONTINUOUS_ON_ID; REAL_CONTINUOUS_ON_CONST]]);;

let SOAP_SNAP_INCREASING = prove
 (`!x y. &1 <= x /\ x < y ==> soap_snap x < soap_snap y`,
  REPEAT STRIP_TAC THEN REWRITE_TAC[soap_snap] THEN
  MATCH_MP_TAC SOAP_SNAP_MONOTONE_ALGEBRA THEN
  ASM_REWRITE_TAC[] THEN CONJ_TAC THENL
   [MATCH_MP_TAC REAL_EXP_LT_1 THEN ASM_REAL_ARITH_TAC;
    REWRITE_TAC[REAL_EXP_MONO_LT] THEN ASM_REAL_ARITH_TAC]);;

let SOAP_SNAP_SMALL = prove
 (`!t. &0 < t /\ t <= &1 ==> soap_snap t < &0`,
  REPEAT STRIP_TAC THEN REWRITE_TAC[soap_snap] THEN
  MATCH_MP_TAC SOAP_SNAP_SMALL_ALGEBRA THEN
  ASM_REWRITE_TAC[REAL_EXP_POS_LE]);;

let CATENOID_SNAP_ENCLOSURE = prove
 (`(?t. &11996786402 / &10000000000 < t /\
         t < &11996786403 / &10000000000 /\ t * soap_tanh t = &1) /\
   (!t. &0 < t /\ t * soap_tanh t = &1
        ==> &11996786402 / &10000000000 < t /\
            t < &11996786403 / &10000000000)`,
  REWRITE_TAC[SOAP_SNAP_EQUATION] THEN CONJ_TAC THENL
   [MP_TAC(ISPECL [`soap_snap`; `&11996786402 / &10000000000`;
                  `&11996786403 / &10000000000`; `&0`]
                 REAL_IVT_INCREASING) THEN
    SIMP_TAC[SOAP_SNAP_CONTINUOUS;
             REAL_LT_IMP_LE; SOAP_SNAP_LOWER_SIGN; SOAP_SNAP_UPPER_SIGN] THEN
    CONV_TAC REAL_RAT_REDUCE_CONV THEN
    REWRITE_TAC[IN_REAL_INTERVAL] THEN
    MESON_TAC[SOAP_SNAP_LOWER_SIGN; SOAP_SNAP_UPPER_SIGN; REAL_LT_LE];
    MATCH_MP_TAC (SPECL [`soap_snap`; `&11996786402 / &10000000000`;
                        `&11996786403 / &10000000000`] SOAP_ZERO_BRACKET) THEN
    REPEAT CONJ_TAC THENL
     [CONV_TAC REAL_RAT_REDUCE_CONV;
      CONV_TAC REAL_RAT_REDUCE_CONV;
      MATCH_ACCEPT_TAC SOAP_SNAP_LOWER_SIGN;
      MATCH_ACCEPT_TAC SOAP_SNAP_UPPER_SIGN;
      MATCH_ACCEPT_TAC SOAP_SNAP_INCREASING;
      MATCH_ACCEPT_TAC SOAP_SNAP_SMALL]]);;

let CATENOID_SNAP_UNIQUE = prove
 (`!x y. &0 < x /\ &0 < y /\
          x * soap_tanh x = &1 /\ y * soap_tanh y = &1 ==> x = y`,
  REWRITE_TAC[SOAP_SNAP_EQUATION] THEN
  MATCH_MP_TAC (SPEC `soap_snap` SOAP_ZERO_UNIQUE) THEN
  CONJ_TAC THENL
   [MATCH_ACCEPT_TAC SOAP_SNAP_INCREASING;
    MATCH_ACCEPT_TAC SOAP_SNAP_SMALL]);;

print_endline "CATENOID SNAP: 1.1996786402 < t < 1.1996786403 (unique positive root of t*tanh(t)=1)";;
