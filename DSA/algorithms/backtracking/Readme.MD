add current_list in result_list
return

1.  Run find_all_permutations
    result_list = []
    current_list = []
    used_list = [False, False, False]

    run backtrack (1)
    check current_list length == 3 (NO)
    MOVE

    loop at i = 0 / A
    check A = False??? (YES) ===========================================> USED = [False, False, False] , current_list = []
    then
    current_list = [A]  ===========================================> current_list = [A]
    A = True ===========================================> USED = [TRUE, False, False]

(1 -> 1R)   backtrack (1 -> 1R)
                 check current_list length == 3 (NO)
                     MOVE

                loop at j = 0 / A
                     check A = False??? (NO) ===========================================> USED = [TRUE, False, False]
(1 -> 2R)        loop at j = 1 / B
                     check B = False??? (YES) ===========================================> USED = [TRUE, False, False]
                     then
                         current_list = [A, B] ===========================================> current_list = [A, B]
                         B = True ===========================================> USED = [TRUE, TRUE, False]

1 -> 2 -> 1R        backtrack (1 -> 2 -> 1R)
                            check current_list length == 3 (NO)  =========================> current_list = [A, B]
                                 MOVE

1 -> 2 -> 1                 loop at k = 0 / A
                                 check A = False??? (NO)  ===========================================> USED = [TRUE, TRUE, False]
1 -> 2 -> 2                 loop at k = 1 / B
                                 check B = False??? (NO)  ===========================================> USED = [TRUE, TRUE, False]
1 -> 2 -> 3                 loop at k = 2 / C
                                 check C = False??? (YES)  ===========================================> USED = [TRUE, TRUE, False]
                                 then
                                    current_list = [A, B, C] =========================> current_list = [A, B, C]
                                    C = True  ===========================================> USED = [TRUE, TRUE, TRUE]

1 -> 2 -> 3 -> 1R                   backtrack (1 -> 2 -> 3 -> 1R)
                                        check current_list length == 3 (YES) =========================> current_list = [A, B, C]
                                        then
                                            print(A,B,C) ============= result_list = [[A, B, C]]
                                            return backtrack (1 -> 2 -> 3 -> 1R ) is closed

                                    CONTINUE Backtrack (1 -> 2 -> 3) and MOVE_BACKWARD
                                    C = FALSE ===========================================> USED = [TRUE, TRUE, FALSE]
                                    Current List - Remove C ============================> current_list = [A, B]
                            backtrack (1 -> 2 -> 3) is completed
                            backtrack (1 -> 2 -> 1R) is completed

                        CONTINUE Backtrack (1 -> 2R) and MOVE_BACKWARD
                        B = FALSE ===========================================> USED = [TRUE, FALSE, FALSE]
                        Current List - Remove B ============================> current_list = [A]
                
1 -> 3R            loop at j = 2 / C
                    check C = False ???   ===========================================> USED = [TRUE, FALSE, FALSE]
                    then
                        current_list = [A, C] ===========================================> current_list = [A, C]
                        C = True  ===========================================> USED = [TRUE, FALSE, TRUE]

1 -> 3 -> 1R        backtrack (1 -> 3 -> 1R)
                       check current_list length == 3 (No) =========================> current_list = [A, C]
                              MOVE

1 -> 3 -> 1                 loop at k = 0 / A
                                check A = False??? (NO)  ===========================================> USED = [TRUE, FALSE, TRUE]
1 -> 3 -> 1                 loop at k = 1 / B
                                check B = False??? (Yes)  ===========================================> USED = [TRUE, FALSE, TRUE]
                                then
                                    current add B =========================> current_list = [A, C, B]
                                    B = TRUE  ===========================================> USED = [TRUE, TRUE, TRUE]