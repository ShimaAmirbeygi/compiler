Program -> Declaration-list $
Declaration-list -> Declaration Declaration-list
Declaration-list -> ε
Declaration -> Declaration-initial Declaration-prime
Declaration-initial -> #get_id_type Type-specifier #pid ID
Declaration-prime -> Fun-declaration-prime
Declaration-prime -> Var-declaration-prime
Var-declaration-prime -> ; #define_variable
Var-declaration-prime -> [ #push_num NUM ] ; #define_array
Fun-declaration-prime -> #define_params ( Params ) #record_params #create_return Compound-stmt #end_return #return_anyway #finish_function
Type-specifier -> int
Type-specifier -> void
Params -> #get_id_type int #pid ID #define_variable Param-prime Param-list
Params -> void
Param-list -> , Param #define_variable Param-list
Param-list -> ε
Param -> Declaration-initial Param-prime
Param-prime -> #define_array_argument [ ]
Param-prime -> ε
Compound-stmt -> #increase_scope { Declaration-list Statement-list } #decrease_pop_scope
Statement-list -> Statement Statement-list
Statement-list -> ε
Statement -> Expression-stmt
Statement -> Compound-stmt
Statement -> Selection-stmt
Statement -> Iteration-stmt
Statement -> Return-stmt
Expression-stmt -> Expression ; #pop
Expression-stmt -> break ; #break_loop
Expression-stmt -> ;
Selection-stmt -> if ( Expression ) #save Statement else #jpf_save Statement #jump
Iteration-stmt -> repeat #label Statement until ( Expression ) #until #handle_breaks
Return-stmt -> return Return-stmt-prime #save_return
Return-stmt-prime -> #push_index ;
Return-stmt-prime -> Expression ;
Expression -> Simple-expression-zegond
Expression -> #pid_address ID B
B -> = Expression #assign
B -> [ Expression ] #array_index H
B -> Simple-expression-prime
H -> = Expression #assign
H -> G D C
Simple-expression-zegond -> Additive-expression-zegond C
Simple-expression-prime -> Additive-expression-prime C
C -> #push_operator Relop Additive-expression #save_operation
C -> ε
Relop -> <
Relop -> ==
Additive-expression -> Term D
Additive-expression-prime -> Term-prime D
Additive-expression-zegond -> Term-zegond D
D -> #push_operator Addop Term #save_operation D
D -> ε
Addop -> +
Addop -> -
Term -> Factor G
Term-prime -> Factor-prime G
Term-zegond -> Factor-zegond G
G -> * Factor #mult G
G -> ε
Factor -> ( Expression )
Factor -> #pid_address ID Var-call-prime
Factor -> #push_num NUM
Var-call-prime -> ( Args #implicit_output ) #call_function
Var-call-prime -> Var-prime
Var-prime -> [ Expression ] #array_index
Var-prime -> ε
Factor-prime -> ( Args #implicit_output ) #call_function
Factor-prime -> ε
Factor-zegond -> ( Expression )
Factor-zegond -> #push_num NUM
Args -> Arg-list
Args -> ε
Arg-list -> Expression Arg-list-prime
Arg-list-prime -> , Expression Arg-list-prime
Arg-list-prime -> ε