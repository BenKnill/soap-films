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

(* The root exclusion and uniqueness arguments use only order, not analysis. *)
let SOAP_ZERO_BRACKET = prove
 (`!f a b.
     &1 < a /\ &1 < b /\ f a < &0 /\ &0 < f b /\
     (!x y. &1 <= x /\ x < y ==> f x < f y) /\
     (!t. &0 < t /\ t <= &1 ==> f t < &0)
     ==> !t. &0 < t /\ f t = &0 ==> a < t /\ t < b`,
  REPEAT GEN_TAC THEN STRIP_TAC THEN X_GEN_TAC `t:real` THEN STRIP_TAC THEN
  SUBGOAL_THEN `&1 < t` ASSUME_TAC THENL
   [ASM_MESON_TAC[REAL_NOT_LT; REAL_LT_REFL]; ALL_TAC] THEN
  CONJ_TAC THENL
   [ASM_CASES_TAC `t < a` THENL
     [SUBGOAL_THEN `(f:real->real) t < f a` ASSUME_TAC THENL
       [ASM_MESON_TAC[REAL_LT_IMP_LE]; ASM_REAL_ARITH_TAC];
      SUBGOAL_THEN `~(t:real = a)` ASSUME_TAC THENL
       [ASM_MESON_TAC[REAL_LT_REFL]; ASM_REAL_ARITH_TAC]];
    ASM_CASES_TAC `b < t` THENL
     [SUBGOAL_THEN `(f:real->real) b < f t` ASSUME_TAC THENL
       [ASM_MESON_TAC[REAL_LT_IMP_LE]; ASM_REAL_ARITH_TAC];
      SUBGOAL_THEN `~(t:real = b)` ASSUME_TAC THENL
       [ASM_MESON_TAC[REAL_LT_REFL]; ASM_REAL_ARITH_TAC]]]);;

let SOAP_ZERO_UNIQUE = prove
 (`!f.
     (!x y. &1 <= x /\ x < y ==> f x < f y) /\
     (!t. &0 < t /\ t <= &1 ==> f t < &0)
     ==> !x y. &0 < x /\ &0 < y /\ f x = &0 /\ f y = &0
               ==> x = y`,
  REPEAT STRIP_TAC THEN
  SUBGOAL_THEN `&1 < x /\ &1 < y` STRIP_ASSUME_TAC THENL
   [ASM_MESON_TAC[REAL_NOT_LT; REAL_LT_REFL];
    ASM_MESON_TAC[REAL_LT_IMP_LE; REAL_LT_TOTAL; REAL_LT_REFL]]);;
