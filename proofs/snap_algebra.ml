(* Algebraic leaves independent of the transcendental library. *)
prioritize_real();;

let SOAP_SNAP_ALGEBRA = prove
 (`!t e. &0 < e + &1
         ==> (t * ((e - &1) / (e + &1)) = &1 <=>
              (t - &1) * e - (t + &1) = &0)`,
  REPEAT STRIP_TAC THEN MATCH_MP_TAC (REAL_FIELD
   `~(e + &1 = &0)
    ==> (t * ((e - &1) / (e + &1)) = &1 <=>
         (t - &1) * e - (t + &1) = &0)`) THEN
  ASM_REAL_ARITH_TAC);;

let SOAP_SNAP_MONOTONE_ALGEBRA = prove
 (`!x y u v. &1 <= x /\ x < y /\ &1 < u /\ u < v
             ==> (x - &1) * u - (x + &1) <
                 (y - &1) * v - (y + &1)`,
  REPEAT STRIP_TAC THEN
  SUBGOAL_THEN `&0 < (y - x) * (u - &1)` ASSUME_TAC THENL
   [MATCH_MP_TAC REAL_LT_MUL THEN ASM_REAL_ARITH_TAC; ALL_TAC] THEN
  SUBGOAL_THEN `&0 < (y - &1) * (v - u)` ASSUME_TAC THENL
   [MATCH_MP_TAC REAL_LT_MUL THEN ASM_REAL_ARITH_TAC;
    ASM_REAL_ARITH_TAC]);;

let SOAP_SNAP_SMALL_ALGEBRA = prove
 (`!t e. &0 < t /\ t <= &1 /\ &0 <= e
         ==> (t - &1) * e - (t + &1) < &0`,
  REPEAT STRIP_TAC THEN
  SUBGOAL_THEN `&0 <= (&1 - t) * e` ASSUME_TAC THENL
   [MATCH_MP_TAC REAL_LE_MUL THEN ASM_REAL_ARITH_TAC;
    ASM_REAL_ARITH_TAC]);;
